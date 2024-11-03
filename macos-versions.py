#!/usr/bin/env python3
"""
Sum totals for macOS major.minor versions.

First do something like:
$ pypinfo --limit 1000 --json --markdown pillow system distro-version > macos.json

Then:
$ python3 macos-versions.py

This then takes the JSON output file of that, and sums up the downloads for
each macOS major.minor version, ignoring the patch number: x.y.z -> x.y
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import sys
from collections import OrderedDict

from natsort import natsorted  # pip install natsort
from prettytable import PrettyTable, TableStyle  # pip install prettytable

# from pprint import pprint
# from rich import print  # pip install rich


# https://stackoverflow.com/a/5734564/724176
def month_year_iter(start_month, start_year, end_month, end_year):
    ym_start = 12 * start_year + start_month - 1
    ym_end = 12 * end_year + end_month - 1
    for ym in range(ym_start, ym_end):
        y, m = divmod(ym, 12)
        yield y, m + 1


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-i", "--inspec", default="macos.json", help="Input file spec")
    args = parser.parse_args()

    new_rows = []
    darwin_downloads = {}

    files = glob.glob(args.inspec)
    files = sorted(files)

    if len(files) == 0:
        sys.exit("No files matching " + args.inspec)

    for f in files:
        # print(f)
        with open(f) as json_data:
            d = json.load(json_data)
            # pprint(d)
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
                if int(x) >= 11:
                    xy = f"{x}"
                else:
                    xy = f"{x}.{y}"
                if xy == "10.16":
                    xy = "11"
                # print(distro_version)
                # print(x, y)
                # print(xy)
                try:
                    darwin_downloads[xy] += download_count
                except KeyError:
                    darwin_downloads[xy] = download_count
                # pprint(darwin_downloads)

    # Sort by version number
    ordered_keys = natsorted(darwin_downloads)
    darwin_downloads = OrderedDict((key, darwin_downloads[key]) for key in ordered_keys)

    darwin_total = sum(darwin_downloads.values())
    # print(darwin_total)

    for version in darwin_downloads:
        percent = darwin_downloads[version] / darwin_total * 100
        row = {
            "system_name": "Darwin",
            "distro_version": version,
            "download_count": darwin_downloads[version],
            "percent": f"{round(percent, 2):.2f}%",
        }
        new_rows.append(row)

    # pprint(new_rows)

    fieldnames = ["system_name", "distro_version", "percent", "download_count"]
    with open("macos.csv", "w+") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(new_rows)

    summed_percent = 0
    for row in new_rows[::-1]:
        summed_percent += float(row["percent"].rstrip("%"))
        row["summed_percent"] = f"{round(summed_percent, 2):.2f}%"

    t = PrettyTable()
    t.set_style(TableStyle.MARKDOWN)
    t.field_names = new_rows[0].keys()
    for row in new_rows:
        t.add_row(row.values())
    t.align["distro_version"] = "r"
    t.align["download_count"] = "r"
    t.align["percent"] = "r"
    t.align["summed_percent"] = "r"
    t.custom_format["download_count"] = lambda _, v: f"{v:,}"
    print(t)


if __name__ == "__main__":
    main()
