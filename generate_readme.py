#!/usr/bin/env python
"""
Generate Markdown with charts, showing with most downloads first
"""
from __future__ import annotations

import argparse
import glob
from pprint import pprint

from termcolor import cprint  # pip install termcolor

from jsons2csv import load_data_from_json

DETAILS = {
    # "project": {
    #     "name": "Example",  # Only needed if different from project
    #     "url": "https://github.com/org/example", # If different from https://github.com/{project}/{project}  # noqa: E501
    #     "description": "Example library",
    # },
    "attrs": {
        "url": "https://github.com/python-attrs/attrs",
        "description": "Python classes without boilerplate",
    },
    "black": {
        "name": "Black",
        "url": "https://github.com/psf/black",
        "description": "The uncompromising Python code formatter",
    },
    "certifi": {
        "name": "Certifi",
        "url": "https://github.com/certifi/python-certifi",
        "description": "Provides Mozilla's CA Bundle",
    },
    "cibuildwheel": {
        "url": "https://github.com/pypa/cibuildwheel",
        "description": "Build Python wheels on CI with minimal configuration",
    },
    "colorama": {
        "name": "Colorama",
        "url": "https://github.com/tartley/colorama",
        "description": "Simple cross-platform colored terminal text in Python",
    },
    "coverage": {
        "name": "Coverage.py",
        "url": "https://github.com/nedbat/coveragepy",
        "description": "Code coverage testing",
    },
    "cryptography": {
        "url": "https://github.com/pyca/cryptography",
        "description": "Cryptographic recipes and primitives for developers",
    },
    "cython": {
        "name": "Cython",
        "description": "Python to C compiler",
    },
    "django": {
        "name": "Django",
        "url": "https://github.com/python-pillow/Pillow",
        "description": "Web framework",
    },
    "flake8": {
        "name": "Flake8",
        "url": "https://github.com/PyCQA/flake8",
        "description": "Linter",
    },
    "project": {
        "name": "Flask",
        "url": "https://github.com/pallets/flask",
        "description": "Micro framework for building web apps",
    },
    "html5lib": {
        "url": "https://github.com/html5lib/html5lib-python",
        "description": "HTML parser",
    },
    "httpx": {
        "name": "HTTPX",
        "url": "https://github.com/encode/httpx",
        "description": "HTTP client",
    },
    "humanize": {
        "url": "https://github.com/jmoiron/humanize",
        "description": "Humanization utilities",
    },
    "matplotlib": {
        "name": "Matplotlib",
        "description": "2D plotting library",
    },
    "nose2": {
        "name": "nose2",
        "url": "https://github.com/nose-devs/nose2",
        "description": "Testing framework",
    },
    "numpy": {
        "name": "NumPy",
        "description": "Scientific computing library",
    },
    "pandas": {
        "url": "https://github.com/pandas-dev/pandas",
        "description": "Data analysis toolkit",
    },
    "paramiko": {
        "name": "Paramiko",
        "description": "SSHv2 protocol library",
    },
    "pillow": {
        "name": "Pillow",
        "url": "https://github.com/python-pillow/Pillow",
        "description": "Imaging library",
    },
    "pip": {
        "url": "https://github.com/pypa/pip",
        "description": "The package installer",
    },
    "prettytable": {
        "name": "PrettyTable",
        "url": "https://github.com/jazzband/prettytable",
        "description": "Display data in visually appealing ASCII table format",
    },
    "pycodestyle": {
        "url": "https://github.com/PyCQA/pycodestyle",
        "description": "Style checker",
    },
    "pyflakes": {
        "name": "Pyflakes",
        "url": "https://github.com/PyCQA/pyflakes",
        "description": "Checks source files for errors",
    },
    "pylast": {
        "description": "Interface to Last.fm",
    },
    "pylint": {
        "name": "Pylint",
        "url": "https://github.com/PyCQA/pylint",
        "description": "Linter",
    },
    "pytest": {
        "url": "https://github.com/pytest-dev/pytest",
        "description": "Testing framework",
    },
    "pytest-cov": {
        "url": "https://github.com/pytest-dev/pytest-cov",
        "description": "Coverage plugin for pytest",
    },
    "python-dateutil": {
        "name": "dateutil",
        "url": "https://github.com/dateutil/dateutil",
        "description": "Useful extensions to the standard datetime features",
    },
    "pytz": {
        "url": "https://github.com/stub42/pytz",
        "description": "historical timezone library and database",
    },
    "requests": {
        "name": "Requests",
        "url": "https://github.com/psf/requests",
        "description": "HTTP library",
    },
    "rich": {
        "name": "Rich",
        "url": "https://github.com/Textualize/rich",
        "description": "Library for rich text and beautiful formatting in the terminal",
    },
    "scikit-learn": {
        "description": "Machine learning",
    },
    "scipy": {
        "name": "SciPy",
        "description": "For mathematics, science, and engineering",
    },
    "setuptools": {
        "url": "https://github.com/pypa/setuptools",
        "description": "Build system",
    },
    "six": {
        "url": "https://github.com/benjaminp/six",
        "description": "Python 2 and 3 compatibility library",
    },
    "tablib": {
        "name": "Tablib",
        "url": "https://github.com/jazzband/tablib",
        "description": "Format-agnostic tabular dataset library",
    },
    "tensorflow": {
        "name": "TensorFlow",
        "description": "Machine learning library",
    },
    "termcolor": {
        "description": "ANSI color formatting for output in terminal",
    },
    "tox": {
        "url": "https://github.com/tox-dev/tox",
        "description": "Generic virtualenv management and test command line tool",
    },
    "tqdm": {
        "description": "Extensible progress bar",
    },
    "twitter": {
        "name": "Python Twitter Tools",
        "url": "https://github.com/python-twitter-tools/twitter",
        "description": "Python Twitter API",
    },
    "ujson": {
        "name": "UltraJSON",
        "url": "https://github.com/ultrajson/ultrajson",
        "description": "JSON decoder and encoder",
    },
    "urllib3": {
        "description": "HTTP client",
    },
    "virtualenv": {
        "url": "https://github.com/pypa/virtualenv",
        "description": "Virtual Python environment builder",
    },
    "wheel": {
        "url": "https://github.com/pypa/wheel",
        "description": "Binary distribution format",
    },
}


def remove_prefix(text, prefix):
    # Python 3.9+
    try:
        return text.removeprefix(prefix)
    except AttributeError:
        if text.startswith(prefix):
            return text[len(prefix) :]
        return text


def remove_suffix(text, suffix):
    # Python 3.9+
    try:
        return text.removesuffix(suffix)
    except AttributeError:
        if text.endswith(suffix):
            return text[: -len(suffix)]
        return text


def get_output(projects: list[str], number: int | None = 0) -> str:
    output = ""
    if not number:
        number = len(projects)

    for project in projects[:number]:
        name = DETAILS[project].get("name", project)
        url = DETAILS[project].get("url", f"https://github.com/{project}/{project}")
        description = DETAILS[project]["description"]

        new = f"""
### [{name}]({url})

{description}

![](images/{project}.png)
        """.strip()

        output += new + "\n\n"

    return output


def update_file(projects: list[str], filename: str, number: int | None = None) -> None:
    output = get_output(projects, number)
    with open(filename) as f:
        contents = f.read()

    before, delim1, _ = contents.partition("[start_generated]: # (start_generated)\n")
    _, delim2, after = contents.partition("[end_generated]: # (end_generated)\n")

    new_contents = before + delim1 + output + delim2 + after

    if contents == new_contents:
        cprint(f"No changes to {filename}", "green")
    else:
        with open(filename, "w") as f:
            f.write(new_contents)
        cprint(f"{filename} updated", "green")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-i", "--inspec", default="images/*.png", help="Input file spec"
    )
    args = parser.parse_args()

    images = sorted(glob.glob(args.inspec))
    pprint(images)
    project_downloads = dict()

    for image in images:
        project = image
        project = remove_prefix(project, "images/")
        project = remove_suffix(project, ".png")

        # Special case, already in the file
        if project == "all":
            continue

        # No need processing new project not yet added to DETAILS
        try:
            assert DETAILS[project]
        except KeyError:
            cprint(f"{project} not found in DETAILS, skipping", "yellow")
            continue

        json_spec = f"data/{project}*.json"
        all_data, _ = load_data_from_json(json_spec)
        total_downloads = 0
        for x in all_data:
            downloads = [v for v in x.values() if isinstance(v, int)]
            total_downloads += sum(downloads)

        project_downloads[project] = total_downloads

    # pprint(project_downloads)
    # Sort projects by most downloads
    projects = sorted(project_downloads, key=project_downloads.get, reverse=True)
    # pprint(projects)

    # Output Markdown images, most downloaded first
    update_file(projects, "README.md", 2)
    update_file(projects, "charts.md")


if __name__ == "__main__":
    main()

# End of file
