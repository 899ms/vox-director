#!/usr/bin/env python3
"""
Style bake-off: render ONE representative beat in several candidate collage styles so
the user can pick the visual idiom before committing the whole film.

Hybrid selection: Claude reads the topic and chooses which idioms to try (names from
styles.STYLE_LIBRARY, or a custom idiom string), matching the topic's era/culture/tone —
don't default to Chinese motifs for a Western topic. Then the human picks by eye.

Usage:
  python3 style_bakeoff.py <project_dir> [style1,style2,...] [beat_index]
Defaults: the 4 Western library styles, beat 0. Output -> <project>/style-bakeoff/<style>.jpg
Then set  "collage_style": "<pick>"  in beats.json, clear old keyframe_url/path, re-run keyframes.
"""
import json
import os
import sys
import time

import atlas
from styles import compose_collage_prompt, STYLE_LIBRARY, THEME_PRESETS, resolve_theme

IMAGE_MODEL = "google/nano-banana-2/text-to-image"
# candidates are THEME names (full look bundles); Claude picks topic-fitting ones
DEFAULT_CANDIDATES = ["american-retro", "swiss-modern", "punk-zine", "atomic-age"]


def first_shot(beat):
    return beat["shots"][0] if beat.get("shots") else beat


def run(project_dir, styles=None, beat_index=0):
    styles = styles or DEFAULT_CANDIDATES
    with open(os.path.join(project_dir, "beats.json")) as f:
        doc = json.load(f)
    aspect = doc.get("aspect", "16:9")
    beat = doc["beats"][beat_index]
    shot = first_shot(beat)
    scene, bg = shot["scene"], beat.get("bg", "warm ochre")
    tcn, ten = beat.get("title_cn", ""), beat.get("title_en", "")
    out = os.path.join(project_dir, "style-bakeoff"); os.makedirs(out, exist_ok=True)

    jobs = {}
    for name in styles:
        tp = resolve_theme(name) or {}              # theme name -> full look bundle
        prompt = compose_collage_prompt(scene, tcn, ten, bg, aspect,
                                        style=tp.get("idiom", name), palette=tp.get("palette"),
                                        type_style=tp.get("type_style"), finish=tp.get("finish"))
        jobs[name] = atlas.submit_image(IMAGE_MODEL, prompt, aspect_ratio=aspect, resolution="2k")
        tag = "library" if name in STYLE_LIBRARY else "custom"
        print(f"[{name}] ({tag}) submitted {jobs[name]}")

    done, deadline = {}, time.time() + 240
    while len(done) < len(jobs) and time.time() < deadline:
        time.sleep(3)
        for name, pid in jobs.items():
            if name in done:
                continue
            try:
                d = atlas._get(f"/model/prediction/{pid}").get("data", {})
            except atlas.AtlasError as e:
                done[name] = None; print(f"[{name}] FAILED: {str(e)[:120]}"); continue
            st = d.get("status")
            if st in ("completed", "succeeded"):
                o = d.get("outputs") or d.get("output")
                done[name] = o[0] if isinstance(o, list) else o
                print(f"[{name}] done")
            elif st == "failed":
                done[name] = None; print(f"[{name}] FAILED: {d.get('error','')[:120]}")

    for name, url in done.items():
        if url:
            atlas.download(url, os.path.join(out, f"{name}.jpg"))
    print(f"\nsaved candidates to {out} — review, then set \"collage_style\" in beats.json.")


if __name__ == "__main__":
    proj = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else
                           os.path.join(os.path.dirname(__file__), "..", "out", "money-60s"))
    styles = sys.argv[2].split(",") if len(sys.argv) > 2 else None
    bi = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    run(proj, styles, bi)
