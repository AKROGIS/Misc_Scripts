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

See `test.csv` for structure of the input CSV.

Third party requirements:
* arcpy - Installed with ArcGIS
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import math

import csv23


def corners(p_1, p_3):
    """Calculate the missing corners and side_len of a 2D quadrangle given two points."""

    delta = (p_3[0] - p_1[0], p_3[1] - p_1[1])
    diag = math.sqrt(delta[0] ** 2 + delta[1] ** 2)
    side_len = diag / math.sqrt(2.0)
    theta = math.atan2(delta[1], delta[0])  # operand order is (y,x)
    alpha = math.pi / 4.0
    p_2 = (
        p_1[0] + side_len * math.cos(theta - alpha),
        p_1[1] + side_len * math.sin(theta - alpha),
    )
    p_4 = (
        p_1[0] + side_len * math.cos(theta + alpha),
        p_1[1] + side_len * math.sin(theta + alpha),
    )
    # print(delta, diag, side_len, theta, alpha)
    return p_2, p_4, side_len, 0


def corners3d(p_1, p_3):
    """Calculate the missing corners, diagonal and slope of a 3D quadrangle given two points."""

    delta = (p_3[0] - p_1[0], p_3[1] - p_1[1], p_3[2] - p_1[2])
    diag = math.sqrt(delta[0] ** 2 + delta[1] ** 2 + delta[2] ** 2)
    side_len = diag / math.sqrt(2.0)
    slope = 100.0 * delta[2] / side_len
    # print(round(delta[2],2), round(slope,2))
    theta = math.atan2(delta[1], delta[0])  # operand order is (y,x)
    alpha = math.pi / 4.0
    p_2 = (
        p_1[0] + side_len * math.cos(theta - alpha),
        p_1[1] + side_len * math.sin(theta - alpha),
        0,
    )
    p_4 = (
        p_1[0] + side_len * math.cos(theta + alpha),
        p_1[1] + side_len * math.sin(theta + alpha),
        0,
    )
    # print(delta, diag, side_len, theta, alpha)
    return p_2, p_4, side_len, slope


def readfile(filename):
    """Read the input CSV data in filename (formatted as described above)."""
    data = {}
    with csv23.open(filename, "r") as in_file:
        reader = csv.reader(in_file)
        next(reader)  # ignore the header
        for row in reader:
            row = csv23.fix(row)
            # print(row[2:7])
            site = row[0]
            team = row[2]
            quad = row[3]
            name = "{0}|{1}{2}".format(site, team, quad)
            corner = int(row[4][-1:])
            if corner not in (1, 2):
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
    """Write the data as CSV in filename."""

    with csv23.open(filename, "w") as out_file:
        writer = csv.writer(out_file)
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
                p_1 = data[name][1]
            else:
                print("Error Corner 1 not found in " + name)
                continue
            if 2 in data[name]:
                p_3 = data[name][2]
            else:
                print("Error Corner 2 not found in " + name)
                continue
            p_2, p_4, side_len, slope = corners3d(p_1, p_3)
            row = [
                site,
                team,
                quad,
                3,
                p_2[0],
                p_2[1],
                round(side_len, 3),
                round(slope, 3),
            ]
            csv23.write(writer, row)
            row = [
                site,
                team,
                quad,
                4,
                p_4[0],
                p_4[1],
                round(side_len, 3),
                round(slope, 3),
            ]
            csv23.write(writer, row)
            # shape = [p_1,p_2,p_3,p_4,p_1]
            # write_feature([team, quad, side_len, shape)


def writefc(fcname, data):
    """
    Write the data to a polygon feature class.

    First create new FGDB, and polygon FC with projection AK StatePlane 5 meters (nad83)
    Then create the fields listed below as text, except SideLength and Slope are Double.
    """

    import arcpy

    fields = ["Site", "Team", "Quad", "SideLength", "Slope", "SHAPE@"]
    cursor = arcpy.da.InsertCursor(fcname, fields)
    for name in sorted(data.keys()):
        site, teamquad = name.split("|")
        team = teamquad[:1]
        quad = teamquad[1:]
        p_1 = data[name][1]
        p_3 = data[name][2]
        p_2, p_4, side_len, slope = corners3d(p_1, p_3)
        points = [p_1, p_2, p_3, p_4, p_1]
        shape = arcpy.Polygon(arcpy.Array([arcpy.Point(*coords) for coords in points]))
        cursor.insertRow((site, team, quad, side_len, slope, shape))
    del cursor


def test1():
    """Test calculating 2D corners."""
    p_1 = (3, 2)
    p_3 = (7, 6)
    p_2, p_4, side_len, _ = corners(p_1, p_3)
    print(p_1, p_2, p_3, p_4, side_len)


def test2():
    """Test calculating 3D corners."""
    p_1 = (3, 1, 0)
    p_3 = (6, 5, 5)
    p_2, p_4, side_len, _ = corners3d(p_1, p_3)
    print(p_1, p_2, p_3, p_4, side_len)


def test3():
    "Test reading CSV and writing to CSV."
    filename = "test"
    data = readfile(filename + ".csv")
    writedata(filename + "_out.csv", data)


def test4():
    "Test reading CSV and writing to feature class."
    filename = "test"
    data = readfile(filename + ".csv")
    writefc("/tmp/Sarah.gdb/quads", data)


# test1()
# test2()
test3()
# test4()
