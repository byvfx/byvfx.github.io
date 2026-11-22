# byvfx.github.io

Source for [byvfx.github.io](https://byvfx.github.io), Brandon Young's portfolio of software and engineering work.

VFX work is on [byvfx.com](https://byvfx.com).

## Pages

- `/` is the homepage: featured Clippa case study, selected projects, and smaller tools.
- `/clippa/` is the Clippa case study.

The site is static HTML for GitHub Pages (`.nojekyll`). IBM Plex is loaded from the local files in `fonts/`.

## Rebuild

From the repo root:

```bash
python3 tools/build_home.py
python3 tools/build_case.py
```

`tools/build_home.py` writes `index.html` from `tools/home.template.html`. Project names, descriptions, releases, and licenses live in that script.

`tools/build_case.py` points `clippa/index.html` at the local fonts, `site.css`, and `clippa/restyle.css`. It replaces the old top nav with the shared nav, the Work / Clippa breadcrumb (GitHub and Docs links kept), and the prev/next links. It does not change the case-study text or markup. Running it again on an already restyled page leaves that page as it is.
