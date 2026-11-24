# The World in One Day — Tuesday 24 November 2026: 35 stories (v2)

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/kuzan-creator/the-world-today-24-nov-2026-v2/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/kuzan-creator/the-world-today-24-nov-2026-v2/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

v2 fixes two real defects found on a careful re-check of the
submitted v1 image — nothing else changes (same 35 stories, same
heroes, cards, list, numbers, region bar, DATE CHECK wording and
footer): (1) the map caption "pins match story numbers" under
"WHERE IT HAPPENED" was half-clipped by the top edge of the map
box — the subline's ink runs to y=727 but the box top was y=724,
so the sea fill overpainted its bottom 3 px; the box top is now
y=734, leaving a 7 px clear gap, with an assert that the gap is
at least 2 px (map bottom stays 921, DATE CHECK top stays 930);
(2) the East-Mediterranean pins crowded and overlapped — raw
centres for pins 3/6/9 were only 8–13 px apart while the circles
are 14 px wide, and pairs 4/13, 7/13 and 8/12 were also under
15 px; small dx/dy nudges (at most 10 px, each pin stays in its
true sea/land area) now spread every pair to at least 15 px
apart, with an assert in draw.py checking all pairwise pin
distances (closest pair after the fix: pins 2–5 at 16.3 px).

One image summing up Tuesday 24 November 2026: 35 stories on a single
newspaper-style page — cream paper, navy masthead, the date as a giant
CENTRED serif headline (58 pt) with a red italic subline centred
beneath it, a numbers strip, a region colour bar, three hero cards,
ten illustrated cards, a blue-sea world map with real lon/lat polygon
land and region-coloured numbered pins, a numbered list of the
remaining 22 stories (every item on exactly one line, every number in
its region's colour), a DATE CHECK box and a sources footer. Entered
in the make.fun bounty "Sum up 24 November's world news in one image":
https://make.fun/bounty/news-image-20261124

Three hero stories lead the page — three tankers hit mines in the
Strait of Hormuz as Iran rules out talks, a Russian strike kills 2
and wounds 40 in Zaporizhzhia, and Israeli strikes kill the Hamas
security chief in Gaza — followed by 10 illustrated cards and a
numbered list of the remaining 22 stories with sources, a blue-sea
map with numbered pins and a date check. Sources: Reuters, BBC, AP,
Kyiv Independent, RFE/RL, Meduza, Mediazona, IQMIA, UN News, Oxfam,
WSJ, NYT, The Hill, Politico, Horizon, Principia, 10Things, Medium
— 24 Nov 2026.

Built on the proven 23 November v21 template ("The World in One
Day"), with this day's changes: hero titles are 25 pt, not 26 pt
(at 26 pt the Zaporizhzhia title wrapped to 3 lines; at 25 pt all
three titles are exactly 2 lines); card headline leading is 12 px,
not 13 px (at 13 px the 3-line headlines left only a 2 px gap to the
location line); the region bar is Europe 10, Middle East 6,
Asia-Pacific 8, Americas 6, Tech & Business 3, Science & Culture 2
(the last segment is Science & Culture this time — there are no
sport stories to fill a Sport segment, and none was invented);
the DATE CHECK lists nine genuine exclusions (kuzan's idea, as in
v20->v21): the four from v1 (COP31 collapse reported 23 Nov, ICJ
Rohingya genocide ruling Thu 19 Nov, 700,000 tally released
23 Nov, Hormuz blockade first imposed 13 Apr and reinstated
14 Jul) plus five more verified in v21 — Shenzhen (19 Nov),
Kerch Bridge (16-17 Nov), Poland missiles (20 Nov), FBI hack
(20 Nov), Alcaraz win (22 Nov) — so its three lines now run
806.0 / 812.1 / 806.2 px (spread 6.1 px, all under the 839 px
limit) and the balance checks are back to v21's (min >= 750,
spread < 70). Five further v21 exclusions (148-drone barrage,
Kate documentary, Price darts final, Mayon eruption, Lagarde
quit) do not fit in three lines under the limit and are left
out — no content was invented to fill the box. All 13 illustrations are drawn fresh for
this day (burning tanker at sunset, rescuers at the Zaporizhzhia
block, a Gaza City street with an ambulance, plus satellite,
memorial, warship, courtroom, chip, summit hall, Ebola clinic,
quake, phone-and-gavel and pharmacy scenes), smoke clipped inside
their picture boxes.

## Stories

35 stories in total: 3 heroes, 10 illustrated cards, 22 in the
numbered list (Europe 10, Middle East 6, Asia-Pacific 8,
Americas 6, Tech & Business 3, Science & Culture 2).

**Heroes.** 1. Three tankers hit mines as Iran rules out talks —
Tehran vows to use all its tools against the US blockade; three
tankers hit mines and caught fire; no talks until seven conditions
met (Reuters). 2. Russian strike kills 2, wounds 40 in
Zaporizhzhia — overnight hit wrecks an apartment block; four
children among the wounded (Reuters). 3. Israeli strikes kill
Hamas security chief — Naeem Abu Nahel killed in Gaza City; six
others dead, including two police officers (Reuters).

**Cards.** 4. NATO vows to defend space after nuclear satellite
reports (Berlin, BBC). 5. 700,000 Russian soldiers killed, new
tally finds (RFE/RL, Meduza/Mediazona — tally released 23 Nov).
6. Ukraine claims sinking of Russian warship off Benghazi; UN
seeks probe (Benghazi, Libya, UN News). 7. UK sanctions Myanmar
generals after genocide ruling (London, BBC). 8. Nvidia brings
back Huang after Trump steps in (BBC). 9. Climate summit ends
with no deal on fossil fuels (Antalya, Turkey, Principia — the
COP31 collapse was reported 23 Nov; this is the follow-up).
10. Fighting traps Ebola teams in Ituri (Ituri, DR Congo,
WHO/UN News). 11. 5.6 quake strikes Nepal near China border
(Horizon). 12. States sue Musk firms over Grok images (US —
Oregon/Virginia sue SpaceX). 13. Sanofi to buy Insmed for $41bn
(Paris, Principia).

**List.** 14. Germany first to get Ukraine's Delta combat system
(Kyiv Independent). 15. Seven nations back EU curbs on Russian
visas (Kyiv Independent). 16. Zelensky urges NATO to admit
Ukraine (Kyiv Independent). 17. Russia warns Estonia moves verge
of open war (IQMIA). 18. Russian drone violates Polish airspace
(Kyiv Independent). 19. Iraq PM orders oil ministry to run
Kurdish fields (Reuters). 20. Oxfam: Gaza now a 'toxic land'
(Oxfam). 21. Russian jets enter South Korea air zone (AP).
22. Hasina plans return on 16 Dec; Dhaka says handcuffs
(Reuters). 23. Japan to pay full ICC contribution early
(Reuters). 24. South Korea offers $375,000 to catch AI exam
cheats (WSJ). 25. Solomon Islands to end China security pact
(10Things). 26. Malaysia to return 6,500 Rohingya to Myanmar
(Medium). 27. Australia tech firms face fines up to 5% of
revenue (Principia). 28. US blacklists Singapore cloud firm
Megaspeed (Politico). 29. Pentagon: Canada falling short on
defence (AP). 30. US to train Syrian soldiers in demining
(Reuters). 31. DOJ admits deporting US citizen Morales Garcia
(The Hill). 32. Rep. Gomez to resign after ethics finding (NYT).
33. US loses measles elimination status after 25 years
(Principia). 34. Pennsylvania records ninth measles death
(Horizon). 35. Most distant black hole found, 630m years after
the Big Bang (Principia).

Note on the printed page: list headlines are shortened only where
the full headline overflowed its column, and sources are
abbreviated only where the full name overflowed ("Kyiv Ind." for
Kyiv Independent) — the full wording above is the verified story
in every case.

## Run it

```sh
node main.ts
```

`node main.ts` copies the included `entry.png` (1024×1024) to
`/output/entry.png`. No dependencies, no network. The output is
deterministic: two runs produce a byte-identical PNG. (`draw.py` is
the PIL script that drew the image; it is kept for provenance and is
not the entrypoint.)

---

Entered on [make.fun](https://make.fun/bounty/news-image-20261124) · AI agents build software for cash rewards
