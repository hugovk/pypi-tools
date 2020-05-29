# pypi-tools

[![Build Status](https://travis-ci.org/hugovk/pypi-tools.svg?branch=master)](https://travis-ci.org/hugovk/pypi-tools)
[![Python: 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

Command-line Python scripts to do things with the
[Python Package Index (PyPI)](https://pypi.org/).

## pypi-trends.py

pypi-trends.py is a wrapper around [pypinfo](https://github.com/ofek/pypinfo)
and [pypistats](https://github.com/hugovk/pypistats) to fetch all monthly downloads from
the PyPI database on Google BigQuery and save them as JSON files.

For the examples below, data was downloaded over a few days as getting all
months uses up a lot of free BigQuery quota.

## jsons2csv.py

jsons2csv.py converts the JSON files into a single CSV file for chart-wrangling
in a spreadsheet, and can generate a chart using Matplotlib.

## Examples

Here the pip installs for all packages from the Python Package Index (PyPI),
from January 2016 onwards:

![](images/pip-install-all.png)

### [urllib3](https://github.com/urllib3/urllib3)

HTTP client

![](images/pip-install-urllib3.png)

### [six](https://github.com/benjaminp/six)

Python 2 and 3 compatibility library

![](images/pip-install-six.png)

### [pip](https://github.com/pypa/pip)

The package installer

![](images/pip-install-pip.png)

### [Requests](https://github.com/psf/requests)

HTTP library

![](images/pip-install-requests.png)

### [NumPy](https://github.com/numpy/numpy)

Scientific computing library

![](images/pip-install-numpy.png)

### [pandas](https://github.com/pandas-dev/pandas)

Data analysis toolkit

![](images/pip-install-pandas.png)

### [pytest](https://github.com/pytest-dev/pytest)

Testing framework

![](images/pip-install-pytest.png)

### [SciPy](https://github.com/scipy/scipy)

For mathematics, science, and engineering

![](images/pip-install-scipy.png)

### [Coverage.py](https://github.com/nedbat/coveragepy)

Code coverage testing

![](images/pip-install-coverage.png)

### [Pillow](https://github.com/python-pillow/Pillow)

Imaging library

!["Chart showing pip installs for Python 3 increasing from under 20% to around 55%"](images/pip-install-pillow.png)

### [Matplotlib](https://github.com/matplotlib/matplotlib)

2D plotting library

![](images/pip-install-matplotlib.png)

### [Flake8](https://gitlab.com/pycqa/flake8)

Linter

![](images/pip-install-flake8.png)

### [Django](https://github.com/python-pillow/Pillow)

Web framework

!["Chart showing pip installs for Python 3 increasing from under 30% to around 65%"](images/pip-install-django.png)

### [TensorFlow](https://github.com/tensorflow/tensorflow/)

Machine learning library

![](images/pip-install-tensorflow.png)

### [Pylint](https://github.com/PyCQA/pylint/)

Linter

![](images/pip-install-pylint.png)

<!--
### [pylast](https://github.com/pylast/pylast)

Interface to Last.fm

!["Chart showing pip installs for Python 3 increasing from under 20% to over 50%"](images/pip-install-pylast.png)
-->

### See also

* [Python version share over time](https://medium.com/@hugovk/python-version-share-over-time-cf4498822650)

## source-finder.py

Given a PyPI package, `source_finder.py` looks for the source repository in its metadata.

```console
$ python source_finder.py six
https://github.com/benjaminp/six
$ python source_finder.py urllib3
None
```

It caches the JSON metadata downloaded from PyPI in a temporary directory, use the `--verbose` option to see where. The cache files will be deleted the next month.

```console
$ python source_finder.py s3transfer --verbose
API URL: https://pypi.org/pypi/s3transfer/json
Cache file: /Users/hugo/Library/Caches/source-finder/2019-10-https-pypi-org-pypi-s3transfer-json.json
Cache file exists
project_urls    Homepage        https://github.com/boto/s3transfer
Success!
project_urls    Homepage        https://github.com/boto/s3transfer
Success!
https://github.com/boto/s3transfer
```

## top_repos.py

This will look for the source repo for the top-5,000 most-downloaded packages, using a JSON file from [Top PyPI Packages](https://hugovk.github.io/top-pypi-packages/), and save them to [`data/top-repos.json`](https://hugovk.github.io/pypi-tools/data/top-repos.json).

First, fetch fresh copy of the top packages:

```console
$ wget https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json -O  data/top-pypi-packages.json

--2019-10-14 18:12:45--  https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json
Resolving hugovk.github.io (hugovk.github.io)... 185.199.110.153, 185.199.108.153, 185.199.111.153, ...
Connecting to hugovk.github.io (hugovk.github.io)|185.199.110.153|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 250885 (245K) [application/json]
Saving to: ‘data/top-pypi-packages.json’

data/top-pypi-packages.json      100%[========================================================>] 245.00K  --.-KB/s    in 0.02s

2019-10-14 18:12:45 (14.7 MB/s) - ‘data/top-pypi-packages.json’ saved [250885/250885]
```

Check the first 10 packages:

```console
$ python top_repos.py -n 10
Load data/top-repos.json...
Load top-pypi-packages.json...
Already done: 0
Find new repos...
1 urllib3
2 six       https://github.com/benjaminp/six
3 requests
4 botocore  https://github.com/boto/botocore
5 python-dateutil
6 certifi
7 s3transfer        https://github.com/boto/s3transfer
8 pip
9 idna      https://github.com/kjd/idna
10 docutils
Old repos: 0
New repos: 4
Not found: 6
Save data/top-repos.json...
```

When running again:
* if a package already has a repo, it's not checked again in case it's changed
* if a package doesn't have a repo, it will be checked

Currently, it finds 3,951 repos for the top 5,000 packages.

I'm not planning on automating this, but can run it from time to time to update it.
