#!/usr/bin/env python
"""
Generate README with charts shown with most downloads first
"""
import argparse
import glob
from pprint import pprint

from termcolor import cprint  # pip install termcolor

from jsons2csv import load_data_from_json

# Only need name if different from project
# Only need url if different from https://github.com/{project}/{project}
DETAILS = {
    # "example": {
    #     "name": "Example",
    #     "url": "https://github.com/org/example",
    #     "description": "Example library",
    # },
    "coverage": {
        "name": "Coverage.py",
        "url": "https://github.com/nedbat/coveragepy",
        "description": "Code coverage testing",
    },
    "django": {
        "name": "Django",
        "url": "https://github.com/python-pillow/Pillow",
        "description": "Web framework",
    },
    "flake8": {
        "name": "Flake8",
        "url": "https://gitlab.com/pycqa/flake8",
        "description": "Linter",
    },
    "matplotlib": {
        "name": "Matplotlib",
        "description": "2D plotting library",
    },
    "numpy": {
        "name": "NumPy",
        "description": "Scientific computing library",
    },
    "pandas": {
        "url": "https://github.com/pandas-dev/pandas",
        "description": "Data analysis toolkit",
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
    "pycodestyle": {
        "url": "https://github.com/PyCQA/pycodestyle",
        "description": "Style checker",
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
    "requests": {
        "name": "Requests",
        "url": "https://github.com/psf/requests",
        "description": "HTTP library",
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
    "tensorflow": {
        "name": "TensorFlow",
        "description": "Machine learning library",
    },
    "tqdm": {
        "description": "Extensible progress bar",
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


def update_readme(output):
    with open("README.md") as f:
        contents = f.read()

    before, delim1, _ = contents.partition("[start_generated]: # (start_generated)\n")
    _, delim2, after = contents.partition("[end_generated]: # (end_generated)\n")

    new_contents = before + delim1 + output + delim2 + after

    if contents == new_contents:
        cprint("No changes to README.md", "green")
    else:
        with open("README.md", "w") as f:
            f.write(new_contents)
        cprint("README.md updated", "green")


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

        # Special case, already in README
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

    output = ""
    for project in projects:
        name = DETAILS[project].get("name", project)
        url = DETAILS[project].get("url", f"https://github.com/{project}/{project}")
        description = DETAILS[project]["description"]

        new = f"""
### [{name}]({url})

{description}

![](images/{project}.png)
        """.strip()

        output += new + "\n\n"

    update_readme(output)


if __name__ == "__main__":
    main()

# End of file
