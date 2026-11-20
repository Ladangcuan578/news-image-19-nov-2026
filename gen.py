#!/usr/bin/env python3
"""Generate entry.png v2: a front-page newspaper infographic summing up the
world news of Thursday 19 November 2026. Run: python3 gen.py (writes
entry.png beside this file). All headlines, dates and numbers come from the
verified facts file plus the rebuild brief the main agent prepared on 20 Nov;
nothing is invented.

v2 changes vs v1 (both outcomes were unknown at v1 build time):
- HERO: the Trump-Xi-Putin trilateral summit is no longer "meet today" —
  it happened (~90 minutes, no immediate breakthrough) and ended with a
  joint Peace Declaration plus an extended US-China trade truce.
- NEW full-width ICJ band: the court ruled 19 Nov that Myanmar committed
  genocide against the Rohingya in 2017 — 9-6, the first state ever held
  responsible; judgment final, no appeal.
- The six kept story panels and the bottom strip are unchanged in substance;
  the strip's "ICJ set to rule" line is retired.

Layout is measured, not guessed: every section height is computed from the
actual wrapped line counts at render time and printed, so a text change
that no longer fits is visible immediately instead of silently overflowing.

Revision pass: the first v2 render let the grid's adaptive fit drop panel
bodies to 1 line (cutting every body off mid-sentence) because the hero +
ICJ band + 3-row grid needed ~23 px more than the v1 geometry allowed.
Fixed by shrinking the masthead 118->112, hero headline 44->43 and body
21->20, ICJ body 19->18, panel kicker/padding, row gap 10->8, and moving
the strip 900->908 — bodies now keep their full 2 lines with slack."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 238)
INK = (24, 24, 24)
NAVY = (22, 35, 63)
RED = (166, 30, 34)
RULE = (196, 188, 172)
STRIP_BG = (238, 232, 220)
ICJ_BG = (243, 228, 226)

FDIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


BOLD = "DejaVuSans-Bold.ttf"
REG = "DejaVuSans.ttf"

HERO = {
    "kicker": "APEC  \u00b7  SHENZHEN  \u2014  OUTCOME",
    "headline": "TRUMP, XI AND PUTIN MEET 90 MINUTES \u2014 NO BREAKTHROUGH",
    "body": ("First-ever trilateral summit in Shenzhen ends with a joint "
             "Peace Declaration \u2014 UN reform, more refined oil, talks on "
             "cutting nuclear risks, and a pledge that \u2018a nuclear war "
             "cannot be won and must never be fought\u2019. US\u2013China "
             "trade truce extended."),
}

ICJ = {
    "kicker": "THE HAGUE  \u00b7  ICJ",
    "headline": ("ICJ: MYANMAR COMMITTED GENOCIDE \u2014 9\u20136, "
                 "REPARATIONS ORDERED"),
    "body": ("Myanmar committed genocide against the Rohingya in Rakhine "
             "in 2017 \u2014 ~10,000 killed, widespread sexual violence. "
             "First state ever held responsible; final, no appeal."),
}

PANELS = [
    {"kicker": "GAMING  \u00b7  VICE CITY",
     "headline": "GTA VI ROLLS OUT WORLDWIDE",
     "body": ("After a 13-year wait, GTA VI begins its global rollout "
              "today \u2014 gamers enter Vice City.")},
    {"kicker": "GAZA",
     "headline": "ISRAEL LAUNCHES GROUND OPERATION",
     "body": ("Rare ground operation in central Gaza; displaced families "
              "flee their tents and shelters.")},
    {"kicker": "UKRAINE",
     "headline": "CRIMEA BRIDGE HIT AGAIN",
     "body": ("Traffic across the Kerch Bridge suspended after a new "
              "attack, a day after severe damage.")},
    {"kicker": "U.S. POLITICS",
     "headline": "JEFFRIES SET TO BE FIRST AFRICAN-AMERICAN SPEAKER",
     "body": ("Democrats nominate Hakeem Jeffries for Speaker \u2014 the "
              "first African-American in the post.")},
    {"kicker": "EUROPE",
     "headline": "EU PROPOSES \u20ac45BN UKRAINE LOAN",
     "body": ("European Commission proposes a \u20ac45bn loan for Ukraine, "
              "repaid after Russia pays reparations.")},
    {"kicker": "TECH  \u00b7  MARKETS",
     "headline": "ANTHROPIC'S RECORD $81.3BN IPO",
     "body": ("AI giant debuts at $83 a share in the biggest IPO ever, "
              "raising a record $81.3 billion.")},
]

STRIP = [
    "ALSO:  Cyclone Akvan nears India's coast \u2014 landfall expected "
    "between Machilipatnam and Puri",
    "Voyager 1: NASA to confirm today it reached one light-day from Earth",
    "Fed minutes point to more rate hikes  \u00b7  Trump to meet Kim "
    "Jong-un \u2018at some point\u2019",
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
    d.rectangle([0, 0, W, 112], fill=NAVY)
    draw_center(d, 8, "WORLD NEWS", font(BOLD, 74), (255, 255, 255))
    draw_center(d, 86, "THURSDAY  \u00b7  19 NOVEMBER 2026",
                font(BOLD, 23), (255, 255, 255))
    d.rectangle([0, 112, W, 118], fill=RED)

    # ---- Hero -----------------------------------------------------------
    y = 130
    d.text((margin, y), HERO["kicker"], font=font(BOLD, 25), fill=RED)
    y += 32
    head_f = font(BOLD, 43)
    hero_head = wrap(d, HERO["headline"], head_f, content_w)
    for line in hero_head:
        d.text((margin, y), line, font=head_f, fill=INK)
        y += 51
    y += 2
    body_f = font(REG, 20)
    hero_body = wrap(d, HERO["body"], body_f, content_w)
    for line in hero_body:
        d.text((margin, y), line, font=body_f, fill=INK)
        y += 26
    hero_bottom = y + 8
    d.line([(margin, hero_bottom), (W - margin, hero_bottom)],
           fill=RULE, width=2)

    # ---- ICJ band (full width, tinted) ---------------------------------
    band_top = hero_bottom + 12
    icj_kick_f = font(BOLD, 21)
    icj_head_f = font(BOLD, 24)
    icj_body_f = font(REG, 18)
    icj_head = wrap(d, ICJ["headline"], icj_head_f, content_w)
    icj_body = wrap(d, ICJ["body"], icj_body_f, content_w)
    band_h = 26 + 5 + len(icj_head) * 30 + 5 + len(icj_body) * 23 + 10
    d.rectangle([0, band_top, W, band_top + band_h], fill=ICJ_BG)
    d.line([(0, band_top), (W, band_top)], fill=RED, width=3)
    d.line([(0, band_top + band_h), (W, band_top + band_h)],
           fill=RED, width=3)
    by = band_top + 10
    d.text((margin, by), ICJ["kicker"], font=icj_kick_f, fill=RED)
    by += 26 + 5
    for line in icj_head:
        d.text((margin, by), line, font=icj_head_f, fill=INK)
        by += 30
    by += 5
    for line in icj_body:
        d.text((margin, by), line, font=icj_body_f, fill=INK)
        by += 23
    band_bottom = band_top + band_h

    # ---- Story grid: 2 columns x 3 rows, rows sized to content ---------
    gap_x = 24
    row_gap = 8
    col_w = (content_w - gap_x) // 2
    grid_top = band_bottom + 12
    strip_top = 908  # bottom strip band starts here
    avail = strip_top - grid_top - 8
    kick_f = font(BOLD, 19)
    head_f2 = font(BOLD, 21)
    body_f2 = font(REG, 18)

    def panel_height(panel, max_body_lines):
        lines = wrap(d, panel["headline"], head_f2, col_w)
        body = wrap(d, panel["body"], body_f2, col_w)[:max_body_lines]
        return 22 + 4 + len(lines) * 26 + 4 + len(body) * 22 + 6

    max_body = 2
    while True:
        heights = [panel_height(p, max_body) for p in PANELS]
        rows = [max(heights[i], heights[i + 1]) for i in (0, 2, 4)]
        total = sum(rows) + 2 * row_gap
        if total <= avail or max_body <= 1:
            break
        max_body -= 1

    print("layout: hero_head=%d hero_body=%d hero_bottom=%d "
          "icj_head=%d icj_body=%d band_bottom=%d grid_top=%d "
          "row_heights=%s total=%d avail=%d body_lines=%d"
          % (len(hero_head), len(hero_body), hero_bottom,
             len(icj_head), len(icj_body), band_bottom, grid_top,
             rows, total, avail, max_body))
    if total > avail:
        print("WARNING: grid overflows by %d px" % (total - avail))
    if max_body < 2:
        print("WARNING: panel bodies truncated to %d line(s) — "
              "text will be cut off mid-sentence" % max_body)

    y = grid_top
    for r in range(3):
        rh = rows[r]
        for c in range(2):
            p = PANELS[r * 2 + c]
            x = margin + c * (col_w + gap_x)
            py = y
            d.text((x, py), p["kicker"], font=kick_f, fill=RED)
            py += 22 + 4
            for line in wrap(d, p["headline"], head_f2, col_w):
                d.text((x, py), line, font=head_f2, fill=INK)
                py += 26
            py += 4
            for line in wrap(d, p["body"], body_f2, col_w)[:max_body]:
                d.text((x, py), line, font=body_f2, fill=INK)
                py += 22
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
