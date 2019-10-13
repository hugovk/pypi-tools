# pypi-tools

[![Build Status](https://travis-ci.org/hugovk/pypi-tools.svg?branch=master)](https://travis-ci.org/hugovk/pypi-tools)
[![Python: 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

Command-line Python scripts to do things with the
[Python Package Index (PyPI)](https://pypi.org/).

## pypi-trends.py

pypi-trends.py is a wrapper around [pypinfo](https://github.com/ofek/pypinfo)
to fetch all monthly downloads from the PyPI database on Google BigQuery and
save them as JSON files.

For the examples below, data was downloaded over a few days as getting all
months uses up a lot of free BigQuery quota.

## jsons2csv.py

jsons2csv.py converts the JSON files into a single CSV file for chart-wrangling
in a spreadsheet, and can generate a chart using Matplotlib.

## Examples

Here the pip installs for all packages from the Python Package Index (PyPI),
from January 2016 onwards:

![Chart showing pip installs for Python 3 increasing from under 10% to around 35%](images/pip-install-all.png)

### [pip](https://github.com/pypa/pip)

The package installer

![](images/pip-install-pip.png)

### [six](https://github.com/benjaminp/six)

Python 2 and 3 compatibility library

![](images/pip-install-six.png)

### [NumPy](https://github.com/numpy/numpy)

Scientific computing library

!["Chart showing pip installs for Python 3 increasing from under 20% to around 55%"](images/pip-install-numpy.png)

### [pytest](https://github.com/pytest-dev/pytest)

Testing framework

![](images/pip-install-pytest.png)

### [pandas](https://github.com/pandas-dev/pandas)

Data analysis toolkit

![](images/pip-install-pandas.png)

### [Coverage.py](https://github.com/nedbat/coveragepy)

Code coverage testing

![](images/pip-install-coverage.png)

### [Pillow](https://github.com/python-pillow/Pillow)

Imaging library

!["Chart showing pip installs for Python 3 increasing from under 20% to around 55%"](images/pip-install-pillow.png)

### [Matplotlib](https://github.com/matplotlib/matplotlib)

2D plotting library

![](images/pip-install-matplotlib.png)

### [Django](https://github.com/python-pillow/Pillow)

Web framework

!["Chart showing pip installs for Python 3 increasing from under 30% to around 65%"](images/pip-install-django.png)

### [Flake8](https://gitlab.com/pycqa/flake8)

Linter

![](images/pip-install-flake8.png)

### [Pylint](https://github.com/PyCQA/pylint/)

Linter

![](images/pip-install-pylint.png)

### [TensorFlow](https://github.com/tensorflow/tensorflow/)

Machine learning library

![](images/pip-install-tensorflow.png)

### [pylast](https://github.com/pylast/pylast)

Interface to Last.fm

!["Chart showing pip installs for Python 3 increasing from under 20% to over 50%"](images/pip-install-pylast.png)

## See also

* [Python version share over time](https://medium.com/@hugovk/python-version-share-over-time-cf4498822650)
