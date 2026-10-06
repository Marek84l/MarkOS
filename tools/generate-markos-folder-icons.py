#!/usr/bin/env python3

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ICONS_ROOT = (
    ROOT
    / "iso"
    / "config"
    / "includes.chroot"
    / "usr"
    / "share"
    / "icons"
)

THEMES = {
    "Cosmic": {
        "base": "#7c3aed",
        "light": "#a78bfa",
        "dark": "#4c1d95",
    },
    "Midnight": {
        "base": "#2563eb",
        "light": "#60a5fa",
        "dark": "#1e3a8a",
    },
    "Aurora": {
        "base": "#0d9488",
        "light": "#5eead4",
        "dark": "#115e59",
    },
    "Dawn": {
        "base": "#ea580c",
        "light": "#fb923c",
        "dark": "#9a3412",
    },
}

ICONS = {
    "folder": "",
    "folder-home": "⌂",
    "folder-documents": "≡",
    "folder-download": "↓",
    "folder-pictures": "◇",
    "folder-music": "♪",
    "folder-videos": "▶",
}


def make_svg(base, light, dark, symbol):
    symbol_svg = ""

    if symbol:
        symbol_svg = f"""
  <text
    x="32"
    y="42"
    text-anchor="middle"
    font-family="sans-serif"
    font-size="19"
    font-weight="700"
    fill="#ffffff"
    opacity="0.92">{symbol}</text>
"""

    return f"""<svg
  xmlns="http://www.w3.org/2000/svg"
  width="64"
  height="64"
  viewBox="0 0 64 64">

  <defs>
    <linearGradient id="folderGradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{light}"/>
      <stop offset="1" stop-color="{base}"/>
    </linearGradient>
  </defs>

  <path
    d="M7 14
       C7 11.8 8.8 10 11 10
       H26
       L31 16
       H53
       C55.2 16 57 17.8 57 20
       V49
       C57 52.3 54.3 55 51 55
       H13
       C9.7 55 7 52.3 7 49
       Z"
    fill="{dark}"
    opacity="0.95"/>

  <path
    d="M7 22
       C7 19.8 8.8 18 11 18
       H53
       C55.2 18 57 19.8 57 22
       V49
       C57 52.3 54.3 55 51 55
       H13
       C9.7 55 7 52.3 7 49
       Z"
    fill="url(#folderGradient)"/>

  <path
    d="M11 22 H53"
    stroke="#ffffff"
    stroke-width="1"
    opacity="0.18"/>

{symbol_svg}
</svg>
"""


for theme, colors in THEMES.items():
    output_dir = (
        ICONS_ROOT
        / f"MarkOS-{theme}"
        / "scalable"
        / "places"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    for icon_name, symbol in ICONS.items():
        svg = make_svg(
            colors["base"],
            colors["light"],
            colors["dark"],
            symbol,
        )

        output = output_dir / f"{icon_name}.svg"
        output.write_text(
            svg,
            encoding="utf-8",
        )

        print(output)
