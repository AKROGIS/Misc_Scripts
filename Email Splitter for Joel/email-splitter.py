# -*- coding: utf-8 -*-
"""
2020-12-12  Regan Sarwas

Per Joel Cusick, when exporting multiple email messages from MS Outlook they are
concatenated into a single file.  Joel needs them to be individual files so they
can be processed.  He gets these emails frequently, and it is tedious to export
them individually.

Edit the CONFIG properties to alter how the script behaves.
The script will fail if any of the paths in the CONFIG do not
exist, or if there are read or write permissions.  If there
is a failure, just edit the CONFIG and try again.

Tested with Python 2.7 and Python 3.8
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from io import open
import os


CONFIG = {
    # The path and name of the input file
    # the file should contain a concatenation ion of emails from a single addressee
    'input': 'C:/tmp/sample.txt',
    # The first line of a new email.
    # A new file will be created each time a line is found that starts with this text
    'first-line': 'From:	opus <opus@ngs.noaa.gov>',
    # The full path to the folder where the output files will be created
    'folder': 'C:/tmp',
    # The name of the output file
    # Each file will get a sequential numerical suffix and a .txt extension
    'basename': 'opus-email-',
}


def write(lines, counter):
    filename = "{0}{1}.txt".format(CONFIG['basename'], counter)
    filename = os.path.join(CONFIG['folder'], filename)
    with open(filename, 'w', encoding="utf-8") as f2:
        #for line in lines:
        f2.writelines(lines)


with open(CONFIG['input'], 'r', encoding="utf-8") as f:
    lines = []
    counter = 1
    for line in f:
        if line.startswith(CONFIG['first-line']):
            if lines:
                write(lines, counter)
                counter += 1
            lines = []
        lines.append(line)
    if lines:
        write(lines,counter)
