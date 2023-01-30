#!/usr/bin/env python3
"""
Download sdists of top packages on PyPI

Start by:

# Fetch fresh copy of top packages
wget https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json -O \
    data/top-pypi-packages.json

# Download and extract 5 sdists:
python3 download_packages.py --number 5 --extract
"""
from __future__ import annotations

import argparse
import atexit
import os
import shutil
from pathlib import Path
from pprint import pprint  # noqa: F401
from urllib.parse import urlparse

import httpx  # pip install httpx

import source_finder
from repo_checker import create_dir
from source_finder import _clear_cache, _print_verbose, pypi_json
from top_repos import get_top_packages

USER_AGENT = "download_packages.py"
VERBOSE = False
PRINT = False

DOWNLOAD_ROOT = Path.home() / "downloaded_packages" / "sdists"
EXTRACT_ROOT = Path.home() / "downloaded_packages" / "extracted"

atexit.register(_clear_cache)


def find_sdist_url(package):
    """Fetch a package's JSON from PyPI and return the sdist URL (or None)"""
    res = pypi_json(package)
    info = res["info"]
    version = info["version"]
    version_packages = res["releases"][version]
    for package in version_packages:
        if package["packagetype"] == "sdist":
            return package["url"]
    return None


def download_package(client, package) -> Path | None:
    name = package["name"]
    _print_verbose("Package name:", name)
    url = find_sdist_url(name)
    _print_verbose("URL:", url)
    if url is None:
        _print_verbose("No sdist found")
        return None

    u = urlparse(url)
    filename = os.path.basename(u.path)
    filename = DOWNLOAD_ROOT / filename

    _print_verbose("Output filename:", filename)
    if os.path.isfile(filename):
        _print_verbose("File exists, skipping download")
        return filename

    r = client.get(url, headers={"User-Agent": USER_AGENT})

    # Raise if we made a bad request
    # (4XX client error or 5XX server error response)
    _print_verbose("HTTP status code:", r.status_code)
    r.raise_for_status()

    with open(filename, "wb") as f:
        f.write(r.content)

    return filename


def extract_sdist(sdist: Path):
    outdir = str(sdist.name).removesuffix(".tar.gz").removesuffix(".zip")
    if os.path.isdir(EXTRACT_ROOT / outdir):
        _print_verbose("Dir exists, skipping extract")
        return
    shutil.unpack_archive(sdist, EXTRACT_ROOT)


def do_packages(packages_todo, extract: bool):
    with httpx.Client() as client:
        for i, package in enumerate(packages_todo):
            print(i, package)
            filename = download_package(client, package)
            if extract and filename:
                extract_sdist(filename)


def main():
    global VERBOSE
    global PRINT
    # Only print when run via __main__
    PRINT = True
    source_finder.PRINT = True

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-n", "--number", type=int, default=10, help="Max number to fetch"
    )
    parser.add_argument(
        "-s", "--start", type=int, default=1, help="Repo number to begin with"
    )
    parser.add_argument("-x", "--extract", action="store_true", help="Extract sdists")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print debug messages to stderr"
    )
    args = parser.parse_args()

    VERBOSE = args.verbose
    source_finder.VERBOSE = args.verbose

    # Load packages from top-pypi-packages.json
    packages_todo = get_top_packages()
    if args.number:
        packages_todo = packages_todo[args.start - 1 : args.start + args.number - 1]

    create_dir(DOWNLOAD_ROOT)

    do_packages(packages_todo, args.extract)


if __name__ == "__main__":
    main()

# End of file
