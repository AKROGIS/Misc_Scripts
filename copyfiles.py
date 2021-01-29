# -*- coding: utf-8 -*-
"""
Copy files from DENA server to local drive for processing.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import os
import shutil
import sys
import zipfile


CSVNAME = r"C:\tmp\pds\CAKN\files.csv"
REMOTE = r"\\INPDENAFILES\Teams\ResMgmt\Denali Botany\Digital_Imagery_Library"
LOCAL = r"C:\tmp\pds\CAKN\zips"
LOCAL2 = r"C:\tmp\pds\CAKN\Best_Avail_Plot_Imagery"


def open_csv_read(filename):
    """Open a file for CSV reading in a Python 2 and 3 compatible way."""
    if sys.version_info[0] < 3:
        return open(filename, "rb")
    return open(filename, "r", encoding="utf8", newline="")


def main():
    """ Just do it """
    with open_csv_read(CSVNAME) as handle:
        handle.readline()  # remove header
        csvreader = csv.reader(handle)
        for row in csvreader:
            if sys.version_info[0] < 3:
                row = [item.decode("utf-8") for item in row]
            source = row[13]
            if source:
                local = source.replace(REMOTE, LOCAL)
                # print("copy", source, local)
                if not os.path.exists(source):
                    print("File not found", source)
                else:
                    print("copy {0}".format(os.path.basename(local)))
                    try:
                        shutil.copy(source, local)
                    except IOError:
                        os.makedirs(os.path.dirname(local))
                        shutil.copy(source, local)


def unzip():
    """ Just do it """
    with open_csv_read(CSVNAME) as handle:
        handle.readline()  # remove header
        csvreader = csv.reader(handle)
        for row in csvreader:
            if sys.version_info[0] < 3:
                row = [item.decode("utf-8") for item in row]
            park = row[0]
            plot = row[1]
            date = row[5]
            suffix = row[6]
            source = row[13]
            if source:
                local = source.replace(REMOTE, LOCAL)
                dest = os.path.join(LOCAL2, park, plot, date)
                if suffix:
                    dest += suffix
                print("unzip", local, dest)
                try:
                    os.makedirs(dest)
                except WindowsError:
                    print("Failed to create dir", dest)
                    continue
                with zipfile.ZipFile(local, "r") as zip_ref:
                    zip_ref.extractall(dest)


if __name__ == "__main__":
    unzip()
