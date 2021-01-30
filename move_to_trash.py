# -*- coding: utf-8 -*-
"""
Creates a DOS batch file for moving data on a remote servers GIS Extras drive
to the trash on the extras drive.  This should be very fast, even for very large
chunks of data, because it will be just a rename on a single volume.

1. Edit the Config object below as needed for each execution.
2. Create the date folder in the trash before running,

After running this script, copy the output into a batch file and run.
Why not just do the move in python?  Because I usually want to verify the
operations that will be done before actually moving data.  This also makes
it easier to do a small subset first for testing.
"""

from __future__ import absolute_import, division, print_function, unicode_literals


class Config(object):
    """Namespace for configuration parameters. Edit as necessary."""

    # pylint: disable=useless-object-inheritance,too-few-public-methods

    date = "2018-10-18"
    folders = [
        "IKONOS_GeoEye1.gdb",
        "IKONOS_GeoEye1.Overviews",
        "IKONOS_RAW.gdb",
        "IKONOS_RAW.Overviews",
    ]
    parks = [
        "YUGA",
        "WRST",
        "SITK",
        "SEAN",
        "NOME",
        "LACL",
        "KOTZ",
        "KEFJ",
        "KATM",
        "GLBA",
        "KLGO",
    ]
    # {0} will be the park, and {1} will be the folder, {2} will be the date
    source_template = r"C:\tmp\RemoteServers\XDrive-{0}\Mosaics\LACL\{1}"
    destination_template = r"C:\tmp\RemoteServers\XDrive-{0}\Trash\{2}\Mosaics~LACL~{1}"

for park in Config.parks:
    for folder in Config.folders:
        SRC = Config.source_template.format(park, folder)
        DST = Config.destination_template.format(park, folder, Config.date)
        print(r"move {0} {1}".format(SRC, DST))
