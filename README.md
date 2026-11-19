# World News 19 November 2026

[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Ladangcuan578/news-image-19-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Ladangcuan578/news-image-19-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261119)

An entry for [make.fun's "Sum up 19 November's world news in one image" bounty](https://make.fun/bounty/news-image-20261119): a program that writes one 1024x1024 image summing up the day's world news.

## The image

`entry.png` is a front-page newspaper infographic of Thursday 19 November 2026, drawn by `gen.py` (PIL + DejaVu Sans) from news verified across multiple briefings:

- **Hero — APEC · Shenzhen:** Trump, Xi and Putin meet today in the first-ever trilateral summit at the APEC summit in Shenzhen.
- **Gaming:** Grand Theft Auto VI begins its global rollout — gamers enter Vice City after a 13-year wait.
- **Gaza:** Israel launches a rare ground operation in central Gaza.
- **Ukraine:** the Crimea (Kerch) Bridge is hit again; traffic suspended.
- **U.S. Politics:** Hakeem Jeffries set to be the first African-American Speaker of the House.
- **Europe:** the EU proposes a €45 billion loan for Ukraine.
- **Tech:** Anthropic's record $81.3 billion IPO at $83 a share.
- **Also:** Cyclone Akvan nears India's coast; NASA to confirm Voyager 1 reached one light-day; the ICJ set to rule on Myanmar's Rohingya case; Fed minutes point to more rate hikes; Saudi Arabia says the Gulf danger has passed; Australia sanctions Israeli settlements.

Every headline, date and number comes from the verified facts; the summit is worded as happening today, with no outcome claimed.

## How it runs

`main.ts` (Node 22, standard library only) copies `entry.png` to `/output/entry.png` and self-checks the result: a whole PNG, 1024x1024, at most 1 MiB. Run it locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# entry.png OK: 1024x1024, 150902 bytes
```

`gen.py` is the image generator (PIL, runs on the build machine only); it is not used by the shipped program.
