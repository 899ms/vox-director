#!/usr/bin/env python3
"""
Keyframe stage: one styled keyframe per SHOT.

Each beat holds one or more shots (different framings of the same narration
beat) so the cut has variety. Falls back to one implicit shot per beat if a
beat has no "shots". Generates concurrently, downloads to
<project>/keyframes/kf_<beat><shot>.jpg, records url+path onto each shot.

Usage: python3 keyframes.py <project_dir>   (default: out/tang-30s)
"""
import json
import os
import sys
import time

import atlas
from styles import compose_keyframe_prompt, compose_collage_prompt, resolve_theme

IMAGE_MODEL = "google/nano-banana-2/text-to-image"


def shots_of(beat):
    """Yield (shot_dict, shot_key) for a beat; synthesize one shot if none."""
    if beat.get("shots"):
        for s in beat["shots"]:
            yield s, f"{beat['id']}{s.get('id','')}"
    else:
        yield beat, f"{beat['id']}"   # beat acts as its own single shot


def run(project_dir):
    bpath = os.path.join(project_dir, "beats.json")
    with open(bpath) as f:
        doc = json.load(f)
    aspect = doc.get("aspect", "16:9")
    style = doc.get("style", "painterly")
    theme = resolve_theme(doc.get("theme")) or {}   # theme preset -> full look bundle
    collage_style = theme.get("idiom") or doc.get("collage_style", "american-retro")
    # a registered theme wins; a custom (unregistered) theme may set these at doc level
    t_palette = theme.get("palette") or doc.get("palette")
    t_type = theme.get("type_style") or doc.get("type_style")
    t_finish = theme.get("finish") or doc.get("finish")
    era = doc.get("era")            # only needed for the painterly (per-dynasty) style
    kf_dir = os.path.join(project_dir, "keyframes")
    os.makedirs(kf_dir, exist_ok=True)

    jobs = {}   # key -> (pid, shot_ref)
    for beat in doc["beats"]:
        for shot, key in shots_of(beat):
            if shot.get("keyframe_url"):        # already generated (e.g. reused wide) -> skip
                continue
            scene = shot["scene"]
            if style == "collage":
                prompt = compose_collage_prompt(scene, beat["title_cn"], beat["title_en"],
                                                beat.get("bg", "warm ochre"), aspect,
                                                with_title=shot.get("title", True),
                                                style=collage_style, palette=t_palette,
                                                type_style=t_type, finish=t_finish)
            else:
                prompt = compose_keyframe_prompt(era, scene, beat["title_cn"],
                                                 beat["title_en"], aspect)
            shot["keyframe_prompt"] = prompt
            pid = atlas.submit_image(IMAGE_MODEL, prompt, aspect_ratio=aspect, resolution="2k")
            jobs[key] = (pid, shot)
            print(f"[{key}] submitted {pid}")

    done = {}
    deadline = time.time() + 300
    while len(done) < len(jobs) and time.time() < deadline:
        time.sleep(3)
        for key, (pid, _) in jobs.items():
            if key in done:
                continue
            try:
                d = atlas._get(f"/model/prediction/{pid}").get("data", {})
            except atlas.AtlasError as e:
                done[key] = None
                print(f"[{key}] FAILED (poll error): {str(e)[:160]}")
                continue
            st = d.get("status")
            if st in ("completed", "succeeded"):
                out = d.get("outputs") or d.get("output")
                done[key] = out[0] if isinstance(out, list) else out
                print(f"[{key}] done")
            elif st == "failed":
                done[key] = None
                print(f"[{key}] FAILED: {d.get('error','')[:160]}")

    for key, (_, shot) in jobs.items():
        url = done.get(key)
        if not url:
            continue
        dest = os.path.join(kf_dir, f"kf_{key}.jpg")
        atlas.download(url, dest)
        shot["keyframe_url"] = url
        shot["keyframe_path"] = dest
        print(f"[{key}] saved {dest}")

    with open(bpath, "w") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print("updated", bpath)


if __name__ == "__main__":
    proj = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "out", "tang-30s")
    run(os.path.abspath(proj))
