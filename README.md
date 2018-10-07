# pypi-tools

[![Build Status](https://travis-ci.org/hugovk/pypi-tools.svg?branch=master)](https://travis-ci.org/hugovk/pypi-tools)

Command-line Python scripts to do things with the
[Python Package Index (PyPI)](https://pypi.org/).

## pypi-trends.py

pypi-trends.py is a wrapper around [pypinfo](https://github.com/ofek/pypinfo)
to fetch all monthly downloads from the PyPI database on Google BigQuery and
save them as JSON files.

For the examples below, data was downloaded over three or four days as getting
all months uses up a lot of free BigQuery quota.

## jsons2csv.py

jsons2csv.py converts the JSON files into a single CSV file for chart-wrangling 
in a spreadsheet, and can generate a chart using Matplotlib.

## Examples

Here the pip installs for all packages from the Python Package Index (PyPI),
from January 2016 onwards:

![Chart showing pip installs for Python 3 increasing from under 10% to around 35%](data/pip-install-all.png)

For the [NumPy](https://github.com/numpy/numpy) scientific computing library:

!["Chart showing pip installs for Python 3 increasing from under 20% to around 55%"](data/pip-install-numpy.png)

For the [Pillow](https://github.com/python-pillow/Pillow) imaging library:

!["Chart showing pip installs for Python 3 increasing from under 20% to around 55%"](data/pip-install-pillow.png)

For the [Django](https://github.com/python-pillow/Pillow) web framework:

!["Chart showing pip installs for Python 3 increasing from under 30% to around 65%"](data/pip-install-django.png)

And for the [pylast](https://github.com/pylast/pylast) interface to Last.fm:

!["Chart showing pip installs for Python 3 increasing from under 20% to over 50%"](data/pip-install-pylast.png)

## See also

* [Python version share over time](https://medium.com/@hugovk/python-version-share-over-time-cf4498822650)
