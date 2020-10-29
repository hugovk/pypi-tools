"""
Read in packages from top-pypi-packages.json and fetch their project_urls metadata.

(Metadata is cached by source_finder.py in CACHE_DIR.)

Return a count of the most common keys.

Start by:

# Fetch fresh copy of top packages
wget https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json -O \
    data/top-pypi-packages.json

# Check the first 10 packages in data/top-pypi-packages.json
python3 project_urls.py --number 10
Load data/top-pypi-packages.json...
Find project_urls...
100%|█████████████████████████████████████████████| 10/10 [00:00<00:00, 167.91project/s]
Counter({'Homepage': 10,
         'Documentation': 4,
         'Source': 2,
         'Code': 1,
         'Issue tracker': 1})

Number with project_urls: 10/10
"""
import argparse
import collections
from pprint import pprint  # noqa: F401

import httpx
from prettytable import MARKDOWN, PrettyTable
from tqdm import tqdm

from source_finder import pypi_json
from top_repos import get_top_packages


def get_project_urls(package):
    try:
        res = pypi_json(package)
        return res["info"]["project_urls"]
    except httpx.HTTPStatusError:
        # e.g. https://pypi.org/project/pprint/ has been removed
        return None


class CustomFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter,
):
    pass


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=CustomFormatter
    )
    parser.add_argument(
        "-n", "--number", type=int, default=100, help="Max number to fetch"
    )
    parser.add_argument("-k", "--key", help="Also show project_urls with this key")
    args = parser.parse_args()

    # Load from top-pypi-packages.json
    packages_todo = get_top_packages()
    if args.number:
        packages_todo = packages_todo[: args.number]

    print("Find project_urls...")

    all_keys = []
    selected_urls = []
    count = 0
    for package in tqdm(packages_todo, unit="project"):
        project_urls = get_project_urls(package["name"])
        if project_urls:
            all_keys.extend(project_urls.keys())
            count += 1
            if args.key:
                try:
                    selected_urls.append((package["name"], project_urls[args.key]))
                except KeyError:
                    pass

    # Counter will sort by most common, but let's sort alphabetically
    # for those with the same count
    all_keys = sorted(all_keys)
    most_common = collections.Counter(all_keys).most_common()

    table = PrettyTable()
    table.field_names = ["Project URL", "Count"]
    table.align = "l"
    table.align["Count"] = "r"
    table.set_style(MARKDOWN)
    for url_count in most_common:
        table.add_row(url_count)
    print()
    print(table)

    print()
    print(f"Projects with project_urls: {count}/{args.number}")

    if args.key:
        print()
        table = PrettyTable()
        table.field_names = ["Project", f"{args.key} URL"]
        table.align = "l"
        table.set_style(MARKDOWN)
        for name_url in selected_urls:
            table.add_row(name_url)
        print(table)
        print()


if __name__ == "__main__":
    main()
