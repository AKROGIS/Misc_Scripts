# -*- coding: utf-8 -*-
"""
Walks a file system and reports the spatial reference of each data frame
in each map (*.mxd) file found.

Third party requirements:
* requests - https://pypi.org/project/requests/
* arcpy - Installed with ArcGIS
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import os

import arcpy.mapping

import csv23

results = r"c:\tmp\sr.csv"
start = r"c:\tmp\Changing Tides"


with csv23.open(results, "w") as f:
    csv_writer = csv.writer(f)
    header = ["mxd", "data_frame", "spatial_reference"]
    csv23.write(csv_writer, header)
    csv_writer.writerow()
    for root, dirs, files in os.walk(start):
        for file in files:
            if os.path.splitext(file)[1].lower() == ".mxd":
                suspect = os.path.join(root, file)
                print("Checking {}".format(suspect))
                try:
                    mxd = arcpy.mapping.MapDocument(suspect)
                    for df in arcpy.mapping.ListDataFrames(mxd):
                        print(
                            "  data frame {0} has spatial reference: {1}".format(
                                df.name, df.spatialReference.name
                            )
                        )
                        row = [suspect, df.name, df.spatialReference.name]
                        csv23.write(csv_writer, row)
                except:
                    print("ERROR: Unable to check document")
                    row = [suspect, "ERROR", "ERROR"]
                    csv23.write(csv_writer, row)
