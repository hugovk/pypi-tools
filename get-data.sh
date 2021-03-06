#!/usr/bin/env bash

FROM="2021-04"
TO=$FROM

# application_limits=["5 per second", "30 per minute"]

python3 pypi-trends.py -f $FROM -t $TO
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p attrs
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p black
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p colorama
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p coverage
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p django
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p flake8
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p humanize
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p matplotlib
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p numpy
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p pandas
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p pillow
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p pip
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p prettytable
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p pycodestyle
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p pyflakes
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p pylast
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p pylint
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p pytest
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p requests
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p scipy
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p setuptools
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p six
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p tablib
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p tensorflow
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p tox
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p tqdm
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p twitter
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p ujson
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p urllib3
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p wheel
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p virtualenv

# Just the "free" data for these for now
python3 pypi-trends.py --pypistats -p cryptography
python3 pypi-trends.py --pypistats -p httpx
python3 pypi-trends.py --pypistats -p paramiko
python3 pypi-trends.py --pypistats -p python-dateutil
python3 pypi-trends.py --pypistats -p pytz
python3 pypi-trends.py --pypistats -p scikit-learn
