#!/usr/bin/env python3
"""
Find PyPI packages in pypi-deps-db which depend on a given package

Uses:
https://github.com/DavHau/pypi-deps-db

Start by:

# Fetch fresh copy of pypi-deps-db
cd /tmp
wget https://github.com/DavHau/pypi-deps-db/archive/refs/heads/master.zip -O \
    pypi-deps-db.zip
unzip pypi-deps-db.zip  # extracts to /tmp/pypi-deps-db-master

# Fetch fresh copy of top packages
wget https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json -O \
    data/top-pypi-packages.json

Example usage:

# Print only those found in the top 4,000
python3 dependency_finder.py sklearn

# Print all
python3 dependency_finder.py sklearn --all
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from pprint import pprint  # noqa: F401

from termcolor import cprint  # pip install termcolor
from tqdm import tqdm  # pip install tqdm

import source_finder
from source_finder import _print_verbose
from top_repos import get_top_packages

BASE_URL = "https://pypi.org/pypi"
DB_DIR = Path("/tmp/pypi-deps-db-master")
USER_AGENT = "source_finder.py"
VERBOSE = False
PRINT = False

# PEP 426: Only valid characters in a name are:
# the ASCII alphabet, ASCII numbers, ., -, and _.
# PEP 523: Normalised names are lowercase with all runs of the
# characters ., -, or _ replaced with a single - character.
# So "^([a-z0-9-]+)"
REQUIRES_DIST_NAME_REGEX = re.compile("^([a-z0-9-]+)")


def do_sdist(target_package: str, data: dict) -> dict:
    found = defaultdict(set)

    for package in data:  # e.g. "a10-neutron-lbaas"
        _print_verbose(package)
        last_package = None
        last_version = None
        for version in data[package]:  # e.g. "1.0.1"
            _print_verbose(" " + version)

            if not isinstance(data[package][version], dict):
                continue
            for py_ver in data[package][version]:  # e.g. "27"
                if "install_requires" not in data[package][version][py_ver]:
                    continue
                install_requires = data[package][version][py_ver]["install_requires"]

                for dependency in install_requires:
                    _print_verbose("    " + dependency)
                    result = REQUIRES_DIST_NAME_REGEX.match(dependency)
                    if result:
                        _print_verbose("    " + result.group(0))
                        if result.group(0) == target_package:
                            last_package = package
                            last_version = version

        if last_package:
            found[last_package].add(last_version)

    return found


def do_wheel(target_package: str, data: dict) -> dict:
    found = defaultdict(set)

    for package in data:  # e.g. "aap-client-python"
        _print_verbose(package)
        for tag in data[package]:  # e.g. "py2.py3"
            _print_verbose(" " + tag)
            requires_dist = None
            last_package = None
            last_dist = None

            for version in data[package][tag]:  # e.g. "0.1.1"
                _print_verbose("  " + version)

                # e.g. "aap_client_python-0.1.1-py2.py3-none-any.whl"
                for dist in data[package][tag][version]:
                    _print_verbose("   " + dist)

                    # We only want info for the last version, okay to overwrite
                    if "requires_dist" not in data[package][tag][version][dist]:
                        continue
                    requires_dist = data[package][tag][version][dist]["requires_dist"]
                    last_package = package
                    last_dist = dist

            _print_verbose(" " + str(requires_dist))
            if not requires_dist:
                continue
            for dependency in requires_dist:
                _print_verbose("    " + dependency)
                result = REQUIRES_DIST_NAME_REGEX.match(dependency)
                if result:
                    _print_verbose("    " + result.group(0))
                    if result.group(0) == target_package:
                        found[last_package].add(last_dist)

    return found


def find_dependant_packages(target_package: str, all: bool):
    _print_verbose(target_package)
    found = defaultdict(set)

    json_files = DB_DIR.glob("**/*.json")
    # json_files = [Path("/private/tmp/pypi-deps-db-master/sdist/4a.json")]
    for json_file in tqdm(list(json_files), unit="file"):
        # _print_verbose(json_file)
        if "sdist-errors" in str(json_file):
            continue

        with json_file.open("r") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                cprint(f"Error opening {json_file}", "red")

        if "sdist" in json_file.parts:
            new = do_sdist(target_package, data)
            found = found | new
        if "wheel" in json_file.parts:
            new = do_wheel(target_package, data)
            found = found | new

    if all:
        pprint(found)
        return

    top_packages = [package["name"] for package in get_top_packages()]
    for top_package in top_packages:
        if top_package in found:
            print(top_package, found[top_package])


def main():
    global VERBOSE
    global PRINT
    # Only print when run via __main__
    PRINT = True
    source_finder.PRINT = True

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("package", help="Package")
    parser.add_argument(
        "-a", "--all", action="store_true", help="Show all matching packages"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print debug messages to stderr"
    )
    args = parser.parse_args()

    VERBOSE = args.verbose
    source_finder.VERBOSE = args.verbose

    find_dependant_packages(args.package, args.all)


if __name__ == "__main__":
    main()

# End of file
