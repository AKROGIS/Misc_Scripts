# -*- coding: utf-8 -*-
"""
Adds milepost numbers into the Denali road observation database for
records that have a lat/long but no milepost.
The data paths are hardcoded in this file, so edit before using.

Third party requirements:
* pyodbc - https://pypi.org/project/pyodbc/
* arcpy - Installed with ArcGIS
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys


#############################
# Start Configuration Options
#############################

# The file path to the MS Access database of road observations.
# This was tested with version XXX of MS Access.
database_path = r"C:\Users\resarwas\Desktop\ProcessingTool_build.mdb"

# The connection string to the MS Access database.  In pyodbc format
# See https://code.google.com/p/pyodbc/wiki/ConnectionStrings
# The following works on 64bit windows 7 enterprise with MS Access 2010
connection = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)}; Dbq='+database_path
# Neither works on 64bit Windows 8.1 with MS Access 2013
#connection = r'Provider=Microsoft.ACE.OLEDB.12.0;Data Source={0};Persist Security Info=False;'.format(database_path)

# The name of the measured park road feature class.
# Could be any valid ArcCatalog path, but the data set must be measured.
# Only file geodatabase feature classes (not in a feature data set) have been tested.
road_fc = r"X:\Albers\parks\dena\GeoDB\DENA_Base.gdb\DENA_TRANS_RoadsLocal_ln"

# A list of the names of the MS Acccess tables that holds the road observation data
table_names = ["HikerWaitTime", "OtherStop", "RestStop", "WildlifeNoStop", "WildlifeStop"]

# This tool assumes that all the tables listed above are in the same database file,
# And that all the tables have the same 4 columns listed below.

# The name of the unique id field in the MS Access table. 
id_field_name = "Point_ID"

# The name of the latitude field in the MS Access table. Should be a double
latitude_field_name = "Latitude"

# The name of the longitude field in the MS Access table. Should be a double
longitude_field_name = "Longitude"

# The name of the milepost field in the MS Access table. Should be a double
milepost_field_name = "MilePost"

# This is the ObjectID of the linear feature in the 'road_fc' that is used
# for linear referencing the mile posts along the road center
# Must be a number or None.  If it is None, then the first feature in 'road_fc'
# will be used.
road_id = 4

# This is the value that is assigned to the starting node of the road feature
# mile markers are assigned based on the length along the road feature plus
# the value of the starting mile.
# The starting mile can be positive or negative.
road_start_mile = 0

# This is the search radius for linear referencing points
# If the point is not within this distance of the park road
# the point will be not get a milepost.
search_radius = "100 meters"

#############################
# End Configuration Options (do not edit below this line)
#############################


##############################
# Begin Environment validation
##############################

# Check for Python 2.7
major, minor, micro, releaselevel, serial = sys.version_info
if (major,minor) != (2,7):
    print("This tool is only supported with Python 2.7 (ArcGIS 10.x)")
    sys.exit()

# Check for 32 bit Python
if sys.maxsize > 2**32:
    print("This tool does not work with 64 bit python")
    sys.exit()

# Check for existence of MS Access database
if not os.path.exists(database_path):
    print("The database does not exist at " + database_path +
          ". Please check the path, then edit the configuration in " +
          __file__ + " and try again.")
    sys.exit()

# Try loading required database connection module
try:
    import pyodbc                     
except ImportError:
    print("You must install the pyodbc extension for python. " +
          "Get it at https://pypi.org/project/pyodbc/)
    sys.exit()

# Try loading required ArcGIS module
print("Loading ArcGIS...")
try:
    import arcpy                     
except ImportError:
    print("You must have ArcGIS Installed.")
    sys.exit()

# Try finding the road feature class
if not arcpy.Exists(road_fc):
    print("Could not find the roads at " + road_fc +
          ". Please check the path, then edit the configuration in " +
          __file__ + " and try again.")
    sys.exit()
    
# Find the measured road centerline
print("Getting Measured Road Centerline...")
road = None
where = None
if road_id:
    where = "{} = {}".format(arcpy.Describe(road_fc).OIDFieldName,road_id)
with arcpy.da.SearchCursor(road_fc, "Shape@", where) as cursor:
    row = cursor.next()
    if row:
        road = row[0]

if not road:
    id = "first"
    if road_id:
        id = "oid = {0}".format(road_id)
    print("The road feature was not found ({0} in {1})".format(id,road_fc))
    sys.exit()

############################
# End Environment validation
############################

def calculate(pts, line, start = 0, search_radius = "100 Meters"):
    # pts = sequence of (id,lat,lon)
    # line = linear feature class with routes (linear referencing)
    rid = "ROUTE"
    props = "ID POINT MP"
    tbl = "in_memory/results"
    srs = arcpy.SpatialReference(4326) #WGS84
    pt_fc = arcpy.CreateFeatureclass_management("in_memory", "pt_fc", "POINT", "", "DISABLED", "DISABLED", srs)
    arcpy.AddField_management(pt_fc,"OBS_ID","Long")
    with arcpy.da.InsertCursor(pt_fc, ["OBS_ID","SHAPE@XY"]) as in_cursor:
        for pt in pts:
            in_cursor.insertRow([pt[0],(pt[2],pt[1])])
    arcpy.LocateFeaturesAlongRoutes_lr(pt_fc, road_fc, rid, search_radius, tbl, props)
    with arcpy.da.SearchCursor('in_memory\\results',['OBS_ID','MP']) as out_cursor:
        mileposts = dict(out_cursor)
    if start != 0:
        for id in mileposts:
            mileposts[id] = mileposts[id] + start
    arcpy.Delete_management(tbl)
    arcpy.Delete_management(pt_fc)
    return mileposts


for table_name in table_names:
    print("Processing Table {0} ...".format(table_name))
    # Get records that need to be updated
    print("  Finding Road Observations to Update...")
    sql = ("SELECT {0},{2},{3} FROM {4} " + 
           "WHERE {1} IS NULL AND {2} IS NOT NULL AND {3} IS NOT NULL")
    sql = sql.format(id_field_name, milepost_field_name, latitude_field_name,
                     longitude_field_name, table_name)

    rcursor = None
    try:
        rcursor = pyodbc.connect(connection).cursor()
        pass
    except pyodbc.Error as e:
        print("Rats!!  Unable to connect to your database.")
        print("Contact Regan (regan_sarwas@nps.gov) for assistance.")
        print("  Connection: " + connection)
        print("  Error: " + e[1])
        sys.exit()
    rows = rcursor.execute(sql).fetchall()

    print("  Calculating {0} Road Observations".format(len(rows)))
    mileposts = calculate(rows, road, road_start_mile, search_radius)

    print("\n  Updating Database...")
    wcursor = pyodbc.connect(connection).cursor()
    for id in mileposts:
        sql = "UPDATE {0} SET {1} = {2} WHERE {3} = {4}"
        sql = sql.format(table_name, milepost_field_name, mileposts[id],
                         id_field_name, id)
        #print(sql)
        wcursor.execute(sql)
    wcursor.commit()
