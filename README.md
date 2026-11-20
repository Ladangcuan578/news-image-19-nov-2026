# World News 19 November 2026

[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Ladangcuan578/news-image-19-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Ladangcuan578/news-image-19-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261119)

An entry for [make.fun's "Sum up 19 November's world news in one image" bounty](https://make.fun/bounty/news-image-20261119): a program that writes one 1024x1024 image summing up the day's world news.

## The image

`entry.png` is a front-page newspaper infographic of Thursday 19 November 2026, drawn by `gen.py` (PIL + DejaVu Sans) from news verified across multiple briefings. v2 was rebuilt on 20 November after the day's two biggest stories reached their outcomes:

- **Hero — APEC · Shenzhen (outcome):** Trump, Xi and Putin met for 90 minutes with no immediate breakthrough; the first-ever trilateral summit ended with a joint Peace Declaration — UN reform, more refined oil, talks on cutting nuclear risks, and a pledge that "a nuclear war cannot be won and must never be fought". The US–China trade truce was extended.
- **ICJ — The Hague (new, large panel):** the International Court of Justice ruled 9–6 that Myanmar committed genocide against the Rohingya in Rakhine in 2017 — ~10,000 killed, widespread sexual violence — the first state ever held responsible for genocide. Judgment final, no appeal; reparations ordered.
- **Gaming:** Grand Theft Auto VI begins its global rollout — gamers enter Vice City after a 13-year wait.
- **Gaza:** Israel launches a rare ground operation in central Gaza.
- **Ukraine:** the Crimea (Kerch) Bridge is hit again; traffic suspended.
- **U.S. Politics:** Hakeem Jeffries set to be the first African-American Speaker of the House.
- **Europe:** the EU proposes a €45 billion loan for Ukraine.
- **Tech:** Anthropic's record $81.3 billion IPO at $83 a share.
- **Also:** Cyclone Akvan nears India's coast; NASA to confirm Voyager 1 reached one light-day; Fed minutes point to more rate hikes; Trump to meet Kim Jong-un "at some point"; Saudi Arabia says the Gulf danger has passed; Australia sanctions Israeli settlements.

Every headline, date and number comes from the verified facts; v1's "meet today" and "ICJ set to rule" wordings are retired now that both outcomes are known.

## How it runs

`main.ts` (Node 22, standard library only) copies `entry.png` to `/output/entry.png` and self-checks the result: a whole PNG, 1024x1024, at most 1 MiB. Run it locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# entry.png OK: 1024x1024, 155510 bytes
```

`gen.py` is the image generator (PIL, runs on the build machine only); it is not used by the shipped program.
