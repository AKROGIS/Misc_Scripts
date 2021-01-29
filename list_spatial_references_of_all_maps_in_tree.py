# -*- coding: utf-8 -*-
"""
Walks a file system and reports the spatial reference of each data frame
in each map (*.mxd) file found.

Third party requirements:
* requests - https://pypi.org/project/requests/
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import os

import arcpy.mapping


results = r'c:\tmp\sr.csv'
start = r'c:\tmp\Changing Tides'


def open_csv_write(filename):
    """Open a file for CSV writing in a Python 2 and 3 compatible way."""
    if sys.version_info[0] < 3:
        return open(filename, "wb")
    return open(filename, "w", encoding="utf8", newline="")


def write_csv_row(writer, row):
    """writer is a csv.writer, and row is a list of unicode or number objects."""
    if sys.version_info[0] < 3:
        # Ignore the pylint error that unicode is undefined in Python 3
        # pylint: disable=undefined-variable
        writer.writerow(
            [
                item.encode("utf-8") if isinstance(item, unicode) else item
                for item in row
            ]
        )
    else:
        writer.writerow(row)


with open_csv_write(results) as f:
    csv_writer = csv.writer(f)
    header = ['mxd','data_frame','spatial_reference']
    write_csv_row(csv_writer, header)
    csv_writer.writerow()
    for root, dirs, files in os.walk(start):
        for file in files:
            if os.path.splitext(file)[1].lower() == '.mxd':
                suspect = os.path.join(root, file)
                print('Checking {}'.format(suspect))
                try:
                    mxd = arcpy.mapping.MapDocument(suspect)
                    for df in arcpy.mapping.ListDataFrames(mxd):
                        print('  data frame {0} has spatial reference: {1}'.format(df.name, df.spatialReference.name))
                        row = [suspect, df.name, df.spatialReference.name]
                        write_csv_row(csv_writer, row)
                except:
                    print('ERROR: Unable to check document')
                    row = [suspect, 'ERROR', 'ERROR']
                    write_csv_row(csv_writer, row)
