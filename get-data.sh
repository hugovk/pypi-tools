#!/usr/bin/env bash

FROM="2019-08"

python3 pypi-trends.py -f $FROM
python3 pypi-trends.py -f $FROM -p pillow
python3 pypi-trends.py -f $FROM -p pytest
python3 pypi-trends.py -f $FROM -p pip
python3 pypi-trends.py -f $FROM -p pylast
python3 pypi-trends.py -f $FROM -p coverage
python3 pypi-trends.py -f $FROM -p numpy
python3 pypi-trends.py -f $FROM -p django
python3 pypi-trends.py -f $FROM -p matplotlib
python3 pypi-trends.py -f $FROM -p pylint
python3 pypi-trends.py -f $FROM -p flake8
python3 pypi-trends.py -f $FROM -p six
python3 pypi-trends.py -f $FROM -p tensorflow

# pep8
# pycodestyle
