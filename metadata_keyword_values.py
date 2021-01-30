# -*- coding: utf-8 -*-
"""
Looks at a bunch of metadata files in a several folders and reports on the
various values found for a specific keyword.

Edit the Config object below as needed for each execution.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from io import open
import os


class Config(object):
    """Namespace for configuration parameters. Edit as necessary."""

    # pylint: disable=useless-object-inheritance,too-few-public-methods

    DSM = r"\\INPAKROVMDIST\GISData2\Extras\AKR\Statewide\DEM\NPRA-IfSAR_Intermap_2002\DSM"
    DTM = r"\\INPAKROVMDIST\GISData2\Extras\AKR\Statewide\DEM\NPRA-IfSAR_Intermap_2002\DTM"
    ORI = r"\\INPAKROVMDIST\GISData2\Extras\AKR\Statewide\DEM\NPRA-IfSAR_Intermap_2002\ORI"
    prefix = "        Beginning_Date: "

for folder in [Config.DSM, Config.DTM, Config.ORI]:
    d = {}
    for name in os.listdir(folder):
        path = os.path.join(folder, name)
        ext = os.path.splitext(path)[1].lower()
        if os.path.isfile(path) and ext == ".txt":
            date = "none"
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith(Config.prefix):
                        date = line.replace(Config.prefix, "").strip()
                        break
            # print(date)
            if date not in d:
                d[date] = 0
            d[date] = d[date] + 1
    print("Stats for " + folder[-3:])
    keys = sorted(d.keys())
    for key in keys:
        print("  " + key + ":" + str(d[key]))
