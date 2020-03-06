 #!/usr/bin/env bash

FROM="2020-02"
TO=$FROM

python3 pypi-trends.py -f $FROM -t $TO
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p coverage
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p django
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p flake8
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p matplotlib
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p numpy
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p pandas
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p pillow
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p pip
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p pylast
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p pylint
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p pytest
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p requests
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p scipy
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p setuptools
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p six
python3 pypi-trends.py --pypistats -f $FROM -t $TO -p tensorflow

python3 pypi-trends.py -p setuptools

# pep8
# pycodestyle
