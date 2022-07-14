#!/usr/bin/env python3
"""
For a given project, get list of dependants from libraries.io

Log in and get your key from https://libraries.io/api

Then:

export LIBRARIES_API_KEY=TODO_ENTER_YOURS_HERE

python3 repo_checker.py my_package --projects

OR

python3 repo_checker.py my_package --repos
"""
import argparse
from pprint import pprint  # noqa: F401

# from pybraries.search import Search
from pybraries.search_helpers import search_api

try:
    from rich import print
except ImportError:
    pass


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("library", help="Library to search for dependants for")
    parser.add_argument(
        "-p", "--projects", action="store_true", help="Show dependant projects"
    )
    parser.add_argument(
        "-r", "--repos", action="store_true", help="Show dependant repos"
    )
    args = parser.parse_args()

    # search = Search()

    if args.projects:
        # Get projects that have at least one version that depends on a given project.
        # https://pybraries.readthedocs.io/en/latest/modules.html
        # #pybraries.search.Search.project_dependents
        print("DEPENDANTS")
        # dependants = search.project_dependents("pypi", args.library)
        page = 0
        total = 0
        while True:
            page += 1
            projects = search_api(
                "project_dependents", "pypi", args.library, per_page=100, page=page
            )
            if not projects:
                break
            for project in projects:
                print(
                    project["name"],
                    # "\t",
                    # project["homepage"],
                    "\t",
                    project["repository_url"],
                    # "\t",
                    # project["description"],
                )
            total += len(projects)
            print(len(projects), total)

        print()

    if args.repos:
        # Get repositories that depend on a given project.
        # https://pybraries.readthedocs.io/en/latest/modules.html
        # #pybraries.search.Search.project_dependent_repositories
        print("DEPENDANT REPOS")
        # repos = search.project_dependent_repositories("pypi", args.library)
        page = 0
        total = 0
        while True:
            page += 1
            repos = search_api(
                "project_dependent_repositories",
                "pypi",
                args.library,
                per_page=100,
                page=page,
            )
            if not repos:
                break
            for repo in repos:
                print(repo["full_name"], "\t", repo["homepage"])
            total += len(repos)
            print(len(repos), total)


if __name__ == "__main__":
    main()
