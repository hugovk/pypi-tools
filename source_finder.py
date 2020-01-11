#!/usr/bin/env python3
"""
Thing to find the repo for a package on PyPI

Example usage:

$ python3 source_finder.py six
https://github.com/benjaminp/six

$ python3 source_finder.py urllib3
None
"""
import argparse
import atexit
import json
import sys
from datetime import datetime
from pathlib import Path
from pprint import pprint  # noqa: F401
from urllib.parse import urlparse

import requests  # pip install requests
from appdirs import user_cache_dir  # pip install appdirs
from slugify import slugify  # pip install python-slugify
from termcolor import colored  # pip install termcolor

BASE_URL = "https://pypi.org/pypi"
CACHE_DIR = Path(user_cache_dir("source-finder"))
USER_AGENT = "source_finder.py"
VERBOSE = False
PRINT = False


def _print_verbose(*args, **kwargs):
    """Print if verbose"""
    if PRINT and VERBOSE:
        _print_stderr(*args, **kwargs)


def _print_stderr(*args, **kwargs):
    """Print to stderr"""
    if PRINT:
        print(*args, file=sys.stderr, **kwargs)


def _cache_filename(url):
    """yyyy-mm-url-slug.json"""
    today = datetime.utcnow().strftime("%Y-%m")
    slug = slugify(url)
    filename = CACHE_DIR / f"{today}-{slug}.json"

    return filename


def _load_cache(cache_file):
    if not cache_file.exists():
        return {}

    with cache_file.open("r") as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            return {}

    return data


def _save_cache(cache_file, data):
    try:
        if not CACHE_DIR.exists():
            CACHE_DIR.mkdir(parents=True)

        with cache_file.open("w") as f:
            json.dump(data, f)

    except OSError:
        pass


def _clear_cache():
    """Delete old cache files, run as last task"""
    cache_files = CACHE_DIR.glob("**/*.json")
    this_month = datetime.utcnow().strftime("%Y-%m")
    for cache_file in cache_files:
        if not cache_file.name.startswith(this_month):
            cache_file.unlink()


atexit.register(_clear_cache)


def json_url(package_name):
    return BASE_URL + "/" + package_name + "/json"


def pypi_json(package):
    url = json_url(package)
    cache_file = _cache_filename(url)
    _print_verbose("API URL:", url)
    _print_verbose("Cache file:", cache_file)

    res = {}
    if cache_file.is_file():
        _print_verbose("Cache file exists")
        res = _load_cache(cache_file)

    if res == {}:
        # No cache, or couldn't load cache
        r = requests.get(url, headers={"User-Agent": USER_AGENT})

        # Raise if we made a bad request
        # (4XX client error or 5XX server error response)
        _print_verbose("HTTP status code:", r.status_code)
        r.raise_for_status()

        res = r.json()

        _save_cache(cache_file, res)

    return res


def _has_scm_link(s):
    return (
        "github.com" in s
        or "gitlab.com" in s
        or "bitbucket.org" in s
        or "bitbucket.com" in s
    )


def _normalise_url(url):
    """Strip out junk"""
    if not url:
        return url

    if not _has_scm_link(url):
        return url

    u = urlparse(url)
    path_parts = u.path.split("/")
    keep_parts = path_parts[:3]
    new_path = "/".join(keep_parts)
    return url.replace(u.path, new_path)


def find_source_repo(package):

    found_url = None

    res = pypi_json(package)
    info = res["info"]
    project_urls = info["project_urls"]

    if project_urls:
        # Check for explicit ones first, assume have SCM link
        for text in ["Source Code", "Code", "Source"]:
            if text in project_urls:
                url = project_urls[text]
                _print_verbose(f"project_urls\t{text}\t{url}")
                _print_verbose("Success!")
                if not found_url:
                    found_url = url

        # Check for explicit ones first, must have SCM link
        for text in ["Homepage"]:
            if text in project_urls:
                url = project_urls[text]
                _print_verbose(f"project_urls\t{text}\t{url}")
                if _has_scm_link(url):
                    _print_verbose("Success!")
                    if not found_url:
                        found_url = url

        # Check them all
        for url in project_urls:
            _print_verbose(f"project_urls\t{url}\t{project_urls[url]}")
            if _has_scm_link(project_urls[url]):
                _print_verbose("Success!")
                if not found_url:
                    found_url = project_urls[url]

    if _has_scm_link(info["description"]):
        _print_verbose("git link in description")
        _print_verbose("Semi-success!")
        if not found_url:
            _print_verbose("TODO extract URL from description")
            _print_verbose(info["description"])

    found_url = _normalise_url(found_url)

    if found_url and PRINT:
        print(colored(found_url, "green"))
    else:
        _print_stderr(colored(found_url, "red"))

    return found_url


def main():
    global VERBOSE
    global PRINT
    # Only print when run via __main__
    PRINT = True

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("package", help="Package")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print debug messages to stderr"
    )
    args = parser.parse_args()

    VERBOSE = args.verbose
    find_source_repo(args.package)


if __name__ == "__main__":
    main()

# End of file
