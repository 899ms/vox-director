#!/usr/bin/env python3
"""
Audio stage: per-beat narration (one consistent voice) + one instrumental BGM.

Narration uses xai/tts-v1 (a real multilingual TTS: named `voice_id` + language),
so every beat is spoken in the same voice — this sidesteps Omni's clip-to-clip
voice drift. Seed-Audio was tried and dropped: as a general *sound* model it gave
wildly inconsistent narration lengths unless a speaker is pinned (see VOICE_MODEL).

Usage: python3 audio.py <project_dir>   (default: out/tang-30s)
"""
import json
import os
import subprocess
import sys
import time

import atlas

# xai/tts-v1 is a clean, predictable multilingual TTS (named voices + language
# select). Seed-Audio is a general *sound* model that injects pauses/SFX and
# gave wildly inconsistent narration lengths, so we use a real TTS here.
VOICE_MODEL = "xai/tts-v1"
MUSIC_MODEL = "minimax/music-2.6"


def probe_dur(path: str) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    try:
        return float(out.strip())
    except ValueError:
        return 0.0


def run(project_dir: str):
    bpath = os.path.join(project_dir, "beats.json")
    with open(bpath) as f:
        doc = json.load(f)
    adir = os.path.join(project_dir, "audio")
    os.makedirs(adir, exist_ok=True)

    voice = doc.get("voice", {})
    voice_id = voice.get("voice_id", "leo")     # named male documentary-ish voice
    language = voice.get("language", doc.get("language", "en"))
    speed = float(voice.get("speed", 1.0))

    jobs = {}
    for beat in doc["beats"]:
        pid = atlas.submit_media(VOICE_MODEL, text=beat["narration"], language=language,
                                 voice_id=voice_id, codec="mp3", sample_rate=44100, speed=speed)
        jobs[("narr", beat["id"])] = pid
        print(f"[narr {beat['id']}] submitted {pid}")

    # BGM: only generate if we don't already have one (it's slow + costs more).
    bgm_path = os.path.join(adir, "bgm.mp3")
    if not os.path.exists(bgm_path):
        music_prompt = doc.get("music", "cinematic majestic traditional Chinese guzheng erhu, warm")
        mpid = atlas.submit_media(MUSIC_MODEL, prompt=music_prompt, is_instrumental=True,
                                  format="mp3")
        jobs[("bgm", 0)] = mpid
        print(f"[bgm] submitted {mpid}")
    else:
        print(f"[bgm] reuse existing {bgm_path}")

    # poll all
    done = {}
    deadline = time.time() + 600
    while len(done) < len(jobs) and time.time() < deadline:
        time.sleep(4)
        for key, pid in jobs.items():
            if key in done:
                continue
            d = atlas._get(f"/model/prediction/{pid}").get("data", {})
            st = d.get("status")
            if st in ("completed", "succeeded"):
                out = d.get("outputs") or d.get("output")
                done[key] = out[0] if isinstance(out, list) else out
                print(f"{key} done")
            elif st == "failed":
                done[key] = None
                print(f"{key} FAILED: {json.dumps(d)[:200]}")

    # download + record
    for beat in doc["beats"]:
        url = done.get(("narr", beat["id"]))
        if url:
            dest = os.path.join(adir, f"narr_{beat['id']}.mp3")
            atlas.download(url, dest)
            beat["narration_audio"] = dest
            beat["narration_dur"] = round(probe_dur(dest), 2)
            print(f"[narr {beat['id']}] {beat['narration_dur']}s -> {dest}")
    bgm_url = done.get(("bgm", 0))
    if bgm_url:
        bgm = os.path.join(adir, "bgm.mp3")
        atlas.download(bgm_url, bgm)
        doc["bgm_path"] = bgm
        doc["bgm_dur"] = round(probe_dur(bgm), 2)
        print(f"[bgm] {doc['bgm_dur']}s -> {bgm}")

    with open(bpath, "w") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print("updated", bpath)


if __name__ == "__main__":
    proj = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "out", "tang-30s")
    run(os.path.abspath(proj))
