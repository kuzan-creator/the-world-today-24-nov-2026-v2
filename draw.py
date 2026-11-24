#!/usr/bin/env python3
"""Draw "The World in One Day" -- Tuesday 24 November 2026.

A single cream newspaper page summing up the day's world news:
35 stories, 3 heroes, 10 illustrated cards, a numbered list of 22,
a world map with pins, a date check and a sources footer.

Everything is drawn from scratch with PIL shapes; no outside images.
Run:  python3 draw.py [output.png]   (default: entry.png next to this file)
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "entry.png"

PAGE_W, PAGE_H = 1024, 1024
EDGE = 24                      # side margin; content runs 24..1000
RIGHT = PAGE_W - EDGE

# --- palette (sampled from the approved page) ---
PAPER = (247, 240, 221)
CARD = (255, 253, 247)
INK = (26, 26, 26)
SOFT = (74, 74, 70)            # grey body text
NAVY = (18, 38, 74)
RED = (176, 32, 28)
SEA = (127, 179, 213)
LAND = (214, 208, 182)
LAND_LINE = (96, 96, 84)
RULE = (198, 192, 177)         # hairlines on the paper

REGION = {                     # key -> (colour, bar label, story count)
    "EU":   ((46, 95, 163),   "EUROPE", 10),
    "ME":   ((176, 32, 28),   "MIDDLE EAST", 6),
    "AP":   ((81, 160, 160),  "ASIA-PACIFIC", 8),
    "AM":   ((53, 129, 56),   "AMERICAS", 6),
    "TECH": ((108, 79, 161),  "TECH & BUSINESS", 3),
    "SCI":  ((183, 121, 31),  "SCIENCE & CULTURE", 2),
}
BAR_ORDER = ["EU", "ME", "AP", "AM", "TECH", "SCI"]

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
LIB_DIR = Path("/usr/share/fonts/truetype/liberation")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def lib(name, size):
    return ImageFont.truetype(str(LIB_DIR / name), size)


def f_serif_b(s):
    return font("DejaVuSerif-Bold.ttf", s)


def f_serif(s):
    return font("DejaVuSerif.ttf", s)


def f_sans_b(s):
    return font("DejaVuSans-Bold.ttf", s)


def f_sans(s):
    return font("DejaVuSans.ttf", s)


def f_lib_b(s):
    return lib("LiberationSans-Bold.ttf", s)


def f_lib(s):
    return lib("LiberationSans-Regular.ttf", s)


def f_lib_serif_b(s):
    return lib("LiberationSerif-Bold.ttf", s)


def f_lib_serif_i(s):
    return lib("LiberationSerif-Italic.ttf", s)


def wrap(text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if fnt.getlength(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading):
    """Draw stacked lines starting at (x, y); returns bottom y."""
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def number_disc(d, cx, cy, r, num, fill=RED):
    """Small filled disc with a white number, like the story badges."""
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)
    fnt = f_sans_b(11 if r <= 9 else 12)
    d.text((cx, cy), str(num), font=fnt, fill=(255, 255, 255),
           anchor="mm")




# ---------------------------------------------------------------- top of page

def draw_masthead(d):
    """Navy band: title left, story count right."""
    d.rectangle((0, 0, PAGE_W, 26), fill=NAVY)
    d.text((EDGE, 6), "THE WORLD IN ONE DAY",
           font=f_sans_b(13), fill=(255, 255, 255))
    right = "35 STORIES \u00b7 6 REGIONS \u00b7 EVERY ONE DATED " \
            "TUESDAY 24 NOVEMBER 2026"
    d.text((RIGHT, 7), right, font=f_sans_b(11),
           fill=(255, 255, 255), anchor="ra")


def draw_headline(img, d):
    """Giant centred serif date, red slanted subline beneath."""
    title = "Tuesday 24 November 2026"
    d.text((PAGE_W // 2, 33), title, font=f_lib_serif_b(58), fill=INK,
           anchor="ma")
    sub = ("Three tankers hit mines \u00b7 Russian strike kills 2, "
           "wounds 40 \u00b7 Israeli strikes kill Hamas security chief")
    d.text((PAGE_W // 2, 100), sub, font=f_lib_serif_i(16), fill=RED,
           anchor="ma")
    d.line((EDGE, 124, RIGHT, 124), fill=RULE, width=1)


NUMBERS = [
    ("3", "tankers hit mines in Hormuz"),
    ("40", "wounded in Zaporizhzhia"),
    ("700,000", "Russian soldiers killed"),
    ("14", "nations back ICJ ruling"),
    ("$41bn", "Sanofi deal for Insmed"),
    ("6,500", "Rohingya to return"),
]


def draw_numbers(d):
    """Six-cell strip: big red figure over a small grey label."""
    top, bottom = 127, 166
    cell = (RIGHT - EDGE) / len(NUMBERS)
    for i, (figure, label) in enumerate(NUMBERS):
        cx = EDGE + cell * (i + 0.5)
        d.text((cx, top + 1), figure, font=f_lib_serif_b(23), fill=RED,
               anchor="ma")
        d.text((cx, top + 23), label, font=f_lib(10), fill=SOFT,
               anchor="ma")
        if i:
            x = EDGE + cell * i
            d.line((x, top + 4, x, bottom - 4), fill=RULE, width=1)
    d.line((EDGE, bottom, RIGHT, bottom), fill=RULE, width=1)


# Segment edges measured off the approved page (x positions).
BAR_EDGES = [24, 194, 344, 524, 664, 824, 1000]


def draw_region_bar(d):
    """Six coloured segments, one per region, white bold labels."""
    top, bottom = 170, 192
    for key, x0, x1 in zip(BAR_ORDER, BAR_EDGES, BAR_EDGES[1:]):
        colour, label, _count = REGION[key]
        d.rectangle((x0, top, x1, bottom), fill=colour)
        d.text(((x0 + x1) // 2, top + 4), f"{label} {REGION[key][2]}",
               font=f_lib_b(12), fill=(255, 255, 255), anchor="ma")


# ------------------------------------------------------------ hero pictures

def scene_tanker(d, x0, y0, x1, y1):
    """Burning tanker at sunset on a blue sea."""
    w, h = x1 - x0, y1 - y0
    # sunset bands, orange at the horizon fading up to dusk purple
    bands = [(252, 164, 60), (247, 140, 40), (238, 110, 40),
             (222, 84, 48), (120, 70, 90)]
    for i, col in enumerate(bands):
        d.rectangle((x0, y0 + i * h // 5, x1, y0 + (i + 1) * h // 5),
                    fill=col)
    d.ellipse((x0 + w * 0.68, y0 + 6, x0 + w * 0.68 + 34,
               y0 + 40), fill=(255, 224, 150))          # low sun
    for cx, cy, r in [(0.12, 0.16, 16), (0.22, 0.10, 20), (0.30, 0.20, 13)]:
        d.ellipse((x0 + w * cx - r, y0 + h * cy - r // 2,
                   x0 + w * cx + r, y0 + h * cy + r // 2),
                  fill=(70, 62, 78))                    # smoke clouds
    sea_y = y0 + int(h * 0.58)
    d.rectangle((x0, sea_y, x1, y1), fill=(16, 44, 84))  # dark sea
    for i in range(5):                                   # wave glints
        yy = sea_y + 10 + i * 9
        d.arc((x0 + 12 + i * 30, yy, x0 + 52 + i * 30, yy + 10),
              200, 340, fill=(150, 190, 225), width=2)
    # tanker: black hull, red waterline, white bridge, containers
    hull_y = sea_y - 14
    d.polygon([(x0 + 18, hull_y), (x0 + w - 14, hull_y),
               (x0 + w - 30, hull_y + 16), (x0 + 34, hull_y + 16)],
              fill=(24, 24, 28))
    d.rectangle((x0 + 30, hull_y + 12, x0 + w - 26, hull_y + 16),
                fill=RED)
    d.rectangle((x0 + w - 78, hull_y - 26, x0 + w - 34, hull_y),
                fill=(240, 240, 235))
    for i in range(3):
        d.rectangle((x0 + 40 + i * 4, hull_y - 8, x0 + 48 + i * 4,
                     hull_y - 2), fill=(120, 170, 220))
    for i in range(4):                                   # deck boxes
        d.rectangle((x0 + 44 + i * 34, hull_y - 16,
                     x0 + 72 + i * 34, hull_y - 2),
                    fill=[(180, 60, 40), (60, 110, 160),
                          (200, 160, 60), (90, 140, 90)][i])
    # flames licking up from three deck fires
    for fx, fh in [(0.24, 26), (0.40, 40), (0.55, 28)]:
        bx = x0 + w * fx
        d.polygon([(bx - 15, hull_y - 2), (bx, hull_y - fh),
                   (bx + 15, hull_y - 2)], fill=(255, 120, 20))
        d.polygon([(bx - 8, hull_y - 2), (bx, hull_y - fh * 0.62),
                   (bx + 8, hull_y - 2)], fill=(255, 205, 60))
    # orange reflection streaks on the water
    for sx, sw in [(0.30, 46), (0.44, 30), (0.58, 38)]:
        d.rectangle((x0 + w * sx, sea_y + 22, x0 + w * sx + sw, sea_y + 25),
                    fill=(240, 140, 50))
    for cx, cy, r in [(0.30, 0.10, 12), (0.34, 0.04, 9),
                      (0.52, 0.06, 13), (0.57, 0.12, 8)]:
        d.ellipse((x0 + w * cx - r, y0 + h * cy - r,
                   x0 + w * cx + r, y0 + h * cy + r),
                  fill=(90, 84, 92))                    # fire smoke


def scene_rescue_night(d, x0, y0, x1, y1):
    """Rescuers at a damaged apartment block, at night.

    Big dark slab with a grid of lit windows, a black blast hole
    ringed in orange, grey smoke, a crane arm swinging in from the
    top right, rubble and two orange rescuers at the base.
    """
    w, h = x1 - x0, y1 - y0
    d.rectangle((x0, y0, x1, y1), fill=(22, 27, 52))
    for sx, sy in [(0.08, 0.12), (0.25, 0.06), (0.45, 0.15),
                   (0.62, 0.07), (0.80, 0.12), (0.92, 0.05),
                   (0.35, 0.22), (0.70, 0.22)]:
        d.ellipse((x0 + w * sx - 2, y0 + h * sy - 2,
                   x0 + w * sx + 2, y0 + h * sy + 2),
                  fill=(230, 230, 200))
    d.ellipse((x0 + w * 0.82, y0 + 8, x0 + w * 0.82 + 26, y0 + 34),
              fill=(238, 232, 200))                     # moon
    # main block, filling the left two thirds
    bx0, bx1 = x0 + 14, x0 + int(w * 0.62)
    d.rectangle((bx0, y0 + 22, bx1, y1 - 20), fill=(38, 38, 52))
    for r in range(4):
        for c in range(3):
            wx = bx0 + 12 + c * 52
            wy = y0 + 34 + r * 19
            lit = (r * 3 + c) % 4 != 3
            d.rectangle((wx, wy, wx + 26, wy + 12),
                        fill=(255, 205, 90) if lit else (16, 16, 26))
    # blast hole with an orange rim, smoke curling out of it
    hx, hy = x0 + int(w * 0.34), y0 + int(h * 0.48)
    d.ellipse((hx - 20, hy - 14, hx + 20, hy + 14), fill=(255, 120, 30))
    d.ellipse((hx - 15, hy - 10, hx + 15, hy + 10), fill=(8, 8, 12))
    for cx, cy, r in [(0.34, 0.22, 13), (0.38, 0.16, 10), (0.30, 0.28, 9)]:
        d.ellipse((x0 + w * cx - r, y0 + h * cy - r,
                   x0 + w * cx + r, y0 + h * cy + r),
                  fill=(110, 108, 115))
    # lower block on the right with a few lit windows
    d.rectangle((x0 + int(w * 0.68), y0 + 52, x1 - 14, y1 - 20),
                fill=(30, 30, 44))
    for r in range(2):
        for c in range(2):
            wx = x0 + int(w * 0.68) + 12 + c * 34
            wy = y0 + 62 + r * 20
            d.rectangle((wx, wy, wx + 18, wy + 12),
                        fill=(255, 205, 90) if (r + c) % 2 else (16, 16, 26))
    # crane arm swinging in from the top right
    d.line((x1 - 6, y0 + 6, x0 + int(w * 0.66), y0 + int(h * 0.42)),
           fill=(10, 10, 14), width=4)
    d.line((x0 + int(w * 0.66), y0 + int(h * 0.42),
            x0 + int(w * 0.66), y0 + int(h * 0.58)),
           fill=(10, 10, 14), width=2)
    d.rectangle((x0 + int(w * 0.66) - 7, y0 + int(h * 0.58),
                 x0 + int(w * 0.66) + 7, y0 + int(h * 0.66)),
                fill=(200, 170, 60))
    # rubble mound, small fire glow, two rescuers
    d.polygon([(x0 + 10, y1), (x0 + 70, y1 - 24), (x0 + 150, y1 - 12),
               (x0 + 190, y1)], fill=(58, 56, 60))
    d.ellipse((x0 + int(w * 0.48) - 12, y1 - 16,
               x0 + int(w * 0.48) + 12, y1 - 2), fill=(255, 140, 40))
    d.ellipse((x0 + int(w * 0.48) - 6, y1 - 12,
               x0 + int(w * 0.48) + 6, y1 - 2), fill=(255, 210, 90))
    for rx, ry in [(0.60, 0.80), (0.78, 0.76)]:
        px, py = x0 + w * rx, y0 + h * ry
        d.ellipse((px - 5, py - 16, px + 5, py - 6), fill=(255, 200, 150))
        d.rectangle((px - 6, py - 6, px + 6, py + 12),
                    fill=(255, 120, 30))
        d.rectangle((px - 6, py + 12, px - 2, py + 22), fill=(40, 40, 50))
        d.rectangle((px + 2, py + 12, px + 6, py + 22), fill=(40, 40, 50))


def scene_gaza_street(d, x0, y0, x1, y1):
    """Gaza City street in bright daylight.

    Pale tower blocks, one with a black blast hole ringed in orange;
    ambulance at the left, two rescuers carrying a red stretcher
    at the right, rubble and a fallen concrete slab on the street.
    """
    w, h = x1 - x0, y1 - y0
    d.rectangle((x0, y0, x1, y0 + int(h * 0.55)), fill=(184, 210, 224))
    d.ellipse((x0 + w * 0.80, y0 + 8, x0 + w * 0.80 + 30, y0 + 38),
              fill=(255, 240, 170))                     # sun
    for cx, cy, r in [(0.15, 0.12, 14), (0.30, 0.08, 18), (0.55, 0.14, 12)]:
        d.ellipse((x0 + w * cx - r, y0 + h * cy - r // 2,
                   x0 + w * cx + r, y0 + h * cy + r // 2),
                  fill=(240, 240, 235))
    # back row of pale tower blocks with windows
    for bx, bw, bh in [(0.04, 0.20, 0.42), (0.28, 0.16, 0.50),
                       (0.48, 0.22, 0.38), (0.74, 0.20, 0.46)]:
        d.rectangle((x0 + w * bx, y0 + h * (0.55 - bh),
                     x0 + w * (bx + bw), y0 + h * 0.55),
                    fill=(196, 182, 158))
        for r in range(3):
            for c in range(3):
                wx = x0 + w * bx + 8 + c * 16
                wy = y0 + h * (0.55 - bh) + 8 + r * 13
                d.rectangle((wx, wy, wx + 9, wy + 8),
                            fill=(90, 110, 130))
    # blast hole with orange rim on the middle block, smoke above it
    hx, hy = x0 + int(w * 0.40), y0 + int(h * 0.30)
    d.ellipse((hx - 17, hy - 12, hx + 17, hy + 12), fill=(255, 120, 30))
    d.ellipse((hx - 12, hy - 8, hx + 12, hy + 8), fill=(8, 8, 12))
    for cx, cy, r in [(0.40, 0.08, 12), (0.45, 0.04, 10), (0.36, 0.13, 9)]:
        d.ellipse((x0 + w * cx - r, y0 + h * cy - r,
                   x0 + w * cx + r, y0 + h * cy + r), fill=(70, 70, 72))
    # street, rubble mounds and a fallen concrete slab
    d.rectangle((x0, y0 + int(h * 0.55), x1, y1), fill=(150, 146, 138))
    d.polygon([(x0 + 8, y1), (x0 + 60, y1 - 22), (x0 + 120, y1 - 10),
               (x0 + 150, y1)], fill=(110, 106, 100))
    d.polygon([(x1 - 150, y1), (x1 - 100, y1 - 18), (x1 - 40, y1 - 8),
               (x1 - 10, y1)], fill=(120, 116, 108))
    d.polygon([(x1 - 70, y1 - 22), (x1 - 30, y1 - 26), (x1 - 14, y1 - 12),
               (x1 - 56, y1 - 10)], fill=(225, 222, 212))
    # ambulance at the left: white box, red stripe, red cross, blue light
    ax0, ay0 = x0 + 10, y0 + int(h * 0.58)
    ax1, ay1 = x0 + int(w * 0.44), y0 + int(h * 0.88)
    d.rectangle((ax0, ay0, ax1, ay1), fill=(248, 248, 246))
    d.rectangle((ax0, ay1 - 10, ax1, ay1 - 6), fill=RED)
    d.rectangle((ax0 + 52, ay0 + 8, ax0 + 60, ay0 + 24), fill=RED)
    d.rectangle((ax0 + 46, ay0 + 12, ax0 + 66, ay0 + 20), fill=RED)
    d.rectangle((ax0 + 8, ay0 + 8, ax0 + 32, ay0 + 22), fill=(150, 200, 230))
    d.ellipse((ax0 + 76, ay0 - 4, ax0 + 88, ay0 + 4), fill=(40, 90, 200))
    for wx in (ax0 + 22, ax1 - 26):
        d.ellipse((wx - 9, ay1 - 2, wx + 9, ay1 + 10), fill=(30, 30, 32))
        d.ellipse((wx - 4, ay1 + 3, wx + 4, ay1 + 7), fill=(160, 160, 160))
    # two rescuers carrying a red stretcher at the right
    for rx in (0.60, 0.78):
        px, py = x0 + w * rx, y0 + h * 0.78
        d.ellipse((px - 5, py - 16, px + 5, py - 6), fill=(230, 190, 150))
        d.rectangle((px - 6, py - 6, px + 6, py + 12),
                    fill=(255, 120, 30))
        d.rectangle((px - 6, py + 12, px - 2, py + 22), fill=(40, 40, 50))
        d.rectangle((px + 2, py + 12, px + 6, py + 22), fill=(40, 40, 50))
    d.rectangle((x0 + w * 0.60, y0 + h * 0.86, x0 + w * 0.80,
                 y0 + h * 0.90), fill=(200, 40, 40))

HEROES = [
    dict(num=1, region="ME", kicker="STRAIT OF HORMUZ \u00b7 IRAN WAR",
         title="Three tankers hit mines as Iran rules out talks",
         deck=("Tehran vows to use all its tools against the US blockade; "
               "three tankers hit mines and caught fire. (Reuters)"),
         caption="Burning tanker \u00b7 Reuters", scene=scene_tanker),
    dict(num=2, region="EU", kicker="ZAPORIZHZHIA, UKRAINE \u00b7 WAR",
         title="Russian strike kills 2, wounds 40 in Zaporizhzhia",
         deck=("Overnight hit wrecks an apartment block; four children "
               "among the wounded. (Reuters)"),
         caption="Rescuers at work \u00b7 Reuters", scene=scene_rescue_night),
    dict(num=3, region="ME", kicker="GAZA \u00b7 ISRAEL-HAMAS WAR",
         title="Israeli strikes kill Hamas security chief",
         deck=("Naeem Abu Nahel killed in Gaza City; six others dead, "
               "including two police officers. (Reuters)"),
         caption="Gaza City street \u00b7 Reuters", scene=scene_gaza_street),
]
HERO_X = [(24, 337), (356, 668), (687, 999)]
HERO_TOP, HERO_PIC_BOT, HERO_CAP_BOT, HERO_BOT = 196, 295, 312, 424


def draw_hero(d, hero, x0, x1):
    """One hero card: picture, black caption strip, kicker, title, deck."""
    d.rectangle((x0, HERO_TOP, x1, HERO_BOT), fill=CARD,
                outline=INK, width=1)
    hero["scene"](d, x0 + 1, HERO_TOP + 1, x1 - 1, HERO_PIC_BOT)
    d.rectangle((x0 + 1, HERO_PIC_BOT + 1, x1 - 1, HERO_CAP_BOT),
                fill=INK)
    d.text((x0 + 10, HERO_PIC_BOT + 4), hero["caption"],
           font=f_sans(11), fill=(255, 255, 255))
    pad = 10
    d.text((x0 + pad, HERO_CAP_BOT + 6), hero["kicker"],
           font=f_sans_b(11), fill=RED)
    number_disc(d, x1 - 14, HERO_CAP_BOT + 15, 10, hero["num"])
    title_lines = wrap(hero["title"], f_sans_b(19), (x1 - x0) - 2 * pad)
    text_block(d, x0 + pad, HERO_CAP_BOT + 26, title_lines,
               f_sans_b(19), INK, 30)
    deck_lines = wrap(hero["deck"], f_sans(10), (x1 - x0) - 2 * pad)
    text_block(d, x0 + pad, HERO_BOT - 26, deck_lines,
               f_sans(10), SOFT, 12)


# ------------------------------------------------------------ card pictures

def scene_satellite(d, x0, y0, x1, y1):
    """NATO space: a satellite over the curve of the Earth."""
    w, h = x1 - x0, y1 - y0
    d.rectangle((x0, y0, x1, y1), fill=(16, 32, 72))
    for sx, sy in [(0.1, 0.15), (0.3, 0.08), (0.55, 0.18), (0.75, 0.1),
                   (0.9, 0.22), (0.2, 0.3), (0.65, 0.3)]:
        d.ellipse((x0 + w * sx - 1, y0 + h * sy - 1,
                   x0 + w * sx + 1, y0 + h * sy + 1),
                  fill=(240, 240, 220))
    d.ellipse((x0, y1 - 26, x1, y1 + 46), fill=(40, 110, 170))  # Earth
    d.ellipse((x0 + 20, y1 - 26, x0 + 90, y1 + 30), fill=(60, 150, 90))
    cx, cy = x0 + w * 0.5, y0 + h * 0.38                      # satellite
    d.rectangle((cx - 34, cy - 8, cx - 8, cy + 8), fill=(30, 90, 160))
    d.rectangle((cx + 8, cy - 8, cx + 34, cy + 8), fill=(30, 90, 160))
    d.rectangle((cx - 10, cy - 7, cx + 10, cy + 7), fill=(200, 205, 210))
    d.ellipse((cx - 13, cy - 9, cx + 13, cy + 9), outline=(255, 80, 40),
              width=2)
    d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=(40, 90, 170))
    d.line((cx - 10, cy + 7, cx - 22, cy + 20), fill=(220, 220, 210),
           width=2)


def scene_crosses(d, x0, y0, x1, y1):
    """War toll: rows of white crosses in a field at dusk."""
    w, h = x1 - x0, y1 - y0
    d.rectangle((x0, y0, x1, y0 + int(h * 0.55)), fill=(238, 150, 60))
    d.ellipse((x0 + w * 0.72, y0 + 6, x0 + w * 0.72 + 24, y0 + 30),
              fill=(255, 230, 160))
    d.rectangle((x0, y0 + int(h * 0.55), x1, y1), fill=(120, 90, 55))
    for r in range(3):
        for c in range(6):
            cx = x0 + 18 + c * 28
            cy = y0 + int(h * 0.62) + r * 14
            s = 7 - r
            d.rectangle((cx - 1, cy - s, cx + 1, cy + s), fill=(245, 245, 240))
            d.rectangle((cx - s, cy - 2, cx + s, cy + 2), fill=(245, 245, 240))


def scene_warship(d, x0, y0, x1, y1):
    """Warship hit: grey warship, black smoke, orange blast."""
    w, h = x1 - x0, y1 - y0
    d.rectangle((x0, y0, x1, y0 + int(h * 0.55)), fill=(150, 190, 220))
    for cx, cy, r in [(0.2, 0.12, 10), (0.45, 0.08, 13), (0.75, 0.14, 9)]:
        d.ellipse((x0 + w * cx - r, y0 + h * cy - r // 2,
                   x0 + w * cx + r, y0 + h * cy + r // 2),
                  fill=(240, 240, 238))
    d.rectangle((x0, y0 + int(h * 0.55), x1, y1), fill=(30, 80, 130))
    for i in range(4):
        yy = y0 + int(h * 0.62) + i * 8
        d.arc((x0 + 10 + i * 40, yy, x0 + 50 + i * 40, yy + 8),
              200, 340, fill=(180, 210, 235), width=2)
    hy = y0 + int(h * 0.52)
    d.polygon([(x0 + 16, hy), (x0 + w - 16, hy), (x0 + w - 34, hy + 14),
               (x0 + 30, hy + 14)], fill=(90, 95, 100))
    d.rectangle((x0 + 66, hy - 18, x0 + 118, hy), fill=(110, 115, 120))
    d.rectangle((x0 + 84, hy - 28, x0 + 92, hy - 18), fill=(80, 85, 90))
    d.line((x0 + 88, hy - 28, x0 + 88, hy - 38), fill=(60, 60, 62), width=2)
    for fx, fh in [(0.62, 26), (0.70, 18)]:
        bx = x0 + w * fx
        d.polygon([(bx - 12, hy), (bx, hy - fh), (bx + 12, hy)],
                  fill=(255, 120, 20))
        d.polygon([(bx - 6, hy), (bx, hy - fh * 0.6), (bx + 6, hy)],
                  fill=(255, 205, 60))
    for cx, cy, r in [(0.66, 0.10, 10), (0.72, 0.05, 8)]:
        d.ellipse((x0 + w * cx - r, y0 + h * cy - r,
                   x0 + w * cx + r, y0 + h * cy + r), fill=(60, 60, 64))


def scene_court(d, x0, y0, x1, y1):
    """Genocide ruling: flags and the scales of justice."""
    w, h = x1 - x0, y1 - y0
    d.rectangle((x0, y0, x1, y1), fill=(196, 164, 120))
    d.rectangle((x0, y0 + int(h * 0.72), x1, y1), fill=(120, 80, 45))
    # two small flags: blue-yellow and red
    for fx, (c1, c2) in enumerate([((40, 90, 170), (255, 210, 60)),
                                   ((176, 32, 28), (255, 255, 255))]):
        bx = x0 + 16 + fx * 58
        d.rectangle((bx, y0 + 10, bx + 34, y0 + 22), fill=c1)
        d.rectangle((bx, y0 + 22, bx + 34, y0 + 34), fill=c2)
        d.line((bx, y0 + 10, bx, y0 + 44), fill=(60, 50, 40), width=2)
    # scales: pole, beam, two pans
    cx, cy = x0 + w * 0.5, y0 + h * 0.30
    d.rectangle((cx - 2, cy, cx + 2, cy + 34), fill=(90, 70, 30))
    d.line((cx - 34, cy + 2, cx + 34, cy + 2), fill=(90, 70, 30), width=3)
    for sx in (-34, 34):
        d.line((cx + sx, cy + 2, cx + sx, cy + 16), fill=(90, 70, 30),
               width=2)
        d.polygon([(cx + sx - 12, cy + 16), (cx + sx + 12, cy + 16),
                   (cx + sx, cy + 26)], fill=(220, 190, 90))
    d.ellipse((cx - 4, cy - 8, cx + 4, cy), fill=(220, 190, 90))


def scene_chip(d, x0, y0, x1, y1):
    """CEO returns: a green AI chip on a circuit board."""
    w, h = x1 - x0, y1 - y0
    d.rectangle((x0, y0, x1, y1), fill=(12, 60, 35))
    for i in range(5):                                       # traces
        yy = y0 + 8 + i * 13
        d.line((x0 + 6, yy, x0 + w - 6, yy), fill=(30, 130, 70), width=1)
    for i in range(6):
        xx = x0 + 14 + i * 28
        d.line((xx, y0 + 6, xx, y0 + h - 6), fill=(30, 130, 70), width=1)
    cx, cy = x0 + w * 0.5, y0 + h * 0.5
    d.rectangle((cx - 34, cy - 22, cx + 34, cy + 22), fill=(20, 160, 90))
    d.rectangle((cx - 34, cy - 22, cx + 34, cy + 22), outline=(220, 255, 230),
                width=2)
    for i in range(4):                                       # pins
        d.line((cx - 34 + i * 18, cy - 22, cx - 34 + i * 18, cy - 30),
               fill=(220, 220, 200), width=3)
        d.line((cx - 34 + i * 18, cy + 22, cx - 34 + i * 18, cy + 30),
               fill=(220, 220, 200), width=3)
    d.text((cx, cy), "AI", font=f_sans_b(20), fill=(255, 255, 255),
           anchor="mm")
    d.line((x0 + 14, y0 + h - 14, x0 + 60, y0 + h - 26, x0 + 110,
            y0 + h - 20), fill=(255, 210, 60), width=2)      # rising chart


def scene_summit(d, x0, y0, x1, y1):
    """COP31: summit hall with flags, a COP31 podium, delegates."""
    w, h = x1 - x0, y1 - y0
    d.rectangle((x0, y0, x1, y1), fill=(222, 200, 150))
    d.rectangle((x0, y0 + int(h * 0.70), x1, y1), fill=(140, 100, 60))
    for i, col in enumerate([(40, 90, 170), (176, 32, 28), (53, 129, 56),
                             (255, 210, 60), (108, 79, 161), (220, 120, 40)]):
        bx = x0 + 10 + i * 29
        d.rectangle((bx, y0 + 8, bx + 20, y0 + 20), fill=col)
        d.line((bx + 10, y0 + 20, bx + 10, y0 + 30), fill=(90, 70, 40),
               width=2)
    # podium with COP31 sign
    px0, px1 = x0 + int(w * 0.32), x0 + int(w * 0.68)
    d.rectangle((px0, y0 + int(h * 0.44), px1, y0 + int(h * 0.72)),
                fill=(60, 60, 90))
    d.rectangle((px0 + 6, y0 + int(h * 0.48), px1 - 6, y0 + int(h * 0.62)),
                fill=(20, 40, 80))
    d.text(((px0 + px1) // 2, y0 + int(h * 0.55)), "COP31",
           font=f_sans_b(13), fill=(255, 255, 255), anchor="mm")
    # seated delegates
    for dx, col in [(0.10, (150, 60, 60)), (0.22, (60, 90, 150)),
                    (0.80, (60, 130, 80)), (0.90, (180, 140, 50))]:
        px, py = x0 + w * dx, y0 + h * 0.86
        d.ellipse((px - 6, py - 22, px + 6, py - 10), fill=(235, 200, 165))
        d.polygon([(px - 11, py + 6), (px - 8, py - 10), (px + 8, py - 10),
                   (px + 11, py + 6)], fill=col)


def scene_clinic(d, x0, y0, x1, y1):
    """Ebola teams: a white clinic tent in a green clearing."""
    w, h = x1 - x0, y1 - y0
    d.rectangle((x0, y0, x1, y0 + int(h * 0.5)), fill=(170, 215, 235))
    d.ellipse((x0 + w * 0.80, y0 + 6, x0 + w * 0.80 + 24, y0 + 30),
              fill=(255, 240, 170))
    d.rectangle((x0, y0 + int(h * 0.5), x1, y1), fill=(110, 170, 90))
    for tx in (0.10, 0.82):                                  # trees
        px = x0 + w * tx
        d.rectangle((px - 3, y0 + h * 0.42, px + 3, y0 + h * 0.62),
                    fill=(110, 80, 40))
        d.ellipse((px - 14, y0 + h * 0.28, px + 14, y0 + h * 0.52),
                  fill=(40, 120, 50))
    # tent with a red cross
    tx0, tx1 = x0 + int(w * 0.28), x0 + int(w * 0.72)
    ty = y0 + int(h * 0.34)
    d.polygon([(tx0, y0 + int(h * 0.72)), (tx0, ty + 12),
               ((tx0 + tx1) // 2, ty), (tx1, ty + 12),
               (tx1, y0 + int(h * 0.72))], fill=(248, 248, 244))
    cx = (tx0 + tx1) // 2
    d.rectangle((cx - 3, ty + 14, cx + 3, ty + 28), fill=RED)
    d.rectangle((cx - 10, ty + 19, cx + 10, ty + 25), fill=RED)
    d.rectangle((cx - 8, y0 + int(h * 0.58), cx + 8, y0 + int(h * 0.72)),
                fill=(90, 70, 50))
    # two camp beds
    for bx in (0.06, 0.72):
        d.rectangle((x0 + w * bx, y0 + h * 0.82, x0 + w * (bx + 0.18),
                     y0 + h * 0.88), fill=(240, 240, 235))


def scene_quake(d, x0, y0, x1, y1):
    """Quake: cracked ground, a leaning house, a seismograph trace."""
    w, h = x1 - x0, y1 - y0
    d.rectangle((x0, y0, x1, y0 + int(h * 0.5)), fill=(190, 215, 235))
    d.polygon([(x0, y0 + int(h * 0.5)), (x0 + 50, y0 + int(h * 0.18)),
               (x0 + 110, y0 + int(h * 0.5))], fill=(120, 140, 160))
    d.polygon([(x0 + 90, y0 + int(h * 0.5)), (x0 + 150, y0 + int(h * 0.24)),
               (x1, y0 + int(h * 0.5))], fill=(100, 125, 150))
    d.rectangle((x0, y0 + int(h * 0.5), x1, y1), fill=(150, 125, 90))
    # leaning house
    d.polygon([(x0 + 26, y0 + int(h * 0.62)), (x0 + 66, y0 + int(h * 0.58)),
               (x0 + 66, y0 + int(h * 0.82)), (x0 + 26, y0 + int(h * 0.86))],
              fill=(210, 180, 140))
    d.polygon([(x0 + 22, y0 + int(h * 0.62)), (x0 + 46, y0 + int(h * 0.50)),
               (x0 + 70, y0 + int(h * 0.58))], fill=(150, 60, 50))
    # ground cracks
    d.line((x0 + 90, y1, x0 + 110, y0 + int(h * 0.66), x0 + 130, y1),
           fill=(70, 55, 40), width=2)
    d.line((x0 + 140, y1, x0 + 155, y0 + int(h * 0.72)), fill=(70, 55, 40),
           width=2)
    # red seismograph zigzag across the top
    pts = []
    for i, yy in enumerate([14, 26, 8, 30, 12, 24, 10, 28, 14]):
        pts.append((x0 + 96 + i * 10, y0 + yy))
    d.line(pts, fill=RED, width=2)


def scene_phone_gavel(d, x0, y0, x1, y1):
    """Grok sued: a phone showing AI, a gavel, courthouse columns."""
    w, h = x1 - x0, y1 - y0
    d.rectangle((x0, y0, x1, y1), fill=(200, 220, 235))
    for i in range(4):                                       # columns
        cx = x0 + 22 + i * 44
        d.rectangle((cx - 8, y0 + 10, cx + 8, y0 + int(h * 0.62)),
                    fill=(235, 232, 220))
        d.rectangle((cx - 11, y0 + 6, cx + 11, y0 + 12), fill=(210, 205, 190))
    d.rectangle((x0, y0 + int(h * 0.62), x1, y0 + int(h * 0.68)),
                fill=(190, 185, 170))
    # phone
    px0, py0 = x0 + int(w * 0.30), y0 + 12
    px1, py1 = x0 + int(w * 0.66), y0 + int(h * 0.86)
    d.rounded_rectangle((px0, py0, px1, py1), radius=8,
                        fill=(30, 32, 40))
    d.rectangle((px0 + 5, py0 + 8, px1 - 5, py1 - 8), fill=(220, 235, 245))
    d.text(((px0 + px1) // 2, (py0 + py1) // 2), "AI", font=f_sans_b(16),
           fill=(40, 90, 170), anchor="mm")
    # gavel leaning on the phone
    gx, gy = x0 + int(w * 0.74), y0 + int(h * 0.60)
    d.line((gx, gy, gx + 26, gy - 26), fill=(120, 85, 40), width=5)
    d.rectangle((gx + 18, gy - 34, gx + 34, gy - 18), fill=(90, 60, 25))


def scene_pharmacy(d, x0, y0, x1, y1):
    """Sanofi deal: a pharmacy front with a green cross and capsules."""
    w, h = x1 - x0, y1 - y0
    d.rectangle((x0, y0, x1, y0 + int(h * 0.45)), fill=(170, 205, 230))
    d.ellipse((x0 + w * 0.78, y0 + 6, x0 + w * 0.78 + 24, y0 + 30),
              fill=(255, 240, 170))
    d.rectangle((x0, y0 + int(h * 0.45), x1, y1), fill=(120, 125, 120))
    # shop front
    bx0, bx1 = x0 + 18, x1 - 18
    d.rectangle((bx0, y0 + int(h * 0.28), bx1, y0 + int(h * 0.78)),
                fill=(245, 243, 235))
    d.rectangle((bx0 + 8, y0 + int(h * 0.52), bx1 - 8, y0 + int(h * 0.74)),
                fill=(150, 200, 230))
    d.line((bx0 + 8, y0 + int(h * 0.52), bx1 - 8, y0 + int(h * 0.52)),
           fill=(120, 120, 115), width=2)
    # green cross sign
    cx, cy = (bx0 + bx1) // 2, y0 + int(h * 0.40)
    d.rectangle((cx - 4, cy - 12, cx + 4, cy + 12), fill=(30, 160, 70))
    d.rectangle((cx - 12, cy - 4, cx + 12, cy + 4), fill=(30, 160, 70))
    # capsules on the pavement
    for kx, col in [(0.16, (200, 60, 60)), (0.30, (60, 90, 200)),
                    (0.72, (200, 60, 60)), (0.86, (60, 90, 200))]:
        px, py = x0 + w * kx, y0 + h * 0.88
        d.ellipse((px - 12, py - 5, px + 12, py + 5), fill=col)
        d.ellipse((px - 12, py - 5, px, py + 5), fill=(245, 245, 240))
    d.text((x0 + w * 0.52, y0 + h * 0.88), "$", font=f_sans_b(13),
           fill=(30, 130, 60), anchor="mm")


CARDS = [
    dict(num=4, region="EU", tag="SPACE THREAT",
         head="NATO vows to defend space after nuclear satellite reports",
         place="BERLIN", scene=scene_satellite),
    dict(num=5, region="EU", tag="WAR TOLL",
         head="700,000 Russian soldiers killed, new tally finds",
         place="RUSSIA-UKRAINE WAR", scene=scene_crosses),
    dict(num=6, region="ME", tag="WARSHIP HIT",
         head="Ukraine claims sinking of Russian warship off Benghazi",
         place="BENGHAZI, LIBYA", scene=scene_warship),
    dict(num=7, region="EU", tag="GENOCIDE RULING",
         head="UK sanctions Myanmar generals after genocide ruling",
         place="LONDON", scene=scene_court),
    dict(num=8, region="TECH", tag="CEO RETURNS",
         head="Nvidia brings back Huang after Trump steps in",
         place="SANTA CLARA, US", scene=scene_chip),
    dict(num=9, region="EU", tag="COP31 FAILS",
         head="Climate summit ends with no deal on fossil fuels",
         place="ANTALYA, TURKEY", scene=scene_summit),
    dict(num=10, region="SCI", tag="EBOLA TRAPPED",
         head="Fighting traps Ebola teams in Ituri",
         place="ITURI, DR CONGO", scene=scene_clinic),
    dict(num=11, region="AP", tag="M5.6 QUAKE",
         head="5.6 quake strikes Nepal near China border",
         place="NEPAL", scene=scene_quake),
    dict(num=12, region="AM", tag="GROK SUED",
         head="States sue Musk firms over Grok images",
         place="US STATES", scene=scene_phone_gavel),
    dict(num=13, region="EU", tag="$41BN DEAL",
         head="Sanofi to buy Insmed for $41bn",
         place="PARIS", scene=scene_pharmacy),
]
CARD_X = [25, 222, 419, 616, 813]
CARD_W = 185
CARD_ROWS = [430, 563]
CARD_H = 130
PIC_H = 69


def draw_card(d, card, x0, y0):
    """One illustrated card: picture with tag, headline, place, badge."""
    x1, y1 = x0 + CARD_W, y0 + CARD_H
    d.rectangle((x0, y0, x1, y1), fill=CARD, outline=INK, width=1)
    card["scene"](d, x0 + 1, y0 + 1, x1 - 1, y0 + PIC_H)
    # repaint the body: scenes must never bleed below the picture
    d.rectangle((x0 + 1, y0 + PIC_H + 1, x1 - 1, y1 - 1), fill=CARD)
    tag_bg = (183, 121, 31) if card["num"] == 13 else RED
    tag_txt = INK if card["num"] == 13 else (255, 255, 255)
    tw = int(f_sans_b(9).getlength(card["tag"])) + 10
    d.rectangle((x0 + 1, y0 + 1, x0 + 1 + tw, y0 + 14), fill=tag_bg)
    d.text((x0 + 6, y0 + 3), card["tag"], font=f_sans_b(9), fill=tag_txt)
    lines = wrap(card["head"], f_lib_b(13), 160)
    text_block(d, x0 + 8, y0 + PIC_H + 7, lines, f_lib_b(13), INK, 13)
    d.text((x0 + 8, y1 - 12), card["place"],
           font=f_sans_b(10), fill=REGION[card["region"]][0])
    number_disc(d, x1 - 12, y1 - 12, 9, card["num"])


# ---------------------------------------------------------------- bottom half

MAP_BOX = (24, 734, 360, 927)          # x0, y0, x1, y1
# v2: top was 724 -- the "pins match story numbers" subline at y=716
# has ink down to y=727, so the sea fill (drawn after the headers)
# overpainted its bottom 3 px. Top 734 leaves a 7 px clear gap
# (727 -> 734) above the box. Bottom stays 921 / 927, DATE CHECK
# top stays 930.
SEA_BOTTOM = 921                # sea ends here; white strip below it


def _mx(lon):
    return MAP_BOX[0] + 2 + (lon + 170) / 360 * (MAP_BOX[2] - MAP_BOX[0] - 4)


def _my(lat):
    return MAP_BOX[1] + (78 - lat) / 138 * (MAP_BOX[3] - MAP_BOX[1])


# Rough continent outlines in lon/lat, drawn freehand to read as a
# world map inside the box. Deliberately simplified -- coastlines are
# approximate, not traced data.
CONTINENTS = [
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 68),
     (-105, 68), (-95, 69), (-85, 66), (-80, 62), (-70, 58), (-60, 55),
     (-55, 52), (-60, 47), (-65, 44), (-70, 42), (-74, 39), (-76, 35),
     (-80, 32), (-81, 27), (-84, 30), (-89, 29), (-94, 29), (-97, 26),
     (-102, 24), (-106, 22), (-110, 24), (-114, 29), (-118, 33),
     (-122, 38), (-124, 44), (-125, 49), (-130, 55), (-138, 58),
     (-148, 60), (-158, 58), (-165, 60), (-168, 66)],
    [(-55, 60), (-45, 60), (-40, 64), (-32, 68), (-22, 70), (-30, 74),
     (-45, 76), (-58, 74), (-60, 68), (-55, 60)],
    [(-79, 9), (-72, 12), (-64, 10), (-57, 6), (-52, 4), (-50, 0),
     (-44, -3), (-38, -5), (-35, -8), (-38, -14), (-40, -21), (-46, -26),
     (-52, -32), (-58, -35), (-65, -41), (-69, -48), (-72, -54),
     (-70, -48), (-71, -38), (-71, -28), (-70, -20), (-74, -15),
     (-79, -8), (-81, -2), (-80, 5), (-79, 9)],
    [(-6, 35), (0, 36), (9, 37), (18, 33), (25, 32), (31, 31), (34, 28),
     (33, 22), (37, 18), (40, 15), (44, 11), (48, 11), (51, 10), (48, 4),
     (43, -2), (40, -8), (38, -15), (35, -20), (32, -26), (28, -32),
     (22, -35), (18, -33), (15, -27), (13, -18), (12, -10), (9, 4),
     (4, 6), (-4, 5), (-8, 4), (-13, 8), (-16, 12), (-17, 18),
     (-16, 25), (-12, 30), (-6, 35)],
    [(-10, 36), (-9, 40), (-9, 43), (-4, 44), (-2, 46), (-4, 48),
     (-1, 50), (3, 51), (5, 53), (8, 55), (8, 57), (12, 56), (18, 55),
     (21, 55), (24, 57), (26, 59), (28, 61), (30, 63), (28, 66),
     (25, 69), (21, 70), (17, 69), (14, 67), (12, 64), (8, 62), (5, 60),
     (5, 58), (1, 55), (-2, 51), (-5, 46), (-8, 41), (-10, 36)],
    [(28, 62), (32, 66), (38, 68), (44, 68), (50, 69), (56, 69),
     (62, 70), (68, 72), (75, 73), (82, 73), (90, 75), (98, 76),
     (106, 76), (114, 74), (122, 73), (130, 72), (138, 72), (146, 71),
     (154, 69), (160, 66), (162, 61), (160, 56), (156, 52), (150, 48),
     (144, 44), (141, 39), (139, 35), (135, 34), (131, 33), (127, 35),
     (126, 38), (122, 39), (120, 33), (118, 28), (114, 23), (110, 20),
     (108, 15), (106, 10), (103, 8), (100, 7), (98, 10), (96, 14),
     (94, 17), (92, 21), (89, 22), (87, 22), (85, 19), (83, 17),
     (81, 13), (80, 9), (78, 8), (76, 10), (74, 14), (72, 19),
     (69, 22), (66, 25), (63, 25), (60, 25), (57, 26), (54, 27),
     (52, 29), (50, 30), (48, 30), (46, 29), (44, 29), (42, 28),
     (40, 30), (38, 31), (36, 35), (34, 36), (32, 38), (30, 40),
     (29, 44), (28, 48), (28, 54), (28, 58), (28, 62)],
    [(113, -22), (114, -28), (115, -33), (118, -35), (122, -34),
     (126, -32), (130, -32), (133, -32), (136, -35), (139, -36),
     (142, -38), (146, -39), (149, -37), (151, -34), (153, -31),
     (153, -27), (150, -23), (147, -19), (144, -15), (142, -11),
     (139, -12), (136, -12), (133, -12), (130, -13), (127, -14),
     (124, -15), (121, -17), (118, -20), (114, -22), (113, -22)],
    [(130, 31), (132, 33), (134, 34), (136, 35), (138, 37), (140, 39),
     (141, 41), (143, 43), (142, 44), (140, 41), (138, 38), (136, 36),
     (133, 34), (131, 32), (130, 31)],
    [(95, 5), (98, 4), (101, 1), (104, -1), (107, -4), (110, -6),
     (113, -8), (116, -9), (119, -9), (122, -8), (125, -8), (128, -6),
     (130, -3), (128, -1), (124, -2), (120, -4), (116, -6), (112, -7),
     (108, -6), (104, -3), (100, 0), (96, 3), (95, 5)],
]

# story number -> (lon, lat, region, dx, dy) for the map pins.
# dx/dy are small pixel nudges off the true lon/lat centre (v2): the
# pin circles are 14 px wide, but the raw centres in the East Med
# were only 8-13 px apart, so circles 3/6/9 touched and overlapped,
# and so did 4/13, 7/13 and 8/12. Nudges below (all <= 10 px, each pin
# stays in its true sea/land area) spread every pair to >= 15 px
# apart; check_map_layout() asserts that for every pair.
PINS = [
    (1, 57, 26, "ME", 0, 0), (2, 35, 48, "EU", 0, 0),
    (3, 34.5, 31.5, "ME", -8, 10), (4, 13.4, 52.5, "EU", 0, 0),
    (5, 44, 58, "EU", 0, 0), (6, 20, 32, "ME", -10, 0),
    (7, -8, 55, "EU", -4, -3), (8, -122, 37.3, "TECH", 0, 2),
    (9, 30.7, 36.9, "EU", 8, 6), (10, 29.5, 1.5, "SCI", 0, 0),
    (11, 85, 28, "AP", 0, 0), (12, -122.5, 45.5, "AM", 0, -8),
    (13, 2.3, 48.9, "EU", -6, 7),
]


def _pin_xy(pin):
    """Pixel centre of a map pin, true lon/lat plus its dx/dy nudge."""
    _num, lon, lat, _region, dx, dy = pin
    return _mx(lon) + dx, _my(lat) + dy


def check_map_layout():
    """v2 guards: map caption clear of the box; no two pins overlap."""
    import math
    probe = ImageDraw.Draw(Image.new("RGB", (PAGE_W, PAGE_H), PAPER))
    sub = probe.textbbox((EDGE, 716), "pins match story numbers",
                         font=f_sans(9))
    gap = MAP_BOX[1] - sub[3]
    print(f"map caption ink bottom y={sub[3]}, box top y={MAP_BOX[1]}, "
          f"gap {gap}px")
    assert gap >= 2, (f"map caption still clipped: ink bottom {sub[3]} "
                      f"only {gap}px above box top {MAP_BOX[1]}")
    centres = {pin[0]: _pin_xy(pin) for pin in PINS}
    worst = (999, None, None)
    for a in centres:
        for b in centres:
            if a < b:
                dist = math.dist(centres[a], centres[b])
                if dist < worst[0]:
                    worst = (dist, a, b)
    print(f"closest pin pair: {worst[1]}-{worst[2]} at {worst[0]:.1f}px")
    assert worst[0] >= 15, (f"pins {worst[1]} and {worst[2]} only "
                            f"{worst[0]:.1f}px apart (need >= 15)")


def draw_map(d):
    """Bright blue sea, light land, region-coloured numbered pins."""
    x0, y0, x1, y1 = MAP_BOX
    d.rectangle((x0 + 1, y0 + 1, x1 - 1, SEA_BOTTOM), fill=SEA)
    d.rectangle((x0 + 1, SEA_BOTTOM + 1, x1 - 1, y1 - 1), fill=CARD)
    for poly in CONTINENTS:
        pts = [(_mx(lon), _my(lat)) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    for pin in PINS:
        num, _lon, _lat, region = pin[:4]
        cx, cy = _pin_xy(pin)
        col = REGION[region][0]
        d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=col,
                  outline=(255, 255, 255), width=1)
        d.text((cx, cy), str(num), font=f_sans_b(8),
               fill=(255, 255, 255), anchor="mm")
    d.rectangle((x0, y0, x1, y1), outline=INK, width=1)


LIST_ITEMS = [
    (14, "EU", "Germany first to get Delta system (Kyiv Ind.)"),
    (15, "EU", "Seven nations back EU Russian visa curbs (Kyiv Ind.)"),
    (16, "EU", "Zelensky urges NATO to admit Ukraine (Kyiv Ind.)"),
    (17, "EU", "Russia warns Estonia moves verge of war (IQMIA)"),
    (18, "EU", "Russian drone violates Polish airspace (Kyiv Ind.)"),
    (19, "ME", "Iraq PM: oil ministry to run Kurdish fields (Reuters)"),
    (20, "ME", "Oxfam: Gaza now a \u2018toxic land\u2019 (Oxfam)"),
    (21, "AP", "Russian jets enter South Korea air zone (AP)"),
    (22, "AP", "Hasina to return 16 Dec; Dhaka: handcuffs (Reuters)"),
    (23, "AP", "Japan to pay full ICC contribution early (Reuters)"),
    (24, "AP", "S. Korea offers $375,000 to catch AI cheats (WSJ)"),
    (25, "AP", "Solomon Islands to end China pact (10Things)"),
    (26, "AP", "Malaysia to return 6,500 Rohingya (Medium)"),
    (27, "AP", "Australia tech fines up to 5% of revenue (Principia)"),
    (28, "AM", "US blacklists Singapore cloud firm (Politico)"),
    (29, "AM", "Pentagon: Canada falling short on defence (AP)"),
    (30, "AM", "US to train Syrian soldiers in demining (Reuters)"),
    (31, "AM", "DOJ admits deporting US citizen (The Hill)"),
    (32, "AM", "Rep. Gomez to resign after ethics finding (NYT)"),
    (33, "AM", "US loses measles elimination status (Principia)"),
    (34, "AM", "Pennsylvania\u2019s ninth measles death (Horizon)"),
    (35, "SCI", "Farthest black hole found, 630m yrs on (Principia)"),
]


def draw_bottom_headers(d):
    d.text((EDGE, 704), "WHERE IT HAPPENED", font=f_sans_b(14), fill=INK)
    d.text((EDGE, 716), "pins match story numbers", font=f_sans(9),
           fill=SOFT)
    d.text((373, 704), "ALSO ON TUESDAY 24 NOVEMBER", font=f_sans_b(14),
           fill=INK)


def draw_list(d):
    """The remaining 22 stories, two columns of 11, one line each."""
    num_fnt, txt_fnt = f_sans_b(11), f_sans(11)
    for i, (num, region, text) in enumerate(LIST_ITEMS):
        col = 0 if i < 11 else 1
        row = i % 11
        nx = 373 if col == 0 else 693
        tx = nx + 20
        y = 726 + row * 18
        d.text((nx, y), str(num), font=num_fnt, fill=REGION[region][0])
        d.text((tx, y), text, font=txt_fnt, fill=INK)


DATE_CHECK = [
    "Wires read on Tuesday 24 November 2026. Every story happened, or was "
    "first reported, on 24 November 2026 \u2014 in any time zone. Left out: "
    "Shenzhen (19 Nov);",
    "COP31 collapse (23 Nov) \u2014 a follow-up; ICJ Rohingya genocide "
    "ruling (Thu 19 Nov); 700,000 tally released (23 Nov); Kerch Bridge "
    "(16\u201317 Nov); FBI hack (20 Nov);",
    "Poland missiles (20 Nov); Alcaraz win (22 Nov); Hormuz blockade first "
    "imposed (13 Apr), reinstated (14 Jul) \u2014 the tanker attacks are "
    "24 Nov; the blockade is not.",
]


def draw_date_check(d):
    """Red-bordered box: red DATE CHECK band left, three lines right."""
    x0, y0, x1, y1 = EDGE, 930, RIGHT, 992
    d.rectangle((x0, y0, x1, y1), fill=CARD, outline=RED, width=2)
    d.rectangle((x0, y0, 139, y1), fill=RED)
    d.text((82, 961), "DATE CHECK", font=f_lib_b(12),
           fill=(255, 255, 255), anchor="mm")
    body_fnt = f_sans(10)
    for i, line in enumerate(DATE_CHECK):
        d.text((150, y0 + 8 + i * 18), line, font=body_fnt, fill=INK)


def draw_footer(d):
    """Sources line left, paper name right; shrink until both fit."""
    left = ("Sources: Reuters, BBC, AP, Kyiv Ind., RFE/RL, IQMIA, UN News, "
            "Oxfam, WSJ, NYT, The Hill, Politico, Horizon, Principia "
            "\u2014 24 Nov 2026")
    right = ("THE WORLD IN ONE DAY \u2014 TUESDAY 24 NOVEMBER 2026 "
             "\u00b7 ONE PAGE")
    for size in (11, 10, 9):
        if (f_sans(size).getlength(left)
                + f_sans_b(size).getlength(right) + 16 <= RIGHT - EDGE):
            break
    d.text((EDGE, 999), left, font=f_sans(size), fill=INK)
    d.text((RIGHT, 999), right, font=f_sans_b(size), fill=INK,
           anchor="ra")


# ---------------------------------------------------------------- assembly

def build():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_headline(img, d)
    draw_numbers(d)
    draw_region_bar(d)
    for hero, (x0, x1) in zip(HEROES, HERO_X):
        draw_hero(d, hero, x0, x1)
    for i, card in enumerate(CARDS):
        draw_card(d, card, CARD_X[i % 5], CARD_ROWS[i // 5])
    draw_bottom_headers(d)
    draw_map(d)
    draw_list(d)
    draw_date_check(d)
    draw_footer(d)
    return img


def report_layout():
    """Print wrap diagnostics so overflow is caught before looking."""
    for hero in HEROES:
        t = wrap(hero["title"], f_sans_b(19), 313 - 20)
        dk = wrap(hero["deck"], f_sans(10), 313 - 20)
        print(f"hero {hero['num']}: title {len(t)} lines, "
              f"deck {len(dk)} lines")
    for card in CARDS:
        lines = wrap(card["head"], f_lib_b(13), 160)
        print(f"card {card['num']}: headline {len(lines)} lines")
    for i, line in enumerate(DATE_CHECK, 1):
        print(f"datecheck L{i}: {f_sans(10).getlength(line):.1f}px")
    for num, _reg, text in LIST_ITEMS:
        print(f"list {num}: {f_sans(11).getlength(text):.1f}px")


if __name__ == "__main__":
    report_layout()
    check_map_layout()
    page = build()
    page.save(OUT)
    print("saved", OUT, page.size, OUT.stat().st_size, "bytes")
