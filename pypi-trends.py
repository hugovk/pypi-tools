#!/usr/bin/env python
# encoding: utf-8
"""
For a given project, or all projects:
* Fetch pip installs for each Python in a given month of a year
* Save in a JSON file for each month of a year

Requires pypinfo to be installed and configured
* https://github.com/ofek/pypinfo

Alternatively, requires pypistats to be installed
(note: only has 6 months of stats and output JSON is a different format)
* pip install -U pypistats

Notes:
    "Data ingestion into the BigQuery data set was spotty prior to June 2016
    (but it shouldn't be biased, so these percentages are likely to be accurate),
    but you can see a significant uptick in Python 3 based downloads over 2016.
    If these trends continue..."
https://langui.sh/2016/12/09/data-driven-decisions/
"""
import argparse
import os
import subprocess
import sys
from datetime import date, datetime

from dateutil.relativedelta import relativedelta  # pip install python-dateutil
from termcolor import colored  # pip install termcolor

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
    return f"{last.year}-{last.month:02}"


def default_end_date():
    """For the default end date"""
    last = now - relativedelta(months=1)
    return f"{last.year}-{last.month:02}"


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
        "-n", "--dry-run", action="store_true", help="Don't execute pypinfo/pypistats"
    )
    parser.add_argument(
        "--pypistats",
        action="store_true",
        help="Use pypistats instead of pypinfo. Note: only has "
        "6 months of stats, and output JSON is a different "
        "format.",
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
            print(colored("  End date should be in the past", "red"))
            sys.exit(1)

        if args.package in ['""', "''"]:
            prefix = ""
        else:
            prefix = args.package + "-"
        outfile = f"{prefix}{year}-{month:02d}.json"
        outfile = os.path.join("data", outfile)
        if os.path.isfile(outfile):
            print(colored(f"  {outfile} exists, skipping", "yellow"))
            continue

        if args.pypistats:
            cmd = (
                f"pypistats python_minor {args.package} --json "
                f"--start-date {first} --end-date {last} > {outfile}"
            )
        else:
            cmd = (
                f"pypinfo --start-date {first} --end-date {last} --percent --limit 100 "
                f"--json {args.package} pyversion > {outfile}"
            )

        print(cmd)
        print()
        executable = "pypistats" if args.pypistats else "pypinfo"
        if args.dry_run:
            print(f"  Dry run, not executing {executable}")
        else:
            # os.system(cmd)
            exitcode, output = subprocess.getstatusoutput(cmd)
            if exitcode != 0:
                print(colored(output.splitlines()[-1], "red"))
                print()
                if os.path.getsize(outfile) == 0:
                    os.remove(outfile)


# End of file
