#!/usr/bin/env python
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
from __future__ import annotations

import argparse
import datetime as dt
import os
import subprocess
import sys

from dateutil.relativedelta import relativedelta  # pip install python-dateutil
from termcolor import colored, cprint  # pip install termcolor

now = dt.date.today()


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


def spread_order(years_months):
    """
    Sort so months are in this order:
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    =>
    [1, 7, 4, 10, 3, 6, 9, 12, 2, 5, 8, 11]

    :param years_months: list of (year, month) tuples
    :return: re-sorted list of (year, month) tuples
    """
    order = [1, 7, 4, 10, 3, 6, 9, 12, 2, 5, 8, 11]
    output = []
    for o in order:
        for year, month in years_months:
            if month == o:
                # print(year, month)
                output.append((year, month))
    return output


def five_months_ago():
    """For --pypistats, the earliest start date is five whole months ago"""
    first = now - relativedelta(months=5)
    return f"{first.year}-{first.month:02}"


def default_end_date() -> str:
    """For the default end date"""
    last = now - relativedelta(months=1)
    return f"{last.year}-{last.month:02}"


def yyyy_mm_to_ints(yyyy_mm: str) -> tuple[int, int]:
    """Return yyyy-mm as two integers"""
    try:
        the_date = dt.datetime.strptime(yyyy_mm, "%Y-%m")
    except ValueError:
        msg = "Dates must be YYYY-MM"
        raise ValueError(msg)

    return the_date.year, the_date.month


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-p", "--package", default="''", help="Show data for this package"
    )
    parser.add_argument(
        "-f", "--from", dest="from_date", default="2016-01", help="Start YYYY-MM"
    )
    parser.add_argument(
        "-t", "--to", dest="to_date", default=default_end_date(), help="End YYYY-MM"
    )
    parser.add_argument(
        "-s", "--spread", action="store_true", help="Fetch data in spread order"
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

    if args.pypistats:
        earliest_start_date = five_months_ago()
        if args.from_date < earliest_start_date:
            args.from_date = earliest_start_date
            cprint(f"Set earliest start date for pypistats: {args.from_date}", "yellow")

    from_year, from_month = yyyy_mm_to_ints(args.from_date)
    to_year, to_month = yyyy_mm_to_ints(args.to_date)

    print(f"Getting data from {from_month} {from_year} to {to_month} {to_year}\n")

    years_months = list(
        month_year_iter(from_month, from_year, to_month + 1, to_year, reverse=True)
    )
    if args.spread:
        years_months = spread_order(years_months)

    greens, yellows, reds = 0, 0, 0

    for year, month in years_months:
        if year == 2016 and month == 4:
            cprint("  No data for 2016-04, skipping", "yellow")
            continue
        first = dt.date(year, month, 1)
        last = first + relativedelta(months=1) - relativedelta(days=1)
        print(first, last)

        if last >= now:
            cprint("  End date should be in the past", "red")
            reds += 1
            sys.exit(1)

        if args.package in ['""', "''"]:
            prefix = ""
        else:
            prefix = args.package + "-"
        outfile = f"{prefix}{year}-{month:02d}.json"
        outfile = os.path.join("data", outfile)
        if os.path.isfile(outfile):
            cprint(f"  {outfile} exists, skipping", "yellow")
            yellows += 1
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
        executable = "pypistats" if args.pypistats else "pypinfo"
        if args.dry_run:
            print(f"  Dry run, not executing {executable}")
        else:
            # os.system(cmd)
            exitcode, output = subprocess.getstatusoutput(cmd)
            if exitcode == 0:
                cprint(f"  {outfile}", "green")
                greens += 1
            else:
                error = output.splitlines()[-1]
                for line in output.splitlines():
                    if "google.api_core.exceptions" in line:
                        error = line
                        break
                cprint(error, "red")

                reds += 1
                if os.path.getsize(outfile) == 0:
                    os.remove(outfile)

    print(
        colored(f"{greens}", "green"),
        colored(f"{yellows}", "yellow"),
        colored(f"{reds}", "red"),
    )


if __name__ == "__main__":
    main()

# End of file
