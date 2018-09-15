#!/usr/bin/env python3
# encoding: utf-8
"""
Sum totals for macOS major.minor versions.

First do something like:
$ pypinfo --limit 1000 --json --markdown pillow system distro-version > macos.json

Then:
$ python3 macos-versions.py

This then takes the JSON output file of that, and sums up the downloads for
each macOS major.minor version, ignoring the patch number: x.y.z -> x.y
"""
from __future__ import print_function, unicode_literals

import argparse
import csv
import glob
import json
import os
from collections import OrderedDict
from distutils.version import LooseVersion
from pprint import pprint

from pytablewriter import Align, MarkdownTableWriter  # pip install pytablewriter

all_data = []
all_versions = set()

new_rows = []
darwin_downloads = {}


# https://stackoverflow.com/a/5734564/724176
def month_year_iter(start_month, start_year, end_month, end_year):
    ym_start = 12 * start_year + start_month - 1
    ym_end = 12 * end_year + end_month - 1
    for ym in range(ym_start, ym_end):
        y, m = divmod(ym, 12)
        yield y, m + 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-i", "--inspec", default="macos.json", help="Input file spec")

    args = parser.parse_args()

    files = glob.glob(args.inspec)
    files = sorted(files)

    for f in files:
        month_name = os.path.splitext(os.path.basename(f))[0]
        print(f)
        with open(f) as json_data:
            d = json.load(json_data)
            # pprint(d)
            month_data = {"yyyy-mm": month_name}
            for row in d["rows"]:
                # pprint(row)
                # print(row["system_name"])
                if row["system_name"] != "Darwin":
                    continue

                distro_version = row["distro_version"]
                download_count = row["download_count"]
                if distro_version == "None":
                    darwin_downloads[distro_version] = download_count
                    continue

                x, y, *rest = distro_version.split(".")
                xy = "'{}.{}'".format(x, y)
                # print(distro_version)
                # print(x, y)
                # print(xy)
                try:
                    darwin_downloads[xy] += download_count
                except KeyError:
                    darwin_downloads[xy] = download_count
                # pprint(darwin_downloads)

    # Sort by version number
    orderedKeys = sorted(darwin_downloads, key=LooseVersion)
    darwin_downloads = OrderedDict((key, darwin_downloads[key]) for key in orderedKeys)

    darwin_total = sum(darwin_downloads.values())
    # print(darwin_total)

    for version in darwin_downloads:
        percent = darwin_downloads[version] / darwin_total * 100
        row = {
            "system_name": "Darwin",
            "distro_version": version,
            "download_count": darwin_downloads[version],
            "percent": "{:.2f}%".format(round(percent, 2)),
        }
        new_rows.append(row)

    # pprint(new_rows)


fieldnames = ["system_name", "distro_version", "percent", "download_count"]
with open("macos.csv", "w+") as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(new_rows)


writer = MarkdownTableWriter()
writer.header_list = fieldnames
writer.value_matrix = new_rows
writer.align_list = [Align.AUTO, Align.AUTO, Align.RIGHT, Align.AUTO]
writer.margin = 1
writer.write_table()


# End of file
