# -*- coding: utf-8 -*-
"""
Walk a folder and write the path of all files matching the search type.

Edit the Config object below as needed for each execution.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from io import open
import os


class Config(object):
    """Namespace for configuration parameters. Edit as necessary."""

    # pylint: disable=useless-object-inheritance,too-few-public-methods

    out_list = r"C:\tmp\list2.txt"
    search_folder = (
        r"T:\PROJECTS\AKR\FMSS\TRAILS\Data\DENA\2015_FMSSMapping\SavageAlpine"
    )
    extensions = [".jpg", ".jpeg"]


with open(Config.out_list, "w", encoding="utf-8") as out_file:
    for (root, _, files) in os.walk(Config.search_folder):
        for name in files:
            _, ext = os.path.splitext(name)
            if ext.lower() in Config.extensions:
                out_file.write(os.path.join(root, name) + "\n")
