#!/usr/bin/env python
# encoding: utf-8
"""
Tabulate the output JSON files from pypi-trends.py into a CSV file, pypi-trends.csv
"""
from __future__ import print_function, unicode_literals

import argparse
import csv
import glob
import json
import os
from pprint import pprint

all_data = []
all_versions = set()


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
    parser.add_argument("-i", "--inspec", default="data/*.json", help="Input file spec")

    args = parser.parse_args()

    files = glob.glob(args.inspec)
    files = sorted(files)
    pprint(files)

    for f in files:
        month_name = os.path.splitext(os.path.basename(f))[0]
        print(f)
        with open(f) as json_data:
            d = json.load(json_data)
            # pprint(d)
            month_data = {"yyyy-mm": month_name}
            for row in d["rows"]:
                print(row)
                month_data[row["python_version"]] = float(row["percent"]) * 100
                all_versions.add(row["python_version"])
            pprint(month_data)
        all_data.append(month_data)

    pprint(all_data)
    pprint(all_versions)
    all_versions = list(sorted(all_versions))

    f = csv.writer(open(os.path.join("data", "pypi-trends.csv"), "w+"))
    f.writerow(["", "Python version"])
    f.writerow(["Month"] + all_versions)
    for x in all_data:
        pprint(x)
        row = [x["yyyy-mm"]]
        for version in all_versions:
            row.append(x.get(version, 0))
        pprint(row)
        f.writerow(row)

# End of file
