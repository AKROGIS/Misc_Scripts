Miscellaneous Scripts
=====================

A collection of miscellaneous scripts.  Typically these are user requested
scripts for a specific on-off problem unrelated to some larger project.

Many of these are old and un-documented. I've tried to summarize them as
best I could.  See the code for additional details on use the scripts.

Most of the scripts were written for python 2.7 and may not work correctly
with python 3.x

## Creating Quadrat Corners

A python script for Sarah Venator that reads records in a CSV with 3D
location of two opposite corners of a square and calculates the two
missing corners to create a polygon.  See the instructions at the head
of the script.

## DENA Roads

A python script for the Denali Road Ecology team that adds milepost
numbers into the Denali road observation database for records that
have a lat/long but no milepost. The data paths are hardcoded in the
script so edit before using.

## Fish Data Collation

A script for Dan Young that summarizes the fish counts in a sonar
data file (see `sample.txt`). The scope of this request was poorly
understood.  Eventually 100s of theses sonar files were loaded into
the [LACL Fish Database](https://github.com/AKROGIS/LACL_Fish#phase-2-sonar)
for summarization in a database table.

## Mosaic Datasets

This was a tool written to understand the inter-relation between mosaic
datasets in the PDS before the reorganization in 2017.  Many of the
mosaic datasets that John Pinamont created were reference mosaics
https://desktop.arcgis.com/en/arcmap/latest/manage-data/raster-and-images/creating-a-mosaic-dataset-from-an-existing-catalog-or-mosaic.htm.
John did this before processing templates were available or understood.
For example to create a hillshade he would create a new mosaic that
referenced the elevation mosaic.  This script may be useful (with some
rework) to find any outstanding reference mosaic datasets.

## Raster Conversions

A sample DOS (Windows command line) batch file that finds all the
*.tif files in a folder and uses the [GDAL toolkit](https://gdal.org/)
to create a new compressed GeoTIFF, add overviews (pyramids) and
statistics. GDAL provides more (and better) compression options than
ArcGIS and uses the internal pyramid system in GeoTIFFs to avoid the
sidecar pyramid file.  The stats are created as an auxillary file
because that is the only format ArcGIS understands.  There are
additional similar scripts in SFM Processing folder of the
[PDS Managment Repo](https://github.com/AKROGIS/PDS-Data-Management/tree/master/sfm_processing/GDAL_Processing)

## `attributes_of_photo_files.py`

Copy this script to a folder with photos and run to create a file called
`PhotoList.csv` with the file and EXIF properties of all `*.jpg`
files found in the folder.  Requires the
[exifread](https://pypi.python.org/pypi/ExifRead) python module
(install with `pip`).  The CSV file will have the following columns
`folder, filename, exifdate, lat, lon, gpsdate, filedate` and a row
for each `*.jpg` file found.

## `features_in_npsapi_to_csv.py`

An example of using the
[NPS API](https://www.nps.gov/subjects/developer/api-documentation.htm)
To query various web enabled structured datasets and create CSV files
for Alaska features with a lat/long.  Requires the use of an `API Key`.
There is one in the KeyPass Password keeper on the T drive, or a new
one can be requested at the link above.

## `find_photos.py`

Will recursively scan a folder for *.jpg and *.jpeg files and write the
complete path and name of each file found into separate columns in a CSV file.
Edit the script to change folder searched and the path/name of the output
CSV file.

## `list_spatial_references_of_all_maps_in_tree.py`

Walks a file system and reports the spatial reference of each data frame
in each map (*.mxd) file found.  Edit the start of the script to specify
the starting folder, and the location/name of the output CSV file.
The CSV file will have the following columns
`mxd,data_frame,spatial_reference` and a row
for each data frame found.

## `metadata_keyword_values.py`

Given a list of folders to search (hard coded at the head of the script),
this script will search the subfolders for `*.txt` files and scan each line
looking for a specific prefix (hard coded at head of script) and summarize
the various values found on the rest of the line.
This was used to search all the IFSAR metadata files to ground source
data of the for each tile.

## `move_remote_ifsar_mosaic.bat`

A PDS management script that was used to move data from the external hard
drive at a park to the robo copy folder.  This is required when there is a
change to the robo copy portion of the PDS that is too large to robo.
This must be run from inside a junction point to a remote server
i.e. `cd \tmp\RemoteServers\XDrive-YUGA\Mosaics\Statewide\DEMs`
This had to be done for all the parks over a period of several months
while the new external drives were delivered and connected before we
could switch over to the new IFSAR mosaics.

## `move_to_trash.py`

A PDS Management Script to for efficiently manipulating the remote park servers.
The script creates a DOS batch file for moving data on a remote server's
GIS Extras drive to the trash on the extras drive.  This should be very fast,
even for very large chunks of data, because it will be just a rename on a single
volume.  To use the script, it must be edited with the date and other configuration
settings. After running this script, copy/paste the output into a batch file and run.
Why not just do the moves in python?  Because I usually want to verify the
operations that will be done before actually moving data.  This also makes
it easier to do a small subset first for testing.
