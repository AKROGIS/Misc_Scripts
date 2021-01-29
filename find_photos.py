# -*- coding: utf-8 -*-
"""
Walk the SEARCH_FOLDER and write the path of any file with an extension in
EXTENSIONS to the file OUT_LIST.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from io import open
import os

OUT_LIST = r"C:\tmp\list2.txt"
SEARCH_FOLDER = r"T:\PROJECTS\AKR\FMSS\TRAILS\Data\DENA\2015_FMSSMapping\SavageAlpine"
EXTENSIONS = [".jpg", ".jpeg"]

with open(OUT_LIST, "w", encoding="utf-8") as out_file:
    for (root, _, files) in os.walk(SEARCH_FOLDER):
        for name in files:
            _, ext = os.path.splitext(name)
            if ext.lower() in EXTENSIONS:
                out_file.write(os.path.join(root, name) + "\n")
