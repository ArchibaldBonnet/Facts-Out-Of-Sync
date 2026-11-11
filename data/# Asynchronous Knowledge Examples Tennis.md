# Asynchronous Knowledge Examples (Tennis Ecosystem)

### Example 0 — Wimbledon 2026 Men's Singles Final: Jannik Sinner

| Source | Timestamp (UTC)    | Verified change                                                                                     |
|--------|--------------------|-----------------------------------------------------------------------------------------------------|
| **Table**  | 12 Jul 2026, 18:56 | [Final set cells completed the bracket: Sinner beat Zverev 6–7, 7–6, 6–3, 6–4.](https://en.wikipedia.org/w/index.php?diff=1363830828&oldid=1363825275&title=2026_Wimbledon_Championships_%E2%80%93_Men%27s_singles)                       |
| **Text**   | 12 Jul 2026, 19:00 | [Article text explicitly says Jannik Sinner defeated Alexander Zverev in the final to win the title.](https://en.wikipedia.org/w/index.php?diff=1363831183&oldid=1363830994&title=2026_Wimbledon_Championships_%E2%80%93_Men%27s_singles) |
| **KG**     | 12 Jul 2026, 19:12 | [P1346 (winner) = Jannik Sinner; no qualifiers; winner identity only, not the set score.](https://www.wikidata.org/w/index.php?diff=prev&oldid=2516735987&title=Q135443559)             |

**Timeline**

TABLE (18:56) ── **4 min** ──▶ TEXT (19:00) ── **12 min** ──▶ KG (19:12)

**Total table → KG gap:** 16 minutes.

**Description.** At 18:56 UTC on 12 July 2026, the article’s **table** completed the score for Jannik Sinner’s win over Alexander Zverev, 6–7, 7–6, 6–3, 6–4 [e0-1](https://en.wikipedia.org/w/index.php?diff=1363830828&oldid=1363825275&title=2026_Wimbledon_Championships_%E2%80%93_Men%27s_singles). At 19:00, the article’s **text** said Sinner had defeated Zverev in the final to win the title [e0-2](https://en.wikipedia.org/w/index.php?diff=1363831183&oldid=1363830994&title=2026_Wimbledon_Championships_%E2%80%93_Men%27s_singles). At 19:12, the **Wikidata KG** added winner (P1346) = Jannik Sinner, with no score qualifier [e0-3](https://www.wikidata.org/w/index.php?diff=prev&oldid=2516735987&title=Q135443559).

**Status by stage**
 
| Stage | Timestamp (UTC) | Text | Table | KG |
|-------|-----------------|------|-------|----|
| 0 — Before first update | Before 18:56 | `EMPTY` | `EMPTY` | `EMPTY` |
| 1 — Table update | 12 Jul 2026, 18:56 | `EMPTY` | `UP_TO_DATE` | `EMPTY` |
| 2 — Text update | 12 Jul 2026, 19:00 | `UP_TO_DATE` | `UP_TO_DATE` | `EMPTY` |
| 3 — KG update | 12 Jul 2026, 19:12 | `UP_TO_DATE` | `UP_TO_DATE` | `UP_TO_DATE` |
 
---

### Example 1 — Wimbledon 2024 Prize Money (£50 Million)

| Source | Timestamp (UTC)    | Verified change                                                                 |
|--------|--------------------|---------------------------------------------------------------------------------|
| **Text**   | 13 Jun 2024, 18:53 | [Added text stating the 2024 total prize money was £50,000,000.](https://en.wikipedia.org/w/index.php?diff=1228882896&oldid=1228592214&title=2024+Wimbledon+Championships)                  |
| **KG**     | 30 Jun 2024, 00:05 | [P2121 (prize money) = £50,000,000 (GBP); no qualifiers.](https://www.wikidata.org/w/index.php?diff=prev&oldid=2191692104&title=Q121046430)                         |
| **Table**  | 7 Jun 2025, 02:04  | [The actual prize-money table gained a 2024 row ending with a £50,000,000 total.](https://en.wikipedia.org/w/index.php?diff=1294327380&oldid=1292390294&title=Wimbledon+Championships) |

**Timeline**

TEXT (13 Jun 2024, 18:53) ── **16d 5h 12m** ──▶ KG (30 Jun, 00:05) ── **342d 1h 59m** ──▶ TABLE (7 Jun 2025, 02:04)

**Total text → table gap:** 358 days, 7 hours, 11 minutes.

**Description.** At 18:53 UTC on 13 June 2024, the article’s **text** stated that Wimbledon’s 2024 total prize money was £50 million [e1-1](https://en.wikipedia.org/w/index.php?diff=1228882896&oldid=1228592214&title=2024+Wimbledon+Championships). At 00:05 UTC on 30 June, the **Wikidata KG** added prize money (P2121) = £50,000,000 in GBP, with no qualifiers [e1-2](https://www.wikidata.org/w/index.php?diff=prev&oldid=2191692104&title=Q121046430). On 7 June 2025 at 02:04 UTC, the actual **table** added a 2024 row showing the same total [e1-3](https://en.wikipedia.org/w/index.php?diff=1294327380&oldid=1292390294&title=Wimbledon+Championships).

**Status by stage**
 
| Stage | Timestamp (UTC) | Text | Table | KG |
|-------|-----------------|------|-------|----|
| 0 — Before first update | Before 13 Jun 2024, 18:53 | `EMPTY` | `EMPTY` | `EMPTY` |
| 1 — Text update | 13 Jun 2024, 18:53 | `UP_TO_DATE` | `EMPTY` | `EMPTY` |
| 2 — KG update | 30 Jun 2024, 00:05 | `UP_TO_DATE` | `EMPTY` | `UP_TO_DATE` |
| 3 — Table update | 7 Jun 2025, 02:04 | `UP_TO_DATE` | `UP_TO_DATE` | `UP_TO_DATE` |

---

### Example 2 — 2024 French Open Men's Singles Final: Carlos Alcaraz (Match Result)

| Source | Timestamp (UTC)    | Verified change                                                                                     |
|--------|--------------------|-----------------------------------------------------------------------------------------------------|
| **Table**  | 9 Jun 2024, 17:31  | [Final set score added to the tournament bracket: Alcaraz beat Zverev 6–3, 2–6, 5–7, 6–1, 6–2.](https://en.wikipedia.org/w/index.php?title=2024_French_Open_–_Men%27s_singles&diff=next&oldid=1228130514) |
| **Text**   | 9 Jun 2024, 17:31  | [Prose updated in the lead paragraph stating Carlos Alcaraz won the title over Alexander Zverev.](https://en.wikipedia.org/w/index.php?title=2024_French_Open_–_Men%27s_singles&diff=next&oldid=1228139843) |
| **KG**     | 9 Jun 2024, 19:22  | [P1346 (winner) = Carlos Alcaraz (Q85518537) added to the tournament entity (Q119056221).](https://www.wikidata.org/w/index.php?title=Q119056221&diff=prev&oldid=2175226479) |

**Timeline**

TABLE (17:31) ── **0 min** ──▶ TEXT (17:31) ── **1h 51m** ──▶ KG (19:22)

**Total table → KG gap:** 1 hour, 51 minutes.

**Description.** At 17:31 UTC on 9 June 2024, the article’s **table** added the final set score to the tournament bracket for Carlos Alcaraz’s win over Alexander Zverev, 6–3, 2–6, 5–7, 6–1, 6–2 [e2-1](https://en.wikipedia.org/w/index.php?title=2024_French_Open_–_Men%27s_singles&diff=next&oldid=1228130514). Within the same minute at 17:31 UTC, the article’s **text** was updated in the lead paragraph to state that Carlos Alcaraz won the title over Alexander Zverev [e2-2](https://en.wikipedia.org/w/index.php?title=2024_French_Open_–_Men%27s_singles&diff=next&oldid=1228139843). At 19:22 UTC, the **Wikidata KG** added winner (P1346) = Carlos Alcaraz (Q85518537) to the tournament entity (Q119056221) [e2-3](https://www.wikidata.org/w/index.php?title=Q119056221&diff=prev&oldid=2175226479).

**Status by stage**
 
| Stage | Timestamp (UTC) | Text | Table | KG |
|-------|-----------------|------|-------|----|
| 0 — Before first update | Before 9 Jun 2024, 17:31 | `EMPTY` | `EMPTY` | `EMPTY` |
| 1 — Table + Text update | 9 Jun 2024, 17:31 | `UP_TO_DATE` | `UP_TO_DATE` | `EMPTY` |
| 2 — KG update | 9 Jun 2024, 19:22 | `UP_TO_DATE` | `UP_TO_DATE` | `UP_TO_DATE` |

---

### Example 3 — 2024 US Open Men's Singles Final: Jannik Sinner (Match Result & Erroneous Score Revert)

| Source | Timestamp (UTC) | Verified change |
|--------|-----------------|-----------------|
| **Text + Table** | 8 Sep 2024, 20:32 | [Wikipedia prose and infobox/bracket table simultaneously updated stating Sinner defeated Taylor Fritz to claim the title.](https://en.wikipedia.org/w/index.php?title=2024_US_Open_–_Men%27s_singles&diff=next&oldid=1244719958) |
| **KG** | 9 Sep 2024, 19:28 | [P1346 (winner) = Jannik Sinner (Q54812588) added to the US Open entity (Q121872692).](https://www.wikidata.org/w/index.php?title=Q121872692&diff=prev&oldid=2245951608) |

**Timeline**

 TEXT + TABLE (8 Sep, 20:32) ── **22h 56m** ──▶ KG (9 Sep, 19:28)

**Total text/table → KG gap:** 22 hours, 56 minutes.

**Description.** Following match point at 20:32 UTC, both the article’s **text** and **table** (`| champion =` field and RD4 bracket) were updated to state that Jannik Sinner defeated Taylor Fritz in straight sets [e3-1](https://en.wikipedia.org/w/index.php?title=2024_US_Open_–_Men%27s_singles&diff=next&oldid=1244719958). Nearly a day later, on 9 September 2024 at 19:28 UTC, the **Wikidata KG** added winner (P1346) = Jannik Sinner (Q54812588) to the US Open entity (Q121872692) [e3-2](https://www.wikidata.org/w/index.php?title=Q121872692&diff=prev&oldid=2245951608).

**Status by stage**

| Stage | Timestamp (UTC) | Text | Table | KG |
|-------|-----------------|------|-------|----|
| 0 — Before first update | Before rev 1244540224 | `EMPTY` | `EMPTY` | `EMPTY` |
| 1 — Official Text + Table update | 8 Sep 2024, 20:32 | `UP_TO_DATE` | `UP_TO_DATE` | `EMPTY` |
| 2 — KG update | 9 Sep 2024, 19:28 | `UP_TO_DATE` | `UP_TO_DATE` | `UP_TO_DATE` |

### Example 4 — 2025 Australian Open Men's Singles Final: Jannik Sinner (Match Result)

| Source | Timestamp (UTC)    | Verified change                                                                                     |
|--------|--------------------|-----------------------------------------------------------------------------------------------------|
| **Table**  | 26 Jan 2025, 11:28 | [Bracket updated with the final winning score for Jannik Sinner.](https://en.wikipedia.org/w/index.php?title=2025_Australian_Open_–_Men%27s_singles&diff=prev&oldid=1271935138) |
| **Text**   | 26 Jan 2025, 11:28 | [Prose updated to describe Sinner's victory in the final.](https://en.wikipedia.org/w/index.php?title=2025_Australian_Open_–_Men%27s_singles&diff=prev&oldid=1271935138) |
| **KG**     | 12 Oct 2025, 16:53 | [P1346 (winner) = Jannik Sinner (Q54812588) added to the tournament entity (Q124376625).](https://www.wikidata.org/w/index.php?title=Q124376625&diff=prev&oldid=2415551897) |

**Timeline**

TABLE (26 Jan 2025, 11:28) ── **0 min** ──▶ TEXT (26 Jan 2025, 11:28) ── **259d 5h 25m** ──▶ KG (12 Oct 2025, 16:53)

**Total table → KG gap:** 259 days, 5 hours, 25 minutes.

**Description.** At 11:28 UTC on 26 January 2025, a single revision simultaneously updated both the tournament bracket **table** and the article **text** to record Jannik Sinner’s victory in the final [e4-1](https://en.wikipedia.org/w/index.php?title=2025_Australian_Open_–_Men%27s_singles&diff=prev&oldid=1271935138). However, the **Wikidata KG** entity (Q124376625) remained without the winner statement for over eight months until 12 October 2025 at 16:53 UTC, when P1346 (winner) = Jannik Sinner (Q54812588) was finally added [e4-2](https://www.wikidata.org/w/index.php?title=Q124376625&diff=prev&oldid=2415551897).

**Status by stage**
 
| Stage | Timestamp (UTC) | Text | Table | KG |
|-------|-----------------|------|-------|----|
| 0 — Before first update | Before 26 Jan 2025, 11:28 | `EMPTY` | `EMPTY` | `EMPTY` |
| 1 — Table + Text update | 26 Jan 2025, 11:28 | `UP_TO_DATE` | `UP_TO_DATE` | `EMPTY` |
| 2 — KG update | 12 Oct 2025, 16:53 | `UP_TO_DATE` | `UP_TO_DATE` | `UP_TO_DATE` |

---

### Example 5 — Carlos Alcaraz Career Titles Update at Indian Wells (Player Career Statistics)

| Source | Timestamp (UTC)    | Verified change                                                                                     |
|--------|--------------------|-----------------------------------------------------------------------------------------------------|
| **Text**   | 17 Mar 2024, 23:13 | [Text updated to mention Alcaraz won his 13th career title at Indian Wells.](https://en.wikipedia.org/w/index.php?title=Carlos_Alcaraz&diff=prev&oldid=1214271430) |
| **KG**     | None | [Number of wins/titles does not exist on wikidata.] |
| **Table**  | 17 Mar 2024, 22:57 | [Infobox ` titles =` parameter manually changed from 12 to 13.](https://en.wikipedia.org/w/index.php?title=Carlos_Alcaraz&diff=prev&oldid=1214269497) |

**Timeline**

TABLE (17 Mar 2024, 22:57) ── **16 min** ──▶ TEXT (17 Mar 2024, 23:13) ── **∞ (missing on KG)** ──▶ KG (None)

**Total table → text gap:** 16 minutes (**Total table → KG gap:** N/A — property absent on Wikidata).

**Description.** At 22:57 UTC on 17 March 2024, the infobox **table** parameter `| titles =` on Carlos Alcaraz’s Wikipedia article was manually incremented from 12 to 13 [e5-1](https://en.wikipedia.org/w/index.php?title=Carlos_Alcaraz&diff=prev&oldid=1214269497). Sixteen minutes later, at 23:13 UTC, the article’s **text** was updated to mention that Alcaraz won his 13th career title at Indian Wells [e5-2](https://en.wikipedia.org/w/index.php?title=Carlos_Alcaraz&diff=prev&oldid=1214271430). Meanwhile, the **Wikidata KG** exhibits schema/instance incompleteness, as cumulative career titles are not tracked on his Wikidata entity.

**Status by stage**
 
| Stage | Timestamp (UTC) | Text | Table | KG |
|-------|-----------------|------|-------|----|
| 0 — Before first update | Before 17 Mar 2024, 22:57 | `STALE` | `STALE` | `EMPTY` |
| 1 — Table update | 17 Mar 2024, 22:57 | `STALE` | `UP_TO_DATE` | `EMPTY` |
| 2 — Text update | 17 Mar 2024, 23:13 | `UP_TO_DATE` | `UP_TO_DATE` | `EMPTY` |
 

---

### Example 6 — Roger Federer's Retirement Announcement (Player Career Status)

| Source | Timestamp (UTC)    | Verified change                                                                                     |
|--------|--------------------|-----------------------------------------------------------------------------------------------------|
| **Text**   | 15 Sep 2022, 13:39 | [Article text updated to state Federer announced his retirement following the Laver Cup.](https://en.wikipedia.org/w/index.php?title=Roger_Federer&diff=prev&oldid=1110439588) |
| **Table**  | 15 Sep 2022, 13:35 | [Infobox "Retired' in 2022.](https://en.wikipedia.org/w/index.php?title=Roger_Federer&diff=prev&oldid=1110438943) |
| **KG**     | 17 Sep 2022, 10:02 | [P2032 (end time) qualifier added to his occupation as a professional tennis player.](https://www.wikidata.org/w/index.php?title=Q1426&diff=prev&oldid=1730388694) |

**Timeline**

TABLE (15 Sep 2022, 13:35) ── **4 min** ──▶ TEXT (15 Sep 2022, 13:39) ── **1d 20h 23m** ──▶ KG (17 Sep 2022, 10:02)

**Total table → KG gap:** 1 day, 20 hours, 27 minutes.

**Description.** On 15 September 2022 at 13:35 UTC, Roger Federer’s infobox **table** was updated to list his retirement in 2022 [e6-1](https://en.wikipedia.org/w/index.php?title=Roger_Federer&diff=prev&oldid=1110438943). Four minutes later, at 13:39 UTC, the article’s **text** was updated to state that Federer announced his retirement following the Laver Cup [e6-2](https://en.wikipedia.org/w/index.php?title=Roger_Federer&diff=prev&oldid=1110439588). Nearly two days later, on 17 September 2022 at 10:02 UTC, the **Wikidata KG** added work period (end) (P2032) to his entity (Q1426) [e6-3](https://www.wikidata.org/w/index.php?title=Q1426&diff=prev&oldid=1730388694).

**Status by stage**
 
| Stage | Timestamp (UTC) | Text | Table | KG |
|-------|-----------------|------|-------|----|
| 0 — Before first update | Before 15 Sep 2022, 13:35 | `STALE` | `STALE` | `STALE` |
| 1 — Table update | 15 Sep 2022, 13:35 | `STALE` | `UP_TO_DATE` | `STALE` |
| 2 — Text update | 15 Sep 2022, 13:39 | `UP_TO_DATE` | `UP_TO_DATE` | `STALE` |
| 3 — KG update | 17 Sep 2022, 10:02 | `UP_TO_DATE` | `UP_TO_DATE` | `UP_TO_DATE` |

---

### Example 7 — Aryna Sabalenka Reclaims WTA World No. 1 (Player Ranking)

| Source | Timestamp (UTC)    | Verified change                                                                                     |
|--------|--------------------|-----------------------------------------------------------------------------------------------------|
| **KG**     | 23 Oct 2023, 00:30 | [Wikidata update P1352 (ranking) to "1" based on the new official WTA data feed.](https://www.wikidata.org/w/index.php?title=Q23448791&diff=prev&oldid=1972321300) |
| **Table**  | 10 Sep 2023, 17:57 | [Infobox rank number 1 added.](https://en.wikipedia.org/w/index.php?title=Aryna_Sabalenka&diff=prev&oldid=1174790045) |
| **Text**   | 10 Sep 2023, 17:57 | [Introduction paragraph updated to mention the World No. 1 ranking.](https://en.wikipedia.org/w/index.php?title=Aryna_Sabalenka&diff=prev&oldid=1174790045) |

**Timeline**

TEXT (10 Sep 2023, 17:57) ── **0m** ──▶ TABLE (10 Sep 2023, 17:57) ── **42d 6h 33m** ──▶ KG (23 Oct 2023, 00:30)

**Total text → KG gap:** 48 days, 15 hours, 8 minutes (and **Total table → KG gap:** 47 days, 11 hours, 4 minutes).

**Description.** On 10 September 2023 at 09:22 UTC, the introduction **text** of Aryna Sabalenka’s Wikipedia article was updated to mention her World No. 1 ranking [e7-1](https://en.wikipedia.org/w/index.php?title=Aryna_Sabalenka&diff=prev&oldid=1174790045). Her World No. 1 rank was added to the **infobox** [e7-2](https://en.wikipedia.org/w/index.php?title=Aryna_Sabalenka&diff=prev&oldid=1174790045) on the same time. Finally, on 23 October 2023 at 00:30 UTC, the **Wikidata KG** updated P1352 (ranking) on entity Q23448791 [e7-3](https://www.wikidata.org/w/index.php?title=Q23448791&diff=prev&oldid=1972321300).

**Status by stage**
 
| Stage | Timestamp (UTC) | Text | Table | KG |
|-------|-----------------|------|-------|----|
| 0 — Before first update | Before 10 Sep 2023, 17:57 | `STALE` | `STALE` | `STALE` |
| 1 — Table + Text update | 10 Sep 2023, 17:57 | `UP_TO_DATE` | `UP_TO_DATE` | `STALE` |
| 2 — KG update | 23 Oct 2023, 00:30 | `UP_TO_DATE` | `UP_TO_DATE` | `UP_TO_DATE` |
 
---

### Example 8 — Paris Master Relocation (Location)

| Source | Timestamp (UTC)    | Verified change                                                                                     |
|--------|--------------------|-----------------------------------------------------------------------------------------------------|
| **Table**   | 28 Apr 2025, 22:00 | [Infobox venue add La défense arena](https://en.wikipedia.org/w/index.php?title=Paris_Masters&diff=next&oldid=1255493767) |
| **Text**  | 23 Oct 2025, 19:45 | [Intro paragraph updated to mention the new location](https://en.wikipedia.org/w/index.php?title=Paris_Masters&diff=prev&oldid=1318423472) |
| **KG**     | 3 Nov 2025, 19:22 | [Wikidata home venue proprety added (P115)](https://www.wikidata.org/w/index.php?title=Q1230166&diff=prev&oldid=2269555477) |

**Timeline**

TABLE (28 Apr 2025, 22:00) ── **177d 21h 45m** ──▶ TEXT (23 Oct 2025, 19:45) ── **10d 23h 37m** ──▶ KG (3 Nov 2025, 19:22)

**Total table → KG gap:** 188 days, 21 hours, 22 minutes.

**Description.** On 28 April 2025 at 22:00 UTC, the infobox **table** of the Paris Masters article was updated to add Paris La Défense Arena as the venue [e8-1](https://en.wikipedia.org/w/index.php?title=Paris_Masters&diff=next&oldid=1255493767). Nearly six months later, on 23 October 2025 at 19:45 UTC, the introduction **text** was updated to mention the new location [e8-2](https://en.wikipedia.org/w/index.php?title=Paris_Masters&diff=prev&oldid=1318423472). Finally, on 3 November 2025 at 19:22 UTC, the **Wikidata KG** added the home venue property (P115) on entity Q1230166 [e8-3](https://www.wikidata.org/w/index.php?title=Q1230166&diff=prev&oldid=2269555477).
 
**Status by stage**
 
| Stage | Timestamp (UTC) | Text | Table | KG |
|-------|-----------------|------|-------|----|
| 0 — Before first update | Before 28 Apr 2025, 22:00 | `STALE` | `STALE` | `STALE` |
| 1 — Table update | 28 Apr 2025, 22:00 | `STALE` | `UP_TO_DATE` | `EMPTY` |
| 2 — Text update | 23 Oct 2025, 19:45 | `UP_TO_DATE` | `UP_TO_DATE` | `EMPTY` |
| 3 — KG update | 3 Nov 2025, 19:22 | `UP_TO_DATE` | `UP_TO_DATE` | `UP_TO_DATE` |

---

### Example 9 — Novak Djokovic Gold Medal (Trophy)

| Source | Timestamp (UTC)    | Verified change                                                                                     |
|--------|--------------------|-----------------------------------------------------------------------------------------------------|
| **Text**  | 04 Aug 2024, 15:06 | [Article text updated to reflect his Olympic gold medal victory over Carlos Alcaraz.](https://en.wikipedia.org/w/index.php?title=Novak_Djokovic&diff=prev&oldid=1238561956) |
| **Table**   | 04 Aug 2024, 15:05 | [Gold medal in the medals infobox added](https://en.wikipedia.org/w/index.php?title=Novak_Djokovic&diff=next&oldid=1238561667) |
| **KG**     | 09 Aug 2024, 19:09 | [Qualifier 'award received' added](https://www.wikidata.org/w/index.php?title=Q5812&diff=prev&oldid=2223966491) |

**Timeline**

TABLE (4 Aug 2024, 15:05) ── **1 min** ──▶ TEXT (4 Aug 2024, 15:06) ── **5d 4h 3m** ──▶ KG (9 Aug 2024, 19:09)

**Total table → KG gap:** 5 days, 4 hours, 4 minutes.

**Description.** At 15:05 UTC on 4 August 2024, the Olympic gold medal was added to the medals infobox **table** on Novak Djokovic’s Wikipedia page [e9-1](https://en.wikipedia.org/w/index.php?title=Novak_Djokovic&diff=next&oldid=1238561667). One minute later, at 15:06 UTC, the article’s **text** was updated to reflect his Olympic gold medal victory [e9-2](https://en.wikipedia.org/w/index.php?title=Novak_Djokovic&diff=prev&oldid=1238561956). Five days later, on 9 August 2024 at 19:09 UTC, the **Wikidata KG** added the corresponding award statement on entity Q5812 [e9-3](https://www.wikidata.org/w/index.php?title=Q5812&diff=prev&oldid=2223966491).

**Status by stage**
 
| Stage | Timestamp (UTC) | Text | Table | KG |
|-------|-----------------|------|-------|----|
| 0 — Before first update | Before 4 Aug 2024, 15:05 | `EMPTY` | `EMPTY` | `EMPTY` |
| 1 — Table update | 4 Aug 2024, 15:05 | `EMPTY` | `UP_TO_DATE` | `EMPTY` |
| 2 — Text update | 4 Aug 2024, 15:06 | `UP_TO_DATE` | `UP_TO_DATE` | `EMPTY` |
| 3 — KG update | 9 Aug 2024, 19:09 | `UP_TO_DATE` | `UP_TO_DATE` | `UP_TO_DATE` |

---

### Example 10 — Laureus World Sports Award for Sportsman of the Year (Laureus)

| Source | Timestamp (UTC)    | Verified change                                                                                     |
|--------|--------------------|-----------------------------------------------------------------------------------------------------|
| **Text**  | 07 May 2021 12:15 | [Intro paragraph mention the 2021 laureate](https://en.wikipedia.org/w/index.php?title=Laureus_World_Sports_Award_for_Sportsman_of_the_Year&diff=next&oldid=1021921127) |
| **Table**   | 07 May 2021, 00:02 | [Nadal name on winner column added](https://en.wikipedia.org/w/index.php?title=Laureus_World_Sports_Award_for_Sportsman_of_the_Year&diff=next&oldid=1016630803) |
| **KG**     | 07 May 2021, 10:43 | [Proprety winner (P1346) added](https://www.wikidata.org/w/index.php?title=Q1808301&diff=prev&oldid=1416621887) |

**Timeline**

TABLE (7 May 2021, 00:02) ── **10h 41m** ──▶ KG (7 May 2021, 10:43) ── **1h 32m** ──▶ TEXT (7 May 2021, 12:15)

**Total table → text gap:** 12 hours, 13 minutes (and **Total table → KG gap:** 10 hours, 41 minutes).

**Description.** On 7 May 2021 at 00:02 UTC, Rafael Nadal’s name was added to the winner column of the **table** on the Laureus World Sports Award for Sportsman of the Year page [e10-1](https://en.wikipedia.org/w/index.php?title=Laureus_World_Sports_Award_for_Sportsman_of_the_Year&diff=next&oldid=1016630803). At 10:43 UTC, the **Wikidata KG** added winner (P1346) = Rafael Nadal on entity Q1808301 [e10-2](https://www.wikidata.org/w/index.php?title=Q1808301&diff=prev&oldid=1416621887). Finally, at 12:15 UTC, the introductory **text** of the Wikipedia article was updated to mention the 2021 laureate [e10-3](https://en.wikipedia.org/w/index.php?title=Laureus_World_Sports_Award_for_Sportsman_of_the_Year&diff=next&oldid=1021921127).

**Status by stage**
 
| Stage | Timestamp (UTC) | Text | Table | KG |
|-------|-----------------|------|-------|----|
| 0 — Before first update | Before 7 May 2021, 00:02 | `EMPTY` | `EMPTY` | `EMPTY` |
| 1 — Table update | 7 May 2021, 00:02 | `EMPTY` | `UP_TO_DATE` | `EMPTY` |
| 2 — KG update | 7 May 2021, 10:43 | `EMPTY` | `UP_TO_DATE` | `UP_TO_DATE` |
| 3 — Text update | 7 May 2021, 12:15 | `UP_TO_DATE` | `UP_TO_DATE` | `UP_TO_DATE` |

---

### Example — Wimbledon 2025 Total Prize Money (Persistent Human Edit Mistake)

| Source | Timestamp (UTC)    | Verified change                                                                                     |
|--------|--------------------|-----------------------------------------------------------------------------------------------------|
| **Text**  | 14 June 2025 08:51 | [Text mentions wrong total prizepool](https://en.wikipedia.org/w/index.php?title=2025_Wimbledon_Championships&diff=prev&oldid=1295527690) |
| **Table**   | 14 June 2025 08:51 | [Infobox mentions wrong total prizepool](https://en.wikipedia.org/w/index.php?title=2025_Wimbledon_Championships&diff=prev&oldid=1295527751) |
| **KG**     | None | [Proprety prize money P2121 empty]

#### Lifecycle with Status Labels

| Stage | Timestamp (UTC) | Text | Table | KG |
|---|---|---|---|---|---|
| 0 - Before first update | Before 14 June 2025, 08:51 | `EMPTY` | `INCORRECT` | `EMPTY` |
| 1 - Text and table update | 14 June 2025, 08:51 | `INCORRECT` | `INCORRECT` | `EMPTY` |


## Summary & Categorization of Events

### 1. Categorization by Year (2021–2026)

| Year | Count | Annotated Examples | Target Fact Type |
|------|-------|--------------------|------------------|
| **2021** | 1 | **Ex 10:** Laureus World Sports Award (Rafael Nadal) | Annual Award Winner |
| **2022** | 1 | **Ex 6:** Roger Federer's Retirement Announcement | Player Career Status |
| **2023** | 1 | **Ex 7:** Aryna Sabalenka Reclaims WTA World No. 1 | Official WTA Ranking |
| **2024** | 5 | **Ex 1:** Wimbledon Prize Money (£50M)<br>**Ex 2:** French Open Final (Carlos Alcaraz)<br>**Ex 3:** US Open Final & Score Revert (Jannik Sinner)<br>**Ex 5:** Carlos Alcaraz Career Titles (Indian Wells)<br>**Ex 9:** Novak Djokovic Olympic Gold Medal | Tournament Winner, Prize Money, Career Titles, Olympic Medal |
| **2025** | 3 | **Ex 4:** Australian Open Final (Jannik Sinner)<br>**Ex 8:** Paris Masters Relocation to La Défense Arena<br>***Ex 11:** Wimbledon 2025 Total Prize Money | Tournament Winner, Tournament Venue, Tournament prizepool |
| **2026** | 1 | **Ex 0:** Wimbledon Final (Jannik Sinner) | Tournament Winner |

### 2. Synthesis: `EMPTY` vs. `STALE` Information Dynamics

Across our annotated benchmark, the initial pre-update state (`EMPTY` vs. `STALE`) is strictly governed by whether the target page represents an **episodic event** or a **continuous entity**:
* **`EMPTY` states occur on episodic tournament edition pages** (e.g., *2024 French Open*, *2024 US Open*, *2025 Australian Open*, *2026 Wimbledon*). Because these pages and Wikidata items are created ahead of the competition, the winner fields (`| champion =`, bracket finals, and Wikidata `P1346`) are initially blank (`EMPTY`). Once match point occurs, Wikipedia Text and Tables synchronize within **0 to 4 minutes**, whereas Wikidata KG lags from **16 minutes up to 259 days**.
* **`STALE` states occur on continuous player or recurring tournament hub pages** (e.g., *Carlos Alcaraz*, *Aryna Sabalenka*, *Roger Federer*, *Paris Masters*). These pages display time-varying attributes (career title counts, world rankings, active status, current venue) that remain valid until a new real-world event supersedes them. When an update is delayed—such as a 48-day lag for Sabalenka's WTA No. 1 ranking on Wikidata (Ex 7) or a 188-day lag for the Paris Masters venue relocation (Ex 8)—the outdated value continues to be presented as current truth, generating prolonged `STALE` windows across modalities.
