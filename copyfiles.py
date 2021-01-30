# -*- coding: utf-8 -*-
"""
Copy files from DENA server to local drive for processing.

Edit the Config object below as needed for each execution.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import os
import shutil
import zipfile

import csv23


class Config(object):
    """Namespace for configuration parameters. Edit as necessary"""

    # pylint: disable=useless-object-inheritance,too-few-public-methods

    # The location of the CSV file describing the zipped images.
    csv_path = r"C:\tmp\pds\CAKN\files.csv"

    # The network location for the zip files described in the CSV.
    remote = r"\\INPDENAFILES\Teams\ResMgmt\Denali Botany\Digital_Imagery_Library"

    # Copy the zip files to this local directory.
    local_zip = r"C:\tmp\pds\CAKN\zips"

    # Unpack the zipped images to this local folder.
    local_img = r"C:\tmp\pds\CAKN\Best_Avail_Plot_Imagery"


def main():
    """ Just do it """
    with csv23.open(Config.csv_path, "r") as handle:
        csvreader = csv.reader(handle)
        next(csvreader)  # remove header
        for row in csvreader:
            row = csv23.fix(row)
            source = row[13]
            if source:
                local = source.replace(Config.remote, Config.local_zip)
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
    with csv23.open(csv_path, "r") as handle:
        handle.readline()  # remove header
        csvreader = csv.reader(handle)
        for row in csvreader:
            row = csv23.fix(row)
            park = row[0]
            plot = row[1]
            date = row[5]
            suffix = row[6]
            source = row[13]
            if source:
                local = source.replace(Config.remote, Config.local_zip)
                dest = os.path.join(Config.local_img, park, plot, date)
                if suffix:
                    dest += suffix
                print("unzip", local, dest)
                try:
                    os.makedirs(dest)
                except OSError:
                    print("Failed to create dir", dest)
                    continue
                with zipfile.ZipFile(local, "r") as zip_ref:
                    zip_ref.extractall(dest)


if __name__ == "__main__":
    unzip()
