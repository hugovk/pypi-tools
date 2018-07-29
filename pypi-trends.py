#!/usr/bin/env python
# encoding: utf-8
"""
For a given project, or all projects:
* Fetch pip installs for each Python in a given month of a year
* Save in a JSON file for each month of a year

Requires pypinfo to be installed and configured
* https://github.com/ofek/pypinfo

Notes:
    "Data ingestion into the BigQuery data set was spotty prior to June 2016
    (but it shouldn't be biased, so these percentages are likely to be accurate),
    but you can see a significant uptick in Python 3 based downloads over 2016.
    If these trends continue..."
https://langui.sh/2016/12/09/data-driven-decisions/
"""
from __future__ import print_function, unicode_literals

import argparse
import os
import subprocess
import sys
from datetime import date, datetime

from dateutil.relativedelta import relativedelta  # pip install python-dateutil

now = date.today()


# https://stackoverflow.com/a/5734564/724176
def month_year_iter(start_month, start_year, end_month, end_year, reverse=False):
    ym_start = 12 * start_year + start_month - 1
    ym_end = 12 * end_year + end_month - 1
    ym_range = range(ym_start, ym_end)
    if reverse:
        ym_range = reversed(ym_range)
    for ym in ym_range:
        y, m = divmod(ym, 12)
        yield y, m + 1


def default_start_date():
    """For the default start date"""
    last = now - relativedelta(years=1)
    return "{}-{:02}".format(last.year, last.month)


def default_end_date():
    """For the default end date"""
    last = now - relativedelta(months=1)
    return "{}-{:02}".format(last.year, last.month)


def yyyy_mm_to_ints(yyyy_mm):
    """Return yyyy-mm as two integers"""
    try:
        the_date = datetime.strptime(yyyy_mm, "%Y-%m")
    except ValueError:
        raise ValueError("Dates must be YYYY-MM")

    return the_date.year, the_date.month


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-p", "--package", default="''", help="Show data for this package"
    )
    parser.add_argument(
        "-f",
        "--from",
        dest="from_date",
        default=default_start_date(),
        help="Start YYYY-MM",
    )
    parser.add_argument(
        "-t", "--to", dest="to_date", default=default_end_date(), help="End YYYY-MM"
    )
    parser.add_argument(
        "-n", "--dry-run", action="store_true", help="Don't execute pypinfo"
    )
    args = parser.parse_args()

    from_year, from_month = yyyy_mm_to_ints(args.from_date)
    to_year, to_month = yyyy_mm_to_ints(args.to_date)

    print(
        "Getting data from {} {} to {} {}\n".format(
            from_month, from_year, to_month, to_year
        )
    )

    for year, month in month_year_iter(
        from_month, from_year, to_month + 1, to_year, reverse=True
    ):

        first = date(year, month, 1)
        last = first + relativedelta(months=1) - relativedelta(days=1)
        print(first, last)

        if last >= now:
            sys.exit("  End date should be in the past")

        if args.package in ['""', "''"]:
            prefix = ""
        else:
            prefix = args.package + "-"
        outfile = "{}{}-{:02d}.json".format(prefix, year, month)
        outfile = os.path.join("data", outfile)
        if os.path.isfile(outfile):
            print("  {} exists, skipping".format(outfile))
            continue

        new_args = (
            "--start-date {} --end-date {} --percent --limit 100 "
            "--json {} pyversion > {}"
        ).format(first, last, args.package, outfile)
        # --start-date 2018-03-01 --end-date 2018-03-31 --limit 100
        # --percent --json "" pyversion > 2018-03.json

        cmd = "pypinfo {}".format(new_args)
        print(cmd)
        print()
        if args.dry_run:
            print("  Dry run, not executing pypinfo")
        else:
            # os.system(cmd)
            exitcode, output = subprocess.getstatusoutput(cmd)
            if exitcode != 0:
                print(output)
                if os.path.getsize(outfile) == 0:
                    os.remove(outfile)
                sys.exit(exitcode)


# End of file
