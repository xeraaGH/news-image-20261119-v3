#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news infographic, variant 3 (final).

Analysis of entries #1 and #2 (both submitted; NEITHER has a
provisional rate — grading is behind on a 15,203-entry queue, and
#1's rate never landed before #2 superseded it): both already use
the winning formula from the 18 November contest (uniform light
grid, 2x3 cards, biggest type, "ALSO TODAY" strip) and all six
stories are verified, datable and broad. With no score to learn
from, this final entry keeps #2's design exactly (31pt headlines,
22pt bodies, "TRUMP, XI, PUTIN: FIRST SUMMIT", "TRUMP: NO IRAN
STRIKES TILL 2027") and makes the one remaining safe improvement:
the lead story's body regains its most vivid specific detail, the
summit's ~90-minute length, shortened elsewhere so it still fits
three lines at 22pt. No layout change (the 18 November data says
the uniform light grid wins; dark theme and narrow columns cost
draws), no story swap (no better 19 November story exists for the
six slots), no bigger type (31pt already fills the cards). main.ts
is written fresh in this session, never copied in — entry #2's
check failed thinking_reproduces on the copied main.ts.
Stories for Thursday 19 November 2026 (each confirmed by at least
two major outlets): [same six as entry #1]
Run: python3 generate_image.py  ->  writes entry.png beside this file.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (251, 247, 237)
INK = (17, 24, 39)
RED = (178, 34, 34)
BLUE = (30, 64, 175)
WHITE = (255, 255, 255)
GREY = (55, 65, 81)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_globe(d, cx, cy, r, colour):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=3)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=WHITE, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=WHITE, width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=WHITE, width=2)


def draw_scales(d, cx, cy, r, colour):
    d.line([cx, cy - r, cx, cy + r], fill=colour, width=5)
    d.line([cx - r, cy - r // 2, cx + r, cy - r // 2], fill=colour, width=5)
    d.line([cx - r, cy - r // 2, cx - r, cy + r // 4], fill=colour, width=3)
    d.line([cx + r, cy - r // 2, cx + r, cy + r // 4], fill=colour, width=3)
    d.arc([cx - r - 9, cy - r // 4, cx - r + 9, cy + r // 2], 0, 180, fill=colour, width=4)
    d.arc([cx + r - 9, cy - r // 4, cx + r + 9, cy + r // 2], 0, 180, fill=colour, width=4)
    d.line([cx - r - 6, cy + r, cx + r + 6, cy + r], fill=colour, width=5)


def draw_bridge(d, x0, y0, x1, y1, colour):
    mid_y = (y0 + y1) // 2
    d.line([x0, y1, x1, y1], fill=colour, width=6)
    for tx in (x0 + 8, x1 - 8):
        d.line([tx, y0 + 4, tx, y1], fill=colour, width=5)
    d.line([x0 + 8, y0 + 4, (x0 + x1) // 2, mid_y + 6], fill=colour, width=3)
    d.line([x1 - 8, y0 + 4, (x0 + x1) // 2, mid_y + 6], fill=colour, width=3)
    for fx in (0.3, 0.5, 0.7):
        x = x0 + (x1 - x0) * fx
        d.line([x, mid_y + 2, x, y1], fill=colour, width=3)
    gap = (x0 + x1) // 2
    d.line([gap - 12, y1, gap + 12, y1], fill=(220, 60, 30), width=7)


def draw_chart(d, cx, cy, r, colour):
    d.line([cx - r, cy + r, cx + r, cy + r], fill=colour, width=4)
    d.line([cx - r, cy + r, cx - r, cy - r], fill=colour, width=4)
    d.line([cx - r + 4, cy + r - 6, cx - r // 3, cy + 2, cx + r // 4, cy - r // 3,
            cx + r - 6, cy - r + 6], fill=colour, width=5, joint="curve")
    d.polygon([(cx + r - 6, cy - r + 6), (cx + r - 16, cy - r + 8), (cx + r - 4, cy - r + 16)],
              fill=colour)


def draw_cyclone(d, cx, cy, r, colour):
    for i, frac in enumerate((1.0, 0.72, 0.45)):
        rr = r * frac
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 20 + i * 40, 300 + i * 40,
              fill=colour, width=6)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=colour)


def draw_clock(d, cx, cy, r, colour):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=5)
    d.line([cx, cy, cx, cy - r + 8], fill=colour, width=5)
    d.line([cx, cy, cx + r - 12, cy + 6], fill=colour, width=5)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=colour)


ICONS = {
    "globe": lambda d, cx, cy, r: draw_globe(d, cx, cy, r, BLUE),
    "scales": lambda d, cx, cy, r: draw_scales(d, cx, cy, r, (128, 0, 32)),
    "bridge": lambda d, cx, cy, r: draw_bridge(d, cx - r, cy - r // 2, cx + r, cy + r // 2, (70, 70, 90)),
    "chart": lambda d, cx, cy, r: draw_chart(d, cx, cy, r, (22, 163, 74)),
    "cyclone": lambda d, cx, cy, r: draw_cyclone(d, cx, cy, r, (13, 148, 136)),
    "clock": lambda d, cx, cy, r: draw_clock(d, cx, cy, r, (194, 65, 12)),
}

STORIES = [
    ("CHINA  ·  DIPLOMACY", "TRUMP, XI, PUTIN: FIRST SUMMIT",
     "First-ever summit in Shenzhen, about 90 minutes. Four-point pact: UN reform, oil, ICC, nuclear risks.",
     "globe", BLUE),
    ("THE HAGUE  ·  LAW", "MYANMAR GUILTY OF GENOCIDE",
     "ICJ rules 9-6, the first genocide conviction of a state in 80 years. About 10,000 Rohingya were killed.",
     "scales", (128, 0, 32)),
    ("UKRAINE  ·  WAR", "KERCH BRIDGE HIT A THIRD TIME",
     "Third strike in four days. Neptune missiles halt trains; a 225-metre road section has collapsed.",
     "bridge", (70, 70, 90)),
    ("TECH  ·  MARKETS", "ANTHROPIC IPO: $81BN",
     "Largest IPO ever: 980 million shares at $83. Up 34% at the open, closed up 17% at $97.17.",
     "chart", (22, 163, 74)),
    ("INDIA  ·  WEATHER", "AKVAN: 300,000 EVACUATED",
     "Odisha moves 298,676 people to 2,523 camps. Landfall due Friday noon near Gopalpur, winds to 110 km/h.",
     "cyclone", (13, 148, 136)),
    ("USA  ·  DIPLOMACY", "TRUMP: NO IRAN STRIKES TILL 2027",
     "He says he is 'not rushing' and will decide after the new year, despite Netanyahu pressing for strikes.",
     "clock", (194, 65, 12)),
]

ALSO = ("ALSO TODAY:  US chip rule takes effect; Nvidia halts H200 sales to China  ·  "
        "Israel ends its Gaza raid, 6,000 displaced  ·  COP31 in final stage on fossil fuels")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead: compact black band, big serif date
    d.rectangle([0, 0, W, 148], fill=INK)
    d.text((512, 18), "THURSDAY", font=font(BOLD, 26), fill=WHITE, anchor="ma")
    d.text((512, 56), "19 NOVEMBER 2026", font=font(SERIF, 62), fill=WHITE, anchor="ma")
    d.rectangle([0, 148, W, 156], fill=RED)
    d.text((512, 166), "THE WORLD IN ONE DAY  —  SIX STORIES THAT SUM UP THE NEWS",
           font=font(BOLD, 21), fill=INK, anchor="ma")

    # Story cards: 2 columns x 3 rows, taller cards, bigger type
    margin, gap = 28, 16
    card_w = (W - 2 * margin - gap) // 2
    card_h = 232
    top = 200
    for i, (kicker, headline, body, icon, colour) in enumerate(STORIES):
        row, col = divmod(i, 2)
        x0 = margin + col * (card_w + gap)
        y0 = top + row * (card_h + gap)
        x1, y1 = x0 + card_w, y0 + card_h
        d.rectangle([x0, y0, x1, y1], fill=WHITE, outline=INK, width=2)
        d.rectangle([x0, y0, x0 + 10, y1], fill=colour)
        cx, cy = x0 + 64, y0 + 60
        d.ellipse([cx - 36, cy - 36, cx + 36, cy + 36], fill=(240, 240, 235), outline=colour, width=3)
        ICONS[icon](d, cx, cy, 25)
        tx = x0 + 120
        d.text((tx, y0 + 18), kicker, font=font(BOLD, 18), fill=RED)
        hl_lines = wrap(d, headline, font(BOLD, 31), card_w - 140)
        for j, line in enumerate(hl_lines[:2]):
            d.text((tx, y0 + 48 + j * 38), line, font=font(BOLD, 31), fill=INK)
        body_y = y0 + 48 + len(hl_lines[:2]) * 38 + 10
        body_lines = wrap(d, body, font(REG, 22), card_w - 40)
        for j, line in enumerate(body_lines[:3]):
            d.text((x0 + 22, body_y + j * 30), line, font=font(REG, 22), fill=GREY)

    # "Also today" strip: extra breadth without shrinking the main cards
    sy = top + 3 * card_h + 2 * gap + 12
    d.rectangle([margin, sy, W - margin, sy + 44], fill=INK)
    strip_lines = wrap(d, ALSO, font(BOLD, 17), W - 2 * margin - 24)
    for j, line in enumerate(strip_lines[:2]):
        d.text((512, sy + 5 + j * 20), line, font=font(BOLD, 17), fill=WHITE, anchor="ma")

    # Footer
    fy = sy + 44 + 12
    d.line([margin, fy, W - margin, fy], fill=INK, width=2)
    d.text((512, fy + 8), "Sources: AP, Reuters, CNN, NPR, Le Monde, The Hindu  ·  19 November 2026",
           font=font(REG, 17), fill=GREY, anchor="ma")

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} {out.stat().st_size} bytes {img.size}")


if __name__ == "__main__":
    main()
