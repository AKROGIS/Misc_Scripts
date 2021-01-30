# -*- coding: utf-8 -*-
"""
Summarizes the fish counts in a sonar file as CSV data.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from io import open


class Config(object):
    """Namespace for configuration parameters."""

    # pylint: disable=useless-object-inheritance,too-few-public-methods

    in_file = "c:/tmp/dan/sample.txt"
    out_file = "c:/tmp/dan/output.csv"


def main():
    """Summarize the fish counts in a sonar file as CSV data."""

    fish = {}
    in_data_section = False
    for line in open(Config.in_file, "r", encoding="utf-8"):
        if not in_data_section and line.startswith("-----------------"):
            in_data_section = True
            continue
        if in_data_section and len(line.strip()) == 0:
            in_data_section = False
        if in_data_section:
            date = line[100:110] + " " + line[90:98]
            if date not in fish:
                fish[date] = 0
            fish[date] += 1
    with open(Config.out_file, "w", encoding="utf-8") as out_file:
        out_file.write("datetime,count\n")
        for date, count in sorted(fish.items()):
            out_file.write("{0},{1}\n".format(date, count))


if __name__ == "__main__":
    main()
