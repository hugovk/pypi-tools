"""
Read in packages from top-pypi-packages.json and create
a corresponding list of repos in data/top_repos.json

Start by:

# Fetch fresh copy of top packages
wget https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json -O \
    top-pypi-packages.json

# Check the first 10 packages in top-pypi-packages.json
python3 top_repos.py --number 10

# Repos are added to data/top_repos.json. Doesn't check or update existing repos.
"""
import argparse
import datetime
import json
from pprint import pprint  # noqa: F401

import pytz  # pip install pytz
from termcolor import colored  # pip install termcolor

import source_finder


def get_top_packages():
    packages = load_from_file("top-pypi-packages.json", "rows")

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
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    with open(file_name, "w") as f:
        f.write(
            json.dumps(
                {"data": packages, "last_update": now.strftime("%A, %d %B %Y, %X %Z")}
            )
        )


def main():

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-n", "--number", type=int, help="Max number to fetch")
    args = parser.parse_args()

    try:
        packages_done = load_from_file("data/top_repos.json", "data")
    except FileNotFoundError:
        packages_done = []

    # Load from top-pypi-packages.json
    packages_todo = get_top_packages()
    if args.number:
        packages_todo = packages_todo[: args.number]

    # Remove packages that are already done
    new = []
    count = 0
    for package in packages_todo:
        todo = package["name"]
        # Already there?
        exists = any(d["name"] == todo for d in packages_done)
        if exists:
            count += 1
        else:
            new.append(package)
    print(f"Already done: {count}")

    packages_todo = new

    print("Find new repos...")
    new = []
    # TODO multiprocessing
    count = 0
    for i, package in enumerate(packages_todo):
        repo = source_finder.find_source_repo(package["name"])
        if repo:
            package["repo"] = repo
            new.append(package)
            print(colored(f"{i} {package['name']}\t{repo}", "green"))
        else:
            print(colored(f"{i} {package['name']}", "red"))
            count += 1
    packages_todo = new
    print(f"New repos: {len(new)}, no repo: {count}")

    save_to_file(packages_done + packages_todo, "data/top_repos.json")


if __name__ == "__main__":
    main()
