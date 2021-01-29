# -*- coding: utf-8 -*-
"""
Uses the [NPS API](https://www.nps.gov/subjects/developer/api-documentation.htm)
To query various datasets and create CSV files for features with a lat/long

Third party requirements:
* requests - https://pypi.org/project/requests/
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import json
import sys

import requests


KEY = 'xxx___YOUR_API_KEY_GOES_HERE___xxx'
# To get an API Key, See https://www.nps.gov/subjects/developer/get-started.htm 
STATE = 'ak'
URL = 'https://developer.nps.gov/api/v1/{0}?stateCode={1}&start={2}&limit={3}&api_key={4}'

def get_some_items(kind, start=0, limit=50):
    url = URL.format(kind, STATE, start, limit, KEY)
    response = requests.get(url).json()
    total = int(response['total'])
    end = min(total, start + limit)
    print('Got {0}-{1} of {2} records for {3}'.format(start, end, total, kind))
    return response['data']

def get_all_items(kind):
    all_data = []
    start = 0
    limit = 50
    while True:
        some_data = get_some_items(kind, start, limit)
        all_data += some_data
        if len(some_data) < limit:
            return all_data
        start += limit

# items is a dict keyed with strings
# keys is a list of strings that are keys in items
# returns a list of strings reresenting the values of the items matching the keys
# if a key in keys is not a key in items, it is silently ignored
def simplify(item, keys):
    d = []
    for key in keys:
        try:
            d.append(str(item[key]))
        except KeyError:
            d.append(None)
    return d

def open_csv_write(filename):
    """Open a file for CSV writing in a Python 2 and 3 compatible way."""
    if sys.version_info[0] < 3:
        return open(filename, "wb")
    return open(filename, "w", encoding="utf8", newline="")


def write_csv_row(writer, row):
    """writer is a csv.writer, and row is a list of unicode or number objects."""
    if sys.version_info[0] < 3:
        # Ignore the pylint error that unicode is undefined in Python 3
        # pylint: disable=undefined-variable
        writer.writerow(
            [
                item.encode("utf-8") if isinstance(item, unicode) else item
                for item in row
            ]
        )
    else:
        writer.writerow(row)


def make_csv(kind, fields):
    data = get_all_items(kind)
    with open(kind+'.csv') as f:
        writer = csv.writer(f)
        write_csv_row(writer, fields)
        for item in data:
            values = simplify(item, fields)
            write_csv_row(writer, values)

def main():
    # Features with no lat/long: ['amenities', 'passportstamplocations']
    features = ['campgrounds', 'places', 'visitorcenters','webcams' ]
    for feature in features: 
        make_csv(feature, ['id','title','latitude','longitude','url'])

if __name__ == '__main__':
    main()
