# Prompt Vocabulary Bank (image + video) — for building theme presets

Distilled from the official prompt guides of Midjourney, Flux, Google Nano-Banana/Gemini,
OpenAI, Ideogram (image) and Runway, Kling, ByteDance Seedance, Google Veo, OpenAI Sora,
Luma (video), plus StudioBinder/Swiss/riso design references. Use it two ways: (1) mix a
dimension's terms to compose a keyframe/motion prompt; (2) combine dimensions into named
**theme presets** (see the bottom table).

Everything here sits on top of the **common Vox constraints** (never drop these):
> torn/scissor-cut paper edges · tape · halftone dots · newspaper clippings · paper-stencil
> shapes · real paper drop-shadows · bold flat color · PRINTED/illustrated cut-outs · **NOT
> 3D, NOT CGI, NOT photoreal** · keep print grain · headline text baked in **"quotes"**.

---

## PART A — IMAGE dimensions

Our old prompt only had: style-idiom + collage-mechanics + scene + headline + aspect. Add these.

| Dimension | Controls | Vocab bank (mix & match) |
|---|---|---|
| **Medium/technique** | the strongest style lever | paper collage · torn-paper collage · photomontage · screenprint · **risograph** · letterpress · linocut/woodcut · lithograph · halftone print · gouache · flat vector · photocopy/xerox · rubber-stamp |
| **Art movement / era** ⭐ | single best "theme knob" — shifts palette+type+layout at once | Swiss/International Typographic · Bauhaus · mid-century modern · Russian Constructivism · Dada photomontage · Pop Art · psychedelic '60s · punk zine · Memphis · Art Deco · WPA/vintage travel poster · Soviet · atomic-age · retro-futurism |
| **Composition/layout** ⭐ | poster hierarchy + negative space | modular grid · asymmetric · strong negative space · diagonal dynamic · foreground–midground–background depth · hero headline + subhead hierarchy · full-bleed · radial · stacked bands · off-center focal |
| **Color palette** ⭐ | cleanest theme distinguisher (stops muddy gradients) | limited 2–3 color · duotone · monochrome + 1 accent · **riso fluorescent-pink + federal-blue** · Bauhaus primaries (red/yellow/blue) · '70s mustard/rust/avocado · '60s pop (hot-pink/orange) · teal-&-orange · CMYK process · cream/kraft base · neon-on-black · named hex (e.g. `#0047AB`) |
| **Typography treatment** ⭐ | headline LOOK (we only passed the words) | **put exact words in "quotes"** + name a REAL type style: bold condensed grotesque (Helvetica/Akzidenz) · geometric sans (Futura/Bauhaus) · slab serif · '70s display serif · wood-type · hand-lettered · **ransom-note cut-out letters** · stencil · all-caps · knockout/reversed · huge headline + small caption |
| **Print finish / texture** | "made by hand, not AI-slick" | halftone dots · **Ben-Day dots** · riso ink misregistration/overprint · letterpress deboss · newsprint · kraft/cardstock · aged/foxed paper · fold creases · coffee stains · deckled vs scissor-cut edges |
| **Lighting / capture** | keeps it "scanned" not "rendered" (anti-3D) | flat even studio light · shadowless scanned-document light · straight-on/head-on · flat-lay top-down · subtle paper drop-shadows |
| **Mood** | tone anchor | playful · bold · urgent · editorial/serious · nostalgic · optimistic · ominous · satirical · activist/protest |

**Image prompt structure** (consensus of Nano-Banana/Ideogram/OpenAI/Flux — Ideogram is
"format-first", best for baked text):
`[MEDIUM] + [ART MOVEMENT/ERA] of [SUBJECT + SCENE], [COMPOSITION/hierarchy/negative space],
[straight-on scanned-flat framing] + [flat even light, paper drop-shadows], [named limited COLOR
PALETTE], [PRINT FINISH/texture], headline "EXACT WORDS" in [NAMED TYPE STYLE] [placement], [MOOD],
[aspect]` — then per model: Omni/Nano-Banana/Flux/DALL·E take **no negatives** (phrase positively);
SDXL needs a negative field; Midjourney uses `--no` + params last.
Sources: Nano-Banana https://deepmind.google/models/gemini-image/prompt-guide/ · Ideogram
https://docs.ideogram.ai/using-ideogram/prompting-guide/2-prompting-fundamentals · OpenAI
https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide · Flux
https://docs.bfl.ml/guides/prompting_summary · Midjourney https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List

---

## PART B — VIDEO dimensions

Our old 5-axis (camera/movement/aesthetic/feel/color + constraints) is missing the axes that
control STABILITY. Add these — they fix the loop / text-wobble / morph we hit.

| Axis | Controls | Vocab / phrasing |
|---|---|---|
| **Motion amplitude** ⭐⭐ | THE anti-morph/anti-text-warp lever | `very subtle` · `minimal` · `moderate` · "~5% movement" · avoid `intense/large/explosive` near text |
| **Camera move** | how the camera travels | **safe for flat paper:** static/locked-off · slow push-in/pull-out · slow pan/tilt · subtle parallax truck. **AVOID (bend 2D into fake 3D):** orbit · crane · dolly-zoom · roll · 3D arc |
| **Shot size / angle** | framing | full poster in frame (default) · slow push to a detail · **eye-level straight-on (default)** · overhead (reads as paper on a table) |
| **Element motion** | what moves inside | **safe paper-native verbs:** drift · sway · ripple · flutter · slide · pivot (rigid) · bob · pulse · shimmer · settle · parallax between layers. **AVOID:** warp · transform · morph · vortex · explode |
| **Speed / easing** | tempo | slow · gentle · continuous · ease-in-ease-out · (risky: quick/snap/whip) |
| **Lighting-over-time** | best "safe motion" for flat art | soft light sweep across the surface · gentle shadow drift · subtle flicker/glow pulse |
| **Dimensional lock** ⭐ | keep it flat | "flat 2D, camera parallel to the poster, no 3D rotation, no perspective change; paper layers parallax only, elements slide/pivot as rigid flat paper, do not bend or morph" |
| **Stability anchors** ⭐⭐ | protect text/layout | "the printed headline, logo and layout stay sharp, legible and perfectly stable — do not redraw, distort or move the lettering" |
| **Shot structure** | cuts / loop | "single continuous shot, no cuts, no scene changes" · one-way: add a **motion endpoint** ("…then settles into place") · seamless loop: say "looping video" (Luma) |

### The best-practice rules that fix our bugs (all from official guides)
1. **Describe motion, not the picture.** The still already has subject/scene/text/style —
   restating them (esp. the text) makes the model re-synthesize and warp them. (Runway, Veo, Kling.)
2. **One camera move + one action per shot.** Multiple simultaneous moves = instability/morph.
   (Sora, Seedance: "specify only 1 type of camera movement… increases image instability".)
3. **Keep amplitude small; motion physically plausible.** (Kling, Seedance: "slow, gentle,
   coherent subtle movements… avoid high-burst, large-dynamic actions".)
4. **Positive phrasing only for Omni/Veo/Runway** — "no/don't" backfires ("may result in the
   opposite"). **Kling & Seedance DO support negative prompts.** Know your model.
5. **Text:** don't ask the video model to render text; anchor it as stable; keep motion away
   from the text region; **for critical text, overlay in post.** (Cross-source.)
6. **Anti-loop:** give a one-way move a settle endpoint, or say "single continuous"; short
   clips shouldn't over-script per-second beats. (Kling, Runway Gen-4.)
7. **Flat-collage:** name the style ("flat 2D paper cutout animation, rigid paper layers")
   and lock dimensionality → steers the model away from 3D morphing. (Storyblocks + rules above.)

**Video prompt structure** (I2V, adapted): `[SHOT SIZE+ANGLE] + [CAMERA MOVE + AMPLITUDE] +
[ELEMENT MOTION + SPEED/EASING] + [LIGHTING-OVER-TIME] + [AESTHETIC/TEXTURE + DIMENSIONAL LOCK] +
[FEEL] + [COLOR] + [STABILITY ANCHORS] + [SHOT STRUCTURE/LOOP]`.
Sources: Runway https://help.runwayml.com/hc/en-us/articles/39789879462419 · Kling I2V
https://kling.ai/quickstart/image-to-video-guide · Seedance https://docs.byteplus.com/en/docs/ModelArk/2222480 ·
Veo https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1 ·
Sora https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide · StudioBinder camera
glossary https://www.studiobinder.com/blog/different-types-of-camera-movements-in-film/

---

## PART C — Building THEME PRESETS (combine the dimensions)

A **theme preset** = one pick from each image dimension + a motion preset, on top of the common
Vox constraints. This is how we offer "different theme options" without hand-writing each prompt.

| Preset | Era/movement | Palette | Type style | Print finish | Motion preset | Fits topics |
|---|---|---|---|---|---|---|
| `american-retro` | 1950s US ad/pulp | bold retro primaries | wood-type / bold slab | halftone, aged | punchy | ads, sports, business, money |
| `swiss-modern` | Swiss/Intl Typographic | 2-color + red accent | Helvetica/Akzidenz grotesk | clean flat, subtle grain | calm | tech, finance, explainers |
| `punk-zine` | 90s punk/DIY | B&W + 1 spot color | ransom-note cut letters | photocopy, misregistration | punchy/max | rebellion, music, counterculture |
| `soviet-constructivist` | Russian Constructivism | red/black/cream | bold condensed diagonal | letterpress, newsprint | punchy | politics, revolution, industry |
| `wpa-propaganda` | 1930s WPA poster | muted 3-color | stencil / gothic | screenprint grain | calm | history, labor, public health |
| `70s-groovy` | 1970s | mustard/rust/avocado | bulbous display serif | riso grain | punchy | culture, food, nostalgia |
| `chinese-ink` | Chinese woodblock/ink | ink + vermilion | Chinese brush + red seal | rice-paper, seal | calm/punchy | Chinese history/culture |
| `atomic-age` | 1950s futurism | teal/orange/cream | atomic script | halftone | punchy | science, space, future |

**How to use:** Claude reads the topic → suggests 3–4 fitting presets (or composes a new one by
mixing the banks above) → `style_bakeoff.py` renders one beat in each → the user picks. The picked
preset's fields drop into the image prompt (via `collage_style` + palette/type/finish) and its
`motion_style` into the video prompt. The common Vox constraints and stability anchors are always on.
