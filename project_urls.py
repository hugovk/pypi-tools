"""
Read in packages from top-pypi-packages.json and fetch their metadata for a given field.

(Metadata is cached by source_finder.py in CACHE_DIR.)

Return a count of the most common values (for strings) or keys (for dicts).

Start by:

# Fetch fresh copy of top packages
wget https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json -O \
    data/top-pypi-packages.json

# Show requires_python for the first 10 packages in data/top-pypi-packages.json
python3 project_urls.py --number 10 --field requires_python
Load data/top-pypi-packages.json...
Find requires_python...
100%|█████████████████████████████████████████████| 10/10 [00:00<00:00, 104.96project/s]

| requires_python                                             | Count |
|:------------------------------------------------------------|------:|
| >= 3.6                                                      |     4 |
| !=3.0.*,!=3.1.*,!=3.2.*,>=2.7                               |     1 |
| >=2.7, !=3.0.*, !=3.1.*, !=3.2.*                            |     1 |
| >=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.* |     1 |
| >=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4      |     1 |
| >=3.6                                                       |     1 |
| >=3.7                                                       |     1 |

Projects with requires_python: 10/10

# Show project_urls for the first 10 packages and also the Source URLs
python3 project_urls.py --number 10 --key Source
Load data/top-pypi-packages.json...
Find project_urls...
100%|█████████████████████████████████████████████| 10/10 [00:00<00:00, 154.35project/s]

| project_urls  | Count |
|:--------------|------:|
| Homepage      |    10 |
| Documentation |     6 |
| Source        |     3 |
| Bug Tracker   |     1 |
| CI            |     1 |
| Code          |     1 |
| Download      |     1 |
| Issue tracker |     1 |
| Mailing lists |     1 |
| Source Code   |     1 |

Projects with project_urls: 10/10

| Project         | Source URL                           |
|:----------------|:-------------------------------------|
| boto3           | https://github.com/boto/boto3        |
| python-dateutil | https://github.com/dateutil/dateutil |
| requests        | https://github.com/psf/requests      |
"""
import argparse
import collections
from pprint import pprint  # noqa: F401

import httpx
from prettytable import MARKDOWN, PrettyTable
from tqdm import tqdm

from source_finder import pypi_json
from top_repos import get_top_packages


def get_field(field: str, package: str):
    try:
        res = pypi_json(package)
        return res["info"][field]
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
    parser.add_argument("-f", "--field", default="project_urls", help="Show this field")
    parser.add_argument(
        "-k", "--key", help="For dict fields, also show the values for this key"
    )
    args = parser.parse_args()

    # Load from top-pypi-packages.json
    packages_todo = get_top_packages()
    if args.number:
        packages_todo = packages_todo[: args.number]

    print(f"Find {args.field}...")

    fields = []
    all_keys = []
    selected_urls = []
    count = 0
    for package in tqdm(packages_todo, unit="project"):
        field = get_field(args.field, package["name"])
        if field:
            fields.append(field)
            if isinstance(field, dict):
                all_keys.extend(field.keys())
                count += 1
                if args.key:
                    try:
                        selected_urls.append((package["name"], field[args.key]))
                    except KeyError:
                        pass

    # For strings, print table of most common
    if isinstance(fields[0], str):
        fields = sorted(fields)
        most_common = collections.Counter(fields).most_common()
        count = len(fields)

    # For dicts, print table of most common keys
    elif isinstance(fields[0], dict):
        # Counter will sort by most common, but let's sort alphabetically
        # for those with the same count
        all_keys = sorted(all_keys)
        most_common = collections.Counter(all_keys).most_common()

    table = PrettyTable()
    table.field_names = [args.field, "Count"]
    table.align = "l"
    table.align["Count"] = "r"
    table.set_style(MARKDOWN)
    table.add_rows(most_common)
    print()
    print(table)

    print()
    print(f"Projects with {args.field}: {count}/{args.number}")

    if args.key:
        print()
        table = PrettyTable()
        table.field_names = ["Project", f"{args.key} URL"]
        table.align = "l"
        table.set_style(MARKDOWN)
        table.add_rows(selected_urls)
        print(table)
        print()


if __name__ == "__main__":
    main()
