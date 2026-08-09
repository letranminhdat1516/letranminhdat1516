#!/usr/bin/env python3
"""Render the profile-summary card as SVG in CICCA colours.

Same layout as github-profile-summary-cards' `profile-details`, but that service
only ships fixed themes (all of them green/purple), so we render it ourselves.

Usage: python3 scripts/profile_card.py > assets/profile-card.svg
"""
import json
import subprocess
import sys
from datetime import datetime, timezone

USER = "letranminhdat1516"
ACCENT = "#E23E63"
AREA = "#AE1D41"
BG = "#1f1f1f"
TEXT = "#c9d1d9"
MUTED = "#8b949e"

W, H = 760, 210
CHART_L, CHART_R = 330, 700
CHART_T, CHART_B = 60, 165

QUERY = """
{ user(login: "%s") {
    name login company createdAt
    repositories(privacy: PUBLIC, ownerAffiliations: OWNER) { totalCount }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { firstDay contributionDays { contributionCount } }
      } } } }
""" % USER

# Simple monochrome glyphs (24x24 viewBox paths), drawn at 12px.
ICONS = {
    "mark": "M12 .5C5.4.5 0 5.9 0 12.6c0 5.3 3.4 9.8 8.2 11.4.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1.1-.8.1-.8.1-.8 1.2.1 1.8 1.3 1.8 1.3 1.1 1.9 2.9 1.3 3.6 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.4-5.5-6 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.6.1-3.2 0 0 1-.3 3.3 1.2a11 11 0 0 1 6 0C17.3 4.2 18.3 4.5 18.3 4.5c.6 1.6.2 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12.1 12.1 0 0 0 24 12.6C24 5.9 18.6.5 12 .5z",
    "repo": "M4 2h13a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H6a2 2 0 0 0-2 2V2zm2 1v14.2c.3-.1.7-.2 1-.2h9V3H6z",
    "clock": "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 2a8 8 0 1 1 0 16 8 8 0 0 1 0-16zm-1 3v6l4.5 2.7.8-1.3-3.8-2.3V7h-1.5z",
    "org": "M3 21V3h11v6h7v12H3zm2-2h4v-3H5v3zm0-5h4v-3H5v3zm0-5h4V6H5v3zm6 10h3v-3h-3v3zm0-5h3v-3h-3v3zm0-5h3V6h-3v3zm5 10h3v-3h-3v3zm0-5h3v-3h-3v3z",
}


def fetch():
    out = subprocess.run(
        ["gh", "api", "graphql", "-f", "query=" + QUERY],
        capture_output=True, text=True, check=True,
    ).stdout
    return json.loads(out)["data"]["user"]


def human(n):
    return f"{n/1000:.2f}k".rstrip("0").rstrip(".") if n >= 1000 else str(n)


def nice_ceiling(v):
    for step in (25, 50, 100, 150, 200, 250, 500):
        if v <= step * 4:
            return step * 4, step
    return v, max(1, v // 4)


def build(u):
    cal = u["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    pts = [(w["firstDay"], sum(d["contributionCount"] for d in w["contributionDays"])) for w in weeks]
    top, step = nice_ceiling(max(v for _, v in pts))

    n = len(pts)
    plot_w = CHART_R - CHART_L
    plot_h = CHART_B - CHART_T

    def x(i):
        return CHART_L + plot_w * i / (n - 1)

    def y(v):
        return CHART_T + plot_h * (1 - v / top)

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
    area = f"{line} L {coords[-1][0]:.1f} {CHART_B:.1f} L {coords[0][0]:.1f} {CHART_B:.1f} Z"

    created = datetime.strptime(u["createdAt"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    years = int((datetime.now(timezone.utc) - created).days / 365.25)

    rows = [
        ("mark", f'{human(cal["totalContributions"])} Contributions on GitHub'),
        ("repo", f'{u["repositories"]["totalCount"]} Public Repos'),
        ("clock", f"Joined GitHub {years} years ago"),
        ("org", u["company"] or ""),
    ]

    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="Segoe UI, Ubuntu, sans-serif">',
        f'<rect width="{W}" height="{H}" rx="10" fill="{BG}"/>',
        f'<text x="28" y="42" fill="{ACCENT}" font-size="19" font-weight="600">'
        f'{u["login"]} ({u["name"]})</text>',
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{AREA}" stop-opacity="0.6"/>'
        f'<stop offset="100%" stop-color="{AREA}" stop-opacity="0.03"/></linearGradient></defs>',
    ]

    ty = 78
    for icon, label in rows:
        if not label:
            continue
        p.append(
            f'<g transform="translate(28 {ty-11}) scale(0.58)">'
            f'<path d="{ICONS[icon]}" fill="{MUTED}"/></g>'
        )
        p.append(f'<text x="52" y="{ty}" fill="{TEXT}" font-size="13.5">{label}</text>')
        ty += 28

    p.append(
        f'<text x="{CHART_R}" y="42" fill="{MUTED}" font-size="11" text-anchor="end">'
        f"contributions in the last year</text>"
    )
    for v in range(0, top + 1, step):
        gy = y(v)
        p.append(
            f'<line x1="{CHART_L}" y1="{gy:.1f}" x2="{CHART_R}" y2="{gy:.1f}" '
            f'stroke="{ACCENT}" stroke-opacity="0.12"/>'
        )
        p.append(
            f'<text x="{CHART_R+8}" y="{gy+4:.1f}" fill="{MUTED}" font-size="10">{v}</text>'
        )

    p.append(f'<path d="{area}" fill="url(#g)"/>')
    p.append(f'<path d="{line}" fill="none" stroke="{ACCENT}" stroke-width="2"/>')

    seen = set()
    for i, (day, _) in enumerate(pts):
        dt = datetime.strptime(day, "%Y-%m-%d")
        if dt.month % 2 == 1 and dt.strftime("%y/%m") not in seen and dt.day <= 7:
            seen.add(dt.strftime("%y/%m"))
            p.append(
                f'<text x="{x(i):.1f}" y="{CHART_B+18:.0f}" fill="{MUTED}" font-size="10" '
                f'text-anchor="middle">{dt.strftime("%y/%m")}</text>'
            )

    p.append("</svg>")
    return "\n".join(p)


if __name__ == "__main__":
    sys.stdout.write(build(fetch()))
