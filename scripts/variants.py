#!/usr/bin/env python3
"""Render alternative card layouts, so we can compare before picking one.

Usage: python3 scripts/variants.py            # writes assets/variants/*.svg
"""
import json
import os
import subprocess
from datetime import datetime, timezone

USER = "letranminhdat1516"
ACCENT = "#E23E63"
AREA = "#AE1D41"
BG = "#1f1f1f"
CELL_EMPTY = "#262626"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
FONT = "Segoe UI, Ubuntu, sans-serif"
OUT = "assets/variants"

QUERY = """
{ user(login: "%s") {
    name login company createdAt
    repositories(privacy: PUBLIC, ownerAffiliations: OWNER) { totalCount }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { firstDay contributionDays { date weekday contributionCount } }
      } } } }
""" % USER


def fetch():
    out = subprocess.run(["gh", "api", "graphql", "-f", "query=" + QUERY],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)["data"]["user"]


def weekly(cal):
    return [(w["firstDay"], sum(d["contributionCount"] for d in w["contributionDays"]))
            for w in cal["weeks"]]


# ---------------------------------------------------------------- variant 1
def stat_tiles(u):
    """Four big numbers, echoing the RPG stat blocks on the portfolio."""
    cal = u["contributionsCollection"]["contributionCalendar"]
    created = datetime.strptime(u["createdAt"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    years = int((datetime.now(timezone.utc) - created).days / 365.25)
    peak = max(v for _, v in weekly(cal))

    stats = [
        (f'{cal["totalContributions"]:,}', "CONTRIBUTIONS"),
        (str(u["repositories"]["totalCount"]), "PUBLIC REPOS"),
        (f"{years}+", "YEARS ON GITHUB"),
        (str(peak), "PEAK WEEK"),
    ]
    W, H, gap = 760, 150, 14
    tw = (W - gap * 3) / 4
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="{FONT}">',
         f'<rect width="{W}" height="{H}" fill="{BG}" rx="10"/>']
    for i, (num, label) in enumerate(stats):
        x = i * (tw + gap)
        cx = x + tw / 2
        p += [
            f'<rect x="{x:.1f}" y="12" width="{tw:.1f}" height="{H-24}" rx="8" '
            f'fill="#242424" stroke="{ACCENT}" stroke-opacity="0.28"/>',
            f'<text x="{cx:.1f}" y="78" fill="{ACCENT}" font-size="38" font-weight="700" '
            f'text-anchor="middle">{num}</text>',
            f'<text x="{cx:.1f}" y="106" fill="{MUTED}" font-size="11" letter-spacing="1.4" '
            f'text-anchor="middle">{label}</text>',
        ]
    p.append("</svg>")
    return "\n".join(p)


# ---------------------------------------------------------------- variant 2
def heatmap(u):
    """GitHub-style calendar, but with dark empty cells instead of white."""
    cal = u["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    peak = max(d["contributionCount"] for w in weeks for d in w["contributionDays"]) or 1
    cell, gap = 11, 3
    L, T = 34, 44
    W = L + len(weeks) * (cell + gap) + 16
    H = T + 7 * (cell + gap) + 26

    def shade(c):
        if not c:
            return CELL_EMPTY
        return f'{ACCENT}{["40","73","a6","ff"][min(3, int(c / peak * 3.999))]}'

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="{FONT}">',
         f'<rect width="{W}" height="{H}" fill="{BG}" rx="10"/>',
         f'<text x="{L}" y="26" fill="{ACCENT}" font-size="14" font-weight="600">'
         f'{cal["totalContributions"]:,} contributions in the last year</text>']

    seen = set()
    for wi, w in enumerate(weeks):
        x = L + wi * (cell + gap)
        dt = datetime.strptime(w["firstDay"], "%Y-%m-%d")
        if dt.strftime("%b") not in seen and dt.day <= 7:
            seen.add(dt.strftime("%b"))
            p.append(f'<text x="{x}" y="{T-6}" fill="{MUTED}" font-size="9">{dt.strftime("%b")}</text>')
        for d in w["contributionDays"]:
            y = T + d["weekday"] * (cell + gap)
            p.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" '
                     f'fill="{shade(d["contributionCount"])}"/>')

    for i, lbl in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        p.append(f'<text x="4" y="{T + i*(cell+gap) + 9}" fill="{MUTED}" font-size="9">{lbl}</text>')
    p.append("</svg>")
    return "\n".join(p)


# ---------------------------------------------------------------- variant 3
def bars(u):
    """Monthly bars — reads as momentum rather than a jagged daily line."""
    cal = u["contributionsCollection"]["contributionCalendar"]
    months = {}
    for w in cal["weeks"]:
        for d in w["contributionDays"]:
            months.setdefault(d["date"][:7], 0)
            months[d["date"][:7]] += d["contributionCount"]
    items = sorted(months.items())[-12:]
    top = max(v for _, v in items) or 1

    W, H = 760, 200
    L, R, T, B = 46, 24, 52, 40
    bw = (W - L - R) / len(items)
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="{FONT}">',
         f'<rect width="{W}" height="{H}" fill="{BG}" rx="10"/>',
         f'<text x="{W/2}" y="30" fill="{ACCENT}" font-size="15" font-weight="600" '
         f'text-anchor="middle">{cal["totalContributions"]:,} contributions in the last year</text>',
         f'<defs><linearGradient id="b" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0%" stop-color="{ACCENT}"/>'
         f'<stop offset="100%" stop-color="{AREA}" stop-opacity="0.35"/></linearGradient></defs>']
    for i, (m, v) in enumerate(items):
        h = (H - T - B) * v / top
        x = L + i * bw + bw * 0.18
        p += [
            f'<rect x="{x:.1f}" y="{H-B-h:.1f}" width="{bw*0.64:.1f}" height="{h:.1f}" '
            f'rx="3" fill="url(#b)"/>',
            f'<text x="{x + bw*0.32:.1f}" y="{H-B-h-6:.1f}" fill="{TEXT}" font-size="10" '
            f'text-anchor="middle">{v}</text>',
            f'<text x="{x + bw*0.32:.1f}" y="{H-B+16:.0f}" fill="{MUTED}" font-size="10" '
            f'text-anchor="middle">{datetime.strptime(m, "%Y-%m").strftime("%b")}</text>',
        ]
    p.append("</svg>")
    return "\n".join(p)


if __name__ == "__main__":
    u = fetch()
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (("stat-tiles", stat_tiles), ("heatmap", heatmap), ("bars", bars)):
        with open(f"{OUT}/{name}.svg", "w") as f:
            f.write(fn(u))
        print(f"{OUT}/{name}.svg")
