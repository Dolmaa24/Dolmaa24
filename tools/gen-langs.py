#!/usr/bin/env python3
"""Regenerate assets/languages.svg from the live GitHub API.

The public github-readme-stats instance is frequently rate-limited into a 503,
so the language chart is rendered locally and committed instead. Re-run this
after adding repos:

    python3 tools/gen-langs.py

Forks are excluded — they measure someone else's code, not yours.
"""

import json
import os
import urllib.request

USER = "Dolmaa24"
TOP_N = 6
# Markup and config that GitHub counts as "languages" but nobody claims as one.
SKIP = {"Mako", "Procfile", "Dockerfile", "Makefile", "Batchfile", "Shell"}

# Rank-graded amber ramp — brightest bar is the largest.
RAMP = ["#e3b341", "#c79b34", "#a9822a", "#8a6a22", "#6b521a", "#4d3b13"]

OUT = os.path.join(os.path.dirname(__file__), os.pardir, "assets", "languages.svg")


def api(path):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "gen-langs"},
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    return json.load(urllib.request.urlopen(req))


def collect():
    totals = {}
    for repo in api(f"/users/{USER}/repos?per_page=100&type=owner"):
        if repo["fork"]:
            continue
        for lang, count in api(f"/repos/{USER}/{repo['name']}/languages").items():
            if lang not in SKIP:
                totals[lang] = totals.get(lang, 0) + count
    return totals


def render(totals):
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])[:TOP_N]
    grand = sum(totals.values())

    row_h, bar_x, bar_w = 34, 210, 520
    top = 96
    # Pad past the *last bar*, not past a phantom seventh row, or the panel
    # ends up visibly bottom-heavy.
    height = top + row_h * (len(ranked) - 1) + 40

    rows = []
    for i, (lang, count) in enumerate(ranked):
        y = top + i * row_h
        pct = count / grand * 100
        rows.append(
            f'  <text class="mono" x="56" y="{y + 4}" font-size="13" letter-spacing="1.8" '
            f'fill="#8b949e">{lang.upper()}</text>\n'
            f'  <rect x="{bar_x}" y="{y - 9}" width="{bar_w}" height="10" rx="5" fill="#161b22"/>\n'
            f'  <rect x="{bar_x}" y="{y - 9}" width="{max(pct / 100 * bar_w, 3):.1f}" height="10" '
            f'rx="5" fill="{RAMP[i]}"/>\n'
            f'  <text class="mono" x="796" y="{y + 4}" font-size="13" text-anchor="end" '
            f'fill="#e6edf3">{pct:.1f}%</text>\n'
            f'  <text class="mono" x="944" y="{y + 4}" font-size="11" text-anchor="end" '
            f'fill="#484f58">{count / 1024:,.0f} KB</text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {height}" width="1000" \
height="{height}" role="img" aria-label="Language distribution across owned repositories">
  <style>
    .mono {{ font-family: ui-monospace, 'SF Mono', 'Cascadia Mono', 'Roboto Mono', Menlo, Consolas, monospace; }}
  </style>

  <rect x="0.5" y="0.5" width="999" height="{height - 1}" rx="10" fill="#0d1117" stroke="#21262d"/>

  <rect x="56" y="44" width="7" height="7" transform="rotate(45 59.5 47.5)" fill="#e3b341"/>
  <text class="mono" x="78" y="52" font-size="12" letter-spacing="2.6" fill="#6e7681">\
LANGUAGE DISTRIBUTION</text>
  <text class="mono" x="944" y="52" font-size="11" letter-spacing="1.2" text-anchor="end" \
fill="#484f58">{len(totals)} LANGUAGES · FORKS EXCLUDED</text>

  <line x1="56" y1="68" x2="944" y2="68" stroke="#21262d"/>

{chr(10).join(rows)}
</svg>
"""


if __name__ == "__main__":
    data = collect()
    with open(os.path.abspath(OUT), "w") as fh:
        fh.write(render(data))
    print(f"wrote {os.path.abspath(OUT)}")
    for lang, count in sorted(data.items(), key=lambda kv: -kv[1]):
        print(f"  {lang:<14} {count:>9,} B")
