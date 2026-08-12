#!/usr/bin/env python3
"""Streak card — the three panels streak-stats.demolab.com used to render.

Rendered here because GitHub's camo proxy returns 504 on that service (the
origin answers fine; camo times out fetching it and caches the failure), so
the README showed a broken image. Same reason stats_card.py exists.

Usage: python3 scripts/streak_card.py > assets/streak-card.svg
"""
import datetime
import json
import math
import subprocess
import sys

USER = "letranminhdat1516"
ACCENT = "#E23E63"
BG = "#1f1f1f"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
WHITE = "#ffffff"
FONT = "Segoe UI, Ubuntu, sans-serif"

W, H = 860, 240
COLS = (143.3, 430.0, 716.7)
RING_CY, RING_R = 96, 46
RING_GAP = 22  # degrees either side of top, left open for the flame

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

FIRE = ("M12 1.5c.6 3.2-1.1 4.7-2.6 6.2C7.7 9.4 6 11.1 6 14a6 6 0 0 0 12 0"
        "c0-2.1-1-3.7-2.1-5.1-.4 1-1.1 1.7-2 2.1.6-2.6-.5-5.5-1.9-9.5z")

YEARS_QUERY = '{ user(login: "%s") { createdAt contributionsCollection { contributionYears } } }' % USER


def gql(query):
    out = subprocess.run(["gh", "api", "graphql", "-f", "query=" + query],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)["data"]["user"]


def fetch():
    """Calendar data, one aliased sub-query per year.

    A contributionsCollection window can't span more than a year, so all-time
    totals have to be stitched together from per-year calendars. Weeks overlap
    at year boundaries, hence the dict keyed by date.
    """
    head = gql(YEARS_QUERY)
    years = sorted(head["contributionsCollection"]["contributionYears"])
    fields = "\n".join(
        f'y{y}: contributionsCollection(from: "{y}-01-01T00:00:00Z", to: "{y}-12-31T23:59:59Z") '
        "{ contributionCalendar { weeks { contributionDays { date contributionCount } } } }"
        for y in years
    )
    data = gql('{ user(login: "%s") { %s } }' % (USER, fields))

    days = {}
    for y in years:
        for week in data[f"y{y}"]["contributionCalendar"]["weeks"]:
            for d in week["contributionDays"]:
                days[d["date"]] = d["contributionCount"]

    created = datetime.date.fromisoformat(head["createdAt"][:10])
    return created, days


def streaks(days):
    today = datetime.date.today()
    series = [(datetime.date.fromisoformat(k), v)
              for k, v in sorted(days.items())
              if datetime.date.fromisoformat(k) <= today]

    total = sum(v for _, v in series)

    # Longest run of non-zero days anywhere in the history.
    longest = (0, None, None)
    run_start = None
    for i, (date, count) in enumerate(series):
        if count:
            run_start = run_start or date
            length = (date - run_start).days + 1
            if length > longest[0]:
                longest = (length, run_start, date)
        else:
            run_start = None

    # Today contributing nothing *yet* doesn't end the streak — it only ends
    # once yesterday is also empty. So drop a zero-valued today before counting.
    tail = series[:-1] if series and series[-1][1] == 0 else series
    current, cur_start, cur_end = 0, None, None
    for date, count in reversed(tail):
        if not count:
            break
        current += 1
        cur_start, cur_end = date, cur_end or date

    return total, (current, cur_start, cur_end), longest


def fmt(d):
    return f"{MONTHS[d.month - 1]} {d.day}, {d.year}"


def span(start, end):
    if not start:
        return fmt(datetime.date.today())
    if start == end:
        return fmt(start)
    if start.year == end.year:
        return f"{MONTHS[start.month - 1]} {start.day} - {fmt(end)}"
    return f"{fmt(start)} - {fmt(end)}"


def ring(cx):
    """Open arc rather than a masked circle — one element, no <mask> to rely on."""
    a0, a1 = math.radians(-90 + RING_GAP), math.radians(-90 - RING_GAP)
    x0, y0 = cx + RING_R * math.cos(a0), RING_CY + RING_R * math.sin(a0)
    x1, y1 = cx + RING_R * math.cos(a1), RING_CY + RING_R * math.sin(a1)
    return (f'<path d="M {x0:.1f} {y0:.1f} A {RING_R} {RING_R} 0 1 1 {x1:.1f} {y1:.1f}" '
            f'fill="none" stroke="{ACCENT}" stroke-width="5" stroke-linecap="round"/>')


def panel(cx, value, label, sub, label_fill):
    return [
        f'<text x="{cx}" y="104" fill="{WHITE}" font-size="34" font-weight="700" '
        f'text-anchor="middle">{value}</text>',
        f'<text x="{cx}" y="136" fill="{label_fill}" font-size="15" font-weight="600" '
        f'text-anchor="middle">{label}</text>',
        f'<text x="{cx}" y="160" fill="{MUTED}" font-size="12.5" '
        f'text-anchor="middle">{sub}</text>',
    ]


def build(created, days):
    total, (current, cur_start, cur_end), (longest, long_start, long_end) = streaks(days)
    cx = COLS[1]

    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="{FONT}">',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{BG}" '
        f'stroke="{ACCENT}" stroke-opacity="0.25"/>',
    ]

    for x in (286.7, 573.3):
        p.append(f'<line x1="{x}" y1="44" x2="{x}" y2="196" stroke="{ACCENT}" '
                 f'stroke-opacity="0.18"/>')

    p += panel(COLS[0], f"{total:,}", "Total Contributions",
               f"{fmt(created)} - Present", TEXT)
    p += panel(COLS[2], f"{longest:,}", "Longest Streak",
               span(long_start, long_end), TEXT)

    # Centre panel carries the ring and flame, so it's laid out on its own.
    p += [
        ring(cx),
        f'<g transform="translate({cx - 20.4} {RING_CY - RING_R - 20.4}) scale(1.7)">'
        f'<path d="{FIRE}" fill="{ACCENT}"/></g>',
        f'<text x="{cx}" y="{RING_CY + 12}" fill="{WHITE}" font-size="34" font-weight="700" '
        f'text-anchor="middle">{current:,}</text>',
        f'<text x="{cx}" y="168" fill="{ACCENT}" font-size="15" font-weight="700" '
        f'text-anchor="middle">Current Streak</text>',
        f'<text x="{cx}" y="192" fill="{MUTED}" font-size="12.5" '
        f'text-anchor="middle">{span(cur_start, cur_end)}</text>',
        "</svg>",
    ]
    return "\n".join(p)


if __name__ == "__main__":
    sys.stdout.write(build(*fetch()))
