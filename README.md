# pypi-tools

[![Build Status](https://travis-ci.org/hugovk/pypi-tools.svg?branch=master)](https://travis-ci.org/hugovk/pypi-tools)

Command-line Python scripts to do things with the
[Python Package Index (PyPI)](https://pypi.org/).

## pypi-trends.py

pypi-trends.py is a wrapper around [pypinfo](https://github.com/ofek/pypinfo)
to fetch all monthly downloads from the PyPI database on Google BigQuery and
save them as JSON files.

## jsons2csv.py

jsons2csv.py converts the JSON files into a single CSV file for
chart-wrangling in a spreadsheet.

## Examples

Here the pip installs for all packages from the Python Package Index (PyPI),
between January 2016 and June 2018:

![alt text](data/pip-install-all.png "Chart showing pip installs for Python 3 increasing from under 10% in 2016-01 to around 35% in 2018-06")

And for the [Pillow](https://github.com/python-pillow/Pillow) imaging library:

![alt text](data/pip-install-pillow.png "Chart showing pip installs for Python 3 increasing from under 10% in 2016-01 to around 35% in 2018-06")

## See also

* [Python version share over time](https://medium.com/@hugovk/python-version-share-over-time-cf4498822650)
