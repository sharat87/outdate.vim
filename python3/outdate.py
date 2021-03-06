import re
import sys
import datetime
from typing import List, Optional

FORMAT_PATTERNS = {
    '%a': r'(?P<wday_short>sun|mon|tue|wed|thu|fri|sat)',
    '%A': r'(?P<wday_long>sunday|monday|tuesday|wednesday|thursday|friday|saturday)',
    '%w': r'(?P<wday>[0-6])',
    '%d': r'(?P<day>\d\d?)',
    '%b': r'(?P<month_short>jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)',
    '%B': r'(?P<month_long>january|february|march|april|may|june|july|august|september|october|november|december)',
    '%m': r'(?P<month>0?1|0?2|0?3|0?4|0?5|0?6|0?7|0?8|0?9|10|11|12)',
    '%y': r'(?P<year_short>\d{2})',
    '%Y': r'(?P<year>\d{4})',
    '%H': r'(?P<hour_24>\d\d?)',
    '%I': r'(?P<hour_12>\d\d?)',
    '%p': r'(?P<meridian>[AP]M\b)',
    '%M': r'(?P<minute>\d\d?)',
    '%S': r'(?P<second>\d\d?)',
    '%f': r'(?P<ms>\d{1,3})',
    # '%z': r'',
    # '%Z': r'',
    # '%j': r'',
    # '%U': r'',
    # '%W': r'',
    # '%c': r'',
    # '%x': r'',
    # '%X': r'',
    '%%': r'%',
}


def apply(to_fmt, line1, line2, range_arg):
    import vim  # Importing locally so that the module can be tested without vim.

    range_arg = int(range_arg, 10)
    if range_arg not in {0, 2}:
        print('Unknown range argument %d.' % range_arg, file=sys.stderr)
        return

    line1, line2 = int(line1, 10) - 1, int(line2, 10)
    has_selection = range_arg == 2
    vmode = vim.eval('visualmode()')

    final_lines = reformat_date(
        vim.current.buffer[line1:line2],
        vim.current.window.cursor[1],
        vim.eval('g:outdate_parse_formats'),
        to_fmt,
    )

    if vim.current.buffer[line1:line2] != final_lines:
        vim.current.buffer[line1:line2] = final_lines


def to_re(fmt):
    for k, v in FORMAT_PATTERNS.items():
        fmt = re.sub('(?<!%)' + k, v.replace('\\', '\\\\'), fmt)
    return re.compile(fmt, re.IGNORECASE | re.VERBOSE)


def reformat_date(in_lines, position, parse_formats, to_fmt):
    out_lines = []
    for line in in_lines:
        dt, match = find_date(line, position, parse_formats)

        if dt and match:
            start, end = match.span()
            out_lines.append(line[:start] + dt.strftime(to_fmt) + line[end:])

        else:
            out_lines.append(line)

    return out_lines


def build_datetime(*, year=None, year_short=None,
            month=None, month_short=None, month_long=None,
            day=None,
            **kwargs) -> datetime.datetime:
    now = datetime.datetime.now()

    if year is None and year_short is not None:
        year = 1900 + int(year_short)
        if year < 1930:
            year += 100

    if month is None and (month_long or month_short):
        month = datetime.datetime.strptime((month_long or month_short)[:3], '%b').month

    return datetime.datetime(
        int(now.year if year is None else year),
        int(now.month if month is None else month),
        int(now.day if day is None else day),
    )


def find_date(line: str, position: int, formats: List[str]):
    match = dt = None
    dates_found = []

    for fmt in formats:
        for match in to_re(fmt).finditer(line):
            start, end = match.span()

            if end < position:
                # Matched date is to the left of the cursor position. No match!
                match = None
                continue

            try:
                dt = datetime.datetime.strptime(match.group(), fmt)
            except ValueError:
                try:
                    dt = build_datetime(**match.groupdict())
                except ValueError:
                    # Matched string is not a valid date. No match!
                    match = None
                    continue

            # A valid date found. Record it along with it's position.
            dates_found.append((start, dt, match))

    if not dates_found:
        return None, None

    # Return the left-most matched date.
    _, dt, match = min(dates_found)
    return dt, match
