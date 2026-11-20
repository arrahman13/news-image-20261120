#!/usr/bin/env python3
"""Build the front page for Friday 20 November 2026.

Draws a broadsheet-style newspaper front page at 1024 x 1024 with PIL,
recording every drawing operation so the same layout is also written
out as entry.svg. Deterministic: no clocks, no randomness, no network.

Stories were compiled on the evening of 20 November 2026 (Asia time)
from wire reporting of that day: Reuters, AP, BBC, France 24, CNBC,
Al Jazeera, the Japan Times, CBC and AllAfrica.
"""

from PIL import Image, ImageDraw, ImageFont

W = 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952 px of content width

PAPER = (248, 244, 233)
INK = (25, 21, 18)
MUTED = (92, 85, 70)
RED = (158, 27, 27)
NAVY = (31, 58, 95)
GOLD = (176, 132, 28)
CARD_BG = (253, 251, 245)
HAIRLINE = (196, 188, 168)
DUSK = (32, 48, 60)
RIVER = (51, 86, 107)
BRIDGE = (214, 205, 182)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(kind, size):
    name = {
        "serif": "DejaVuSerif.ttf",
        "serif_b": "DejaVuSerif-Bold.ttf",
        "sans": "DejaVuSans.ttf",
        "sans_b": "DejaVuSans-Bold.ttf",
    }[kind]
    return ImageFont.truetype(FONT_DIR + name, size)


def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)


def wrap(draw, s, fnt, width):
    """Greedy word wrap against real font metrics."""
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- stories

HERO_KICKER = "UKRAINE WAR · BERLIN AND KYIV · THE DAY AFTER SHENZHEN"
HERO_HEADLINE = ["EUROPE DEMANDS A SEAT", "AT THE UKRAINE TABLE"]
HERO_DECK = (
    "Left out at Shenzhen, Ukraine's allies met in Berlin and closed ranks "
    "against any peace deal cut over their heads. US envoy Jared Kushner "
    "floated a NATO-style Article 5 guarantee for Kyiv, Merz attacked the "
    "three-power format, and Putin invited the Europeans to Moscow. As "
    "they talked, Russian missiles struck Kyiv overnight: three killed, "
    "nine injured, all three Dnipro bridges closed."
)

STATS = [
    ("3", "killed in Kyiv overnight"),
    ("3", "Dnipro bridges closed"),
    ("11", "nations drilling in Poland"),
]

CARDS = [
    {
        "tag": "MARKETS · TOKYO",
        "color": NAVY,
        "headline": "Asia rout deepens the AI sell-off",
        "body": (
            "The Nikkei fell 4.8% and SoftBank plunged 16% as the AI rout "
            "spread from Wall Street, where the S&P 500 fell 2% for a "
            "fifth straight day."
        ),
    },
    {
        "tag": "CLIMATE · ANTALYA",
        "color": (30, 110, 76),
        "headline": "COP31 draft drops fossil-fuel exit",
        "body": (
            "On the final day in Antalya, negotiators cut the fossil-fuel "
            "phase-out call and the net-zero dates from the draft. Pacific "
            "nations demanded both back."
        ),
    },
    {
        "tag": "TECHNOLOGY · CALIFORNIA",
        "color": (110, 60, 140),
        "headline": "California subpoenas Nvidia over China chips",
        "body": (
            "The probe follows CEO Jensen Huang's exit. A House panel says "
            "US licences approved 879,000 AI chip sales to China."
        ),
    },
    {
        "tag": "MIDDLE EAST · IRAQ",
        "color": (150, 96, 20),
        "headline": "Iraqi forces enter militia stronghold",
        "body": (
            "Baghdad's forces will deploy in Jurf al-Sakhar, bastion of "
            "Iran-backed Kataib Hezbollah, under a compromise to calm "
            "tensions."
        ),
    },
    {
        "tag": "BRITAIN–EU · BRUSSELS",
        "color": (24, 96, 128),
        "headline": "UK and EU near youth mobility deal",
        "body": (
            "Friday's Brussels summit is set to approve a youth mobility "
            "scheme, with food trade and carbon deals also on the table."
        ),
    },
    {
        "tag": "ASIA · SHENZHEN",
        "color": (178, 44, 44),
        "headline": "Prabowo and Xi talk South China Sea",
        "body": (
            "Indonesia's president met Xi Jinping on Friday to discuss "
            "investment and South China Sea cooperation."
        ),
    },
    {
        "tag": "AFRICA · SUDAN",
        "color": (128, 84, 24),
        "headline": "Drone strike kills 10 at gold mine",
        "body": (
            "A strike on the Bajoun mine in South Kordofan killed at least "
            "10. Amnesty wants RSF drone attacks on civilians probed as "
            "war crimes."
        ),
    },
    {
        "tag": "UNITED STATES · WASHINGTON",
        "color": (70, 70, 120),
        "headline": "Shutdown fight looms before Christmas",
        "body": (
            "Congress faces a pre-Christmas government shutdown as the war "
            "in Iran splits lawmakers over federal spending."
        ),
    },
]

WIRES = [
    ("IRAN WAR", "cost put at $48.3bn; a tanker is ablaze after hitting a mine in Hormuz"),
    ("RIYADH", "first damage photos of the PIF Tower hit on Thursday; no injuries"),
    ("WASHINGTON", "Trump ousts the US cyber director amid outage criticism"),
    ("SAN SALVADOR", "President Bukele launches his bid for a third term"),
    ("SHENZHEN", "Xi urges trust-based ties in talks with Australia's Albanese"),
]

FOOTER = (
    "Compiled from Reuters, AP, BBC, France 24, CNBC, Al Jazeera, the "
    "Japan Times, CBC and AllAfrica reports of Friday 20 November 2026"
)


# ---------------------------------------------------------------- drawing

SVG_FONT = {
    "serif": ("Georgia, 'Times New Roman', serif", "normal"),
    "serif_b": ("Georgia, 'Times New Roman', serif", "bold"),
    "sans": ("Helvetica, Arial, sans-serif", "normal"),
    "sans_b": ("Helvetica, Arial, sans-serif", "bold"),
}


def hexcol(c):
    return "#%02x%02x%02x" % c


class Page:
    """Records draw ops once, renders them to both PIL and SVG."""

    def __init__(self):
        self.img = Image.new("RGB", (W, W), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.svg = []

    def rect(self, x, y, w, h, fill=None, outline=None, width=1):
        self.d.rectangle([x, y, x + w, y + h], fill=fill, outline=outline,
                         width=width)
        s = f'x="{x}" y="{y}" width="{w}" height="{h}"'
        if fill:
            s += f' fill="{hexcol(fill)}"'
        if outline:
            s += f' stroke="{hexcol(outline)}" stroke-width="{width}"'
        self.svg.append(f"<rect {s}/>")

    def line(self, x1, y1, x2, y2, fill=INK, width=1):
        self.d.line([x1, y1, x2, y2], fill=fill, width=width)
        self.svg.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{hexcol(fill)}" stroke-width="{width}"/>')

    def poly(self, pts, fill):
        self.d.polygon(pts, fill=fill)
        p = " ".join(f"{x},{y}" for x, y in pts)
        self.svg.append(f'<polygon points="{p}" fill="{hexcol(fill)}"/>')

    def text(self, x, y, s, kind, size, fill=INK, anchor="la"):
        fnt = font(kind, size)
        self.d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)
        fam, weight = SVG_FONT[kind]
        anch = {"la": "start", "ma": "middle", "ra": "end"}[anchor[0] + "a"]
        # PIL's default anchor sits on the ascender line; SVG needs a
        # baseline, so shift down by roughly the ascent.
        base = y + int(size * 0.82)
        esc = (s.replace("&", "&amp;").replace("<", "&lt;")
               .replace(">", "&gt;"))
        self.svg.append(
            f'<text x="{x}" y="{base}" font-family="{fam}" '
            f'font-size="{size}" font-weight="{weight}" fill="{hexcol(fill)}" '
            f'text-anchor="{anch}">{esc}</text>')

    def centered(self, cx, y, s, kind, size, fill=INK):
        self.text(cx, y, s, kind, size, fill, anchor="ma")


def draw_bridge_band(pg, x, y, w, h):
    """A dusk strip: skyline, a river, and three bridge spans."""
    pg.rect(x, y, w, h, fill=DUSK)
    # skyline silhouettes along the top of the band
    towers = [(0, 16, 10), (26, 24, 8), (52, 13, 12), (84, 20, 9),
              (120, 28, 7), (170, 15, 11), (230, 22, 8), (300, 12, 13),
              (380, 19, 9), (470, 26, 8), (560, 14, 12), (650, 21, 9),
              (740, 16, 10), (830, 25, 8)]
    base = y + h - 16
    for tx, th, tw in towers:
        if tx + tw <= w:
            pg.rect(x + tx, base - th, tw, th, fill=(16, 24, 30))
    # river
    pg.rect(x, base, w, 16, fill=RIVER)
    # three bridge decks with piers; the middle one is shut
    span = w // 3
    for i in range(3):
        sx = x + i * span + 14
        ex = x + (i + 1) * span - 14
        col = BRIDGE if i != 1 else RED
        pg.line(sx, base - 6, ex, base - 6, fill=col, width=3)
        pg.line(sx + 8, base - 6, sx + 8, base + 8, fill=col, width=2)
        pg.line(ex - 8, base - 6, ex - 8, base + 8, fill=col, width=2)
        pg.line(sx, base - 6, (sx + ex) // 2, base - 20, fill=col, width=1)
        pg.line((sx + ex) // 2, base - 20, ex, base - 6, fill=col, width=1)


def build():
    pg = Page()
    d = pg.d

    # --- masthead ------------------------------------------------------
    pg.line(MARGIN, 26, W - MARGIN, 26, fill=INK, width=3)
    pg.centered(W // 2, 36, "THE WORLD IN ONE IMAGE", "serif_b", 58)
    pg.line(MARGIN, 106, W - MARGIN, 106, fill=INK, width=1)
    pg.rect(MARGIN, 114, CW, 38, fill=INK)
    pg.text(MARGIN + 14, 123, "ONE DAY · ONE IMAGE", "sans_b", 13,
            fill=(214, 205, 182))
    pg.centered(W // 2, 118, "FRIDAY 20 NOVEMBER 2026", "sans_b", 25,
                fill=(255, 255, 255))
    pg.text(W - MARGIN - 14, 123, "FROM THE WIRE REPORTS", "sans_b", 13,
            fill=(214, 205, 182), anchor="ra")

    # --- hero ----------------------------------------------------------
    hy, hh = 166, 348
    pg.rect(MARGIN, hy, CW, hh, outline=INK, width=2)
    pg.text(MARGIN + 18, hy + 14, HERO_KICKER, "sans_b", 15, fill=RED)
    hsize = 50
    while text_w(d, HERO_HEADLINE[0], font("serif_b", hsize)) > CW - 36:
        hsize -= 1
    yy = hy + 42
    for ln in HERO_HEADLINE:
        pg.text(MARGIN + 18, yy, ln, "serif_b", hsize)
        yy += hsize + 8
    deck_f = font("serif", 17)
    yy += 2
    for ln in wrap(d, HERO_DECK, deck_f, CW - 36):
        pg.text(MARGIN + 18, yy, ln, "serif", 17)
        yy += 23
    draw_bridge_band(pg, MARGIN + 18, hy + hh - 56, CW - 36, 38)

    # --- stat strip ------------------------------------------------------
    sy = hy + hh + 10
    colw = CW // 3
    for i, (num, label) in enumerate(STATS):
        cx = MARGIN + i * colw
        pg.text(cx + 6, sy, num, "serif_b", 34, fill=RED)
        nw = text_w(d, num, font("serif_b", 34))
        pg.text(cx + 14 + nw, sy + 12, label.upper(), "sans_b", 13,
                fill=MUTED)
    pg.line(MARGIN, sy + 44, W - MARGIN, sy + 44, fill=HAIRLINE, width=1)

    # --- story cards -----------------------------------------------------
    gy = sy + 56
    gap = 10
    cardw = (CW - 3 * gap) // 4
    cardh = 168
    for idx, card in enumerate(CARDS):
        cx = MARGIN + (idx % 4) * (cardw + gap)
        cy = gy + (idx // 4) * (cardh + gap)
        pg.rect(cx, cy, cardw, cardh, fill=CARD_BG, outline=HAIRLINE,
                width=1)
        pg.rect(cx, cy, cardw, 5, fill=card["color"])
        pg.text(cx + 11, cy + 13, card["tag"], "sans_b", 11,
                fill=card["color"])
        head_lines = wrap(d, card["headline"], font("serif_b", 19),
                          cardw - 22)
        body_lines = wrap(d, card["body"], font("sans", 12), cardw - 22)
        bottom = 32 + 23 * len(head_lines) + 3 + 16 * (len(body_lines) - 1) + 12
        if bottom > cardh - 4:
            print(f"WARNING: card {card['tag']} overflows "
                  f"({bottom} > {cardh - 4})")
        ty = cy + 32
        for ln in head_lines:
            pg.text(cx + 11, ty, ln, "serif_b", 19)
            ty += 23
        ty += 3
        for ln in body_lines:
            pg.text(cx + 11, ty, ln, "sans", 12, fill=(52, 47, 40))
            ty += 16

    # --- late wires ------------------------------------------------------
    wy = gy + 2 * cardh + gap + 14
    pg.rect(MARGIN, wy, CW, 56, fill=INK)
    wire_text = "  ◆  ".join(f"{k}: {v}" for k, v in WIRES)
    lines = wrap(d, wire_text, font("sans", 12), CW - 150)
    pg.text(MARGIN + 14, wy + 10, "LATE", "sans_b", 15, fill=GOLD)
    pg.text(MARGIN + 14, wy + 30, "WIRES", "sans_b", 15, fill=GOLD)
    ly = wy + 8
    for ln in lines[:3]:
        pg.text(MARGIN + 84, ly, ln, "sans", 12, fill=(240, 236, 224))
        ly += 16

    # --- footer ----------------------------------------------------------
    pg.centered(W // 2, wy + 66, FOOTER + " · One image, one day",
                "sans", 11, fill=MUTED)

    return pg


def main():
    pg = build()
    pg.img.save("entry.png", optimize=True)
    head = ('<svg xmlns="http://www.w3.org/2000/svg" width="1024" '
            'height="1024" viewBox="0 0 1024 1024">\n'
            f'<rect width="1024" height="1024" fill="{hexcol(PAPER)}"/>\n')
    with open("entry.svg", "w", encoding="utf-8") as fh:
        fh.write(head + "\n".join(pg.svg) + "\n</svg>\n")
    print("wrote entry.png and entry.svg")


if __name__ == "__main__":
    main()
