# -*- coding: utf-8 -*-
"""
Creates a DOS batch file for moving data on a remote servers GIS Extras drive
to the trash on the extras drive.  This should be very fast, even for very large
chunks of data, because it will be just a rename on a single volume.

Create the date folder in the trash before running,
Check and edit the Configuration settings before running.

After running this script, copy the output into a batch file and run.
Why not just do the move in python?  Because I usually want to verify the
operations that will be done before actually moving data.  This also makes
it easier to do a small subset first for testing.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

#Configuration settings
date = '2018-10-18'
folders = ['IKONOS_GeoEye1.gdb','IKONOS_GeoEye1.Overviews','IKONOS_RAW.gdb','IKONOS_RAW.Overviews']
parks = ['YUGA', 'WRST','SITK','SEAN','NOME','LACL','KOTZ','KEFJ','KATM','GLBA','KLGO']
# {0} will be the park, and {1} will be the folder, {2} will be the date
src_template = r'C:\tmp\RemoteServers\XDrive-{0}\Mosaics\LACL\{1}'
dst_template =r'C:\tmp\RemoteServers\XDrive-{0}\Trash\{2}\Mosaics~LACL~{1}'

for park in parks:
    for folder in folders:
        src = src_template.format(park, folder)
        dst = dst_template.format(park, folder, date)
        print(r'move {0} {1}'.format(src,dst))
