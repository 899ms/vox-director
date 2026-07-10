#!/usr/bin/env python3
"""
Text overlays via Pillow -> transparent PNG (this ffmpeg has no libass/drawtext,
so captions/watermark are rendered as images and composited with `overlay`).
"""
import os
from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]
FONT_REG = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
]


def _font(paths, size):
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def _wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render_caption(text, out_path, W=1920, H=1080, margin_v=None):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    size = int(min(W, H) * 0.045)              # size by short edge (works 16:9 & 9:16)
    if margin_v is None:
        margin_v = int(H * 0.06)
    fnt = _font(FONT_BOLD, size)
    lines = _wrap(d, text, fnt, int(W * 0.8))
    lh = int(size * 1.32)
    total_h = lh * len(lines)
    y = H - margin_v - total_h
    for ln in lines:
        w = d.textlength(ln, font=fnt)
        x = (W - w) / 2
        d.text((x, y), ln, font=fnt, fill=(255, 255, 255, 255),
               stroke_width=max(2, size // 12), stroke_fill=(0, 0, 0, 235))
        y += lh
    img.save(out_path)
    return out_path


def render_title(text, out_path, W=1080, H=1920, sub=None):
    """Big centered title (dark on transparent) for the ending assembly card."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    size = int(min(W, H) * 0.075)
    fnt = _font(FONT_BOLD, size)
    lines = _wrap(d, text, fnt, int(W * 0.86))
    lh = int(size * 1.2)
    y = int(H * 0.1)
    for ln in lines:
        w = d.textlength(ln, font=fnt)
        d.text(((W - w) / 2, y), ln, font=fnt, fill=(40, 30, 24, 255),
               stroke_width=2, stroke_fill=(255, 255, 255, 180))
        y += lh
    if sub:
        sf = _font(FONT_REG, int(size * 0.4))
        sw = d.textlength(sub, font=sf)
        d.text(((W - sw) / 2, y + 6), sub, font=sf, fill=(150, 40, 30, 255))
    img.save(out_path)
    return out_path


def render_watermark(text, out_path, W=1920, H=1080):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    size = int(min(W, H) * 0.024)              # size by short edge
    fnt = _font(FONT_REG, size)
    tw = d.textlength(text, font=fnt)
    pad = 14
    x, y = W - tw - 28 - pad, H - size - 28 - pad
    d.rounded_rectangle([x - pad, y - pad, x + tw + pad, y + size + pad + 4],
                        radius=8, fill=(0, 0, 0, 90))
    d.text((x, y), text, font=fnt, fill=(255, 255, 255, 210))
    img.save(out_path)
    return out_path
