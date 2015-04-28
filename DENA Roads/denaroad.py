"""
Adds milepost numbers into the Denali road observation database for
records that have a lat/long but no milepost.
The data paths are hardcoded in this file, so edit before using
"""

from __future__ import print_function
import os
import sys

#############################
# Start Configuration Options
#############################

# The file path to the MS Access database of road observations.
# This was tested with version XXX of MS Access.
database_path = r"c:\Users\resarwas\Desktop\denaroad.accdb"

# The connection string to the MS Access database.  In pyodbc format
# See https://code.google.com/p/pyodbc/wiki/ConnectionStrings
connection = "Driver={Microsoft Access Driver (*.mdb, *.accdb)}; Dbq=" + database_path

# The name of the measured park road feature class.
# Could be any valid ArcCatalog path, but the data set must be measured.
# Only file geodatabase feature classes (not in a feature data set) have been tested.
road_fc = r"X:\Albers\parks\dena\GeoDB\DENA_Base.gdb\DENA_TRANS_RoadsLocal_ln"

# The name of the MS Acccess table that holds the road observation data
table_name = "obs"

# The name of the unique id field in the MS Access table
id_field_name = "ID"

# The name of the latitude field in the MS Access table
latitude_field_name = "Lat"

# The name of the longitude field in the MS Access table
longitude_field_name = "Lon"

# The name of the milepost field in the MS Access table
milepost_field_name = "MP"

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
          "Get it at https://code.google.com/p/pyodbc/ " + 
          "Be sure to get the 32bit version for python 2.7 " +
          "for example pyodbc-x.x.x.win32-py2.7.exe")
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

print(road)
print(road.getPart()[0][0])

# FIXME - what about projection issues

############################
# End Environment validation
############################

def GetMmax(geom):  
    # get the max(M) from a geometry  
    mmax = -9999  
    for part in geom.getPart():  
        for point in part:  
            m = point.M 
            if m > mmax:  
                mmax = m  
    return mmax  


def calculate(lat, lon, line, start):
	GetMmax(line)

# Get records that need to be updated
print("Finding Road Observations to Update...")
rcursor = pyodbc.connect(connection).cursor()
sql = ("SELECT {0},{2},{3} FROM {4} " + 
       "WHERE {1} IS NULL AND {2} IS NOT NULL AND {3} IS NOT NULL")
sql = sql.format(id_field_name, milepost_field_name, latitude_field_name,
                 longitude_field_name, table_name)
                 
mileposts = {}
rows = rcursor.execute(sql).fetchall()
print("Calculating {0} Road Observations".format(len(rows)), end="")
for row in rows:
    id = row[0]
    latitude = row[1]
    longitude = row[2]
    new_milepost = calculate(latitude, longitude, road, road_start_mile)
    mileposts[id] = new_milepost
    print(".", end="")

print("\nUpdating Database...")
wcursor = pyodbc.connect(connection).cursor()
for id in mileposts:
    sql = "UPDATE {0} SET {1} = {2} WHERE {3} = {4}"
    sql = sql.format(table_name, milepost_field_name, mileposts[id],
	                 id_field_name, id)
    print(sql)
    wcursor.execute(sql)
wcursor.commit()
	
