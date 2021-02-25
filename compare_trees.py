# -*- coding: utf-8 -*-
"""
Compares two similar folders and prints a report of differences.

Edit (or at least review) the Config properties before running.

Works with Python 2.7+ and Python 3.3+
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os


class Config(object):
    """Namespace for configuration parameters. Edit as needed."""

    # pylint: disable=useless-object-inheritance,too-few-public-methods

    # old_root is where the older 'established' files exist
    old_root = r"X:\Extras\AKR\Statewide\Charts/USGS_Topo\Current_GeoPDF"

    # new_root is where the newer 'replacement' files exist
    new_root = r"B:\work\topo\Current_GeoPDF"

    # Show the count of files in each location, and for each category below
    print_summary = True

    # Print the relative file paths in the following categories?
    # adds are relative file paths in new_root, but not old_root
    print_adds = False
    # extras are relative file paths in old_root, but not new_root
    print_extras = False
    # duplicates are relative file paths in both new_root and old_root
    print_duplicates = True


def walk_tree(root):
    """ returns a set of relative paths below root """
    paths = set()
    for folder, _, files in os.walk(root):
        for filename in files:
            relative_path = os.path.join(folder, filename).replace(root, "")
            paths.add(relative_path)
    return paths


def main():
    """Compare two similar folders and prints a report of differences."""

    old_root = Config.old_root
    new_root = Config.new_root
    old_paths = walk_tree(old_root)
    new_paths = walk_tree(new_root)
    adds = new_paths - old_paths
    extras = old_paths - new_paths
    duplicates = old_paths & new_paths

    if Config.print_summary:
        print("Summary")
        print("=======")
        print("Existing Files: {0} at {1}".format(len(old_paths), old_root))
        print("Replacement Files: {0} at {1}".format(len(new_paths), new_root))
        print("New Files: {0}".format(len(adds)))
        print("Extra Files: {0}".format(len(extras)))
        print("Duplicate Files: {0}".format(len(duplicates)))

    if Config.print_extras:
        print("")
        print("Extra Files")
        print("===========")
        for name in sorted(list(extras)):
            print(name)

    if Config.print_adds:
        print("")
        print("New Files")
        print("=========")
        for name in sorted(list(adds)):
            print(name)

    if Config.print_duplicates:
        print("")
        print("Duplicate Files")
        print("===============")
        for name in sorted(list(duplicates)):
            print(name)


if __name__ == "__main__":
    main()
