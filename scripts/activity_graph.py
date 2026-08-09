#!/usr/bin/env python3
"""Render a full-year contribution area chart as SVG, in CICCA colours.

Third-party graph services cap at ~90 days, so we build the yearly view here.
Data comes from the GitHub GraphQL contribution calendar.

Usage: python3 scripts/activity_graph.py > assets/activity.svg
"""
import json
import subprocess
import sys
from datetime import datetime

USER = "letranminhdat1516"
ACCENT = "#E23E63"
AREA = "#AE1D41"
BG = "#1f1f1f"
MUTED = "#8b949e"

W, H = 1000, 300
PAD_L, PAD_R, PAD_T, PAD_B = 62, 24, 58, 46

QUERY = """
{ user(login: "%s") {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { firstDay contributionDays { date contributionCount } }
      } } } }
""" % USER


def fetch():
    out = subprocess.run(
        ["gh", "api", "graphql", "-f", "query=" + QUERY],
        capture_output=True, text=True, check=True,
    ).stdout
    return json.loads(out)["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def nice_ceiling(v):
    for step in (5, 10, 20, 25, 50, 100, 200, 250, 500):
        if v <= step * 4:
            return step * 4, step
    return v, max(1, v // 4)


def build(cal):
    weeks = cal["weeks"]
    pts = [(w["firstDay"], sum(d["contributionCount"] for d in w["contributionDays"])) for w in weeks]
    top, step = nice_ceiling(max(v for _, v in pts))

    plot_w = W - PAD_L - PAD_R
    plot_h = H - PAD_T - PAD_B
    n = len(pts)

    def x(i):
        return PAD_L + plot_w * i / (n - 1)

    def y(v):
        return PAD_T + plot_h * (1 - v / top)

    # Catmull-Rom -> cubic bezier, so the line curves like the old graph did.
    coords = [(x(i), y(v)) for i, (_, v) in enumerate(pts)]
    d = [f"M {coords[0][0]:.1f} {coords[0][1]:.1f}"]
    for i in range(len(coords) - 1):
        p0 = coords[i - 1] if i else coords[i]
        p1, p2 = coords[i], coords[i + 1]
        p3 = coords[i + 2] if i + 2 < len(coords) else p2
        d.append(
            "C {:.1f} {:.1f}, {:.1f} {:.1f}, {:.1f} {:.1f}".format(
                p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
                p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6,
                p2[0], p2[1],
            )
        )
    line = " ".join(d)
    base = PAD_T + plot_h
    area = f"{line} L {coords[-1][0]:.1f} {base:.1f} L {coords[0][0]:.1f} {base:.1f} Z"

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI, Ubuntu, sans-serif">',
        f'<rect width="{W}" height="{H}" rx="10" fill="{BG}"/>',
        f'<text x="{W/2:.0f}" y="32" fill="{ACCENT}" font-size="18" font-weight="600" text-anchor="middle">'
        f'{cal["totalContributions"]:,} contributions in the last year</text>',
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{AREA}" stop-opacity="0.55"/>'
        f'<stop offset="100%" stop-color="{AREA}" stop-opacity="0.02"/></linearGradient></defs>',
    ]

    for v in range(0, top + 1, step):
        gy = y(v)
        parts.append(
            f'<line x1="{PAD_L}" y1="{gy:.1f}" x2="{W-PAD_R}" y2="{gy:.1f}" '
            f'stroke="{ACCENT}" stroke-opacity="0.13" stroke-dasharray="3 4"/>'
        )
        parts.append(
            f'<text x="{PAD_L-10}" y="{gy+4:.1f}" fill="{MUTED}" font-size="11" text-anchor="end">{v}</text>'
        )

    parts.append(f'<path d="{area}" fill="url(#g)"/>')
    parts.append(f'<path d="{line}" fill="none" stroke="{ACCENT}" stroke-width="2.5" stroke-linecap="round"/>')

    seen = set()
    for i, (day, _) in enumerate(pts):
        dt = datetime.strptime(day, "%Y-%m-%d")
        label = dt.strftime("%b")
        if label not in seen and dt.day <= 7:
            seen.add(label)
            parts.append(
                f'<text x="{x(i):.1f}" y="{base+22:.0f}" fill="{MUTED}" font-size="11" text-anchor="middle">{label}</text>'
            )

    parts.append(
        f'<text x="{W/2:.0f}" y="{H-10}" fill="{MUTED}" font-size="10" text-anchor="middle" '
        f'letter-spacing="1">CONTRIBUTIONS PER WEEK</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    sys.stdout.write(build(fetch()))
