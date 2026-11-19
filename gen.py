#!/usr/bin/env python3
"""Generate entry.png: a front-page newspaper infographic summing up the world
news of Thursday 19 November 2026. Run: python3 gen.py (writes entry.png
beside this file). All headlines, dates and numbers come from the verified
facts file the main agent researched; nothing is invented. The trilateral
summit is worded as happening TODAY (it had not happened at research time),
never as an outcome.

Revision pass: the first render cut every panel body off mid-sentence (the
adaptive fit had dropped bodies to 2 lines). Fixed by shortening the hero
body to two lines so all three body lines fit in every panel, adding a fourth
bottom-strip line for completeness, and tightening row spacing for slack."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 238)
INK = (24, 24, 24)
NAVY = (22, 35, 63)
RED = (166, 30, 34)
RULE = (196, 188, 172)
STRIP_BG = (238, 232, 220)

FDIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


BOLD = "DejaVuSans-Bold.ttf"
REG = "DejaVuSans.ttf"

HERO = {
    "kicker": "APEC  ·  SHENZHEN",
    "headline": "TRUMP, XI AND PUTIN MEET TODAY",
    "body": ("First-ever trilateral summit at the APEC summit in Shenzhen "
             "\u2014 after Xi and Putin met on Wednesday, the three leaders "
             "sit down together today."),
}

PANELS = [
    {"kicker": "GAMING  ·  VICE CITY",
     "headline": "GTA VI ROLLS OUT WORLDWIDE",
     "body": ("After a 13-year wait, Grand Theft Auto VI begins its global "
              "rollout today \u2014 gamers enter Vice City.")},
    {"kicker": "GAZA",
     "headline": "ISRAEL LAUNCHES GROUND OPERATION",
     "body": ("Rare ground operation in central Gaza, in an area left under a "
              "ceasefire; displaced families flee their tents.")},
    {"kicker": "UKRAINE",
     "headline": "CRIMEA BRIDGE HIT AGAIN",
     "body": ("Traffic across the Kerch Bridge suspended after a new attack, "
              "a day after severe damage to the supply route.")},
    {"kicker": "U.S. POLITICS",
     "headline": "JEFFRIES SET TO BE FIRST AFRICAN-AMERICAN SPEAKER",
     "body": ("Democrats nominate Hakeem Jeffries for Speaker of the House "
              "\u2014 the first African-American to hold the post.")},
    {"kicker": "EUROPE",
     "headline": "EU PROPOSES \u20ac45BN UKRAINE LOAN",
     "body": ("European Commission proposes a \u20ac45 billion loan for "
              "Ukraine's budget, to be repaid after Russia pays reparations.")},
    {"kicker": "TECH  ·  MARKETS",
     "headline": "ANTHROPIC'S RECORD $81.3BN IPO",
     "body": ("AI giant debuts at $83 a share in the biggest IPO of all time, "
              "raising a record $81.3 billion.")},
]

STRIP = [
    "ALSO:  Cyclone Akvan nears India's coast \u2014 landfall expected "
    "between Machilipatnam and Puri",
    "Voyager 1: NASA to confirm today it reached one light-day from Earth",
    "ICJ set to rule on Myanmar's Rohingya case  \u00b7  Fed minutes point "
    "to more rate hikes",
    "Saudi Arabia says the Gulf danger has passed  \u00b7  Australia "
    "sanctions Israeli settlements",
]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, y, text, fnt, fill, x0=0, x1=W):
    draw.text(((x0 + x1 - draw.textlength(text, font=fnt)) / 2, y),
              text, font=fnt, fill=fill)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    margin = 32
    content_w = W - 2 * margin

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    draw_center(d, 10, "WORLD NEWS", font(BOLD, 78), (255, 255, 255))
    draw_center(d, 92, "THURSDAY  \u00b7  19 NOVEMBER 2026",
                font(BOLD, 24), (255, 255, 255))
    d.rectangle([0, 118, W, 124], fill=RED)

    # ---- Hero -----------------------------------------------------------
    y = 136
    d.text((margin, y), HERO["kicker"], font=font(BOLD, 25), fill=RED)
    y += 32
    head_f = font(BOLD, 47)
    for line in wrap(d, HERO["headline"], head_f, content_w):
        d.text((margin, y), line, font=head_f, fill=INK)
        y += 56
    y += 2
    body_f = font(REG, 25)
    for line in wrap(d, HERO["body"], body_f, content_w):
        d.text((margin, y), line, font=body_f, fill=INK)
        y += 31
    hero_bottom = y + 8
    d.line([(margin, hero_bottom), (W - margin, hero_bottom)],
           fill=RULE, width=2)

    # ---- Story grid: 2 columns x 3 rows, rows sized to content ---------
    gap_x = 24
    row_gap = 10
    col_w = (content_w - gap_x) // 2
    grid_top = hero_bottom + 14
    strip_top = 896  # bottom strip band starts here
    avail = strip_top - grid_top - 8
    kick_f = font(BOLD, 21)
    head_f2 = font(BOLD, 27)
    body_f2 = font(REG, 21)

    def panel_height(panel, max_body_lines):
        lines = wrap(d, panel["headline"], head_f2, col_w)
        body = wrap(d, panel["body"], body_f2, col_w)[:max_body_lines]
        return 25 + 6 + len(lines) * 32 + 6 + len(body) * 24 + 10

    max_body = 3
    while True:
        heights = [panel_height(p, max_body) for p in PANELS]
        rows = [max(heights[i], heights[i + 1]) for i in (0, 2, 4)]
        total = sum(rows) + 2 * row_gap
        if total <= avail or max_body <= 2:
            break
        max_body -= 1

    print("layout: hero_bottom=%d grid_top=%d row_heights=%s total=%d "
          "avail=%d body_lines=%d" % (hero_bottom, grid_top, rows, total,
                                      avail, max_body))

    y = grid_top
    for r in range(3):
        rh = rows[r]
        for c in range(2):
            p = PANELS[r * 2 + c]
            x = margin + c * (col_w + gap_x)
            py = y
            d.text((x, py), p["kicker"], font=kick_f, fill=RED)
            py += 25 + 6
            for line in wrap(d, p["headline"], head_f2, col_w):
                d.text((x, py), line, font=head_f2, fill=INK)
                py += 32
            py += 6
            for line in wrap(d, p["body"], body_f2, col_w)[:max_body]:
                d.text((x, py), line, font=body_f2, fill=INK)
                py += 24
        # vertical divider between columns
        d.line([(margin + col_w + gap_x // 2, y + 2),
                (margin + col_w + gap_x // 2, y + rh - 4)],
               fill=RULE, width=2)
        if r < 2:
            d.line([(margin, y + rh + row_gap // 2),
                    (W - margin, y + rh + row_gap // 2)],
                   fill=RULE, width=2)
        y += rh + row_gap

    # ---- Bottom strip ---------------------------------------------------
    d.rectangle([0, strip_top, W, H], fill=STRIP_BG)
    d.line([(0, strip_top), (W, strip_top)], fill=RULE, width=2)
    strip_f = font(REG, 20)
    sy = strip_top + 11
    for line in STRIP:
        draw_center(d, sy, line, strip_f, INK)
        sy += 25
    d.rectangle([0, H - 6, W, H], fill=NAVY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
