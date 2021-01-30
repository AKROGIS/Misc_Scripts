# -*- coding: utf-8 -*-
"""
Reads records in a CSV with 3D location of two opposite corners of
a square and calculates the two missing corners to create a polygon

The CSV data is RTK GPS data for opposite corners of a rigid pvc
square that is placed on a rocky shoreline.  The pvc square is the
same for all pairs of measurements, but the size is unknown.

The current script ignores elevation, as there is not enough
information to determine the 3D orientation.  It is assumed that the
GPS coordinates are on solid ground, but the corner of the quadrant
being measured may be in the air due to rocks supporting other parts
of the pvc square

The structure of the CSV looks like this:

Site,Name,Team,Quad,FeatureCod,Easting,Northing,Orth_Elev,LocalLatit,LocalLongi,LocalEllip,H_Prec_Obs,V_Prec_Obs,Date_Obs,Time_Obs
19,19_TA_QU01,A,1,QUAD_C1,493338.2325,581494.5272,-1.574847,59.222571,-154.116672,10.665757,0.013484,0.017039,5/15/2018,9:38:27 AM
19,19_TA_QL01,A,1,QUAD_C2,493338.8142,581494.9555,-1.655107,59.222575,-154.116662,10.585469,0.013476,0.017026,5/15/2018,9:38:54 AM
19,19_TA_QL02,A,2,QUAD_C2,493332.2278,581497.0564,-1.776223,59.222594,-154.116777,10.464726,0.013578,0.016955,5/15/2018,9:45:20 AM
19,19_TA_QU02,A,2,QUAD_C1,493331.5725,581496.7227,-1.771056,59.222591,-154.116789,10.469926,0.013561,0.016915,5/15/2018,9:45:53 AM

Third party requirements:
* arcpy - Installed with ArcGIS
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import math

import csv23


def corners(p1, p3):
    delta = (p3[0] - p1[0], p3[1] - p1[1])
    diag = math.sqrt(delta[0] ** 2 + delta[1] ** 2)
    l = diag / math.sqrt(2.0)
    theta = math.atan2(delta[1], delta[0])  # operand order is (y,x)
    alpha = math.pi / 4.0
    p2 = (p1[0] + l * math.cos(theta - alpha), p1[1] + l * math.sin(theta - alpha))
    p4 = (p1[0] + l * math.cos(theta + alpha), p1[1] + l * math.sin(theta + alpha))
    # print(delta, diag, l, theta, alpha)
    return p2, p4, l, 0


def corners3d(p1, p3):
    delta = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])
    diag = math.sqrt(delta[0] ** 2 + delta[1] ** 2 + delta[2] ** 2)
    l = diag / math.sqrt(2.0)
    slope = 100.0 * delta[2] / l
    # print(round(delta[2],2), round(slope,2))
    theta = math.atan2(delta[1], delta[0])  # operand order is (y,x)
    alpha = math.pi / 4.0
    p2 = (p1[0] + l * math.cos(theta - alpha), p1[1] + l * math.sin(theta - alpha), 0)
    p4 = (p1[0] + l * math.cos(theta + alpha), p1[1] + l * math.sin(theta + alpha), 0)
    # print(delta, diag, l, theta, alpha)
    return p2, p4, l, slope


def readfile(filename):
    data = {}
    with csv23.open(filename, "r") as fi:
        _ = fi.readline()  # ignore the header
        reader = csv.reader(fi)
        for row in reader:
            row = csv23.fix(row)
            # print(row[2:7])
            site = row[0]
            team = row[2]
            quad = row[3]
            name = site + "|" + team + str(quad)
            corner = int(row[4][-1:])
            if corner != 1 and corner != 2:
                print(site, team, name, name, corner)
                continue
            x = float(row[5])
            y = float(row[6])
            z = float(row[7])
            if name not in data:
                data[name] = {corner: (x, y, z)}
            else:
                data[name][corner] = (x, y, z)
    return data


def writedata(filename, data):
    with csv23.open(filename, "w") as fo:
        writer = csv.writer(fo)
        header = [
            "Site",
            "Team",
            "Quad",
            "Corner",
            "Easting",
            "Northing",
            "SideLength",
            "Slope(%)",
        ]
        csv23.write(writer, header)
        for name in sorted(data.keys()):
            site, teamquad = name.split("|")
            team = teamquad[:1]
            quad = teamquad[1:]
            if 1 in data[name]:
                p1 = data[name][1]
            else:
                print("Error Corner 1 not found in " + name)
                continue
            if 2 in data[name]:
                p3 = data[name][2]
            else:
                print("Error Corner 2 not found in " + name)
                continue
            p2, p4, l, slope = corners3d(p1, p3)
            row = [site, team, quad, 3, p2[0], p2[1], round(l, 3), round(slope, 3)]
            csv23.write(writer, row)
            row = [site, team, quad, 4, p4[0], p4[1], round(l, 3), round(slope, 3)]
            csv23.write(writer, row)
            # shape = [p1,p2,p3,p4,p1]
            # write_feature([team, quad, l, shape)


def writefc(fcname, data):
    # Create new FGDB, and polygon FC with projection AK StatePlane 5 meters (nad83)
    # Create the following fields, text, except SideLength and Slope are Double
    import arcpy

    fields = ["Site", "Team", "Quad", "SideLength", "Slope", "SHAPE@"]
    cursor = arcpy.da.InsertCursor(fcname, fields)
    for name in sorted(data.keys()):
        site, teamquad = name.split("|")
        team = teamquad[:1]
        quad = teamquad[1:]
        p1 = data[name][1]
        p3 = data[name][2]
        p2, p4, l, slope = corners3d(p1, p3)
        points = [p1, p2, p3, p4, p1]
        shape = arcpy.Polygon(arcpy.Array([arcpy.Point(*coords) for coords in points]))
        cursor.insertRow((site, team, quad, l, slope, shape))
    del cursor


def test1():
    p1 = (3, 2)
    p3 = (7, 6)
    p2, p4, l = corners(p1, p3)
    print(p1, p2, p3, p4, l)


def test2():
    p1 = (3, 1, 0)
    p3 = (6, 5, 5)
    p2, p4, l = corners3d(p1, p3)
    print(p1, p2, p3, p4, l)


def test3():
    filename = "/Users/RESarwas/Downloads/All_Quadrats_V2"
    data = readfile(filename + ".csv")
    writedata(filename + "_out.csv", data)


def test4():
    filename = "/Users/RESarwas/Downloads/All_Quadrats_V2"
    data = readfile(filename + ".csv")
    writefc("/tmp/Sarah.gdb/quads", data)


# test1()
# test2()
# test3()
test4()
