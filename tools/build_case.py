#!/usr/bin/env python3
"""Add site chrome to clippa/index.html without editing the case study.

Replaces the old top nav with the shared nav and a Work / Clippa breadcrumb,
points the page at the local fonts plus site.css and clippa/restyle.css, and
adds the prev/next links. The case-study style block, copy, and markup inside
the page are left as they are. Safe to run again.

    python3 tools/build_case.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "clippa" / "index.html"

NAV = """<header class="site-wrap sitenav">
  <a class="brand" href="/">Brandon Young</a>
  <nav aria-label="Primary">
    <a href="/#work" aria-current="page">Work</a><span class="dot" aria-hidden="true">·</span>
    <a href="/#about">About</a><span class="dot" aria-hidden="true">·</span>
    <a href="https://github.com/byvfx">GitHub</a>
    <a class="vfx" href="https://byvfx.com" title="VFX work at byvfx.com">VFX ↗</a>
  </nav>
</header>
<nav class="site-wrap crumbs" aria-label="Project">
  <span><a href="/#work">Work</a> <span aria-hidden="true">/</span> Clippa</span>
  <span><a href="https://github.com/byvfx/clipper">GitHub</a><a href="https://github.com/byvfx/clipper/wiki">Docs</a></span>
</nav>
"""

PREVNEXT = """<nav class="site-wrap prevnext" aria-label="More projects">
  <a href="/#work"><span class="k">← Back to</span><span class="n">All work</span></a>
  <a href="https://github.com/byvfx/bif" class="next"><span class="k">Next project →</span><span class="n">BIF</span></a>
</nav>
"""


def main():
    src = PATH.read_text()
    src = re.sub(r"<link rel=\"preconnect\"[^>]*>\n", "", src)
    src = re.sub(
        r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>',
        '<link rel="stylesheet" href="../fonts/plex.css">\n<link rel="stylesheet" href="../site.css">',
        src,
    )
    if 'href="../fonts/plex.css"' not in src or 'href="../site.css"' not in src:
        raise SystemExit("clippa/index.html is missing the local font or site.css link")
    if 'href="restyle.css"' not in src:
        src = src.replace("</head>", '<link rel="stylesheet" href="restyle.css">\n</head>')

    old_nav = re.search(r'<nav class="wrap topnav".*?</nav>\s*', src, re.S)
    if old_nav:
        src = src[: old_nav.start()] + NAV + src[old_nav.end() :]
    elif 'class="site-wrap sitenav"' not in src or 'class="site-wrap crumbs"' not in src:
        raise SystemExit("clippa/index.html has neither the original top nav nor the site chrome")

    if 'class="site-wrap prevnext"' not in src:
        if "</body>" not in src:
            raise SystemExit("clippa/index.html has no </body>")
        src = src.replace("</body>", PREVNEXT + "</body>", 1)

    PATH.write_text(src)
    print("updated clippa/index.html")


if __name__ == "__main__":
    main()
