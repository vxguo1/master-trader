# Market Context Snapshot: Regime and Structural Trends (Nov 2026)

*Read when: a user asks what the market backdrop is right now (Fed, inflation, yields, dollar, credit, oil, gold, AI trade, crypto); a strategy's fit depends on the current regime; you are about to quote any 2026 level, flow or market-structure statistic; or a user cites a 2026 event (Hormuz, Warsh Fed, 5% 10-year, Nov 5 AI selloff, Binance hack) and you need dated context.*

> **Snapshot as of 9-12 Nov 2026 (market series through 11 Nov 2026). Treat every level as historical; refresh with live sources before quoting.**

**Evidence tags for this file.** `[Strong]` = primary/official data read directly (BLS, BEA, Fed, FRED, FactSet, company IR); `[Moderate]` = reputable wire or industry body via secondary summary, consistent across sources; `[Weak]` = single, undated, low-profile or self-published source; `[Contested]` = credible sources disagree (both given); `[Lore]` = practitioner heuristic. **FORECAST** = a projection, never an outcome. "(FRED, verified 12 Nov)" = pulled from FRED this session.

## Contents
1. How to refresh · 2. Core principles · 3. Regime summary · 4. US macro and the Fed · 5. Global central banks and FX · 6. Rates, term premium, Treasury plumbing · 7. Credit · 8. Equities · 9. Volatility and hedge behaviour · 10. Commodities · 11. Crypto · 12. Structural trends · 13. Key events timeline · 14. Debates and signposts · 15. 2027 consensus (FORECASTS) · 16. Implications for strategy selection · 17. Failure modes / traps · 18. Toolkit hooks · 19. Key sources

---

## 1. How to refresh

**Procedure (run before quoting anything in this file):**
1. List the figures your answer depends on. Any price, yield, spread, vol level, probability or flow figure must be refreshed or quoted with its as-of date.
2. Staleness rule `[Lore]`: levels go stale after about 1 trading day. Regime labels go stale after the next FOMC, CPI or payrolls release, or after any large cross-asset move (an oil swing of 5-10% on a headline is common in 2026). Structural statistics (0DTE share, ETF flows, AUM) go stale after about a quarter.
3. FRED: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=ID1,ID2&cosd=YYYY-MM-DD`. A request with several IDs downloads as a zip of CSVs, so unzip it before reading. FRED lags: DGS10 and T10YIE about 1 day, Brent/WTI spot and the broad dollar index several days. The ICE BofA spread series keep only about 3 years of history.
4. Fastest refresh: `python scripts/fetch.py macro` (dated FRED dashboard of rates, curve, inflation, spreads, VIX, NFCI, USD, Fed balance sheet/TGA/RRP, oil, S&P 500), `fetch.py fred ID... --out` for any other series, and `fetch.py prices SYMBOL` for daily OHLCV (Yahoo, unofficial). Compare each live value against this snapshot and say what has moved.
5. If you cannot refresh, say so and give the as-of date: "As of 11 Nov 2026, HY OAS was 3.30%; I can't confirm today's level."
6. If a refreshed number contradicts the regime summary (for example, Hormuz reopens or the Fed skips December), re-derive the regime read and the strategy implications. Do not patch a single number and leave the old conclusions in place.

| What | Source | Series / location | Cadence |
|---|---|---|---|
| Policy rate, dots | Fed statements, SEP; FOMC calendar | FRED `DFEDTARL`/`DFEDTARU`, `EFFR`; federalreserve.gov/monetarypolicy/fomccalendars.htm | 8 scheduled meetings (format changing, §4) |
| Rate-path pricing | CME FedWatch | hike/cut odds per meeting | live |
| Inflation | BLS CPI; BEA PCE | `CPIAUCSL`, `CPILFESL`, `PCEPILFE` | monthly |
| Labor | BLS Employment Situation | `PAYEMS`, `UNRATE` | monthly |
| Growth | BEA GDP | `A191RL1Q225SBEA` | quarterly + revisions |
| Yields, real, breakeven | Treasury / FRED | `DGS2`, `DGS10`, `DGS30`, `DFII10`, `T10YIE` | daily |
| Term premium | FRED (Kim-Wright); NY Fed (ACM) | `THREEFYTP10`; ACM on newyorkfed.org | daily (model-dependent) |
| Treasury supply | Quarterly refunding / TBAC | home.treasury.gov | quarterly (next early Feb 2027) |
| Repo / basis stress | FRED; OFR; Fed FSR | `SOFR`; OFR Hedge Fund Monitor | daily / semiannual |
| Credit spreads | ICE BofA via FRED | `BAMLH0A0HYM2` (HY), `BAMLC0A0CM` (IG), `BAMLH0A3HYC` (CCC) | daily |
| Private credit | Fitch US Private Credit Default Rate; BDC NAV/10-Qs; Octus | n/a | monthly / quarterly |
| Equity vol | Cboe / FRED | `VIXCLS`; VIX term structure | daily |
| Dollar | FRED broad index; ICE DXY | `DTWEXBGS` | daily |
| Index levels | FRED | `SP500`, `NASDAQCOM` | daily |
| Earnings, valuation | FactSet Earnings Insight | blended EPS growth, fwd P/E, beat rate | weekly (Fridays) |
| Concentration | S&P DJI index data | top-10 weight | monthly |
| Oil | EIA STEO, Weekly Petroleum Status Report, chokepoint data; ICE/NYMEX futures | `DCOILBRENTEU`, `DCOILWTICO` (spot) | weekly / monthly |
| Gold | World Gold Council Gold Demand Trends; Goldhub ETF flows | n/a | quarterly / monthly |
| Copper | LME and COMEX inventories; ICSG | n/a | daily / monthly |
| Crypto ETF flows | Farside Investors (daily); CoinShares Digital Asset Fund Flows (weekly) | n/a | daily / weekly |
| Options volume | Cboe monthly volume reports; OCC monthly statistics | SPX 0DTE share, industry ADV | monthly |
| ETF flows | ETFGI; issuer data | active vs passive share | monthly |
| Hedge funds / CTAs | HFR (HFRI monthly); SG CTA and SG Trend indices | n/a | monthly / daily |
| Prediction markets | Kalshi / Polymarket volume (The Block data) | n/a | monthly |
| Plumbing milestones | DTCC, Nasdaq, NYSE, Cboe; FCA / ESMA (T+1) | n/a | event-driven |

---

## 2. Core principles

- **Levels decay fast and regime labels decay slowly, but both decay.** Use this file to frame the question and choose which data to pull. Do not use it as a quote sheet.
- **2026 is not 2025.** The 2025 setup was AI plus Fed cuts. In 2026 an energy supply shock (the Iran war and Hormuz closure from 28 Feb 2026) landed on strong growth and an AI capex boom, and the Fed turned to hiking. Advice built on the 2025 setup ("buy duration, the Fed has your back") is now stale.
- **Oil is the master variable.** In late 2026 oil drives headline CPI, front-end pricing, the dollar, breakevens and equity sector rotation (energy-led EPS). Check oil before you interpret any macro print. A portfolio long energy, short duration and long USD may be one bet on oil, not three. `[Moderate]`
- **Separate headline from core.** Sep 2026 CPI was 3.7% headline but 2.6% core, with energy +20.4% y/y (BLS). The Warsh Fed hiked anyway, so its reaction function now weights credibility over looking through a supply shock. `[Strong]`
- **The 5% 10-year was a real-rate shock, not an inflation-expectations shock.** Real yields rose about 1.2pp while 10-year breakevens stayed near 2.2-2.4%. Term-premium readings depend on the model, so do not state "term premium rose" as fact. `[Strong]` for the yields, `[Contested]` for the term premium.
- **The shock type decides what hedges.** In the March oil shock, Treasuries sold off together with stocks. In the 5 Nov AI scare, Treasuries rallied. Do not assume a negative stock-bond correlation. `[Strong]` (FRED data, §9)
- **AI risk in late 2026 is about financing, not demand.** Earnings are booming. The weak points are credit backstops, project finance, negative FCF at Meta, 5% yields, and political backlash over data-center power costs. `[Moderate]`
- **Stress sits in illiquid wrappers and venues, not public investment grade.** The places to watch are private credit and BDC gates, CCC bonds, and crypto venue risk (Binance). Public IG has stayed orderly. `[Moderate]`
- **Market plumbing is moving toward always-on, short-dated trading.** 0DTE is about two-thirds of SPX volume, 24x5 trading is being rolled out, and tokenized assets trade 24/7. Gap risk, weekend risk and intraday reflexivity now matter a lot. `[Moderate]`
- **Flags carry forward.** When you relay a single-source or conflicting figure, keep its tag. Never upgrade a `[Weak]` number by repeating it confidently.

---

## 3. Regime summary (as of 9-12 Nov 2026)

1. **Growth: strong.** Q3 2026 real GDP grew +3.4% SAAR in the advance estimate (BEA, 29 Oct; Q2 was 2.2%), with business equipment +20.9% from AI spending. Oct payrolls were +165k against a consensus of about 65k, and unemployment was 4.1% (BLS, 6 Nov). The IMF puts global growth at 3.1% for 2026 (13 Oct). `[Strong]`
2. **Inflation: energy-led re-acceleration.** Sep CPI was 3.7% y/y, core 2.6%, energy +20.4% and gasoline +34.2% (BLS, released 14 Oct; verified 12 Nov). Oct CPI was +0.4% m/m headline and +0.3% core (BLS, 10 Nov). **BLS did not publish most 12-month changes for October** because October 2025 data were never collected during the shutdown. `[Strong]`
3. **Policy: tightening.** The Fed hiked 25bp to 3.75-4.00% on 16 Sep 2026, its first hike since 2023. It held on 28 Oct on a 10-2 vote, with both dissenters wanting a hike. CME FedWatch priced a 78% chance of a December hike on 28 Oct (`[Strong]`) and about 79-81% in early November (`[Moderate]`; one source undated). Warsh has been chair since 22 May 2026.
4. **Rates: real-rate shock, now off the peak.** The 10-year went from 3.97% (27 Feb) to a peak close of 5.31% (5 Oct) and was 4.88% on 9 Nov. The 10-year real yield went from 1.72% to 2.95% and was 2.66%. The 10-year breakeven was 2.20% on 10 Nov (FRED, verified 12 Nov). `[Strong]` Term-premium direction is `[Contested]` (§6).
5. **Dollar: modest 2026 rebound after a weak 2025.** DXY fell 9.4% in 2025 (`[Moderate]`). The FRED broad dollar index went from 119.75 at end-2025 to a low of 117.44 (29 Jan) and was 121.88 on 6 Nov, +1.8% YTD (FRED, verified 12 Nov). DXY peaked at 102.4 on 12 Oct and slipped after the 3 Nov midterms. `[Moderate]`
6. **Credit: repricing from tights, with stress in private credit.** HY OAS went from its 2026 tight of 2.60% (28 Aug) to its 2026 wide of 3.48% (5 Nov) and was 3.30% on 11 Nov. IG OAS was 0.90% on 11 Nov (FRED, verified 12 Nov). `[Strong]` Fitch's private-credit default rate was 6.0% for the 12 months to Apr 2026, the highest since the index began. `[Moderate]`
7. **Volatility: spiky but quick to revert.** VIX closed at 31.05 on 27 Mar (Iran war, the 2026 high) and 28.18 on 5 Nov (AI selloff), then 17.49 on 11 Nov (FRED, verified 12 Nov). `[Strong]`
8. **Equities: earnings-led, multiple compressing, index concentrated.** The S&P 500 closed at 7,619.38 on 11 Nov, +11.3% YTD on price and 2.6% below its 7,818.93 record close on 6 Oct (FRED, verified 12 Nov). Q3 EPS growth was +31.4% y/y and the forward P/E was 17.7x (FactSet, 6 Nov). Mag 7 Q3 earnings growth came in below that of the other 493 companies. The top-10 weight is "almost 40%" `[Weak, unverified]`.
9. **Commodities: oil supply shock, gold correction, copper distortion.** Brent futures were $92.57 on 9 Nov, down from above $112 at the start of November (AP). EIA estimates Hormuz crude flows at 4.9 mb/d in Q2 2026, against 21.6 mb/d in Q4 2025. Gold was about $4,119 on 9 Nov against an all-time high near $5,595 on 29 Jan. LME copper is near records on US tariff stockpiling. `[Moderate]`
10. **Crypto: bear trend plus a venue shock.** BTC was about $75.9k on 8 Nov, roughly 40% below its high of about $126k on 6 Oct 2025. US spot BTC ETFs were -$914m YTD as of 6 Nov. The Binance hack on 29-30 Oct took about $6.3bn. `[Moderate]`
11. **Global policy: synchronized tightening.** ECB deposit rate 2.50% (hikes in Jun and Sep; held 29 Oct). BoE 4.00% (hiked 5 Nov). BoJ 1.25% (held 30 Oct, with a December hike nearly priced). The PBoC is the exception, on hold with the 1-year LPR at 3.0%. `[Moderate]`
12. **Politics: divided government ahead.** Democrats won both chambers on 3 Nov 2026. The new Congress (Jan 2027) brings scrutiny of the Iran war, risk of data-center and energy regulation, and uncertainty for the CLARITY Act. `[Moderate]`

---

## 4. US macro and the Fed

| Date | Fed action | Target range | Vote / detail |
|---|---|---|---|
| Sep, Oct 2025 | -25bp each | n/a | n/a |
| 10 Dec 2025 | -25bp | 3.50-3.75% | 9-3 (Miran wanted -50bp; Schmid and Goolsbee wanted no change). QT had ended on 1 Dec; reserve-management T-bill purchases started 12 Dec at about $40bn/month `[Moderate]` |
| 16 Sep 2026 | **+25bp** | 3.75-4.00% | Unanimous. Dots show one more 2026 hike; longer-run neutral rose to 3.25%; Warsh submitted no dot `[Moderate]`; secondary summaries of the dot counts conflict, so check the official SEP |
| 28 Oct 2026 | Hold | 3.75-4.00% | 10-2 (Cook and Hammack wanted +25bp). Growth upgraded to "strong"; Warsh said inflation has been above target for close to six years `[Strong]` |
| **8-9 Dec 2026** | Next meeting (with SEP) | n/a | Date per the Fed calendar (fetched 12 Nov) `[Strong]` |

- **Leadership.** Warsh was nominated about 30 Jan 2026, confirmed 54-45 on 13 May (the most partisan Fed-chair vote on record) and sworn in 22 May. Powell stays on as a governor, with a term to Jan 2028. `[Moderate]`
- **Balance sheet.** Warsh calls it "excessively large" and favors a Treasury-Fed accord and a shift toward bills. These are proposals, not adopted policy. A Fed-staff paper estimates $1.2-2.1tn of shrinkage is possible within the ample-reserves framework, and analysts expect a multi-year process. `[Moderate]`
- **Meeting format `[Contested]`.** On 28 Oct, Warsh said some meetings will become strategy sessions. Most reports say one 2027 meeting will have no rate vote and 2028 will have two strategy sessions and six policy meetings. Gulf News reports seven rate-setting meetings in 2027 and six in 2028, not yet final. The Fed's published 2027 calendar (fetched 12 Nov) still lists eight meetings: Jan 26-27, Mar 16-17*, Apr 27-28, Jun 8-9*, Jul 27-28, Sep 14-15*, Oct 26-27, Dec 7-8* (* = SEP). Until the Fed marks which meeting has no vote, do not assume a given meeting is "live".
- **Inflation detail.** In Sep, gasoline accounted for over half of the monthly CPI increase (headline +0.6% m/m, core +0.3%). Oct: energy +0.7% m/m (Sep: +5.2%), food +0.5%, shelter +0.3%. FactSet's pre-release Oct consensus of 4.0% y/y headline and 2.8% core is a **forecast**; BLS published no official y/y figure. Expect noisy y/y narratives until the base effect passes, and lean on m/m and PCE. Sep PCE was not retrieved. `[Strong]`
- **Labor.** Oct: +165k payrolls; Aug and Sep revised up a combined 84k. Unemployment has stayed in a 4.1-4.3% range since March. 2026 payrolls average 86k/month against 10k/month in 2025 (revised). Wages +3.1% y/y; U-6 7.9% (up from 7.6%). `[Strong]`
- **Growth.** Q3 nominal GDP +5.6%; consumer spending +3.8%; net exports subtracted about 2.6-3.3pp. The second estimate is due 25 Nov 2026. `[Strong]`
- **Fiscal.** The FY2026 deficit was $1.993tn (CBO preliminary), about 6.2% of GDP (CRFB). Net interest was the largest increase. Customs receipts fell as IEEPA refunds began. `[Moderate]`
- **Tariffs.** On 20 Feb 2026 the Supreme Court ruled 6-3 in *Learning Resources v. Trump* that IEEPA does not authorize tariffs; potential refunds are about $170bn. A 10% Section 122 global tariff took effect 24 Feb for 150 days (to 24 Jul 2026); its status after that date was not found. Section 232 tariffs remain in force. `[Moderate]`

---

## 5. Global central banks and FX

| Bank | Rate (date) | Last move | Next / pricing |
|---|---|---|---|
| ECB | Deposit 2.50% (held 29 Oct 2026; MRO 2.65%) | Hikes in Jun and Sep 2026; a hike was debated in Oct | Next meeting 17 Dec. Lagarde leaves 7 Feb 2027, about nine months early. French debt concerns in the background `[Moderate]` |
| BoE | 4.00% (5 Nov 2026) | +25bp, 8-1 per the BoE (one vote for 50bp); InvestingLive reported 9-0 `[Contested]`, use the BoE's own report | Survey median 4.25% by Feb 2027 (**FORECAST**) |
| BoJ | 1.25% (held 30 Oct 2026, 8-1) | "Hawkish pause" | December hike almost fully priced (Commerzbank); ING sees about 2.00% by summer 2027 (**FORECAST**) |
| PBoC | 1-yr LPR 3.0%, 5-yr 3.5% | Unchanged for a 17th month as of Oct 2026; relending rates cut to 1.25% in Feb 2026 | Relies on targeted tools `[Moderate]` |

- Euro-area inflation of "3.8%" appears only in one headline and is unverified, so do not quote it.
- USD/JPY: the yen strengthened to 157.89 after the BoJ hold on 30 Oct. There is political pressure on the BoJ from PM Takaichi and the US Treasury. `[Moderate]`
- The DXY low came in late Jan 2026 (a four-year low), and the rebound began on the Warsh nomination. Drivers in 2H 2026: expected Fed tightening, Middle East-driven inflation and US resilience. `[Moderate]`
- End-Oct and Nov DXY levels and the CNY level were not found. Use FRED `DTWEXBGS` (121.88 on 6 Nov) or a live DXY quote.

---

## 6. Rates, term premium, Treasury plumbing

| Series (FRED, verified 12 Nov) | 27 Feb 2026 (pre-war) | Peak | 9-10 Nov 2026 |
|---|---|---|---|
| 10-yr nominal (`DGS10`) | 3.97% (2026 low) | 5.31% (5 Oct close) | 4.88% (9 Nov) |
| 10-yr real (`DFII10`) | 1.72% | 2.95% (5 Oct) | 2.66% (9 Nov) |
| 10-yr breakeven (`T10YIE`) | 2.25% | about 2.3-2.4% through Sep-Oct | 2.20% (10 Nov) |
| Kim-Wright 10-yr term premium (`THREEFYTP10`) | 0.46% | 1.10% (5 Oct) | 0.87% (6 Nov) |

- **When 5% broke.** The first 2026 close at 5% was 5.00% on 15 Sep, the eve of the hike (5.01% on 16 Sep). It closed above 5% continuously from 23 Sep to 21 Oct. The 5.31% peak close was the highest since 2007 (FRED), consistent with AP's "above 5.30%, the highest in two decades." One secondary source's 5.106% peak conflicts with this; use FRED. A 5-year auction cleared at 5.033%, the highest since 2006 `[Moderate]`. The 30-year reached about 5.2%, the highest since 2007, but the date is unclear `[Weak]`.
- **Term premium `[Contested]`.** Rabobank's decomposition has the 10-year term premium falling from 0.78% to 0.57% in early Sep and attributes the selloff to real rates and the Fed's shift to hikes. FRED's Kim-Wright measure rose from 0.88% (3 Sep) to 1.08% (30 Sep). The two models disagree on direction, so name the model whenever you cite term premium. Both agree that inflation expectations were **not** the driver.
- **Supply.** The 4 Nov 2026 refunding was $125bn with coupon sizes unchanged. The guidance changed to "anticipates maintaining... for the next several quarters," which hints at coupon increases in 2027; dealers are eyeing possible long-end cuts `[Moderate]`. Earlier dealer forecasts put the first increase in Feb 2027 (Morgan Stanley) or May 2027 (Citi).
- **Basis trade `[Contested by measure]`.** OFR (19 Aug 2026): hedge funds hold about $2tn of cash Treasuries and about $1.4tn of short futures, and a spike in repo rates or futures margins could force a disorderly unwind. Morgan Stanley estimates leveraged basis positions at about $1.2tn, down about 20% this year. The Dallas Fed (28 May 2026) attributes about 60% of the rise in hedge-fund Treasury holdings to the basis trade. Typical leverage is 20-30x via repo `[Weak]`. The Fed's May 2026 FSR says hedge-fund leverage is near record highs and concentrated in large funds.
- **2025 context.** In May 2025 the 10-year term premium approached about 1%, last seen in 2014, on deficit worries. `[Moderate]`

---

## 7. Credit

**Public spreads (FRED ICE BofA, verified 12 Nov):**

| Date | HY OAS | IG OAS | Note |
|---|---|---|---|
| 22 Jan 2026 | n/a | 0.73% (2026 tight) | n/a |
| 16 Mar 2026 | n/a | 0.94% | Iran war |
| 28 Aug 2026 | 2.60% (2026 tight) | about 0.81% (early Sep) | Reported as the tightest since the GFC (GlobalCapital) |
| 2 Oct 2026 | 3.10% | 0.85% | Matches the CryptoSlate report of FRED data |
| 5 Nov 2026 | **3.48% (2026 wide)** | 0.93% | AI selloff day |
| 11 Nov 2026 | 3.30% | 0.90% | Latest |

- Global corporate spreads reached 129bp around 23 Oct, the widest since May 2025. Three US HY deals were pulled in October. CCC spreads widened more than BB/B. HY dispersion is high while IG dispersion is near historic lows. `[Moderate]`
- Read: October was a repricing from extreme tights, not a disorderly break. Public IG has been resilient. `[Moderate]` (inference)

**Private credit, the main stress point:**
- Fitch's US private-credit default rate was 6.0% for the 12 months to Apr 2026 (Mar: 5.7%), the series high. 7 of April's 10 defaults were "stressed" maturity extensions. No later reading was found. `[Moderate]`
- Non-traded BDCs: net redemptions peaked at 4.6% of net assets in Q4 2025. In Q1 2026, BCRED requests reached 7.9% of NAV; BlackRock HLEND hit its 5% gate for the first time; Blue Owl halted OBDC II redemptions after selling $600m of loans; total requests exceeded $20bn. Q2 2026 BDC non-accruals were 3.74% of cost (Octus). `[Moderate]`
- Named 2026 events: a JPM-led group cut FS KKR's credit line by $648m (KKR then added $150m of equity plus a $150m commitment). BlackRock TCP's NAV/share fell 19% in January, and a DOJ valuation probe has been reported. BXSL's Q1 NAV fell 2.4%. `[Moderate]`
- Counter-view `[Contested]`: Moody's calls asset quality broadly benign, with software loan maturities (about 25% of BDC portfolios) peaking in 2028-29. State Street says gates are not automatically a credit signal and that PIK usage and covenant amendments are better signals. The IMF GFSR (13 Oct) flags rising borrower leverage, and US bank lending to NBFIs is reportedly +18% in 2026 `[Weak, secondary]`.
- Not found: Moody's/S&P HY and leveraged-loan default rates for 2026, and any large 2026 public bankruptcies.

---

## 8. Equities

**Levels (FRED, verified 12 Nov; price only):**

| Index | 31 Dec 2025 | 2026 drawdown, Jan-Mar | Record close | 5 Nov 2026 | 11 Nov 2026 |
|---|---|---|---|---|---|
| S&P 500 | 6,845.50 | -9.1% (27 Jan 6,978.60 to 30 Mar 6,343.72) | 7,818.93 (6 Oct) | 7,353.73 (-4.4% on the day) | 7,619.38 (+11.3% YTD, -2.6% from record) |
| Nasdaq Comp. | 23,241.99 | -12.8% (28 Jan to 30 Mar) | 27,599.89 (6 Oct) | 24,315.00 (-11.9% from record) | 25,466.19 (+9.6% YTD, -7.7% from record) |

- **2025 recap.** S&P 500 price +16.39%, total return +17.9%; Nasdaq price +20.36%. The S&P gained about 39% (total return) from the April 2025 tariff low to year-end. The Mag 7 were roughly a third of S&P 500 market cap (figures vary by source and date; 25% appears in some) and produced 52% of the S&P's 2025 total return (RBC). `[Moderate]`
- **Earnings and valuation (FactSet, 6 Nov 2026) `[Strong]`.** Q3 blended EPS growth +31.4% (third straight quarter above 25%); revenue +14.3%; 84% beat, but the average surprise of 2.7% is the smallest since Q4 2022. Energy, IT and Materials lead. Forward 12-month P/E is 17.7x, against 19.0 on 30 Sep, a 5-year average of 19.8 and a 10-year average of 19.1; it is the lowest since Nov 2023. Forward EPS is up about 33.6% YTD while price is up about 7.4%, so **the multiple compressed through earnings growth, not a falling price**. CY2026 EPS growth is estimated at 33.3% and Q4 2026 at 28.4% (**FORECAST**). The Mag 7 posted lower Q3 earnings growth than the other 493, a sign of earnings broadening even though index weight stays concentrated.
- **Concentration.** The top 10 are "almost 40%" of S&P weight, a record `[Weak, undated, unverified]`; Alphabet, Nvidia and Micron account for about 40% of 2026 EPS-forecast gains (same source). Use S&P DJI data before you quote these.

**AI capex (Q3 2026 earnings, late Oct) `[Moderate]`:**

| Company | 2026 capex guide | Notes |
|---|---|---|
| Amazon | about $220bn cash capex (Q3 $75.9bn) | "Meaningfully more" in 2027 |
| Alphabet | $195-205bn (Q3 $51.4bn) | CFO expects a "significant" rise in 2027 |
| Microsoft | about $170bn (trimmed from $175bn) | Third-party data-center capacity delays |
| Meta | $135-145bn (low end raised) | **Q3 FCF -$2.1bn** |
| Aggregate (4) | above $720bn (NYT); up to $828bn including SpaceX | About $700bn in May 2026 |

- Capex definitions conflict: cash capex differs from PP&E including finance leases (e.g. Microsoft at $45.2bn vs $39.4bn for the same quarter). State which definition you are using. `[Contested]`
- **The financing debate (the live AI risk).** 27 Jul: reports that Nvidia was negotiating a roughly $250bn credit backstop for OpenAI's buildout revived "circular financing" worries. 28 Oct: Bloomberg reported obstacles to financing an Anthropic-linked data center in Hubbard, Texas. **5 Nov: AI stocks lost about $2.5tn of Nasdaq-100 value in one day**; Nvidia fell about 8-9% (turning negative for 2026) and AMD about 17%. Triggers cited: funding costs, tighter credit and post-midterm regulation fears. Morgan Stanley and UBS called it an overreaction `[Contested]`. 9 Nov: Nvidia fell 4.3% after the company opened an investigation involving its CEO (per the NYT, an intelligence-related report). The IMF GFSR names an AI-linked correction as one of three key stability risks. `[Moderate]`
- **Leadership shock (12 Nov 2026).** Jensen Huang resigned as CEO and director effective immediately (8-K Item 5.02); CFO Colette Kress is interim CEO and Harvey C. Jones became the first board Chair. Early web-search summaries lagged the filing -- check EDGAR first for company news. See `equity-analysis.md` for the worked NVDA example.
- **Next catalyst.** Nvidia's fiscal Q3 2027 results come **17 Nov 2026 after the close** (call at 5pm ET), per Nvidia IR (verified 12 Nov). Some calendars list 18 or 25 Nov, which are estimates. Consensus expects data-center revenue up more than 12% q/q `[Weak]`.
- Not found: Shiller CAPE, Russell 2000 YTD, and an authoritative top-10 weight.

---

## 9. Volatility and hedge behaviour

| VIX close (FRED `VIXCLS`, verified 12 Nov) | Value | Context |
|---|---|---|
| 24 Dec 2025 | 13.47 | Late-2025 calm |
| 27 Mar 2026 | **31.05 (2026 high)** | Iran war, oil shock |
| 30 Apr 2026 | 16.89 | After the truce and the equity rebound |
| 22 Sep 2026 | 14.21 (2026 low close) | Just before the 10-year's sustained run above 5% |
| 5 Nov 2026 | 28.18 | AI selloff |
| 11 Nov 2026 | 17.49 | Back below 20 within four sessions |

**Did bonds hedge? It depended on the shock (FRED, verified 12 Nov) `[Strong]`:**

| Episode | S&P 500 | 10-yr yield | Broad USD | Read |
|---|---|---|---|---|
| Oil/war shock, 27 Feb to 30 Mar 2026 | -7.8% | +38bp (3.97% to 4.35%) | +2.9% | Bonds **failed** as a hedge; USD hedged |
| AI scare, 4 to 5 Nov 2026 | -4.4% | -6bp (4.90% to 4.84%) | about flat | Bonds hedged modestly |

- Rule: classify the shock (inflation/supply vs growth/risk) before you rely on duration as a hedge. Inflation-shock hedges in 2026 were USD, energy and trend exposure. `[Moderate]` (one year of data; see macro-regimes.md for long-run stock-bond correlation regimes)
- After both 2026 spikes, VIX was back below 20 within days to weeks. Selling vol after a spike paid in 2026, but only for positions that survived the spike itself (§16).

---

## 10. Commodities

**Oil, the dominant 2026 shock:**

| Date | Event |
|---|---|
| 28 Feb 2026 | US/Israel strike Iran; Hormuz effectively closed |
| Mar 2026 | Largest monthly oil rise on record (Brent +50%+, WTI +69%); WTI settles above $100 on 30 Mar for the first time since 2022 |
| 8 Apr | Two-week truce; Brent's biggest one-day fall since 1991; a US naval blockade followed |
| Late Apr | Brent futures peak: $119.50 vs $126.41 (30 Apr, single source) `[Contested]` |
| About 17 Jun | US-Iran MoU briefly reopens the strait; Brent about $72 in late June |
| 8 Jul / 9 Aug | Strikes resume; Iran rejects talks |
| 9 Sep | Brent back above $100 |
| 28 Oct | WTI just above $100, +78% YTD |
| Early Nov | Brent above $112 |
| 9 Nov | Brent -5.8% to $92.57 after Trump said resumed strikes are "highly unlikely" if talks progress |

- **Name the contract.** EIA's Brent **spot** series (FRED `DCOILBRENTEU`) peaked at $138.21 on 7 Apr and $135.51 on 2 Oct, and was $107.03 on 3 Nov. That is far above the futures headlines. Physical spot and front-month futures diverged sharply in this shock, so always say which one you are quoting. `[Strong]` (FRED, verified 12 Nov)
- **Flows.** EIA estimates Hormuz crude flows at 4.9 mb/d in Q2 2026, against 21.6 mb/d in Q4 2025. In mid-August transits fell to six vessels in a day. `[Moderate]` About 20% of world LNG also transits Hormuz; its impact was not quantified in the sources.
- **Gaps.** OPEC+ policy, the Nov EIA STEO and the Hormuz status as of 12 Nov were not found.

**Gold:**
- All-time high: intraday $5,594.82 on 29 Jan 2026 (Trading Economics lists $5,608.35) `[Contested, minor]`; silver topped $120. On 30 Jan gold fell about 11.4% to about $4,745, its worst day since 1983, and silver fell 25-31% (sources differ). Deutsche Bank called the Warsh nomination "the clear catalyst", with a dollar rebound and forced futures liquidation adding to the fall. `[Moderate]`
- Recent prices: a multi-month low of about $3,870 on 30 Oct (labelled a "one-year low" by one source, which looks inconsistent with Q3's $4,262 average `[Weak]`), $3,927 on 3 Nov, $4,146.63 on 5 Nov, and about $4,119 on 9 Nov. `[Moderate]`
- WGC Q3 2026 (3 Nov) `[Strong]`: total demand 1,369t (-1% y/y; value +22%). Central banks bought a net 321t (+42% y/y), 675t YTD. ETFs took in 211t, taking holdings to a **record 4,256t**. Jewellery volume fell 17%, the weakest Q3 in the series. The structural official-sector and ETF bid survived the price crash.

**Copper:**
- The LME 3-month record was $14,527.50 in Jan 2026, with a reported new record above $14,700 on 9 Sep `[Weak, single source]`. COMEX inventories reached a record 675,185t while available LME stocks fell to about 90kt. This is tariff arbitrage, not a global shortage (Reuters analysts). `[Moderate]`
- 2026 balance forecasts `[Contested]`: ICSG sees a 150kt deficit, ING about a 600kt deficit and CRU a 639kt surplus. Grasberg is running at 40-50% capacity, with recovery in 2027-28. Treat copper as a tariff-headline trade. The status of refined-copper tariffs after August was not found.

---

## 11. Crypto

- **Price path.** BTC hit an all-time high of about $126,080 on 6 Oct 2025 `[Weak, single source]`. On 10-11 Oct 2025 more than $19bn was liquidated in 24h, the largest liquidation event on record, triggered by the 100% China tariff announcement; about $16.7bn of that was longs, and CoinShares says real losses may have exceeded $50bn. Nov 2025 saw record monthly spot BTC ETF outflows of about $3.5-3.8bn (sources differ). BTC closed Oct 2026 at $77,430 (-7.3%, likely its weakest October since 2014; Oct 2016 was a gain, so the "since 2016" in reports is doubtful) and was about $75,880 on 8 Nov. ETH was about $2,244 on 8 Nov. `[Moderate]`
- **ETF flows (week to 6 Nov 2026, The Block) `[Strong]`.**

| Product | Week | YTD 2026 | AUM |
|---|---|---|---|
| US spot BTC ETFs | -$1.28bn (worst since late June); 6 Nov -$643m day | **-$914m** (flipped negative) | $95.9bn (about 6.3% of BTC market cap); IBIT $60.3bn |
| ETH ETFs | -$365m (6th straight negative week) | -$406m | $12.84bn |
| SOL ETFs | n/a | +$676m | $1.31bn |

- **Binance hack.** A hot-wallet breach on 29-30 Oct 2026 took $6.34bn (Binance) or $6.43bn (Elliptic) `[Contested, minor]`, the largest crypto theft ever. The FBI attributed it to North Korea's TraderTraitor group on 31 Oct. Binance says it replenished 98% of the assets and is covering the cost, and withdrawals were restored in phases from 1 Nov. The attack-vector details come from low-profile sources `[Weak]`.
- **Treasury companies.** Strategy held 849,327 BTC on 1 Nov 2026. It **sold** 1,395 BTC in Q2 and 5,552 in Q3 to fund preferred dividends and STRC buybacks. Its mNAV was about 1.13x on 3 Nov. Its stated policy is to issue common stock above 1x mNAV and sell BTC below 1x, so a sustained mNAV below 1.0 means mechanical BTC supply. `[Moderate]`
- **Stablecoins and regulation.** Supply reached a record of about $322bn in Jun 2026 and was about $310bn at end-July (USDT about $184bn, USDC about $73bn). The GENIUS Act was signed 18 Jul 2025, and its implementing rules missed the first-anniversary deadline. The CLARITY Act cleared Senate Banking 15-9 on 14 May 2026 and then stalled with no cloture vote; the Democratic sweep adds uncertainty. Stablecoin supply after July was not found. `[Moderate]`
- **Regime read.** Crypto traded as high-beta risk correlated with AI/tech and weak under Fed hikes and a strong USD. It was not an inflation hedge in 2026. `[Moderate]` (inference)

---

## 12. Structural trends (each dated)

**0DTE and retail options.** 0DTE reached a record 66% of SPX options volume in Jul 2026 (63% in Feb). SPX ADV set a record 5.4m contracts in Mar 2026, with 0DTE at 3.2m; the single-day record was 7.8m on 5 Jun. US industry ADV was 72.8m in Q2 2026, up more than 19% y/y. FLEX set a record 2.33m ADV in Q3 2026 (Cboe). `[Strong]` The Q3 0DTE share and the 2026 retail share were not found.
- So what: dealer-gamma and short-dated flow are first-order intraday drivers, especially around macro prints and Iran headlines. Intraday moves can extend or pin depending on positioning, so do not read intraday trend as information about multi-day trend. `[Moderate]`

**ETFs: passive, active and leveraged.** US ETF net inflows exceeded $1tn in 1H 2026 and reached a record $1.2tn through July (ETFGI); Goldman expects more than $2tn for 2026 (**FORECAST**). Active ETFs took about 35% of 2026 flows but hold about 13% of US ETF assets. Global active ETF assets are $2.59tn, and 1,212 of 2,141 global launches through July were active. Leveraged single-stock ETFs: a 2x SpaceX ETF set the first-week volume record (above $4bn in four days), but about 70% of single-stock ETFs have less than $25m AUM (Strategas) and the median one has lost 38% (Morningstar). `[Moderate]`
- So what: daily-reset leveraged and inverse products rebalance in the direction of the day's move `[Moderate]`. If a user holds single-stock leveraged ETFs, check volatility decay and closure risk; the median single-stock ETF's -38% shows how large these costs get.

**24-hour trading.** NSCC 24x5 clearing was scheduled for 28 Jun 2026. Nasdaq targets 24-hour trading in 2H 2026, NYSE Arca 22-hour weekday trading in late 2026, and Cboe plans 24x5 on EDGX, all pending SIP and DTCC readiness. **Whether any of these went live by Nov 2026 is unconfirmed.** `[Moderate]`
- So what `[Lore]`: expect thin overnight sessions with wide spreads, so price discovery will often happen in gaps. Do not treat an overnight print as a reliable reference price.

**T+1.** The US moved to T+1 in May 2024; the CNS fail rate was 1.9% on day one against a 2.01% May average, and fails normalized quickly. **The UK, EU and Switzerland go to T+1 on 11 Oct 2027.** The internal readiness deadline is 31 Dec 2026 and industry testing starts Feb 2027. The FCA warns that unprepared firms may face action. `[Strong]`
- So what `[Lore]`: there is less time for cross-border FX funding and securities-lending recalls, so watch for settlement-fail and borrow-cost spikes around 11 Oct 2027. The US switch in 2024 normalized quickly.

**Tokenization.** An SEC no-action letter (11 Dec 2025) authorized a three-year DTCC pilot covering Russell 1000 equities, Treasuries and major index ETFs. The first live production trades were on 15 Jul 2026 with 30+ firms; the October full launch is **unconfirmed**. The SEC's "innovation exemption" was delayed a second time by mid-August. Tokenized Treasuries were about $14.7bn in late Sep 2026. Tokenized stocks grew from about $0.96bn (Mar) to about $2.2-2.3bn (mid-Jul), with Ondo holding about 60%. Total RWA size depends on methodology: $29bn (Q1, RWA.xyz) vs more than $51bn (Jun, Bernstein) `[Contested]`.

**Prediction markets.** Kalshi plus Polymarket volume exceeded $44bn in 2025 and passed $150bn lifetime in Apr 2026. Monthly volume set a record of about $50.6bn in Jul 2026 (Kalshi $37.7bn, boosted by the World Cup), up from $24.5bn in March. Sports are about 87% of Kalshi volume. The CFTC is supportive, while more than a dozen states are suing under gambling law. `[Moderate]` Aug-Nov volumes, including election night, were not found.
- So what: event-contract prices are a usable real-time probability input for macro and political events, but check liquidity and the resolution wording before you treat a price as a probability. `[Lore]`

**Multi-manager pods and hedge funds.**

| | 2025 | 2026 (latest found) |
|---|---|---|
| Point72 | +17.5% | n/a |
| Balyasny | +16.7% | -3.8% YTD after a -4.3% March, then about +0.5% YTD (around Aug) |
| Millennium | +10.5% | +6.1% YTD through May |
| Citadel Wellington | +10.2% | about +2.4% YTD through April |
| HFRI Macro (Total) | n/a | +12.2% YTD through Q3; Oct -1.0% |
| HFRI Macro: Systematic Diversified / CTA | n/a | **+16.6% YTD through Q3**; Oct systematic trend -0.1% |
| HFRI Macro: Commodity | n/a | +11.5% YTD through Q3; Oct -1.9% |
| HFRI Fund Weighted Composite | n/a | Oct -1.4%, about 60% of funds negative; discretionary thematic -3.2% |
| SG Trend Index | n/a | about +14.9% YTD through Oct `[Weak, from a LinkedIn post]` |

Hedge funds took in $44.5bn of net inflows in Q1 2026, the most since 2007. February 2026 was "chaotic" and Q1 was choppy for multi-strategy funds, with a rebound in April. `[Moderate]` Pod returns for Sep-Oct, full-year 2025 HFRI and CTA figures, and an official SG Trend figure were not found.

**AI in trading.** AIMA (2025): 95% of hedge funds use GenAI in some capacity (86% in 2023). Hedgeweek's Q1 2026 survey: 41% rank AI integration as their top priority, about a third report significant integration. Mercer (May 2026, via a secondary source): only 6% of asset managers let AI make final investment decisions, 8% report measurable return gains and 69% report efficiency gains `[Weak]`. Barclays finds AI is used mainly in research, data analysis and idea generation, with caution on execution and portfolio construction. `[Moderate]`
- So what: an "AI-driven" strategy pitch claims something that only a few percent of managers report doing, so ask what decision the model actually makes and how it was validated out-of-sample.

---

## 13. Key events timeline (late 2025 to Nov 2026)

| Date | Event | Market impact |
|---|---|---|
| 6 Oct 2025 | BTC all-time high, about $126k | Crypto cycle top |
| 10-11 Oct 2025 | 100% China tariff announcement | $19bn+ crypto liquidations, a record |
| Sep-Dec 2025 | Three Fed cuts to 3.50-3.75% (10 Dec); QT ends; bill purchases from 12 Dec | Easing regime peaks |
| Nov 2025 | Record monthly BTC ETF outflows ($3.5-3.8bn) | n/a |
| 11 Dec 2025 | SEC no-action letter for DTCC tokenization pilot | n/a |
| CY2025 | S&P +16.4% price; DXY -9.4% | n/a |
| Jan 2026 | LME copper record $14,527.50 | Tariff stockpiling |
| 29 Jan 2026 | Gold all-time high, about $5,595 intraday | n/a |
| 30 Jan 2026 | Warsh nominated | Gold -11.4% (worst day since 1983), silver -25-31%, USD rebounds from 4-year low |
| 20-24 Feb 2026 | SCOTUS strikes down IEEPA tariffs; 10% Sec. 122 tariff for 150 days | About $170bn in potential refunds |
| 28 Feb 2026 | US/Israel strike Iran; Hormuz closed | Regime break |
| Mar 2026 | Record monthly oil rise; WTI above $100 (30 Mar); VIX 31.05 (27 Mar) | S&P -5.1% for the month; 10-yr +38bp |
| 8 Apr 2026 | Two-week truce | Brent's biggest one-day fall since 1991 |
| Q1-Apr 2026 | BDC gates (HLEND, OBDC II); Fitch private-credit default rate 6.0% (Apr) | Private credit stress |
| 13-22 May 2026 | Warsh confirmed 54-45, sworn in | n/a |
| Jun 2026 | ECB hike; stablecoins at a record of about $322bn; US-Iran MoU (about 17 Jun) | Brent about $72 late June |
| 8 Jul 2026 | Strikes resume | Oil back up |
| 15 Jul 2026 | First live DTCC tokenized trades | n/a |
| Jul 2026 | 0DTE record 66% of SPX; prediction markets about $50.6bn/month | n/a |
| 27 Jul 2026 | Nvidia-OpenAI roughly $250bn backstop report | AI selloff ("circular financing") |
| 9 Sep 2026 | Brent back above $100 | n/a |
| Sep 2026 | ECB hike | n/a |
| 16 Sep 2026 | **Fed hikes to 3.75-4.00%** | 10-yr closes at 5.01% |
| 5-6 Oct 2026 | 10-yr peak close 5.31% (5 Oct); S&P and Nasdaq record closes (6 Oct) | n/a |
| 13 Oct 2026 | IMF WEO (3.1% for 2026) and GFSR (AI-correction risk) | n/a |
| 14 Oct 2026 | Sep CPI 3.7% y/y, core 2.6% | n/a |
| About 23 Oct 2026 | Global corporate spreads 129bp, widest since May 2025 | n/a |
| 28 Oct 2026 | Fed holds (10-2); meeting-format change announced; Hubbard TX data-center financing setback | Dec hike odds 78% |
| 29 Oct 2026 | Q3 GDP +3.4%; ECB holds at 2.50% | n/a |
| 29-30 Oct 2026 | Binance hack, about $6.3bn | n/a |
| 30 Oct 2026 | BoJ holds at 1.25% | Yen firmer |
| 3 Nov 2026 | Democrats win both chambers; WGC Q3 report | Stocks and Treasuries up, USD down, oil and defense down |
| 4 Nov 2026 | Refunding $125bn, hints at 2027 coupon increases | n/a |
| 5 Nov 2026 | BoE hikes to 4.00%; AI selloff (about -$2.5tn NDX value) | S&P -4.4%, VIX 28.18, HY OAS 3.48% |
| 6 Nov 2026 | Oct payrolls +165k; BTC ETFs turn negative YTD | n/a |
| 9 Nov 2026 | Trump: strikes "highly unlikely" if talks progress | Brent -5.8% to $92.57; S&P +2.3% |
| 12 Nov 2026 | **Nvidia CEO Jensen Huang resigns** as President, CEO and director, effective immediately; CFO Colette Kress interim CEO (stays CFO); Harvey C. Jones first-ever board Chair; search inside and outside (8-K Item 5.02 filed 12 Nov, 08:52 ET; no reason given) | NVDA opened $150.99, 52-week low $148.80, ~$165.5 midday (from $173.73 on 11 Nov); 9 Nov had already fallen -4.3% on a board investigation report `[Strong for the 8-K; price moves from Yahoo intraday]` |
| 10 Nov 2026 | Oct CPI +0.4% m/m; most y/y figures unpublished | n/a |

**Upcoming dated catalysts (verify each):** Nvidia results 17 Nov (after close, verified). Q3 GDP second estimate 25 Nov. Nov payrolls 4 Dec. **FOMC 8-9 Dec (with SEP), verified.** ECB 17 Dec. BoJ December meeting (check the date). Nov CPI (check the BLS schedule). New Congress in Jan 2027. Hyperscaler Q4 results with 2027 capex guides (Jan-Feb 2027). Treasury refunding in early Feb 2027. Lagarde exits 7 Feb 2027. EU/UK/CH T+1 on 11 Oct 2027.

---

## 14. What the market is debating: signposts to watch

| Live question | Why it matters | Indicators that resolve it | Last read |
|---|---|---|---|
| Does the Fed hike again in Dec and into 2027? | Front end, USD, real yields, long-duration equity | FedWatch odds for 8-9 Dec; core CPI m/m (Oct +0.3%); 4 Dec payrolls; Dec SEP dots; number of hawkish dissents; oil | About 78% on 28 Oct, about 79-81% in early Nov `[Moderate]` |
| Oil/Hormuz: deal or re-escalation? | Master variable for CPI, the Fed, USD and sector rotation | Hormuz transit counts and EIA flow estimates; Brent curve shape; spot-futures spread; negotiation headlines; Congressional war scrutiny from Jan 2027 | Brent $92.57 on 9 Nov after a de-escalation signal |
| Can the AI buildout be financed? | Index concentration plus a large share of credit issuance | Nvidia's 17 Nov guide; hyperscaler 2027 capex guides; Meta FCF; data-center project-finance closings or failures; tech IG/HY spreads; data-center power regulation | -$2.5tn NDX day on 5 Nov; MS/UBS call it overreaction `[Contested]` |
| Is private-credit stress contained? | Illiquid wrappers, bank-NBFI linkages, CCC | Fitch default rate (6.0% Apr); BDC non-accruals (3.74% Q2); PIK share and amendments; Q4 redemption requests vs 5% gates; bank line cuts; CCC OAS | Moody's: benign so far; maturity wall 2028-29 `[Contested]` |
| Do 10-year yields go back above 5%? | Equity multiples, basis-trade stability | DGS10 vs 5.00%; DFII10 vs its 2.95% peak; T10YIE; auction tails; Feb 2027 coupon sizes; SOFR spikes or futures-margin hikes; Warsh balance-sheet steps | 4.88% on 9 Nov |
| Can earnings hand off in 2027? | A 17.7x P/E rests on forward EPS | FactSet forward-EPS revisions; Q4 EPS growth (est. 28.4%); Mag 7 vs the other 493; energy EPS sensitivity to oil | GS: EPS growth slows to 11% (**FORECAST**) |
| Crypto: capitulation or more forced supply? | Reflexive sellers, venue risk | Farside/CoinShares flows; Strategy mNAV vs 1.0x; stablecoin supply; CLARITY under the new Congress; Binance follow-through | BTC ETFs -$914m YTD on 6 Nov |
| Dollar direction | Global financial conditions, EM, gold | Fed vs ECB/BoJ hike pricing; oil; post-midterm fiscal politics; USD/JPY near 158 into the BoJ | Broad USD 121.88 on 6 Nov |

The IMF GFSR's "disorderly correction" tail is these risks interacting: AI-financing or credit retrenchment, a basis-trade or Treasury liquidity event under heavier coupon supply, and an oil re-spike. If two of these move at once, cut gross exposure before the third. `[Lore]`

---

## 15. 2027 consensus (FORECASTS, not outcomes)

| Variable | Forecast | Source, date | Caveat |
|---|---|---|---|
| Global GDP 2027 | 3.4% | IMF WEO, 13 Oct 2026 | OWID shows 3.2% `[Contested]` |
| Global inflation | 4.7% for 2026, 4.1% for 2027 | Ai Group summary, Oct 2026 | `[Weak, single source]` |
| S&P 500 EPS growth | 36% (2026) to 11% (2027 and 2028) | Goldman Sachs AM, late Oct 2026 | FactSet's CY2026 estimate is 33.3% |
| S&P 500 2027 EPS | $415 | Goldman, late Oct 2026 | Earlier GS $385, MS $380, JPM $420 (about May 2026, stale) |
| S&P 500 year-end 2027 | 8,700 (GS, 19 Oct 2026); 8,800 (Barclays, Jun 2026, reaffirmed Sep) | SimianX tracker | The only two major-bank 2027 targets as of 23 Oct; JPM/MS/UBS/BlackRock outlooks pending |
| S&P 500 other | MS 12-month 8,300 (13 May 2026); MS YE2026 8,000 | SimianX; LPL summary | Stale |
| Fed | One more 2026 hike in the Sep dots; longer-run 3.25%; some sources say markets price hikes into 2027 | Sep SEP; Advisor Perspectives | Check the Dec SEP |
| BoJ | About 2.00% by summer 2027 | ING, Oct 2026 | n/a |
| BoE | Median 4.25% by Feb 2027 | BoE survey via AskTraders, Nov 2026 | n/a |
| Treasury coupons | Increases in 2027 (MS: Feb; Citi: May) | Dealer notes before Nov refunding | Long-end cuts possible |
| Brent / WTI, Dec 2026 | $85 / $80 | Goldman, 9 Sep 2026 | Assumes disruption runs into 2027; upside above $120 in Q4 if disruption persists (GS, 20 Jul) |
| Gold, end-2026 | $6,300 | JPMorgan, Feb 2026 | Made before the slump to about $4,100, so likely stale |
| Gold demand | 2026 investment demand about 200t above 2025 | WGC, 3 Nov 2026 | n/a |
| US ETF flows 2026 | More than $2tn | Goldman, via Markets Media (after July data) | Through July: $1.2tn (ETFGI) |

No 2027 consensus was found for the 10-year yield, USD or BTC, so do not invent one. If a user asks, give the scenario drivers from §14 instead.

---

## 16. Implications for strategy selection

The frameworks live in **macro-regimes.md** (growth/inflation quadrants, stock-bond correlation regimes, regime-detection signals) and **strategy-playbook.md** (strategy families, their failure conditions, sizing). The mapping below is a hedged application of those frameworks to this snapshot. It is not a forecast.

**Regime classification `[Moderate]`.** Growth is strong, headline inflation is up on energy, policy is tightening globally, real yields are high, and volatility comes in episodic spikes. That reads as an inflationary boom with a supply shock, not stagflation, because real growth is +3.4%. The classification flips on two signposts: a durable Hormuz reopening would fade the inflation impulse, and AI-financing or credit stress would hit growth.

| Strategy family | 2026 evidence | Why the regime matters | Posture |
|---|---|---|---|
| Trend following / managed futures | HFRI CTA +16.6% YTD Q3; Oct -0.1% `[Moderate]` | Supply shock plus policy pivot produced persistent trends in oil, yields and USD | Historically favored in this setup, but diplomacy headlines cause violent reversals (8 Apr; Jun MoU; 9 Nov -5.8%). Diversify lookbacks and size for reversal days |
| Discretionary macro / FX | HFRI Macro +12.2% YTD Q3; FX drove September | Divergent central-bank timing (BoJ, ECB leadership change) | Favored. Avoid stacking oil-correlated legs |
| Commodities | HFRI Commodity +11.5% YTD Q3; Oct -1.9% | Physical tightness, but headline-driven | Express with defined risk; distinguish spot from futures; copper is a tariff trade |
| Equity long/short, thematic, pods | Thematic -3.2% in Oct; pods in low single digits for 2026 | AI-factor crowding reversed in Feb-Mar and Oct-Nov | Historically punished in factor reversals. Neutralize factor and real-rate beta; cap AI-complex gross |
| Value/energy vs long-duration growth | Energy leads EPS; Mag 7 Q3 growth below the other 493 | Real yields of 2.6-2.95% penalize duration-like equity | Rotation tends to favor cash-flow-now sectors, but rate-down days (9 Nov) snap back. Hedge real-rate exposure explicitly |
| Short vol / premium selling | VIX spikes reverted within days (31 to 17 in about a month; 28 to 17.5 in four sessions) | Carry rich after spikes; gap risk from weekend strikes and hacks; 0DTE reflexivity | Defined-risk structures only. Size so that a -4.4% index day is survivable |
| 60/40, risk parity | Bonds failed in the March oil shock and hedged in the Nov AI scare | In 2026, stock-bond correlation turned positive in the inflation shock (long-run evidence: macro-regimes.md) | Do not count duration as the hedge for supply shocks. Add USD, trend or energy as inflation-shock hedges |
| Credit carry | HY OAS rose from 2.60% to 3.48%; high HY dispersion; BDC gates | Starting from tights makes carry asymmetric; liquidity mismatch in semi-liquid vehicles | Underweight beta carry; prefer selection. Avoid gated vehicles for money that may need liquidity |
| Rates RV / basis | $1.2-2tn, 20-30x leverage | Repo or margin shock plus 2027 supply | Only with an explicit margin-shock stress test |
| Crypto directional | BTC down about 40% from ATH; ETF outflows; mNAV near 1x | Fell with Fed hikes, a strong USD and the AI selloff | Trend-filter exposure; set per-venue counterparty limits; do not frame it as an inflation hedge |
| Gold | Central-bank and ETF bid at records, but -11.4% in a day on a Fed-credibility shock | Real-rate and USD sensitivity | Size for policy-shock gaps |

**Risk posture in this regime `[Lore]`, unless a reference file gives evidence:**
- Event density is high (CPI, payrolls, FOMC, Nvidia, Iran). Reduce size into scheduled events or use options for defined risk, and price the event with `move` first.
- Count correlated exposure through oil: energy equities, short duration, long USD and short JPY can all be the same bet.
- Gap risk is rising as markets move toward 24x5 and 24/7 trading. Weekend strikes and hacks happen while the cash market is closed, so stops do not protect against gaps.
- Vol-targeting with fast windows de-risks at VIX spikes that reverted within days in 2026. Consider slower or blended estimators; see strategy-playbook.md.

---

## 17. Failure modes / traps

1. **Quoting this file as "current".** Every number has an as-of date. Check the user's date against 12 Nov 2026 and refresh (§1).
2. **"October CPI was 4.0% y/y."** That was FactSet's consensus. BLS did not publish most October y/y changes, so any such figure is derived or estimated. Say so.
3. **Mixing Brent definitions.** EIA spot peaked at $138.21 (7 Apr) while futures peaked at about $119.50-126.41. A user's backtest or P&L must match the instrument actually traded.
4. **Calling the inflation shock broad.** Sep core was 2.6% against 3.7% headline. Arguments for persistent inflation need core or services evidence, not gasoline.
5. **Stating term premium as fact.** The Kim-Wright and Rabobank decompositions disagree on direction for Sep 2026, so name the model.
6. **Assuming bonds hedge equities.** That failed in March 2026. Check the shock type (§9).
7. **Upgrading weak figures.** Do not quote the top-10 "almost 40%" weight, the SG Trend +14.9%, Brent $126.41, the copper $14,700 record or the Binance attack details without their tags.
8. **Mixing measures.** Capex: cash vs PP&E including leases. Basis trade: $2tn of cash holdings vs $1.2tn of leveraged positions. RWA size: $29bn vs $51bn. Compare like with like.
9. **Calling two bank targets "consensus."** As of 23 Oct only GS and Barclays had 2027 S&P targets. The full set of outlooks arrives in mid/late November.
10. **Reusing the 2025 playbook.** "Fed cuts plus AI" momentum logic ignores the 2026 hiking cycle, the real-rate shock and the shift from AI demand risk to AI financing risk.
11. **Ignoring FRED lags and history limits.** DGS10 and T10YIE lag about a day, spot oil and the broad dollar several days, and the ICE spread history is about 3 years. Do not run a long credit-spread backtest from FRED alone.
12. **Assuming new plumbing is live.** 24-hour equity sessions and the full DTCC tokenization launch were unconfirmed as of Nov 2026. Do not build execution plans that depend on them.
13. **Treating gates as defaults.** BDC redemption gates are liquidity events. Credit stress shows up in PIK usage, amendments and non-accruals.
14. **Equating "AI selloff" with "AI demand collapse."** Q3 earnings and capex guides rose. The 5 Nov trigger was financing and policy. Diagnose before recommending a fade or a chase.

---

## 18. Toolkit hooks

- **Price scheduled event risk (Nvidia 17 Nov, Dec FOMC, CPI, payrolls).** Get the market's implied move from the straddle with `python scripts/tradekit.py move --S <spot> --days <d> --straddle <ATM straddle price>`. Back out the event-day move from the term structure with `python scripts/tradekit.py move --S <spot> --days <d> --event-vol <IV of expiry spanning event> --base-vol <ex-event IV>`. The straddle approximates the expected **absolute** move (about 0.8 x sigma x sqrt(T) x S), and 1 SD is about 1.25 x the straddle.
- **Compare implied and realized vol after a VIX spike.** Use `python scripts/tradekit.py vol FILE --window 20` (Yang-Zhang and others) on index OHLC, and compare with VIX or option IV from `python scripts/tradekit.py iv --price <opt> --S --K --days --r --kind`.
- **Check whether a macro trend is tradeable after costs** (oil, 10-yr futures, USD) with `python scripts/techkit.py ruletest FILE --rule tsmom --cost-bps 5 --short --vol-target 0.15 --oos 0.3`. Look at OOS results and DSR before claiming that "CTAs work in this regime" applies to the user's version.
- **Measure leadership and breadth (energy vs AI complex, Mag 7 vs equal-weight).** Use `python scripts/techkit.py rank FILE1 FILE2 ... --by voladj`, and `python scripts/techkit.py indicators FILE` for Weinstein stage and the trend template on a single name.
- **Size positions for this vol regime.** Use `python scripts/tradekit.py size --equity <E> --risk 0.5 --entry <px> --atr <ATR14> --atr-mult 2.5` so that stops scale with the higher ATR of headline-driven markets.
- **Set realistic drawdown expectations** for a strategy chosen from §16 with `python scripts/tradekit.py drawdown --sharpe <SR> --vol <vol> --years <y>`.
- **Estimate liquidity cost in thin sessions** (overnight, stressed credit ETFs) with `python scripts/tradekit.py impact --qty <q> --adv <adv> --price <px> --daily-vol <dv> --spread-bps <s>`.

---

## 19. Key sources

- BLS CPI Sep 2026 (released 14 Oct; verified 12 Nov) — https://www.bls.gov/news.release/archives/cpi_10142026.htm
- BLS CPI Oct 2026 (10 Nov; y/y not published) — https://www.bls.gov/news.release/cpi.nr0.htm
- BEA Q3 2026 GDP advance (29 Oct) — https://www.bea.gov/news/2026/gdp-advance-estimate-3rd-quarter-2026/
- Fed FOMC calendars 2026-27 (fetched 12 Nov) — https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- FOMC 28 Oct 2026 hold, 10-2, FedWatch 78% — https://stockanalysis.com/news/fed-holds-rates-steady-oct-2026/
- FOMC meeting-format change (24/7 Wall St, 29 Oct 2026) — https://247wallst.com/investing/2026/10/29/the-fed-is-cutting-back-on-rate-votes-for-the-first-time-since-1981/
- FRED series DGS10, DFII10, T10YIE, THREEFYTP10, BAMLH0A0HYM2, BAMLC0A0CM, VIXCLS, DTWEXBGS, DCOILBRENTEU, SP500, NASDAQCOM (pulled 12 Nov 2026) — https://fred.stlouisfed.org/
- FactSet Earnings Insight (6 Nov 2026) — https://insight.factset.com/sp-500-earnings-season-update-november-6-2026
- AP via AJC, markets 9 Nov 2026 (Brent $92.57, 10-yr 4.87%, Nvidia) — https://www.ajc.com/news/2026/11/us-stocks-rally-and-recover-more-of-last-weeks-losses-as-oil-prices-swing-lower/
- Rabobank 10-yr decomposition (via iTiger) — https://www.itiger.com/news/1110659271
- OFR, hedge-fund Treasury holdings (19 Aug 2026) — https://www.financialresearch.gov/the-ofr-blog/2026/08/19/hedge-funds-cash-treasury-holdings/
- Fitch private credit default rate (via Benefits & Pensions Monitor) — https://www.benefitsandpensionsmonitor.com/news/industry-news/private-credit-defaults-hit-a-record-high-as-treasury-yields-surge/393595
- IMF GFSR Oct 2026, ch.1 — https://www.imf.org/-/media/files/publications/gfsr/2026/october/english/ch1.pdf
- WGC Gold Demand Trends Q3 2026 — https://gold.org/news-and-events/press-releases/central-bank-buying-and-etf-inflows-support-gold-demand-q3
- EIA Hormuz flows (via OGJ) — https://www.ogj.com/general-interest/economics-markets/news/55403773/oil-tops-100-as-middle-east-supply-risks-intensify
- The Block, crypto ETF flows week to 6 Nov 2026 — https://theblock.co/news/markets/2026-11-07-bitcoin-etfs-flip-negative-for-2026-after-1-28-billion-outflow-week-worst-since-june-435984
- Cboe State of the Options Industry Q2 2026 — https://www.cboe.com/insights/posts/state-of-the-options-industry-options-market-continued-to-break-records-in-q-2-2026
- FCA, T+1 for 2027 — https://www.fca.org.uk/news/blogs/t1-settlement-are-firms-ready-2027
- HFR October 2026 (via WealthBriefing) — https://www.wealthbriefing.com/html/article.php/equity-hedge-fund-strategies-fall-in-october%2C-hitting-sector-results--hfr
- Nvidia IR, Q3 FY27 call date — https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Sets-Conference-Call-for-Third-Quarter-Financial-Results/
