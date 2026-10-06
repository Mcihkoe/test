#!/usr/bin/env python3
"""YouTube thumbnail template (1280x720 JPG).

Usage:
  python3 tools/make_thumbnail.py --image visuals/bg.png --out output/thumb.jpg \
      --title "New York|Afternoon Jazz" --kicker "RELAXING JAZZ PLAYLIST" \
      --subtitle "뉴욕 공원의 여유로운 오후 재즈" --badge "1 HOUR" [--side left|right]

Title lines are split with "|". Keep the layout fixed across a series so the channel looks consistent.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1280, 720
FONTS = Path(__file__).resolve().parent.parent / "assets" / "fonts"
CREAM = (250, 240, 222)
GOLD = (232, 182, 92)
INK = (38, 26, 16)


def font(name, size):
    return ImageFont.truetype(str(FONTS / f"{name}.woff"), size)


def is_hangul(ch):
    return "가" <= ch <= "힣" or "㄰" <= ch <= "㆏"


def draw_mixed(d, xy, text, size, fill, ko="noto-sans-kr-korean-500-normal", latin="montserrat-latin-500-normal"):
    """Hangul glyphs from Noto Sans KR, everything else from the latin font."""
    x, y = xy
    fk, fl = font(ko, size), font(latin, size)
    for ch in text:
        f = fk if is_hangul(ch) else fl
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f)
    return x


def cover(img):
    r = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    left, top = (img.width - W) // 2, (img.height - H) // 2
    return img.crop((left, top, left + W, top + H))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="New York|Afternoon Jazz")
    ap.add_argument("--kicker", default="RELAXING JAZZ PLAYLIST")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--badge", default="1 HOUR")
    ap.add_argument("--side", choices=["left", "right"], default="left")
    a = ap.parse_args()

    bg = cover(Image.open(a.image).convert("RGB"))
    # warm grade + slight contrast so text pops
    bg = Image.blend(bg, Image.new("RGB", bg.size, (255, 170, 90)), 0.06)

    # dark gradient on the text side
    grad = Image.new("L", (W, H))
    gd = ImageDraw.Draw(grad)
    for x in range(W):
        u = x / W if a.side == "right" else 1 - x / W
        gd.line([(x, 0), (x, H)], fill=int(205 * max(0, min(1, (u - 0.3) / 0.5)) ** 1.6))
    shade = Image.new("RGB", (W, H), (22, 14, 8))
    img = Image.composite(shade, bg, grad.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(img)

    lines = a.title.split("|")
    x0 = 72 if a.side == "left" else None
    y = 92

    def place(width):
        return x0 if x0 is not None else W - 72 - width

    # kicker with letter spacing
    fk = font("montserrat-latin-700-normal", 24)
    spaced = " ".join(a.kicker)
    kw = d.textlength(spaced, font=fk)
    d.text((place(kw), y), spaced, font=fk, fill=GOLD)
    y += 52

    sizes = [118] + [92] * (len(lines) - 1)
    for line, size in zip(lines, sizes):
        ft = font("playfair-display-latin-700-italic", size)
        tw = d.textlength(line, font=ft)
        px = place(tw)
        # soft shadow
        sh = Image.new("RGBA", (W, H))
        ImageDraw.Draw(sh).text((px + 4, y + 6), line, font=ft, fill=(0, 0, 0, 170))
        img.paste(sh.filter(ImageFilter.GaussianBlur(6)), (0, 0), sh.filter(ImageFilter.GaussianBlur(6)))
        d = ImageDraw.Draw(img)
        d.text((px, y), line, font=ft, fill=CREAM)
        y += int(size * 1.08)

    # gold rule
    y += 34
    rx = place(120)
    d.rectangle([rx, y, rx + 120, y + 4], fill=GOLD)
    y += 30

    if a.subtitle:
        sw = sum(d.textlength(c, font=font("noto-sans-kr-korean-500-normal" if is_hangul(c) else "montserrat-latin-500-normal", 38)) for c in a.subtitle)
        draw_mixed(d, (place(sw), y), a.subtitle, 38, CREAM)

    if a.badge:
        fb = font("montserrat-latin-700-normal", 34)
        bw = d.textlength(a.badge, font=fb)
        bx = 72 if a.side == "left" else W - 72 - bw - 48
        by = H - 72 - 64
        d.rounded_rectangle([bx, by, bx + bw + 48, by + 64], radius=32, fill=GOLD)
        d.text((bx + 24, by + 13), a.badge, font=fb, fill=INK)

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    img.save(a.out, "JPEG", quality=90, optimize=True)
    print(f"wrote {a.out} ({Path(a.out).stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
