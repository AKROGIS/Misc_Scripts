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


def get_latitude(tags):
    """Return the latitude found in the EXIF tags."""

    lat = ""
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
    except (KeyError, ZeroDivisionError):
        pass
    return lat


def get_longitude(tags):
    """Return the latitude found in the EXIF tags."""

    lon = ""
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
    except (KeyError, ZeroDivisionError):
        pass
    return lon


def get_exif_date(tags):
    """Return the camera date as found in the EXIF tags."""

    exif_date = ""
    try:
        time = tags["EXIF DateTimeOriginal"].values
        # exif_date = time.replace(':', '').replace(' ', 'T') #compact iso format
        exif_date = time.replace(":", "-", 2)  # microsoft excel acceptable ISO format
    except KeyError:
        pass

    return exif_date


def get_gps_date(tags):
    """Return the GPS date found in the EXIF tags."""

    gps_date = ""
    try:
        date = tags["GPS GPSDate"].values
        time = tags["GPS GPSTimeStamp"].values
        if date:
            # gps_date = '{0}T{1}{2}{3}'.format(date.replace(':', ''),
            # time[0], time[1], float(time[2].num)/time[2].den)
            gps_date = "{0} {1}:{2}:{3}".format(
                date.replace(":", "-"),
                time[0],
                time[1],
                float(time[2].num) / time[2].den,
            )
        else:
            gps_date = ""
    except KeyError:
        pass
    return gps_date


def write_exif():
    """Write a list of EXIF properties for all files in Config."""

    with open(Config.out_list, "w", encoding="utf-8") as out_file:
        out_file.write("folder,photo,exif_date,lat,lon,gpsdate,filedate\n")
        for filename in os.listdir(Config.search_folder):
            _, extension = os.path.splitext(filename)
            if extension.lower() == ".jpg":
                path = os.path.join(Config.search_folder, filename)
                with open(path, "rb") as in_file:
                    # exifread wants binary data
                    tags = exifread.process_file(in_file, details=False)
                    lat = get_latitude(tags)
                    lon = get_longitude(tags)
                    exif_date = get_exif_date(tags)
                    gps_date = get_gps_date(tags)
                file_date = datetime.datetime.fromtimestamp(
                    os.path.getmtime(path)
                ).isoformat()
                # "Fix" the ISO datetime so that Microsoft excel can understand it.
                file_date = file_date.replace("T", " ")
                out_file.write(
                    "{0},{1},{2},{3},{4},{5},{6}\n".format(
                        Config.search_folder,
                        filename,
                        exif_date,
                        lat,
                        lon,
                        gps_date,
                        file_date,
                    )
                )


if __name__ == "__main__":
    write_exif()
