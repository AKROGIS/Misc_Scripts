# -*- coding: utf-8 -*-
"""
Creates a CSV list of photos (and select metadata) for all photos in a folder.

author = "Regan Sarwas, GIS Team, Alaska Region, National Park Service"
email = "regan_sarwas@nps.gov"
copyright = "Public Domain - product of the US Government"

Edit the Config object below as needed for each execution.

Third party requirements:
* exifread - https://pypi.python.org/pypi/ExifRead
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
from io import open
import os

import exifread


class Config(object):
    """Namespace for configuration parameters. Edit as necessary."""

    # pylint: disable=useless-object-inheritance,too-few-public-methods

    # Look for photos in this folder.
    search_folder = "C:/tmp"

    # Write the list of file data to this file.
    out_list = os.path.join(search_folder, "PhotoList.csv")

def write_exif():
    """Write a list of EXIF properties for all files in Config."""

    with open(Config.out_list, "w", encoding="utf-8") as f:
        f.write("folder,photo,exifdate,lat,lon,gpsdate,filedate\n")
        for filename in os.listdir(Config.search_folder):
            base, extension = os.path.splitext(filename)
            if extension.lower() == ".jpg":
                path = os.path.join(Config.search_folder, filename)
                lat, lon, exifdate, gpsdate = "", "", "", ""
                with open(path, "rb") as pf:
                    # exifread wants binary data
                    tags = exifread.process_file(pf, details=False)
                    try:
                        dms = tags["GPS GPSLatitude"].values
                        deg = float(dms[0].num) / dms[0].den
                        minute = float(dms[1].num) / dms[1].den
                        sec = float(dms[2].num) / dms[2].den
                        if tags["GPS GPSLatitudeRef"].values == "N":
                            sign = 1
                        else:
                            sign = -1
                        lat = sign * (deg + (minute + sec / 60) / 60)
                        if lat == 0:
                            lat = ""
                    except KeyError:
                        pass
                    except ZeroDivisionError:
                        pass
                    try:
                        dms = tags["GPS GPSLongitude"].values
                        deg = float(dms[0].num) / dms[0].den
                        minute = float(dms[1].num) / dms[1].den
                        sec = float(dms[2].num) / dms[2].den
                        if tags["GPS GPSLongitudeRef"].values == "E":
                            sign = 1
                        else:
                            sign = -1
                        lon = sign * (deg + (minute + sec / 60) / 60)
                        if lon == 0:
                            lon = ""
                    except KeyError:
                        pass
                    except ZeroDivisionError:
                        pass
                    try:
                        time = tags["EXIF DateTimeOriginal"].values
                        # exifdate = time.replace(':', '').replace(' ', 'T') #compact iso format
                        exifdate = time.replace(
                            ":", "-", 2
                        )  # microsoft excel acceptable ISO format
                    except KeyError:
                        pass
                    try:
                        date = tags["GPS GPSDate"].values
                        time = tags["GPS GPSTimeStamp"].values
                        if date:
                            # gpsdate = '{0}T{1}{2}{3}'.format(date.replace(':', ''),
                            #                                 time[0], time[1], float(time[2].num)/time[2].den)
                            gpsdate = "{0} {1}:{2}:{3}".format(
                                date.replace(":", "-"),
                                time[0],
                                time[1],
                                float(time[2].num) / time[2].den,
                            )
                        else:
                            gpsdate = ""
                    except KeyError:
                        pass
                filedate = datetime.datetime.fromtimestamp(
                    os.path.getmtime(path)
                ).isoformat()
                filedate = filedate.replace(
                    "T", " "
                )  # microsoft excel acceptable ISO format
                f.write(
                    "{0},{1},{2},{3},{4},{5},{6}\n".format(
                        Config.search_folder, filename, exifdate, lat, lon, gpsdate, filedate
                    )
                )


if __name__ == "__main__":
    write_exif()
