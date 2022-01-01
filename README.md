# pypi-tools

![Test](https://github.com/hugovk/pypi-tools/workflows/Test/badge.svg)
[![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Code style: Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://github.com/psf/black)

Command-line Python scripts to do things with the
[Python Package Index (PyPI)](https://pypi.org/).

## pypi-trends.py

`pypi-trends.py` is a wrapper around [pypinfo](https://github.com/ofek/pypinfo)
and [pypistats](https://github.com/hugovk/pypistats) to fetch all monthly downloads from
the PyPI database on Google BigQuery and save them as JSON files.

For the examples below, data was downloaded over many days as getting all months uses up
a lot of free BigQuery quota.

## jsons2csv.py

`jsons2csv.py` converts the JSON files into a single CSV file for chart-wrangling
in a spreadsheet, and can generate a chart using Matplotlib. Once an image exists, it
can be re-generated with `make -j4`.

## Examples

Here the pip installs for all packages from the Python Package Index (PyPI),
from January 2016 onwards:

![](images/all.png)

[start_generated]: # (start_generated)
### [urllib3](https://github.com/urllib3/urllib3)

HTTP client

![](images/urllib3.png)

### [six](https://github.com/benjaminp/six)

Python 2 and 3 compatibility library

![](images/six.png)

### [dateutil](https://github.com/dateutil/dateutil)

Useful extensions to the standard Python datetime features

![](images/python-dateutil.png)

### [Requests](https://github.com/psf/requests)

HTTP library

![](images/requests.png)

### [setuptools](https://github.com/pypa/setuptools)

Build system

![](images/setuptools.png)

### [pip](https://github.com/pypa/pip)

The package installer

![](images/pip.png)

### [wheel](https://github.com/pypa/wheel)

Binary distribution format

![](images/wheel.png)

### [Colorama](https://github.com/tartley/colorama)

Simple cross-platform colored terminal text in Python

![](images/colorama.png)

### [NumPy](https://github.com/numpy/numpy)

Scientific computing library

![](images/numpy.png)

### [pytz](https://github.com/stub42/pytz)

historical timezone library and database

![](images/pytz.png)

### [cryptography](https://github.com/pyca/cryptography)

cryptographic recipes and primitives to Python developers.

![](images/cryptography.png)

### [attrs](https://github.com/python-attrs/attrs)

Python classes without boilerplate

![](images/attrs.png)

### [pandas](https://github.com/pandas-dev/pandas)

Data analysis toolkit

![](images/pandas.png)

### [pytest](https://github.com/pytest-dev/pytest)

Testing framework

![](images/pytest.png)

### [SciPy](https://github.com/scipy/scipy)

For mathematics, science, and engineering

![](images/scipy.png)

### [Pillow](https://github.com/python-pillow/Pillow)

Imaging library

![](images/pillow.png)

### [scikit-learn](https://github.com/scikit-learn/scikit-learn)

machine learning in Python

![](images/scikit-learn.png)

### [virtualenv](https://github.com/pypa/virtualenv)

Virtual Python environment builder

![](images/virtualenv.png)

### [Coverage.py](https://github.com/nedbat/coveragepy)

Code coverage testing

![](images/coverage.png)

### [Matplotlib](https://github.com/matplotlib/matplotlib)

2D plotting library

![](images/matplotlib.png)

### [tqdm](https://github.com/tqdm/tqdm)

Extensible progress bar

![](images/tqdm.png)

### [Paramiko](https://github.com/paramiko/paramiko)

SSHv2 protocol library

![](images/paramiko.png)

### [pycodestyle](https://github.com/PyCQA/pycodestyle)

Style checker

![](images/pycodestyle.png)

### [TensorFlow](https://github.com/tensorflow/tensorflow)

Machine learning library

![](images/tensorflow.png)

### [Pyflakes](https://github.com/PyCQA/pyflakes)

Checks Python source files for errors

![](images/pyflakes.png)

### [UltraJSON](https://github.com/ultrajson/ultrajson)

JSON decoder and encoder

![](images/ujson.png)

### [Flake8](https://github.com/PyCQA/flake8)

Linter

![](images/flake8.png)

### [pytest-cov](https://github.com/pytest-dev/pytest-cov)

Coverage plugin for pytest

![](images/pytest-cov.png)

### [Pylint](https://github.com/PyCQA/pylint)

Linter

![](images/pylint.png)

### [Django](https://github.com/python-pillow/Pillow)

Web framework

![](images/django.png)

### [html5lib](https://github.com/html5lib/html5lib-python)

HTML parser

![](images/html5lib.png)

### [Black](https://github.com/psf/black)

The uncompromising Python code formatter

![](images/black.png)

### [tox](https://github.com/tox-dev/tox)

Generic virtualenv management and test command line tool

![](images/tox.png)

### [HTTPX](https://github.com/encode/httpx)

HTTP client

![](images/httpx.png)

### [PrettyTable](https://github.com/jazzband/prettytable)

Display data in visually appealing ASCII table format

![](images/prettytable.png)

### [humanize](https://github.com/jmoiron/humanize)

Humanization utilities

![](images/humanize.png)

### [Tablib](https://github.com/jazzband/tablib)

Format-agnostic tabular dataset library

![](images/tablib.png)

### [nose2](https://github.com/nose-devs/nose2)

Testing framework

![](images/nose2.png)

### [Python Twitter Tools](https://github.com/python-twitter-tools/twitter)

Python Twitter API

![](images/twitter.png)

### [pylast](https://github.com/pylast/pylast)

Interface to Last.fm

![](images/pylast.png)

### [cibuildwheel](https://github.com/pypa/cibuildwheel)

Build Python wheels on CI with minimal configuration

![](images/cibuildwheel.png)

[end_generated]: # (end_generated)

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

It caches the JSON metadata downloaded from PyPI in a temporary directory, use the
`--verbose` option to see where. The cache files will be deleted the next month.

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

This will look for the source repo for the most-downloaded packages, using a JSON file
from [Top PyPI Packages](https://hugovk.github.io/top-pypi-packages/), and save them to
[`data/top-repos.json`](https://hugovk.github.io/pypi-tools/data/top-repos.json).

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
