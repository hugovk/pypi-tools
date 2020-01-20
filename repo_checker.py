#!/usr/bin/env python3
"""
Tool to clone repos of popular projects, and run a test command for each.

open list of top repos
open list of repo source
for repo in repos:
    git clone --depth 1 repo_git
    cd repo
    run custom command eg. flake8 --select YTT
    if error, stop (TODO option to keep going)
    TODO option to delete dir

Example usage:

Start by:

# Fetch fresh copy of top packages
wget https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json -O \
    data/top-pypi-packages.json

$ python3 repo_checker.py
$ python3 repo_checker.py --number 10
$ python3 repo_checker.py --number 10 --skip-existing
$ python3 repo_checker.py --number 10 --command "git -C CLONE_DIR pull"
$ python3 repo_checker.py --number 10 -c "flake8 --select XYZ CLONE_DIR" --repos "foo"
"""
import argparse
import os
import subprocess
from pathlib import Path
from pprint import pprint  # noqa: F401

from termcolor import colored  # pip install termcolor

from top_repos import get_top_packages, load_from_file

CLONE_ROOT = Path.home() / "checked_repos"
DEFAULT_CMD = f"flake8 --exclude six.py --extend-ignore C90 --select YTT1 CLONE_DIR"


def create_dir(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)


def recursive_find(inspec):
    import fnmatch
    import os

    matches = []
    head, tail = os.path.split(inspec)
    if len(head) == 0:
        head = "."

    for root, dirnames, filenames in os.walk(head):
        for filename in fnmatch.filter(filenames, tail):
            matches.append(os.path.join(root, filename))

    return matches


def do_cmd(cmd, check_return=True):
    print(cmd)
    result = subprocess.run(cmd.split())
    colour = "green" if result.returncode == 0 else "red"
    print(colored(f"  return code: {result.returncode}", colour))
    if check_return:
        result.check_returncode()


def repo_url_dir_name(url):
    """Like the Linux command: basename url ".git" """
    url = url.rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]
    url = url.split("/")[-1]
    return url


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-n", "--number", type=int, default=10, help="Max number to check"
    )
    parser.add_argument(
        "-c",
        "--command",
        default=DEFAULT_CMD,
        help='Command to run to test a repo. "CLONE_DIR" will be filled in.',
    )
    parser.add_argument(
        "-r", "--repos", nargs="+", help="Skip these repos",
    )
    parser.add_argument(
        "-s",
        "--skip-existing",
        action="store_true",
        help="Don't test existing cloned repos",
    )
    parser.add_argument(
        "--ignore-error",
        action="store_true",
        help="Continue to next repo, even if the command returned an error",
    )
    args = parser.parse_args()

    # Load packages from top-pypi-packages.json
    packages_todo = get_top_packages()
    if args.number:
        packages_todo = packages_todo[: args.number]

    # Load repos from data/top-repos.json
    package_repos = load_from_file("data/top-repos.json", "data")

    repos = {}
    for package_repo in package_repos:
        repos[package_repo["name"]] = package_repo["repo"]

    create_dir(CLONE_ROOT)

    for i, package in enumerate(packages_todo):
        name = package["name"]
        try:
            repo_url = repos[name]
            print(i + 1, colored(f"{name} {repo_url}", "green"))
        except KeyError:
            print(i + 1, colored(f"{name} repo not found", "yellow"))
            continue

        clone_dir = CLONE_ROOT / repo_url_dir_name(repo_url)

        # Skip cloning these
        if name in [
            "aenum",  # Hg
            "backports-ssl-match-hostname",  # Hg
            "enum34",  # Hg
            "et-xmlfile",  # Hg
            "iso8601",  # Hg
            "openpyxl",  # Hg
            "pbr",  # redirect not a repo
            "ruamel-yaml",  # Hg
            "ruamel-yaml-clib",  # Hg
        ]:
            print(colored("  Skipping Hg and uncloneable links", "yellow"))
            continue
        elif os.path.isdir(clone_dir):
            if args.skip_existing:
                print(colored("  Repo exists, skipping", "yellow"))
                continue
        else:
            cmd = f"git clone --depth 1 {repo_url} {clone_dir}"
            do_cmd(cmd)

        # Skip scanning these
        if args.repos and name in args.repos:
            continue

        cmd = f"{args.command}"
        cmd = cmd.replace("CLONE_DIR", str(clone_dir))
        do_cmd(cmd, not args.ignore_error)


if __name__ == "__main__":
    main()

# End of file
