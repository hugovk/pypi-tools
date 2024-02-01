"""
Read in packages from top-pypi-packages.json and create
a corresponding list of repos in top-repos.json

Start by:

# Fetch fresh copy of top packages
wget https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json -O \
    data/top-pypi-packages.json

# Check the first 10 packages in data/top-pypi-packages.json
python3 top_repos.py --number 10

# Repos are added to data/top-repos.json.

# Check the first 10 packages and update URLs if they've changed
python3 top_repos.py --number 10 --update
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import traceback
from pprint import pprint  # noqa: F401

import pypidb  # pip install pypidb
import requests
from termcolor import cprint  # pip install termcolor


def get_top_packages():
    packages = load_from_file("data/top-pypi-packages.json", "rows")

    for package in packages:
        # Don't need download counts
        package.pop("download_count")
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


def save_to_file(packages, file_name):
    print(f"Save {file_name}...")
    now = dt.datetime.now(dt.timezone.utc)

    with open(file_name, "w") as f:
        f.write(
            json.dumps(
                {"data": packages, "last_update": now.strftime("%A, %d %B %Y, %X %Z")},
                indent=0,
            )
        )


def remove_done(packages_todo, packages_done):
    """Remove packages that are already done"""
    new = []
    count_exists = 0
    for package in packages_todo:
        todo = package["name"]
        # Already there?
        exists = any(d["name"] == todo for d in packages_done)
        if exists:
            count_exists += 1
        else:
            new.append(package)
    print(f"Already done: {count_exists}")
    return new, count_exists


def update_existing(packages, name, new_repo):
    updated = 0
    for package in packages:
        if package["name"] == name:
            if package["repo"] != new_repo:
                package["repo"] = new_repo
                updated = 1
    return updated


def main():
    db = pypidb.Database()

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-n", "--number", type=int, default=100, help="Max number to fetch"
    )
    parser.add_argument(
        "-u", "--update", action="store_true", help="Update existing URLs if changed"
    )
    args = parser.parse_args()

    try:
        packages_done = load_from_file("data/top-repos.json", "data")
    except FileNotFoundError:
        packages_done = []

    # Load from top-pypi-packages.json
    packages_todo = get_top_packages()
    if args.number:
        packages_todo = packages_todo[: args.number]

    # Remove packages that are already done
    count_exists = 0
    if not args.update:
        packages_todo, count_exists = remove_done(packages_todo, packages_done)

    print("Find new repos...")
    new = []
    count_updated = 0
    count_not_found = 0
    for i, package in enumerate(packages_todo):
        done = False
        try:
            repo = db.find_project_scm_url(package["name"])
        except (
            pypidb._exceptions.IncompletePackageMetadata,
            pypidb._exceptions.InvalidPackage,
            pypidb._exceptions.InvalidPackageVersion,
            pypidb._exceptions.PackageWithoutUrls,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
        ):
            cprint(traceback.format_exc(), "red")
            repo = None
        if repo:
            package["repo"] = repo
            if args.update:
                updated = update_existing(packages_done, package["name"], repo)
                count_updated += updated
                if updated:
                    done = True
            else:
                new.append(package)
                done = True
            if done:
                cprint(f"{count_exists+i+1} {package['name']}\t{repo}", "green")
        else:
            cprint(f"{count_exists+i+1} {package['name']}", "red")
            count_not_found += 1
    packages_todo = new
    print(f"Old repos: {count_exists}")
    print(f"New repos: {len(new)}")
    print(f"Updated repos: {count_updated}")
    print(f"Not found: {count_not_found}")

    if len(new) or count_updated:
        save_to_file(packages_done + packages_todo, "data/top-repos.json")


if __name__ == "__main__":
    main()
