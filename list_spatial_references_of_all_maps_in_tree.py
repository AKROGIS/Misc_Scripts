"""
Walks a file system and reports the spatial reference of each data frame
in each map (*.mxd) file found
"""

import os
import arcpy.mapping
import csv
results = r'c:\tmp\sr.csv'
start = r'c:\tmp\Changing Tides'
with open(results, 'wb') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['mxd','data_frame','spatial_reference'])
    for root, dirs, files in os.walk(start):
        for file in files:
            if os.path.splitext(file)[1].lower() == '.mxd':
                suspect = os.path.join(root, file)
                print('Checking {}'.format(suspect))
                try:
                    mxd = arcpy.mapping.MapDocument(suspect)
                    for df in arcpy.mapping.ListDataFrames(mxd):
                        print('  data frame {0} has spatial reference: {1}'.format(df.name, df.spatialReference.name))
                        csv_writer.writerow([suspect, df.name, df.spatialReference.name])
                except:
                    print('ERROR: Unable to check document')
                    csv_writer.writerow([suspect, 'ERROR', 'ERROR'])
