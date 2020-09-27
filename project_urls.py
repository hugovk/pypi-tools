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


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-n", "--number", type=int, default=100, help="Max number to fetch"
    )
    args = parser.parse_args()

    # Load from top-pypi-packages.json
    packages_todo = get_top_packages()
    if args.number:
        packages_todo = packages_todo[: args.number]

    print("Find project_urls...")

    all_keys = []
    count = 0
    for package in tqdm(packages_todo, unit="project"):
        project_urls = get_project_urls(package["name"])
        if project_urls:
            all_keys.extend(project_urls.keys())
            count += 1

    # Counter will sort by most common, but let's sort alphabetically
    # for those with the same count
    all_keys = sorted(all_keys)
    pprint(collections.Counter(all_keys))
    print()
    print(f"Number with project_urls: {count}/{args.number}")


if __name__ == "__main__":
    main()
