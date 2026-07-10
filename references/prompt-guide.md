# Prompt Guide — the heart of the Vox collage look

Two prompts decide whether the film reads as a real Vox collage or a moving poster: the
**image prompt** (makes the collage look) and the **video/motion prompt** (makes it move like
collage). Get these right and the rest is plumbing.

- [1. Image prompt — 5-part structure](#1-image-prompt)
- [2. Video / motion prompt — 5-axis structure](#2-video-prompt)
- [3. Why layering the image is what unlocks good AI motion](#3-layering)
- [4. Real people](#4-real-people)

---

## 1. Image prompt

The collage look is *born here*. On the standard (whole-poster-animation) path this single
image carries the entire aesthetic, so invest in it. Structure every image prompt in 5 parts:

```
[1 STYLE BLOCK — identical on every beat]
  Mixed-media hand-cut PAPER COLLAGE, editorial zine style. Torn/scissor-cut paper edges,
  tape corners, halftone print dots, newspaper clippings, paper-stencil shapes, real paper
  drop shadows. Figures are PRINTED-texture cut-outs of real imagery (photo / woodblock /
  mural), NOT CGI, NOT a 3D render — keep print grain and paper imperfections. High-contrast.

[2 SCENE — describe as SEPARATE cut-out pieces]
  SCENE as layered paper cut-outs: {main subject}, {a prop}, {a text strip}, {a decorative
  scrap}; elements have clear edges, distinct layers, each with its own drop shadow.

[3 BACKGROUND — one bold flat color]
  on a bold flat {bg color} paper background.

[4 HEADLINE — baked in, short + bold]
  A torn-paper banner with a big bold headline "{TITLE}" (+ small subtitle), plus a red seal.

[5 TECH]
  aspect ratio {16:9|9:16|3:4}, 2k resolution.
```

### Techniques
- **Reuse the style block verbatim on every beat.** Only the scene, bg color and headline
  change. This is what makes 6 different beats feel like one film.
- **Describe distinct pieces with visible edges + shadows.** Two reasons: it looks assembled
  (collage, not a smooth painting), and it gives the *video* model separable layers to
  parallax (see §3). A blended scene can only be panned as one flat plane.
- **Bake the headline text into the image** — image models render crisp text; video models
  smear it. Keep it short, bold, 2–3 words.
- **Bold flat background color, one per beat.** Busy backgrounds muddy the cut-out silhouettes
  and kill the Vox punch. Let the palette travel across beats to carry mood (see the color
  axis below): e.g. aged sepia → bold pop colors → champion gold.
- **Say "NOT 3D / NOT CGI, printed texture, keep grain"** or the model drifts toward smooth
  render-CGI and loses the paper feel.
- **2k** so cut-outs stay crisp if scaled/animated.
- Keep a **consistent paper-texture language** across beats (edge roughness, halftone
  density); color can change, texture shouldn't.

### Worked example (2008 "KING OF EUROPE" beat, deep-red)
> Mixed-media hand-cut PAPER COLLAGE, editorial zine style; torn edges, tape, halftone dots,
> newspaper clippings, paper-stencil texture, real drop shadows; PRINTED-texture cut-outs, NOT
> 3D/CGI, keep print grain. SCENE as layered paper cut-outs: a roaring footballer in a red
> kit, a gold trophy, a big cut-out "7", a torn "KING OF EUROPE" newspaper strip, a club
> crest, scattered geometric scraps — clear edges and drop shadows. Bold flat deep-red paper
> background. Torn-paper banner headline "KING OF EUROPE" + small subtitle, red seal. 3:4, 2k.

---

## 2. Video prompt

The motion prompt turns "pan a poster" into "a living collage". Use the **5-axis** structure
(this is the structure from the reference cr7 Omni prompt — all five axes matter, especially
**feel** and **color**, which set mood and palette movement):

```
[GOAL] Animate this still into a mixed-media collage MOTION GRAPHIC. Keep it flat 2D paper,
       NOT 3D, no photoreal.

[AXIS 1 · CAMERA]   one smooth continuous move for this shot: {slow push-in | lateral
                    parallax pan | slow rise}.
[AXIS 2 · MOVEMENT] layered paper cut-outs drift with visible drop-shadow parallax; elements
                    and geometric scraps bob/settle gently on the beat; halftone dots pulse;
                    torn edges and tape flutter; a breathing quality.
[AXIS 3 · AESTHETIC]preserve the torn-paper / tape / halftone / newspaper / paper-stencil
                    textures exactly; keep the bold flat background.
[AXIS 4 · FEEL]     {emotional tone of this beat} — e.g. tender / triumphant / cinematic
                    editorial, "a page from a scrapbook".
[AXIS 5 · COLOR]    {this beat's palette}, high contrast; if part of an arc, name where it
                    sits (aged sepia → bold pop → champion gold).

[CONSTRAINTS] keep the layout, the seal and ALL on-screen text perfectly stable and legible;
              ONE smooth continuous move — absolutely NO sudden zoom snaps, NO jump-cuts, NO
              teleporting/re-framing inside the shot; no new objects, no morphing, no drift.
```

### Techniques
- **The MOVEMENT axis is the lever** that makes Omni move *layers* (parallax) instead of
  sliding the whole frame. Name the layered paper motion explicitly.
- **FEEL and COLOR are not decoration** — they steer the model's pacing and grade. A "tender,
  sepia" beat animates slower and warmer than a "triumphant, gold" beat. Don't drop them.
- **The CONSTRAINTS axis prevents the common breaks**: text wobble, 3D drift, and the big one
  — internal jump-cuts.
- **Never write "snap / punch-in / slam / quick zoom".** Omni over-reacts and generates a
  jump *inside* the shot that reads as a one-frame flash. Ask for ONE smooth continuous move.
- **Don't rely on the video model for text** — it's already baked in the keyframe; just tell
  the model to keep it stable.
- **One move per shot.** For richer editing, cut between multiple short shots (wide + detail)
  rather than asking one clip to do a complex timeline.

---

## 3. Layering

Common question: *"can I feed a background + separate component images to the video model to
get dramatic component motion?"* In practice, no — Omni/Kling `reference-to-video` is
**generative**, not a layer compositor: it reinterprets the refs and invents its own motion,
so you get *less* control, not more. For controlled per-element choreography, use the local
engine (`references/local-engine.md`).

But there's a real lever within the standard path: **the more clearly layered your keyframe
is, the more layered motion the video model can produce.** Distinct cut-outs with edges and
shadows → the model can drift them at different depths (parallax) → "living collage". A flat,
blended image → only a whole-frame pan is possible. So push the *layering* in the image
prompt (§1) if you want livelier auto-motion.

---

## 4. Real people

Real-person keyframes are fine to *generate* (use web-search grounding or a reference photo
with an edit model to anchor the face). The catch is *animation*: Google (Omni) and ByteDance
(Seedance) refuse recognizable celebrities / brand logos ("prohibited contents" /
"digital-rights"). Two ways through:
- **Kling O3 pro** allows real people — set it as `video_model` (simplest).
- **Local engine** — animating cut-outs frame-by-frame never touches a video model's content
  filter, and gives full control. Best when you also want dramatic element choreography.
