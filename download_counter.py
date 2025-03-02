"""
Given a list of packages, count their total downloads
from the top-pypi-packages.json list.

Start by:

# Fetch fresh copy of top packages
wget https://hugovk.github.io/top-pypi-packages/top-pypi-packages.min.json -O \
    data/top-pypi-packages.json

# Count 'em
python3 download_counter.py Pillow pylast pypistats pypinfo norwegianblue pepotron \
    termcolor humanize PrettyTable Tablib UltraJSON OSMViz tinytext em-keyboard
"""

from __future__ import annotations

import argparse
import json
from pprint import pprint  # noqa: F401

from rich import print


def get_top_packages():
    packages = load_from_file("data/top-pypi-packages.json", "rows")

    for package in packages:
        # Rename keys
        package["name"] = package.pop("project")

    return packages


def load_from_file(file_name, index):
    print(f"Load {file_name}...")
    try:
        with open(file_name) as f:
            packages = json.load(f)[index]
        return packages

    except json.decoder.JSONDecodeError:
        return None


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("packages", nargs="+", default=[], help="Packages to count")
    args = parser.parse_args()

    # Load from top-pypi-packages.json
    top_packages = get_top_packages()

    my_packages = {p.lower() for p in args.packages}
    my_data = []

    for top_package in top_packages:
        if not len(my_packages):
            break

        if top_package["name"].lower() in my_packages:
            my_packages.remove(top_package["name"])
            my_data.append(top_package)

    print(my_data)
    total = sum(p["download_count"] for p in my_data)
    print(f"Total: {total:,d}")
    print(f"Not in top-pypi-packages.json: {my_packages}")


if __name__ == "__main__":
    main()
