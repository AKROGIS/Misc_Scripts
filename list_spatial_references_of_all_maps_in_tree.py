# -*- coding: utf-8 -*-
"""
Walks a file system and reports the spatial reference of each data frame
in each map (*.mxd) file found.

Edit the Config object below as needed for each execution.

Third party requirements:
* requests - https://pypi.org/project/requests/
* arcpy - Installed with ArcGIS
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import os

import arcpy.mapping

import csv23

class Config(object):
    """Namespace for configuration parameters. Edit as needed."""

    # pylint: disable=useless-object-inheritance,too-few-public-methods

    # Write the results to this file path.
    results = r"c:\tmp\sr.csv"
    # The folder to search.
    start = r"c:\tmp\Changing Tides"


with csv23.open(Config.results, "w") as f:
    csv_writer = csv.writer(f)
    header = ["mxd", "data_frame", "spatial_reference"]
    csv23.write(csv_writer, header)
    csv_writer.writerow()
    for root, dirs, files in os.walk(Config.start):
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
                except arcpy.ExecuteError:
                    print("ERROR: Unable to check document")
                    row = [suspect, "ERROR", "ERROR"]
                    csv23.write(csv_writer, row)
