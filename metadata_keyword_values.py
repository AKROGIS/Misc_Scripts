# -*- coding: utf-8 -*-
"""
Looks at a bunch of metadata files in a several folders and reports on the
various values found for a specific keyword.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from io import open
import os


dsm = r'\\INPAKROVMDIST\GISData2\Extras\AKR\Statewide\DEM\NPRA-IfSAR_Intermap_2002\DSM'
dtm = r'\\INPAKROVMDIST\GISData2\Extras\AKR\Statewide\DEM\NPRA-IfSAR_Intermap_2002\DTM'
ori = r'\\INPAKROVMDIST\GISData2\Extras\AKR\Statewide\DEM\NPRA-IfSAR_Intermap_2002\ORI'
prefix = '        Beginning_Date: '

for dir in [dsm, dtm, ori]:
    d = {}
    for file in os.listdir(dir):
        name = os.path.join(dir,file)
        ext = os.path.splitext(name)[1].lower()
        if os.path.isfile(name) and ext == '.txt' :
            date = 'none'
            with open(name, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith(prefix):
                        date = line.replace(prefix,'').strip()
                        break
            # print(date)
            if date not in d:
                d[date] = 0
            d[date] = d[date] + 1
    print('Stats for ' + dir[-3:])
    keys = sorted(d.keys())
    for key in keys:
        print('  ' + key + ':' + str(d[key]))
                    
