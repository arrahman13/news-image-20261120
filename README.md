[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/arrahman13/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/arrahman13/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The World in One Image — Friday, 20 November 2026

An entry for the make.fun bounty [Sum up 20 November's world news in one image](https://make.fun/bounty/news-image-20261120).

The entry is a single 1024 × 1024 PNG drawn as a broadsheet newspaper front
page: one hero story, a stat strip, eight story cards and a late-wires
ticker, all compiled from wire reports of Friday 20 November 2026 and laid
out to stay legible at thumbnail size.

## The day's front page

**Hero — Europe demands a seat at the Ukraine table.** Sidelined at
Shenzhen, Ukraine's allies met in Berlin and closed ranks against any peace
deal cut over their heads: US envoy Jared Kushner floated a NATO-style
Article 5 guarantee for Kyiv, Chancellor Merz attacked the three-power
format, and Putin invited the Europeans to Moscow. As they talked, Russian
missiles and drones struck Kyiv overnight — three people killed, nine
injured, and all three Dnipro bridges closed.

**The eight cards:**

1. **Asia rout deepens the AI sell-off** — the Nikkei fell 4.8%, SoftBank
   plunged 16% and South Korea halted sell orders after the S&P 500's fifth
   straight fall.
2. **COP31 draft drops fossil-fuel exit** — on the final day in Antalya,
   negotiators cut the phase-out call and net-zero dates from the draft.
3. **California subpoenas Nvidia over China chips** — the probe follows
   CEO Jensen Huang's exit; a House panel counts 879,000 US-licensed AI
   chip sales to Chinese firms.
4. **Iraqi forces enter militia stronghold** — Baghdad deploys in Jurf
   al-Sakhar, the Kataib Hezbollah bastion, under a compromise deal.
5. **UK and EU near youth mobility deal** — Friday's Brussels summit is
   set to approve the scheme a decade after the Brexit vote.
6. **Prabowo and Xi talk South China Sea** — Indonesia's president met Xi
   Jinping on Friday on investment and maritime cooperation.
7. **Drone strike kills 10 at gold mine** — the Bajoun mine attack in
   Sudan's South Kordofan; Amnesty wants RSF drone strikes probed.
8. **Shutdown fight looms before Christmas** — Congress faces a funding
   lapse as the Iran war splits lawmakers over spending.

**Late wires:** the Iran war's $48.3bn cost and a burning tanker in
Hormuz · first damage photos of Riyadh's PIF Tower · Trump ousts the US
cyber director · Bukele's third-term bid · Xi–Albanese talks in Shenzhen.

## How it is built

- `build_image.py` draws the front page with PIL from the story data at
  its top, using measured font metrics for wrapping, and writes both
  `entry.png` and a matching `entry.svg` of the same layout.
- `main.py` is the entry program: it copies the committed `entry.png` to
  `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`), byte for byte, so two
  runs always produce the identical file.

## License

MIT — see `LICENSE`.
