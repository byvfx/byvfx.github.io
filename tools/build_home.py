#!/usr/bin/env python3
"""Regenerate index.html from tools/home.template.html.

The descriptions, releases, licenses, and repository names below are the
approved portfolio facts. Run from anywhere:

    python3 tools/build_home.py
"""
import html
from pathlib import Path

E = html.escape
ROOT = Path(__file__).resolve().parents[1]

FEAT = dict(
    name="Clippa",
    repo="clipper",
    tags=["Python", "ffmpeg", "WhisperX", "Docker", "Modal"],
    rel="v0.3.0",
    lic="MIT",
    desc=(
        "A pipeline that turns long livestreams into reviewed, captioned, "
        "scheduled YouTube videos and Shorts. It runs unattended, and a person "
        "reviews everything before it goes out."
    ),
    stages=[
        "record", "transcribe", "signals", "score", "segments", "cut", "meta",
        "thumbs", "shorts", "faces", "review", "schedule", "upload",
    ],
)
SELECTED = [
    dict(name="BIF", repo="bif", tags=["Rust", "USD", "Vulkan"], rel="v0.16.9", lic="MIT",
         desc="A USD orchestration tool for VFX. Open a stage, pick a working layer, scatter and instance geometry, override materials, and render. Every edit authors clean USD opinions."),
    dict(name="notion-md-sync", repo="go-notion-md-sync", tags=["Go", "Notion API"], rel="v0.17.0", lic="MIT",
         desc="Syncs a folder of Markdown files with a tree of Notion pages in either direction. Only the blocks you changed are touched, so block IDs, comments and links survive."),
    dict(name="Floki", repo="floki", tags=["Rust", "wgpu", "egui", "OpenEXR", "OCIO"], rel="v1.13.3", lic="MIT",
         desc="A GPU-accelerated viewer for multi-layer OpenEXR files. Inspect passes and channels, read floating-point histograms, stack renders to pixel-diff them, and play image sequences in real time."),
    dict(name="Comfyless", repo="comfyless", tags=["Python", "ComfyUI", "Modal"], rel=None, lic="GPL-3.0",
         desc="Adds a Local / Cloud switch next to ComfyUI's Run button. Workflows run on cloud GPUs in your own Modal account, with no server to manage."),
]
PIPELINE = [
    dict(name="CamDB for Houdini", repo="hou-camDb", tags=["Python", "Houdini"], rel=None, lic="MIT",
         desc="Browse real-world cameras and sensor modes, then create a matching Houdini camera in one click."),
    dict(name="DirPipe", repo="dir-pipeline", tags=["Go", "CLI"], rel="v0.1.0", lic=None,
         desc="A command-line tool that creates standardized directory structures for VFX and animation assets and shots."),
]
STUDIES = [
    dict(name="Go Raytracer", repo="go-raytracing", tags=["Go", "Ebiten"], rel=None, lic=None,
         desc="A study built from the Ray Tracing in One Weekend series, extended with parallel bucket rendering and HDRI lighting."),
    dict(name="SDF Maker", repo="sdf-maker", tags=["Rust", "CLI + GUI"], rel=None, lic=None,
         desc="Converts grayscale images into 2D signed distance fields for game engines, with brute-force and jump-flooding algorithms."),
]


def tags(items):
    return '<ul class="tags">' + "".join(f"<li>{E(x)}</li>" for x in items) + "</ul>"


def meta(project):
    rel = f'<span class="rel">{E(project["rel"])}</span>' if project["rel"] else '<span class="none">no release</span>'
    lic = f'<span class="sep">·</span><span>{E(project["lic"])}</span>' if project["lic"] else ""
    repo = project["repo"]
    return (
        f'<p class="meta"><a href="https://github.com/byvfx/{E(repo)}">github.com/byvfx/{E(repo)}</a>'
        f'<span class="sep">·</span>{rel}{lic}</p>'
    )


def card(project):
    repo = project["repo"]
    return (
        '<article class="proj">'
        f'<h3><a class="title" href="https://github.com/byvfx/{E(repo)}">{E(project["name"])}</a></h3>'
        f'<p class="desc">{E(project["desc"])}</p>'
        f'{tags(project["tags"])}'
        f'{meta(project)}'
        "</article>"
    )


def row(project):
    repo = project["repo"]
    return (
        "<li><div>"
        f'<h3><a href="https://github.com/byvfx/{E(repo)}">{E(project["name"])}</a></h3>'
        f'{tags(project["tags"])}</div>'
        f'<p class="desc">{E(project["desc"])}</p>'
        f'{meta(project)}'
        "</li>"
    )


def main():
    stages = "".join(
        f'<li class="human">{name}</li>' if name == "review" else f"<li>{name}</li>"
        for name in FEAT["stages"]
    )
    body = (ROOT / "tools" / "home.template.html").read_text()
    body = (
        body.replace("{{FEAT_TAGS}}", tags(FEAT["tags"]))
        .replace("{{FEAT_META}}", meta(FEAT))
        .replace("{{FEAT_DESC}}", E(FEAT["desc"]))
        .replace("{{STAGES}}", stages)
        .replace("{{SELECTED}}", "".join(card(p) for p in SELECTED))
        .replace("{{PIPELINE}}", "".join(row(p) for p in PIPELINE))
        .replace("{{STUDIES}}", "".join(row(p) for p in STUDIES))
    )
    if "{{" in body:
        raise SystemExit("unreplaced template token in index.html")
    (ROOT / "index.html").write_text(body)
    print("wrote index.html")


if __name__ == "__main__":
    main()
