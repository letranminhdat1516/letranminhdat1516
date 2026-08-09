#!/usr/bin/env python3
"""GitHub Stats card — same shape as github-readme-stats, in CICCA colours.

We render it ourselves because that service is down (503) and only ships fixed
themes anyway. Rows are chosen from what the account actually demonstrates:
stars (2) and issues (0) are left out because they say nothing about the work.

Usage: python3 scripts/stats_card.py > assets/stats-card.svg
"""
import json
import subprocess
import sys

USER = "letranminhdat1516"
NAME = "Lê Trần Minh Đạt"
ACCENT = "#E23E63"
RING_BG = "#3a2029"
BG = "#1f1f1f"
TEXT = "#c9d1d9"
FONT = "Segoe UI, Ubuntu, sans-serif"

W, H = 860, 250
RING_CX, RING_CY, RING_R = 720, 132, 62

QUERY = """
{ user(login: "%s") {
    repositories(privacy: PUBLIC, ownerAffiliations: OWNER) { totalCount }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalRepositoriesWithContributedCommits
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    } } }
""" % USER

ICONS = {
    "commit": "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 2a8 8 0 1 1 0 16 8 8 0 0 1 0-16zm-1 3v6l4.5 2.7.8-1.3-3.8-2.3V7h-1.5z",
    "graph": "M3 3h2v16h16v2H3V3zm15.3 3.3 1.4 1.4-5.7 5.7-3-3-4.3 4.3-1.4-1.4 5.7-5.7 3 3 4.3-4.3z",
    "pr": "M6 3a3 3 0 0 1 1 5.8v6.4a3 3 0 1 1-2 0V8.8A3 3 0 0 1 6 3zm0 2a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm0 12a1 1 0 1 0 0 2 1 1 0 0 0 0-2zM18 3a3 3 0 0 1 1 5.8V15a4 4 0 0 1-4 4h-2v-2h2a2 2 0 0 0 2-2V8.8A3 3 0 0 1 18 3zm0 2a1 1 0 1 0 0 2 1 1 0 0 0 0-2z",
    "repo": "M4 2h13a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H6a2 2 0 0 0-2 2V2zm2 1v14.2c.3-.1.7-.2 1-.2h9V3H6z",
    "network": "M12 2a3 3 0 0 1 1 5.8V10h4a3 3 0 0 1 3 3v1.2a3 3 0 1 1-2 0V13a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1v1.2a3 3 0 1 1-2 0V13a3 3 0 0 1 3-3h4V7.8A3 3 0 0 1 12 2z",
}


def fetch():
    out = subprocess.run(["gh", "api", "graphql", "-f", "query=" + QUERY],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)["data"]["user"]


def build(u):
    c = u["contributionsCollection"]
    total = c["contributionCalendar"]["totalContributions"]
    rows = [
        ("commit", "Total Commits (last year):", f'{c["totalCommitContributions"]:,}'),
        ("graph", "Total Contributions:", f"{total:,}"),
        ("pr", "Total PRs:", f'{c["totalPullRequestContributions"]:,}'),
        ("network", "Contributed to (last year):", f'{c["totalRepositoriesWithContributedCommits"]:,}'),
        ("repo", "Public Repos:", f'{u["repositories"]["totalCount"]:,}'),
    ]

    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="{FONT}">',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{BG}" '
        f'stroke="{ACCENT}" stroke-opacity="0.25"/>',
        f'<text x="46" y="58" fill="{ACCENT}" font-size="23" font-weight="700">'
        f"{NAME}&#8217;s GitHub Stats</text>",
    ]

    y = 104
    for icon, label, value in rows:
        p += [
            f'<g transform="translate(48 {y-14}) scale(0.76)"><path d="{ICONS[icon]}" '
            f'fill="{ACCENT}" fill-opacity="0.85"/></g>',
            f'<text x="82" y="{y}" fill="{TEXT}" font-size="15.5" font-weight="600">{label}</text>',
            f'<text x="430" y="{y}" fill="{TEXT}" font-size="15.5" font-weight="700">{value}</text>',
        ]
        y += 30

    # A sparkline instead of a progress ring: contributions have no ceiling, so
    # any ring reads as "x% of a target" that doesn't exist.
    months = {}
    for w in c["contributionCalendar"]["weeks"]:
        for d in w["contributionDays"]:
            months[d["date"][:7]] = months.get(d["date"][:7], 0) + d["contributionCount"]
    series = [v for _, v in sorted(months.items())[-12:]]
    peak = max(series) or 1

    # Centre the sparkline block (plot + caption) on the rows block, and keep the
    # right margin equal to the left one.
    rows_top, rows_bottom = 104 - 18, y - 30 + 6
    SH, CAPTION_GAP = 92, 22
    SY = (rows_top + rows_bottom) / 2 - (SH + CAPTION_GAP) / 2
    SW = 240
    SX = W - 46 - SW

    def sx(i):
        return SX + SW * i / (len(series) - 1)

    def sy(v):
        return SY + SH * (1 - v / peak)

    pts = [(sx(i), sy(v)) for i, v in enumerate(series)]
    d = [f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        d.append("C {:.1f} {:.1f}, {:.1f} {:.1f}, {:.1f} {:.1f}".format(
            p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
            p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]))
    line = " ".join(d)
    px, py = pts[series.index(peak)]

    p += [
        f'<defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{ACCENT}" stop-opacity="0.5"/>'
        f'<stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/></linearGradient></defs>',
        f'<path d="{line} L {pts[-1][0]:.1f} {SY+SH} L {pts[0][0]:.1f} {SY+SH} Z" fill="url(#s)"/>',
        f'<path d="{line}" fill="none" stroke="{ACCENT}" stroke-width="2.2" stroke-linecap="round"/>',
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.5" fill="{TEXT}"/>',
        f'<text x="{px:.1f}" y="{py-10:.1f}" fill="{TEXT}" font-size="12" font-weight="700" '
        f'text-anchor="middle">{peak}</text>',
        f'<text x="{SX + SW/2:.0f}" y="{SY+SH+22}" fill="{ACCENT}" font-size="9.5" '
        f'letter-spacing="1.3" text-anchor="middle">CONTRIBUTIONS PER MONTH</text>',
        "</svg>",
    ]
    return "\n".join(p)


if __name__ == "__main__":
    sys.stdout.write(build(fetch()))
