# -*- coding: utf-8 -*-
"""
Uses the [NPS API](https://www.nps.gov/subjects/developer/api-documentation.htm)
To query various datasets and create CSV files for features with a lat/long

Edit the Config object below as needed for each execution.

Third party requirements:
* requests - https://pypi.org/project/requests/
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import csv

import requests

import csv23

class Config(object):
    """Namespace for configuration parameters. Edit as necessary"""

    # pylint: disable=useless-object-inheritance,too-few-public-methods

    # To get an API Key, See https://www.nps.gov/subjects/developer/get-started.htm
    key = "xxx___YOUR_API_KEY_GOES_HERE___xxx"

    # Search for feature in this state.
    state = "ak"

    # The features to request.
    features = ["campgrounds", "places", "visitorcenters", "webcams"]

    # Create a CSV for each feature with these fields.
    fields = ["id", "title", "latitude", "longitude", "url"]

    # Location of the web service
    url = (
        "https://developer.nps.gov/api/v1/{0}?stateCode={1}&start={2}&limit={3}&api_key={4}"
    )


def get_some_items(kind, start=0, limit=50):
    """Return a 'page' of items matching kind of feature from the service."""

    url = Config.url.format(kind, Config.state, start, limit, Config.key)
    response = requests.get(url).json()
    total = int(response["total"])
    end = min(total, start + limit)
    print("Got {0}-{1} of {2} records for {3}".format(start, end, total, kind))
    return response["data"]


def get_all_items(kind):
    """Return a list of all the items matching kind of feature from the service."""

    all_data = []
    start = 0
    limit = 50
    while True:
        some_data = get_some_items(kind, start, limit)
        all_data += some_data
        if len(some_data) < limit:
            return all_data
        start += limit


def simplify(item, keys):
    """
    Return a list of just the values in item matching the keys.

    items is a dict keyed with strings
    keys is a list of strings that are keys in items
    returns a list of strings representing the values of the items matching the keys
    if a key in keys is not a key in items, it is silently ignored.
    """

    values = []
    for key in keys:
        try:
            values.append("{0}".format(item[key]))
        except KeyError:
            values.append(None)
    return values


def make_csv(kind, fields):
    """Write a CSV file for all the fields found for kind."""

    data = get_all_items(kind)
    with csv23.open(kind + ".csv", "w") as out_file:
        writer = csv.writer(out_file)
        csv23.write(writer, fields)
        for item in data:
            values = simplify(item, fields)
            csv23.write(writer, values)


def make_all_csv():
    """Create a CSV for each feature."""

    for feature in Config.features:
        make_csv(feature, Config.fields)


if __name__ == "__main__":
    make_all_csv()
