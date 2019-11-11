#!/usr/bin/env python
"""
Tabulate the output JSON files from pypi-trends.py into a CSV file, pypi-trends.csv
"""
import argparse
import csv
import glob
import hashlib
import json
import os
import re
import traceback
from collections import defaultdict
from pprint import pprint

from natsort import natsorted  # pip install natsort
from packaging.version import parse  # pip install packaging
from termcolor import colored  # pip install termcolor


# https://stackoverflow.com/a/5734564/724176
def month_year_iter(start_month, start_year, end_month, end_year):
    ym_start = 12 * start_year + start_month - 1
    ym_end = 12 * end_year + end_month - 1
    for ym in range(ym_start, ym_end):
        y, m = divmod(ym, 12)
        yield y, m + 1


def inspec_to_name(inspec):
    """
    data/X* -> X
    data/X*.json -> X
    data/201*.json -> None
    """
    name = os.path.basename(inspec).split("*")[0]
    if name.isdigit():
        return None
    return name


def dopplr(name):
    """
    Take the MD5 digest of a name,
    convert it to hex and take the
    first 6 characters as an RGB value.
    """
    # Tweak "2.8" because it's too close in colour to "3.5"
    if name == "2.8":
        name = "python 2.8"

    return "#" + hashlib.sha224(name.encode()).hexdigest()[:6]


# https://python-graph-gallery.com/255-percentage-stacked-area-chart/
def make_chart(data, index, project_name, no_show):

    grand_total_downloads = 0
    for version in data:
        grand_total_downloads += sum(dls for dls in data[version])

    import matplotlib.pyplot as plt  # pip install matplotlib
    import numpy as np  # pip install numpy
    import pandas as pd  # pip install pandas
    from matplotlib.ticker import FuncFormatter

    labels = data.keys()

    data = pd.DataFrame(data, index=index)

    # We need to transform the data from raw data to percentage (fraction)
    data_perc = data.divide(data.sum(axis=1), axis=0)

    # Use a hash function to always use the same colour for each version number,
    # regardless of which versions are present in this data
    colors = [dopplr(s) for s in labels]
    print(colors)

    # Make the plot
    plt.stackplot(index, data_perc.T, labels=labels, colors=colors)

    ax = plt.gca()

    # Convert Y axis from 0..1 to 0%..100%
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.0%}"))

    # Major ticks every 10% or 0.1
    major_ticks = np.arange(0, 1.2, 0.1)
    ax.set_yticks(major_ticks)

    # Set X labels to 2016-01, 02, ... 12, 2017-01, 02, ...
    x_labels = []
    last_year = None
    for year_month in index[:-1]:
        year, month = year_month.split("-")
        if year == last_year:
            x_labels.append(month)
        else:
            x_labels.append(year_month)
            last_year = year
    x_labels.append(index[-1])  # No change for last one
    ax.set_xticklabels(x_labels, fontsize=9)

    plt.xticks(rotation=90)

    # Pad margins so that markers don't get clipped by the axes
    # plt.margins(0.2)

    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.2)

    plt.grid()

    plt.margins(0, 0)

    # Shrink current axis by 20% so legend is outside chart
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])

    # To reverse the legend order
    handles, labels = ax.get_legend_handles_labels()

    # Put a legend to the right of the current axis
    ax.legend(
        handles[::-1],
        labels[::-1],
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=8,
    )

    if project_name:
        title = "{}'s pip installs from PyPI over time, by Python version".format(
            project_name
        )
    else:
        title = "pip installs from PyPI over time, by Python version"
        project_name = "all"
    plt.suptitle(title)
    plt.title(f"{grand_total_downloads:,d} total downloads", fontsize=10)

    outfile = f"images/pip-install-{project_name}.png"
    print(colored(outfile, "green"))
    plt.savefig(outfile, dpi=96 * 2.5)
    if not no_show:
        plt.show()


def remove_from_list(items, l):
    for item in items:
        if item in l:
            l.remove(item)
    return l


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-i", "--inspec", default="data/*.json", help="Input file spec")
    parser.add_argument("-c", "--chart", action="store_true", help="Create a chart")
    parser.add_argument(
        "-ns", "--no-show", action="store_true", help="Don't show the chart"
    )
    args = parser.parse_args()

    all_data = []
    all_versions = set()

    files = glob.glob(args.inspec)
    files = sorted(files)
    # Skip data for top_repos.py
    files = remove_from_list(
        ["data/top-pypi-packages.json", "data/top-repos.json"], files
    )

    for f in files:
        # Get the yyyy-dd from the filename
        month_name = "".join(re.findall(r"\d{4}-\d{2}", f))
        print(f, month_name)
        with open(f) as json_data:
            try:
                d = json.load(json_data)
            except json.decoder.JSONDecodeError as e:
                print(colored(traceback.format_exc(), "red"))
                print(colored(f"Skipping {f}: {e}", "yellow"))
                continue
            # pprint(d)
            month_data = defaultdict(int)
            month_data["yyyy-mm"] = month_name
            try:
                # pypinfo
                rows = d["rows"]
                version_index = "python_version"
                downloads_index = "download_count"
            except KeyError:
                # pypistats
                rows = d["data"]
                version_index = "category"
                downloads_index = "downloads"
            for row in rows:
                version = row[version_index]
                base_version = parse(version).base_version  # strips a4, b2, rc1

                if version in ["null", "Sure.0"]:
                    # Harmonise pypistats' "null" with pypinfo's "None"
                    # And include junk "Sure.0"
                    base_version = "None"

                # month_data[row["python_version"]] = float(row["percent"]) * 100
                month_data[base_version] += row[downloads_index]
                all_versions.add(base_version)
        all_data.append(month_data)

    # pprint(all_data)
    pprint(all_versions)
    all_versions = natsorted(all_versions)

    f = csv.writer(open(os.path.join("data", "pypi-trends.csv"), "w+"))
    # f.writerow(["", "Python version"])
    f.writerow(["Month"] + all_versions)
    rows = []
    for x in all_data:
        row = [x["yyyy-mm"]]
        for version in all_versions:
            row.append(x.get(version, 0))
        f.writerow(row)
        rows.append(row)

    if args.chart:
        data = {}
        index = []

        # Initialise dict
        for version in all_versions:
            # print(version)
            data[version] = []

        for month_data in all_data:
            index.append(month_data["yyyy-mm"])
            for version in all_versions:
                downloads = month_data.get(version, 0)
                data[version].append(downloads)

        make_chart(data, index, inspec_to_name(args.inspec), args.no_show)


if __name__ == "__main__":
    main()

# End of file
