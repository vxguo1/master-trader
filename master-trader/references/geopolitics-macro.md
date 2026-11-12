# Geopolitics and Macro Shocks: Channels, Gauges, Base Rates, Scenarios, News Triage

*Read when: a war, strike, sanctions package, tariff announcement, election, coup, chokepoint attack, OPEC or oil-supply event, terror or nuclear threat, sovereign political crisis or cyber incident is moving (or could move) markets; the user asks "is this a dip or a regime change?", "what hedges this?", "what did markets do last time?", or wants a scenario tree, a news-reliability check or a geopolitical exposure review of a book. This is the depth reference for SKILL.md Workflow H.*

**Tags.** Grade: `[Strong]` `[Moderate]` `[Weak]` `[Contested]` `[Lore]`. Provenance (kept from the research notes): `[V]` verified at source; `[V-DATA]` computed from a primary dataset (GPR/TPU files, FRED); `[V-WIKI]` Wikipedia, secondary; `[K]` cited from the literature, not re-read; `[SC]` spot-check before quoting; `[computed]` event-library calculation with `eventkit.py` (in-sample, hand-picked events, small n). Class: (PR) peer-reviewed, (WP) working paper, (OFF) official sector, (VEN) vendor, (LORE), (DATA). `[US]` = US-centric evidence. All market levels are dated; none is "current".

**Not repeated here (go there):** oil/gold/dollar/curve basics and the regime-diagnosis procedure → `macro-regimes.md` §2, §7-§10; the 2026 Iran/Hormuz/tariff narrative, timeline and signposts → `market-context-2026.md` §9-§10, §13-§14; event vol, skew and hedge structures → `options-volatility.md` §8, §10; sizing and tail-hedge budgeting → `risk-sizing-execution.md` §5.2, §8.

## Contents
1. Core principles
2. Event taxonomy x transmission channels
3. Measurement: risk indices and market-implied gauges
4. Published evidence
5. Analog base rates from the event library
6. Regime-change diagnosis: dip or regime shift?
7. Policy reaction functions
8. Scenario method, hedge selection, gap rules
9. News triage for traders
10. Sector and country exposure map
11. Failure modes / traps
12. Toolkit hooks
13. Key sources

---

## 1. Core principles

1. **Most geopolitical shocks are buyable dips.** Across 43 shocks (1990-2026) the S&P's median max drawdown was -3.0%, reached in 13 trading days, recovered in a median 23; 76% were higher 63 days later. Pure risk premia mean-revert, so the money is usually lost by selling into the first print. `[computed, n=43]` `[Moderate]`
2. **The exception is regime change, and it is visible in week one.** When the shock physically removes energy supply and runs through inflation into the central bank (Kuwait 1990, Ukraine 2022, Hormuz 2026), or lands inside an existing downturn, the base rate breaks: the five regime-change events took a median 118 trading days to recover, with a 63d median of -6.7%. The tells are oil, yields and the dollar rising together. `[computed, n=5]` `[Weak]` on the numbers, `[Moderate]` on the mechanism (Hamilton; Kilian; Caldara et al. 2025).
3. **The channel picks the safe haven, not the headline.** Energy-supply shocks: USD up, yen down, Treasuries unreliable. Demand/trade/financial shocks: duration, JPY, CHF work; USD does not. US-policy credibility shocks (Apr 2025): CHF, JPY, gold; Treasuries and USD both failed. `[computed]` + `[V-DATA]` `[Moderate]`
4. **Threats are priced before acts.** Equities sag while war becomes likely and often rally when an anticipated, supply-bounded war starts ("war puzzle"; Iraq 2003: S&P +8.7% in the 5 days *before* the anchor). Unanticipated shocks fall at onset. `[Moderate]` (LWZ 2003 [V]; Brune et al. [K][SC])
5. **An oil premium persists only with physical loss.** Physical loss: Brent +19.8% median at 5d, up 7/7. Threat or risk premium only: +3.0% at 5d, up at 21d in just 38%. Demand-destructive shocks: oil *falls*. `[computed]` `[Moderate]` (consistent with Kilian 2009)
6. **Policy buffers cap the panic, not the barrels.** SPR + IEA + Hormuz bypass ≈ 6 mb/d against ~16-17 mb/d lost in Q2 2026; buffers are depleted as of Nov 2026. Price must ration demand. `[DATA arithmetic]` `[Moderate]`
7. **Indices measure attention, not pricing.** GPR spike size did not predict the equity hit (Spearman +0.27 with day-1 return, the "wrong" sign, p=0.09); the worst equity damage came from demand, policy and financial shocks GPR barely registers. Use indices to classify and to stage an episode, markets to size it. `[computed]` `[Weak]` (low power)
8. **Probabilities, not narratives.** Prediction-market odds and option-implied distributions convert a story into a conditional move (Δasset ≈ β·Δp). Base-rate-anchored, team-aggregated forecasts beat experts. `[Moderate]` (LWZ; Wolfers & Zitzewitz; Good Judgment Project)
9. **Verification beats speed.** Early war reports are often wrong, false news spreads faster than true news, and moves on unconfirmed headlines tend to reverse. Act on two independent tier-1 sources. `[Moderate]` on the mechanisms, case evidence `[K][SC]`.
10. **Gaps are the real risk.** Big shocks cluster on weekends and outside US hours (28 Feb 2026, 7 Oct 2023, 21-22 Jun 2025 were Saturdays); stops do not work across closures. Size for the gap or own options. `[Lore]` backed by `[V-DATA]` timing

---

## 2. Event taxonomy x transmission channels

Classify every event on two axes before trading it: **(a) supply relevance** (does it remove barrels, LNG, grain, chips, or chokepoint flow net of bypass?) and **(b) policy/inflation relevance** (does it change the central-bank reaction function, the fiscal path or capital mobility?). Pure risk-premium shocks mean-revert in days to weeks; supply, sanctions and regime shocks work through inflation, central banks and term premia over months to years. `[Moderate]` (Caldara et al. 2025: supply side dominates for inflation; matrix is a synthesis, no study ranks channels by type)

First-week signs are event-library medians at 5 trading days (S&P, Brent spot, 10y in bp, VIX pts) unless noted. `[computed]`; n per type is 2-7, so type rows are anecdotes with a statistic attached `[Weak]`.

| Type (library n, examples) | Dominant channels | First-week signs (5d medians) | Typical duration | Evidence |
|---|---|---|---|---|
| **Threat / build-up** (not a library type: Iraq 2002-03, Ukraine Jan-Feb 2022) | Risk premium; option richness; precautionary oil demand | GPR Threats up, Acts flat; equities drift down; puts and OVX bid; front oil spreads widen; pre-drift -5.5% before Ukraine | Weeks-months, until resolved | LWZ [V], KPV [V], GPR [V-DATA] `[Moderate]` |
| **War onset, major commodity exporter** (Kuwait 90, Ukraine 22, Hormuz 26) | Commodity supply → inflation → CB reaction; terms of trade; sanctions | Brent +20-34%; 10y up (2022: breakevens +37bp, real -50bp); USD up 5/5; JPY/CHF down; OVX ≫ VIX | Months-years | Kilian [K], Hamilton [V], FRED [V-DATA] `[Moderate]` |
| **War onset, no lasting supply loss** (war_onset n=7 incl. Hezbollah 06, Hamas 23, Israel-Iran Jun 25) | Risk premium only | All war_onset: S&P -1.3%, Brent +11.1% (fades), VIX +2.6, gold -1.1%; 21d S&P +1.3%, 63d +8.9% | Days-weeks | `[computed]` `[Weak]` |
| **Strike / escalation** (n=6: Desert Storm, Crimea, Soleimani, Iran Apr 24, Fordow 25, Jul 26) | Often *removes* a premium (uncertainty resolved) | S&P +0.8% (83% up), Brent -3.1% (21d -11.1%), VIX +0.1 | Days | `[computed]` `[Weak]` |
| **Sanctions / financial weaponization** (n=3: JCPOA exit 18, SWIFT/reserve freeze 22, Rosneft/Lukoil 25) | Capital controls; stranded assets; reserve diversification → gold; commodity rerouting; physical differentials | S&P +2.2%, Brent +4.6%; reserve freeze = regime Y (327 days to recover from that anchor) | Years (structural) | WGC [V], IMF WP [K][SC] `[Moderate]` |
| **Trade / tariffs** (n=4: Sec. 301 18, May-19 tweet, Liberation Day 25, 100% China 25) | Domestic incidence (full pass-through); firm exposure; TPU → investment; policy credibility | S&P -3.0% (0/4 up), VIX +6.9 (largest of any type), Brent -4.8%, 10y -9; Apr 2025: USD -1.9%, CHF +7.6%, 10y +28bp | Months; reversible by policy | ARW [V], AKW [V], `[computed]` `[Strong]` on incidence |
| **Election / referendum** (n=4: Brexit, 2016, 2024, 2026 midterms) | Political-uncertainty premium; fiscal/regulatory path | S&P 1d +1.3%, recovery 3d; 10y +18; VIX -3.5 (vol crush); registers in EPU, not GPR | Into the event, then crush | KPV [V] `[Moderate]` |
| **Coup / regime change** (n=3: Soviet coup 91, Egypt 11, Korea martial law 24) | Sovereign spreads, local FX and equities, trade-partner spillover | S&P 1d -1.8%, 5d +0.6%; US-asset moves small; local markets are where the moves are (not in library) | Days-months | IMF [V] `[Weak]` |
| **Chokepoint / shipping** (n=2: Gulf of Oman 19, Red Sea 23) | Freight, insurance, delivery-time shock → goods inflation with a lag; regional energy differentials | S&P +1.1%, Brent +3.4%; WCI and tanker rates, transit counts, war-risk premiums move most | Months | IMF PortWatch [V], EIA [V] `[Moderate]` |
| **Oil-supply politics** (n=4: Libya 11, Abqaiq 19, OPEC+ war 20, OPEC+ cut 23) | Barrels on/off; spare capacity | Brent +7.9% at 5d, -3.6% at 21d (outages restored, cuts faded); 2020 glut -39.5% | Weeks unless loss persists | `[computed]` `[Weak]` |
| **Terror / domestic security** (n=4: 9/11, Madrid, 7/7, Paris) | Confidence/demand; airlines, travel, insurers; Treasuries and gold up | S&P 1d -0.6%, 5d +1.2%; Brent 21d -3.4% (demand); 9/11: transport -13%, precious metals +7.4% | Days-weeks (9/11 longer, market closed 4 days) | GPR paper [V] `[Moderate]` |
| **Nuclear / missile threat** (n=3: NK test 06, "fire and fury" 17, Putin mobilisation 22) | Risk premium; regional | S&P -0.6%, gold +2.1%, 10y +9 (Sep 2022 shared the day with a 75bp FOMC hike) | Days | `[computed]` `[Weak]` |
| **Sovereign political crisis** (n=3: US downgrade 11, Greece 15, Italy 18) | Financial/sovereign; bank equity; contagion | S&P 1d -2.1%; deepest median MaxDD (-8.4%), slowest recovery (47d); 10y -19 (rallied even on the US downgrade) | Weeks-months | `[computed]` `[Weak]` |
| **Cyber** (no library events, no sources in the notes) | Operational/sector shock by default; supply channel only if it hits energy, payments or market infrastructure | Unmeasured | Unknown | `[Lore]` |
| **Tech / export controls; fiscal-defense regime** (Oct 2022 chips; Germany Mar 2025; NATO 5%) | Sector earnings and supply chains; fiscal → term premium; defense re-rating | Semis relative, TWD, Taiwan CDS; Bund yields; defense equities | Event, then structural | `[K][SC]` `[Weak]` |

**Quick classification test** `[Lore]` (from the notes' synthesis): (1) OVX/VIX > ~3? (2) Brent M1-M6 backwardation widening? (3) breakevens rising while real yields also rise? (4) USD up vs JPY and CHF? Three or more yes → supply/inflation shock: hedge with commodities, USD and options, not duration.

**Geography.** The US is a net energy exporter and gets ~2% of its liquids consumption via Hormuz; 84% of Hormuz crude goes to Asia. A Gulf war's macro hit lands on Asia and Europe while the dollar trades like a petrocurrency — the reverse of 2003, when war risk *weakened* the dollar (Rigobon-Sack). `[V]` EIA; `[Moderate]`

---

## 3. Measurement: risk indices and market-implied gauges

### 3.1 Caldara-Iacoviello Geopolitical Risk index (GPR) `[Strong]` as a measure (PR, AER 2022) [V]
- **Construction:** share of articles about adverse geopolitical events in 10 English-language papers (from 1985; 3 papers from 1900), monthly from 1900 and daily from 1985. Eight categories: war threats, peace threats, military buildups, nuclear threats, terror threats (= **Threats, GPRT**), beginning of war, escalation of war, terror acts (= **Acts, GPRA**). Normalised 1985-2019 = 100 (historical 1900-2019 = 100). Search terms last changed 2021. Human audit of ~7,000 articles.
- **Country indices:** 44 countries (GPRC_xxx), monthly file only. **No Iran index** — proxy with ISR/SAU/USA, aggregate GPRA, or FRED `WUIIRN`.
- **Not on FRED.** Free (CC BY 4.0) at matteoiacoviello.com/gpr.htm; monthly updated at the start of each month, daily on Mondays; latest data are preliminary and revised. Use dated vintages for backtests.
- **`fetch.py gpr`** writes `date,GPR,GPRT,GPRA,GPRH,GPRHT,GPRHA` (monthly) or `date,GPRD` (daily; the date parsing bug that wrote 1970-01-01 is fixed — verified 12 Nov 2026: 15,281 rows, 1985-01-01 to 2026-11-02). The daily CSV has no Threats/Acts split or moving average: compute a 7-day mean yourself, and keep the raw .xls (`--out-xls`) for GPRD_ACT/GPRD_THREAT and country indices.
- **Noise and lag:** the daily denominator is only ~400-500 articles; weekend events register a day or two late (Sat 28 Feb 2026 read 110.6; 2 Mar 500.8; 7-day MA peaked ~369 on 7 Mar). Read the 7-day MA. `[V-DATA]`
- **Staging rule:** rising GPRT with flat GPRA = anticipation (Feb 2022: Threats 320.6 vs Acts 105.2); a GPRA spike = realisation (Mar 2026: Acts 450.4 > Threats 319.2). Tariff shocks show up in TPU/EPU, not GPR (Apr 2025 GPR only 141 while EPU, TPU and EPUTRADE set records). `[V-DATA]` `[Moderate]`

| GPR reading (1985-2019 = 100) | Value | Note |
|---|---|---|
| Monthly record, Oct 2001 | 512.5 | Sep 2001 498.6 |
| Jan 1991 / Mar 2003 | 379.2 / 358.7 | Gulf War; Iraq invasion |
| **Mar 2026 (Iran war)** | **330.2** (T 319.2, A 450.4) | Highest since Mar 2003; 6th-highest month since 1985 |
| Mar 2022 (Ukraine) | 319.0 (T 403.7, A 251.0) | Threat-dominated |
| Jun 2025 / Oct 2023 | 222.5 / 197.9 | Israel-Iran war; Hamas attack |
| Oct 2026 (latest monthly) | 150.5 (T 156.8, A 167.6) | 91st percentile of 1985-2026 |
| Daily record, 25 Sep 2001 | 1,045.6 | Other daily peaks: 23 Jun 2025 540.2; 25 Feb 2022 515.9; 2 Mar 2026 500.8 |

**Current levels vs history (as of the dates shown)** `[computed]`:

| Series | Latest | Percentile (1985-2026) | 2026 peak |
|---|---|---|---|
| GPR daily (2 Nov 2026) | 114 | 68th | 501 (2 Mar) |
| GPR daily 7d / 30d avg (2 Nov 2026) | 159 / 185 | 92nd / 96th | 369 (7 Mar) / 327 (31 Mar) |
| GPR monthly (Oct 2026) | 151 | 91st | 330 (Mar) |
| US EPU daily `USEPUINDXD` (11 Nov 2026) | 276 | 93rd | 1,049 (Sat 2 May; weekend noise) |
| US EPU 7d / 30d avg (11 Nov 2026) | 323 / 295 | 96th / 95th | 535 (25 Feb) / 424 (22 Mar) |

GPR monthly 2026: Jan 168, Feb 122, Mar 330, Apr 253, May 204, Jun 178, Jul 169, Aug 126, Sep 156, Oct 151 (2026 average 186). **The baseline itself is extreme:** the 1-year median of daily GPR (166) is at the 99th percentile of history, so a "2x spike" today (~330) is a top-1% day, and spike ratios vs the 1-year median are compressed (the Feb 2026 war read only 3.6x off a 141 base vs ~98 for the typical library event). Compare a new reading with both the 1-year median and the long-run 100. `[computed]`

### 3.2 Policy-uncertainty family (FRED IDs verified via `fetch.py search`, last obs in brackets) [V]
| Index | FRED ID | Notes |
|---|---|---|
| US EPU, daily / monthly (Baker-Bloom-Davis, QJE 2016) | `USEPUINDXD` [11 Nov 2026] / `USEPUINDXM` [Oct 2026] | Different series: Oct 2026 monthly index 157.0 vs mean of daily ~280 — never mix them. Monthly record Apr 2025 460.1 (COVID 350.5) |
| Global EPU | `GEPUCURRENT`, `GEPUPPP` [Jul 2026] | Record Apr 2025 620.9; Mar 2026 445.9 (4th-highest); Jul 2026 241.7 |
| Categorical EPU (monthly) | `EPUTRADE`, `EPUNATSEC`, `EPUMONETARY`, `EPUFISCAL` [Sep 2026] | EPUTRADE record Apr 2025 7,955.6; Sep 2026 1,400.8 |
| Equity Market Volatility trackers | `EMVOVERALLEMV`, `EMVNATSEC`, `EMVTRADEPOLEMV`, `EMVCOMMMKT`, `EMVELECTGOVRN` [Oct 2026] | Text tracker of *why* equity vol moved; EMVTRADEPOLEMV 50.3 (Apr 2025) vs 1.5 (Oct 2026) |
| Country EPU / TPU | `EUEPUINDXM`, `UKEPUINDXM`, `INDEPUINDXM`, `CHNMAINLANDEPU`, `CHNMAINLANDTPU` | Japan EPU ID not found |
| Trade Policy Uncertainty (Caldara et al., JME 2020) | not on FRED: matteoiacoviello.com/tpu.htm | 100 = 1% of articles; record Apr 2025 1,151.4; Oct 2026 217.9; daily 30d MA 271.5 (9 Nov 2026) |
| World Uncertainty Index (Ahir-Bloom-Furceri; EIU reports, 143 countries, quarterly) | `WUIGLOBALWEIGHTAVG`, `WUIUSA`, `WUIIRN`, `WUITUR` [Q3 2026] | GDP-weighted record Q3 2025 106,862; Q3 2026 72,717 — **did not set a record in the 2026 war** (already saturated by 2025 tariffs) |
| KC Fed Risk-On/Risk-Off | `KCRORO`, `KCROROE` (equities), `KCROROG` (gold+USD), `KCPRU` (policy-rate uncertainty) [11 Nov 2026] | Ready-made cross-asset haven gauge; methodology not fetched |

- **BlackRock BGRI (VEN):** ML-scored brokerage reports (weighted more) and Dow Jones news; 0 = historical average, 1 = one SD above; headline = average of top-10 risks. Its "market movement" score compares trailing 1-month returns with a pre-specified scenario move vector: +1 priced in, 0 no resemblance, -1 market betting against the risk. **High attention + low priced-in score = where hedges are cheapest relative to the risk.** `[V]` design; scores not extracted `[Weak]` as a signal.
- **Predictive value:** EPU is a priced state variable (Brogaard-Detzel, §4). For GPR no out-of-sample test of aggregate return or vol prediction was found; treat GPR "alpha" claims as unproven. `[Weak]`

### 3.3 Market-implied gauges (lead the text indices and price magnitude)
| Gauge | Source / ID | How to read | Benchmarks (dated) |
|---|---|---|---|
| Oil implied vol | `OVXCLS` (USO options) | Precautionary/supply fear before barrels are lost; distorted by ETF/contract mechanics (ATH 325.15 on 21 Apr 2020) | 2026 peak 120.91 (11 Mar); 2022 78.91 (7 Mar); Jun 2025 71.56; 2023-25 median 34.5. First week 2026: 64.7 → 103.6 while VIX 19.9 → 29.5 `[V-DATA]` |
| **OVX/VIX ratio** | derived | > ~3 = commodity-specific shock, not a growth scare → commodity/option hedges over duration `[Lore]` | 4.99x on 11 Mar 2026; ~2.2x on 7 Mar 2022 `[V-DATA]` |
| Oil curve | Brent M1-M6 / M1-M12; Dated (physical) vs front futures; Dubai/Murban vs Brent; EIA `RCLC1`-`RCLC4` (WTI) | Widening backwardation = scarcity or hoarding; spot outrunning futures = physical squeeze | **Name the contract:** 21d after 28 Feb 2026 EIA Brent spot +70.9% vs Brent front futures +55.6%; on the 8 Apr truce spot -11.6%, Brent futures -13.3%, WTI futures -16.4% `[computed]` |
| Equity vol | `VIXCLS`; VIX/VIX3M inversion, 25d put skew, SKEW, VVIX | War shocks produced *less* index vol than the self-inflicted 2025 trade shock | Max closes: 2026 31.05 (27 Mar); 2022 36.45 (7 Mar); 2025 **52.33** (8 Apr) `[V-DATA]` |
| Gold vol | `GVZCLS` | Spikes on Fed-credibility shocks as much as on war | 2026 max 46.02 on 29 Jan (gold crash, not war); 2022 31.70 (8 Mar) `[V-DATA]` |
| Safe-haven FX | `DEXJPUS`, `DEXSZUS` (noon NY; level up = yen/franc weaker), `DTWEXBGS` | Which haven works identifies the channel (§5.3) | 27 Feb-30 Mar 2026: USD +2.9%, JPY -2.2%, CHF -4.1%; 2-11 Apr 2025: USD -1.9%, JPY +4.3%, CHF +7.6% `[V-DATA]` |
| Sovereign CDS | licensed (S&P/Markit, LSEG, Bloomberg); no free series | Average rise after major events: +30bp AEs, +45bp EMs, up to ~4x in some cases; weak-buffer EMs ≥2x | IMF GFSR Apr 2025 `[V]` `[Moderate]` |
| Freight / insurance | Drewry WCI; Baltic TD3C (VLCC MEG→China); IMF PortWatch transit counts; broker war-risk quotes | Use tanker benchmarks, not the Baltic Dry, for oil conflicts; transit counts are ground truth | WCI $4,305/FEU (12 Nov 2026), 53 Suez vs **1 Hormuz transit** that week `[V]`; Red Sea 2024: Suez volume -50% y/y, Cape +74%, +10 days `[V]`; WCI ~$5,900 peak Jul 2024 from ~$1,400; war-risk ~0.1% → 0.5-1.0% of hull value `[K][SC]` |
| Prediction markets | event contracts | Probability → conditional move (§8.3); check liquidity, resolution wording, manipulation | Volumes: `market-context-2026.md` §12 |
| Dry-bulk real activity | FRED `IGREA` (Kilian index) [K][SC] | Separates demand-driven from supply-driven oil moves | — |

---

## 4. Published evidence

| Study | Finding a trader can use | Magnitude | Grade |
|---|---|---|---|
| **Caldara & Iacoviello 2022**, AER 112(4) [V] (PR) `[US]` | GPR shocks (acts *and* threats alone) are contractionary; fatten GDP left tail | 2-SD shock: VIX up briefly, stocks down, **oil down**, 2y down; investment -1.5% at ~1y; +1 SD global GPR raises disaster probability 18pp (country 9pp; onset 2.2% → ~9%); industries: precious metals/petroleum/defense up, shipping/transport down | `[Strong]` measure, `[Moderate]` effects |
| **Caldara, Conlisk, Iacoviello & Penn 2025** WP [V] | In the global long-history panel GPR is a **supply** shock: inflation up, activity down, dollar up | +1 SD country GPR → inflation +1-2pp within 2y; 2022 war: world inflation +1.2pp, GDP -1% | `[Moderate]`. Reconcile with the AER VAR by event type: supply-relevant wars → supply shock; 9/11-style → demand shock |
| **Rigobon & Sack 2003/2005**, NBER w9609, JBF [V] `[US]` | Pre-Iraq war risk: classic risk-off | Equities ~-4%, HY +34bp, BBB +5bp, Treasuries rally (11bp of 10y via lower breakevens), **dollar weaker**, year-ahead oil +77c | `[Moderate]` (one episode) |
| **Leigh, Wolfers & Zitzewitz 2003**, NBER w9587 [V] | Prediction-market war probability prices assets | +10pp war odds → oil +$1 (3-4%), S&P -1.5%; war ≈ +$10/bbl, -15% equities; options: 70% odds of 0 to -15%, 20% -15 to -30%, 10% worse | `[Moderate]` |
| **Brune, Hens, Rieger & Wang 2015** ("war puzzle") [K][SC] | Stocks fall as anticipated war becomes likely, rise at onset; unanticipated wars fall | — | `[Moderate]` pattern (LWZ agrees), citation `[SC]` |
| **Berkman, Jacobsen & Lee 2011**, JFE 101(2) [V] | 447 crises 1918-2006 (~5/yr): crisis risk moves mean and vol of world returns, is priced | Crisis risk ↑ with E/P, D/P; crisis-sensitive industries earn premia | `[Moderate]` |
| **Kelly, Pástor & Veronesi 2016**, JF 71(5) [V] | Options spanning elections/summits are rich | 1m ATM puts +5.1%, 5% OTM +9.6%, 10% OTM +16.0%; larger in weak economies (~8% vs 1% ATM) | `[Strong]` direction, `[Moderate]` size |
| **Pástor & Veronesi 2012, 2013** [K] | Policy-change announcements lower stocks, raise vol and correlations; premium larger in weak economies | — | `[Moderate]` |
| **Brogaard & Detzel 2015**, Mgmt Sci 61(1) [V] `[US]` | EPU is a priced, return-predicting state variable | +1 SD EPU → +1.5% 3-month abnormal return (~6.1%/yr); high minus low EPU-beta -5.53%/yr | `[Moderate]` |
| **IMF GFSR Apr 2025 Ch. 2** (OFF) [V] | Average effect modest; military conflicts and EMs fat-tailed | ~-1pp monthly stock return avg, -2.5pp EM, **-5pp EM stocks in international military conflicts**; CDS +30bp AE / +45bp EM; main trading partner at war → valuations -2.5% | `[Moderate]` |
| **Kilian 2009**, AER 99(3) [K]; Kilian & Park 2009, IER [V] | Oil shocks differ by driver: supply small/transitory; aggregate demand delayed/persistent; **precautionary demand** immediate, large, lowers stocks persistently | Demand+supply shocks explain 22% of long-run US real stock-return variation; "most spikes were demand-driven" `[SC]` | `[Strong]` taxonomy |
| **Hamilton 2011**, NBER w16790 [V] | Oil spikes preceded 10 of 11 postwar US recessions (exception 1960); 11 of 12 oil episodes had recessions (exception **2003**, an anticipated war with bounded supply effect) | Net-oil-price-increase logic: size and persistence vs recent history | `[Strong]` association; `[Contested]` cause — oil vs the policy response (Bernanke-Gertler-Watson 1997 vs Hamilton-Herrera 2004) [K][SC] |
| **Blanchard & Galí 2007**, NBER w13368 [K] | 2000s oil shocks hurt less: lower oil share, less wage indexation, credible monetary policy | — | `[Moderate]` |
| **Amiti, Redding & Weinstein 2019**, JEP [V]; Fajgelbaum et al. 2020, QJE [K] | 2018 tariffs fully passed through to US domestic prices | Real-income loss $1.4bn/month by end-2018; Amiti-Kong-Weinstein: US listed-firm investment growth -1.9pp by end-2020 [V] | `[Strong]` |
| **Ranaldo & Söderlind 2010**, RoF [V] | CHF and JPY appreciate vs USD when US stocks fall and FX vol rises (1993-2008), hours to days | Non-linear in crises | `[Moderate]`; **conditional on channel** — failed in 2022/2026 energy shocks `[V-DATA]` |
| **Baur & Lucey 2010**, Fin Rev [V]; Baur & McDermott 2010 [K][SC] | Gold: hedge on average, safe haven in crashes, **short-lived** (~15 trading days often quoted `[SC]`); not a haven for all markets | — | `[Moderate]` |
| **Baker, Bloom, Davis & Sammon** NBER w28687 [V] | 8,000+ jumps in 19 markets: 38% attributed to US news; policy news drives upward jumps | — | `[Moderate]` |
| **Federle, Meier, Müller & Sehn 2022** CEPR [K][SC] | Ukraine invasion returns worse the closer to Ukraine | ~1pp+ per 1,000 km | `[Weak]` |
| **Guidolin & La Ferrara 2007**, AER [K][SC] | Conflict can pay incumbents: Angola diamond firms fell when the war ended | — | `[Moderate]` |

---

## 5. Analog base rates from the event library

**Library:** `assets/geopolitical_events.csv`, 45 events Aug 1990 - Nov 2026 (`date,label,type,region,primary_channel,regime_change,confounders,notes`): 43 shocks + 2 de-escalation controls (8 Apr 2026 truce, ~17 Jun 2026 MoU). regime_change Y (5): Kuwait 1990, Trump 2016 (a *reflation* regime), Ukraine 2022, SWIFT/reserve freeze 2022, Iran/Hormuz 2026; N (31); ? (9). Date confidence: 36 high, 8 medium, 1 low. **Conventions:** returns from the last close *strictly before* the event date (h=1 = first close after the news); after-close news is dated the next day; weekend events anchor to Friday. "Brent" below = EIA Brent **spot** (`DCOILBRENTEU`) forward-filled onto the S&P calendar. Everything in §5 is `[computed]`.

### 5.1 By type and by regime flag (S&P medians unless stated)
| Group | n | 1d | 5d | 21d | 63d | %>0 21d | MaxDD | Recover (d) | Brent 5d | 10y 5d | VIX 5d |
|---|---|---|---|---|---|---|---|---|---|---|---|
| All shocks | 43 | -0.3% | -0.0% | +0.3% | +3.9% | 57% | -3.0% | 23 | +1.2% | -2 | +0.5 |
| war_onset | 7 | +0.0% | -1.3% | +1.3% | +8.9% | 57% | -4.4% | 19 | +11.1% | +2 | +2.6 |
| military_strike | 6 | -0.5% | +0.8% | +2.4% | +6.8% | 83% | -2.4% | 17 | -3.1% | 0 | +0.1 |
| terror | 4 | -0.6% | +1.2% | +1.2% | +1.1% | 75% | -6.6%* | 38 | +0.6% | -3 | -1.0 |
| trade_tariff | 4 | -2.6% | -3.0% | -0.8% | +2.7% | 25% | -5.8% | 33 | -4.8% | -9 | +6.9 |
| oil_supply_political | 4 | -1.0% | -0.8% | -2.5% | +4.1% | 25% | -5.2%* | 37 | +7.9% | -12 | +1.8 |
| sovereign_political_crisis | 3 | -2.1% | -1.6% | -0.4% | +5.2% | 33% | **-8.4%** | **47** | -4.2% | -19 | +3.0 |
| election_referendum | 4 | +1.3% | +0.6% | +5.0% | +4.2% | 100% | -1.4% | 3 | -1.2% | +18 | -3.5 |
| **regime_change = Y** | 5 | +0.0% | -1.3% | +4.4% | **-6.7%** | 60% | **-7.8%** | **118** | **+25.7%** | **+18** | **+4.4** |
| **regime_change = N** | 29 | -0.3% | +0.1% | +0.4% | +4.2% | 59% | -2.9% | **19** | +0.1% | -3 | +0.1 |

\* inflated by window confounders (Madrid 2004 Fed fears, Paris into Jan-2016 selloff; COVID in the 2020 price war). Remaining types (sanctions, coup, chokepoint, nuclear) have n=2-3: see §2. The dollar rose in all 5 Y events.

### 5.2 Pooled channel split — the most robust result (11-20 events each, large effect) `[Moderate]`
| Measure (median) | Demand / trade / financial (n=11) | Energy-supply (n=20) |
|---|---|---|
| S&P day 1 | **-2.1%** | -0.0% |
| Day-1 positive | 18% | 45% |
| Max drawdown | -6.8% | -3.0% |
| Recovery | 33 days | 19 days |

Demand, policy and financial shocks hurt stocks more and faster than wars; wars hurt oil-importer FX and bonds.

### 5.3 Safe-haven hit rates, first 5 trading days
| Sample | Gold up | 10y yield down | JPY up | CHF up | DXY up |
|---|---|---|---|---|---|
| All shocks | 25/40 (62%) | 23/42 (55%) | 20/42 (48%) | 24/42 (57%) | 26/43 (60%) |
| S&P down after 5d | 14/22 (64%) | 15/22 (68%) | 14/22 (64%) | 13/22 (59%) | 16/23 (70%) |
| **Energy-supply / chokepoint** | 11/18 (61%) | 12/20 (60%) | **7/20 (35%)** | 11/20 (55%) | 13/20 (65%) |
| **Demand / trade / financial** | 7/11 (64%) | 8/11 (73%) | **8/11 (73%)** | 8/11 (73%) | **4/11 (36%)** |
| regime_change = Y | 2/4 (50%) | 2/5 (40%) | 1/5 (20%) | 2/5 (40%) | **5/5 (100%)** |

- Day 1 when the S&P fell: gold up 76%, 10y down 70%, JPY up 67%, CHF up 52%.
- In energy shocks with the S&P down over 5d, the 10y fell in only 5 of 10; in demand/trade/financial risk-off windows it fell in 7 of 8. Treasury failures (yield up in a risk-off week): Kuwait +48bp, Hezbollah +3, Sep 2022 +40 (75bp FOMC hike same day), Apr 2024 +12, Liberation Day +14, Jun 2025 +2, Feb 2026 +18 (+38 at 21d) — 5 of 7 energy shocks.
- **Zero-haven events** (gold, Treasuries, yen and franc all failed over 5d): Hezbollah 2006, Sep 2022, Jun 2025, Feb 2026 — the dollar rose in all four (+0.8% to +3.5%).
- Gold failures: Feb 2026 -1.7% at 5d and **-13.8% at 21d** (real yields and USD up after the Jan blow-off); liquidation episodes (2020, Liberation Day). Gold up at 21d in 24/39 shocks, median +1.2%.
- The franc can be capped by policy: -11.6% in 21d after the 2011 US downgrade (SNB EUR/CHF floor, 6 Sep 2011 `[K high]`).

### 5.4 Oil (Brent spot) by channel
| Channel | n | 1d | 5d | 21d | %>0 5d | %>0 21d |
|---|---|---|---|---|---|---|
| Physical supply loss (Kuwait 90, Libya 11, Abqaiq 19, Ukraine+SWIFT 22, OPEC cut 23, Hormuz 26) | 7 | +8.3% | **+19.8%** | +16.2% | 100% | 71% |
| Risk premium only (no lasting barrels lost) | 13 | -0.1% | +3.0% | -0.8% | 62% | **38%** |
| Demand / trade / financial | 11 | -1.8% | -0.4% | **-5.2%** | 27% | 36% |
| Political / regional | 10 | +1.2% | +0.7% | +3.2% | 60% | 70% |
| De-escalation (2026 truce, MoU) | 2 | -5.9% | -12.3% | -9.7% | 0% | 50% |

- Premium removed by the escalation itself: Desert Storm -30.3% day 1; Iraq 2003 -8.5% (5d); Fordow 2025 -11.9% (5d); Iran attack Apr 2024 -5.5% (5d). Demand destruction beats fear: 9/11 -25.4% (21d), Liberation Day -20.3%.
- Outages that came back fade: Abqaiq +11.7% day 1, -4.0% at 21d; OPEC+ cut 2023 +9.3% (5d), -3.1% (21d).
- OVX in energy war/strike/sanctions events (n=11): median +8.6 pts at 5d, back to +0.6 by 21d.

### 5.5 Other base-rate statements
- **Day-1 drop ≥ 2% (n=9) was usually the worst point to sell:** S&P above its day-1 close 21 days later in 8/9 (coup 1991, 9/11, US downgrade, Greece, Brexit, Sec. 301, Liberation Day, 100% China tariff; exception Libya 2011, Tohoku inside the window). `[Weak]` small n
- **Wars and strikes ex regime change and ex Soleimani/COVID (n=9):** 8/9 up at 21d, 9/9 at 63d, all recovered within 33 days (median 13). Regime cases: Kuwait -16.9% MaxDD / 131 days; Ukraine -7.7% / 118 days (327 from the freeze); Hormuz 2026 -7.8% but only 30 days (AI-earnings boom carried it `[inference]`).
- **"Buy the invasion" when a telegraphed threat resolves:** Desert Storm S&P +15.2% / Brent -32.3% (21d); Iraq 2003 +2.2% / -12.9%; Fordow 2025 +5.7% / -11.5%. Much can be pre-priced (Iraq: +8.7% in the 5 days before).
- **VIX:** median +1.0 day 1, +0.5 at 21d; below its pre-event level by day 21 in 47% of shocks; median max rise within 63 days +6.8. Geopolitical vol spikes have usually been sellable within a month — for positions that survive the spike. `[inference]` rule
- **Sectors (energy-supply war/strike/sanctions):** XLE beat the S&P by +2.3% at 5d but trailed by -1.1% at 21d (outperformed 46%); ITA +1.4% / +0.5% (58%, n=12); EEM lagged both. Energy rotation is a first-week trade that needs physical loss to last. HY OAS barely moved in 2024-26 Middle East shocks (n=6).
- **GPR spike size → equity hit: null.** Spearman rho with S&P day 1 +0.27 (p=0.09), 5d +0.13, MaxDD -0.06; minimum detectable |rho| ~0.42 at n=42 → a low-power null. Biggest GPR spikes (9/11 13.1x, Ukraine 6.4x, Desert Storm 5.3x) included uncertainty-resolving war starts; the worst equity hits (OPEC+ war 0.8x, US downgrade 1.1x) barely registered — they show in **EPU** (Brexit 9.2x, Liberation Day 7.4x).

**Caveats (state them when quoting):** n=2-7 per type; overlapping windows (Feb 2022 pair, Jun 2025 pair, Oct 2025 pair, the 2026 sequence); hindsight selection and hindsight regime flags; no threats that never materialised; confounders named per event (63d column is the most contaminated); day-0 pricing of intraday events is invisible (JCPOA 14:00 ET, Sec. 301 ~12:50, 100% tariff ~11:00); US-listed assets only — local markets (KOSPI, MOEX/RUB, gilts/GBP, Israeli and Gulf assets) are where the largest moves are and are not covered; FRED oil sparse 1993-2006; WTI after Mar 2020 distorted by the -$37.63 settlement (20 Apr 2020); no daily gold before Aug 2000; FX are noon rates. Quote the **channel group** percentile of a new event, not the type median.

---

## 6. Regime-change diagnosis: dip or regime shift?

Score each test in the first 5 trading days. `[Lore]` procedure built on `[computed]` tells and `[Moderate]` literature (Hamilton; Kilian; Blanchard-Galí; Caldara et al. 2025).

| # | Test | Regime-shift reading | Dip reading | Measure |
|---|---|---|---|---|
| 1 | **Energy/supply loss** | Barrels or chokepoint flow physically lost, net of bypass and stock release; Brent 5d > +15% (Y median +25.7%) | Threat only; strike removes premium; Brent 5d < +10% | Transit counts (PortWatch/AIS), Brent M1-M6, spot vs futures gap, OVX/VIX > 3 |
| 2 | **Inflation pass-through** | Breakevens up (2022: +37bp in two weeks while real yields fell -50bp); tariffs with full pass-through; food/fertilizer channel | Breakevens flat or down (Iraq 2003: lower breakevens) | `T10YIE`, `DFII10`, CPI energy weight |
| 3 | **Central-bank reaction** | CB in inflation-fighting mode: 2y/10y *up* in a risk-off week; hikes through the shock (Fed 2022 +425bp; Fed hike Sep 2026) | CB can ease or look through: front end falls (9/11: 2y -72bp in 5d) | 2y yield, OIS/FedWatch odds, CB rhetoric on second-round effects |
| 4 | **Sanctions on reserves / finance** | Reserve freeze, SWIFT exclusion, capital controls, exchange closures or index deletions (MOEX closed ~a month; Russia removed from MSCI at ~zero) | Targeted designations that leak | Sanctions texts, exporter FX vs capital controls, physical differentials (Urals) |
| 5 | **Duration** | Loss expected to outlast buffers (§7 arithmetic); curve implies persistence; prediction markets price no quick resolution | Curve implies fade (2003 futures priced the spike fading by end-2004); quick-resolution odds | Futures curve, event contracts, signposts |
| 6 | **Pre-existing macro** | Recession, tightening cycle or pandemic already under way (Jul 1990 recession; 2022 bear market from 3 Jan; COVID 2020) | Benign backdrop, easing bias | `macro-regimes.md` §2 diagnosis |

**First-week tells (market version of tests 1-3):** oil 5d > +10-15%, 10y yield (or breakevens) up, USD up vs JPY and CHF, VIX +4 or more. **Scoring:** 0-1 → dip base rates apply (N-group median recovery 19 days; wars ex regime 13); 2 → half-size dip buying, hedge with USD/oil optionality; 3+ → size for 3-6 months (Y median recovery 118 days, 63d median -6.7%) and stop treating the analog average as the forecast. `[computed]` numbers, `[Lore]` thresholds.

Nuances a master checks:
- **Yields can miss the tell in week one.** In 2022 the 10y *fell* 13bp at 5d (real -50bp, breakevens +37bp) and rose +35bp at 21d. Read breakevens, not just nominal yields.
- **Regime change is not always down.** Trump 2016 (Y) had yields +34bp and USD up with stocks *up* (reflation). The tells identify a regime; growth vs inflation decides the equity sign.
- **Historical failures of "buy the dip":** 1973 Yom Kippur → embargo → oil ~4x → S&P ~-48% bear market; 1990 Kuwait → oil doubled → recession; 2022 Ukraine → invasion-day intraday reversal (Nasdaq ~-3.5% to +3.3%) then a bear market as CBs hiked into commodity inflation. `[K][SC]`
- **"Buy the invasion" works** when the event was anticipated (GPRT high, skew rich), the supply loss is bounded, the policy reaction benign and positioning defensive; **it fails** when supply loss outruns buffers, sanctions strand assets, or CBs are fighting inflation. `[Lore]` consistent with Hamilton's 2003 exception

---

## 7. Policy reaction functions

**Strategic stocks.** `[V-WIKI]` unless tagged
| Item | Figure |
|---|---|
| US SPR capacity / max drawdown | 714 mb / **2.7 mb/d**; oil reaches market ~13 days after a presidential order |
| Past US releases | 1990-91: 21 mb; 2005 Katrina: 11 mb; 2011 Libya: 30 mb (of a 60 mb IEA action); 2022: 50 mb + 30 mb + **1 mb/d x 180 days = 180 mb** (then a record) |
| **2026** | 11 Mar 2026: 172 mb US release over ~120 days within a **400 mb IEA action by 32 countries**; inventory 285.4 mb (4 Sep 2026), lowest since 1982 by October; release complete 30 Oct 2026 (174.1 mb); refill pledge tied to a Venezuela deal (30 Aug) `[SC]` doubted in press |
| IEA rules | Members hold ≥ 90 days of net imports; collective actions 1991, 2005 (~60 mb), 2011 (60 mb), 2022 (62.7 mb + ~120 mb) `[K][SC]`; 2026 figures need IEA/DOE confirmation |

**Arithmetic for a Hormuz-type shock** `[DATA]`: IEA 400 mb / 120 days ≈ **3.3 mb/d** (US share ≈ 1.4 mb/d, half its 2.7 mb/d maximum) + ~2.6 mb/d unused bypass (Saudi East-West 5 mb/d nominal, 7 temporarily in 2019; UAE Habshan-Fujairah 1.8 mb/d; Iran Goreh-Jask ~0.3, idle since Sep 2024) [V EIA] ≈ **6 mb/d** vs ~16-17 mb/d lost (Hormuz crude 21.6 mb/d Q4 2025 → 4.9 mb/d Q2 2026). Hormuz normally carries ~20 mb/d (~20% of world liquids consumption, >25% of seaborne oil, ~20% of LNG) [V EIA]. **Policy caps the panic; demand destruction (2026 demand -1.6 mb/d, `macro-regimes.md` §10) does the rest.**

**Buffers are depleted (Nov 2026)** `[inference]`: SPR near 40-year lows and IEA stocks drawn, so a 2027 supply shock meets a weaker stock response — price upside oil-vol tails wider than in 2022-26. Refill status unverified.

**OPEC+ spare capacity:** output bringable online in 30 days and sustainable for 90 (EIA definition), concentrated in Saudi Arabia and the UAE, ~4-6 mb/d in 2024-25 `[K][SC]`, likely overstated because output lags quotas, and **mostly behind Hormuz** — useless in a Hormuz closure. Next ministerial 29 Nov 2026.

**Central banks: looking through vs reacting.**
| Episode | Reaction | Lesson |
|---|---|---|
| 1973-74 | Burns Fed accommodated; inflation entrenched; Volcker disinflation → 1980-82 recessions | Accommodation entrenches inflation `[K]` |
| 1970s output loss | Much attributed to the tightening response (Bernanke-Gertler-Watson 1997) vs oil itself (Hamilton-Herrera 2004) | `[Contested]` `[K][SC]` |
| 2000s | Smaller oil-shock effects: credible policy, less indexation (Blanchard-Galí 2007) | Credibility buys the option to look through `[Moderate]` |
| 2022 | Fed +425bp in 2022, ECB first hike Jul 2022, hiking through the energy shock | Post-2021 prior: CBs react to second-round effects and expectations `[K]` |
| 2026 | Fed hiked Sep 2026 (to 3.75-4.00%) despite the oil shock; ECB hiked Jun and Sep; BoE Nov (`market-context-2026.md` §13) | Under the Warsh Fed assume reaction even to headline persistence `[inference]` |

**Default prior (Nov 2026):** an oil shock is **hawkish for the front end** unless growth is collapsing — the inverse of the 1990s-2010s "look through" prior. Geopolitical risk creates stabilisation trade-offs (inflation up, activity down) [Caldara et al. 2025, V].

**Sanctions:** announced fast, enforced slowly, leak. Reserve freeze ~$300bn (Feb 2022); G7 price cap $60 (5 Dec 2022); EU product caps (Feb 2023); EU/UK cap cut to $47.60 (Sep 2025); US sanctions on Rosneft and Lukoil (Oct 2025: Brent spot +6.5% day 1, +2.2% at 21d `[computed]`). Enforcement runs through insurance and P&I clubs, leaks via the shadow fleet (Russia's share of southbound Suez oil 30% in 2021 → 74% in 1H 2023 [V EIA]), and shows up first in **physical differentials (Urals discount)**, freight and the exporter's FX under capital controls — not in Brent flat price. Trade shape: front-loaded headline move, then slow leak. `[K][SC]` `[Moderate]` (Babina et al. 2023). Financial sanctions also push central banks into gold (Arslanalp, Eichengreen & Simpson-Bell 2023 [K][SC]; WGC surveys 2025-26: record 43%/45% plan to add gold, 73-74% expect a lower USD reserve share [V]; flows in `macro-regimes.md` §10).

**Fiscal:** 2022 European energy subsidies and price caps (hundreds of billions of euros); Germany's Mar 2025 debt-brake reform drove the largest one-day 10y Bund yield rise since ~1990; NATO 5% of GDP by 2035 (3.5% core + 1.5%) is a structural channel to sovereign supply, term premia and defense equities. `[K][SC]`

---

## 8. Scenario method, hedge selection, gap rules

### 8.1 Building the tree `[Lore]` built on `[Moderate]` forecasting evidence
1. **Define** 3-5 mutually exclusive end-states at a fixed horizon (e.g., 21 trading days and 90 days): de-escalation / contained (no barrels lost) / escalation with supply loss / tail (regime change).
2. **Anchor** probabilities on base rates (Berkman: ~5 international crises a year; country disaster onset ~2.2%/yr, ~9% after a +1 SD country GPR rise), then adjust with Analysis of Competing Hypotheses: score each piece of evidence for *diagnosticity* and seek disconfirmation (Heuer 1999 [K]).
3. **Cross-check** against market-implied odds: event contracts, option-implied distributions (LWZ's 70/20/10), the oil curve. Where yours differ most is where the trade is.
4. **Map each state to a move vector** from analogs (§5): borrow the channel group's median and the worst case of the closest regime analog, and say which.
5. **Signposts** that move probabilities (energy wars): transit counts (PortWatch/AIS), statements from both sides, force movements, insurance listed-area changes, OPEC+/IEA statements, sanctions designations, CB rhetoric on second-round effects. Current signposts: `market-context-2026.md` §14.
6. **Update** in small steps on noisy news, large steps on diagnostic signposts; keep precise probabilities (rounding to coarse bins worsens accuracy, Friedman et al. 2018 [K]); extremise team aggregates (Baron et al. 2014 [K]); score yourself with Brier = mean((p - outcome)²).
7. **Express** where your probabilities differ from the market's, with convex instruments.

Why this beats expert narrative: the Good Judgment Project (IARPA ACE) was 35-72% more accurate than other research teams; top forecasters reportedly ~30% better than analysts with classified access `[V-WIKI]`, the latter `[SC]`; Tetlock (2005): experts barely beat extrapolation, "foxes" beat "hedgehogs" `[K]`. `[Moderate]`

### 8.2 Worked example: `eventkit.py scenarios` with `--max-loss`
Book: $1m S&P, long Treasuries with DV01 $400/bp, $100k gold. Gulf escalation risk, 21-day horizon. Moves from analogs: de-escalation ≈ 2026 truce (S&P +5.3%, Brent -14.1% at 5d); contained ≈ risk-premium-only medians; escalation ≈ physical-loss group and Hormuz 2026 (S&P -7.8%, 10y +38bp, gold -13.8% at 21d); tail ≈ Kuwait 1990 (MaxDD -16.9%, 10y +57bp at 21d). The hedge, OILCALL, is a 45-day Brent call 10% OTM (S=80, K=88, vol 55%: `tradekit.py bs` price 3.35, delta 0.36); its column is **P&L as % of premium**, repriced per scenario with `tradekit.py bs` at the scenario's spot, vol and remaining days (-100, -46, +552, +1354). Linear tool, so convex hedges enter as precomputed % P&L.

```
scenario,prob,SPX,UST10,GOLD,OILCALL
deescalation,0.30,4,-5,-1,-100
contained_no_barrels_lost,0.40,-2,0,1,-46
escalation_supply_loss,0.22,-8,35,-5,552
tail_regime_change,0.08,-17,55,-10,1354
```
`python scripts/eventkit.py scenarios --file tree.csv --pos SPX=1000000 UST10=400,dv01 GOLD=100000 --max-loss 60000`

| Book | Expected P&L | Worst (tail) | P(loss) | Scale to cap worst at -$60k |
|---|---|---|---|---|
| Unhedged | -$33,240 | -$202,000 | 70% | x0.30 |
| + $10k premium in OILCALL (`OILCALL=10000`) | -$15,104 | -$66,600 | 70% | x0.90 |

Read: Treasuries *lose* in both bad states (energy shock → yields up) and gold loses in the tail, so the "balanced" book has no hedge for this channel; ~1% of the book in oil-call premium cuts the worst case by two-thirds. Sanity check: these probabilities make the call worth ~+181% of premium in expectation vs a risk-neutral P(ITM) of 28.6% — either you have an edge on the escalation odds or the tree is too fat-tailed. Vary each probability ±10 points and check the decision survives.

### 8.3 Prediction-market conditional moves (LWZ method) `[Moderate]`
```
Δasset ≈ β × Δp          war-state price ≈ P_now + β(1 − p)          no-war price ≈ P_now − β·p
```
LWZ 2003: β(oil) ≈ $10 per 100pp, so at p = 75% and $35 oil → $37.50 with war, $27.50 without. Estimate β from past moves in price vs probability (Snowberg-Wolfers-Zitzewitz 2007 election-night template [K]). Before use: liquidity, favourite-longshot bias, **resolution wording** (e.g., the Mar 2025 Polymarket "Ukraine mineral deal" UMA-vote dispute [K][SC]), and insider trading on government decisions. Manipulation historically moved prices only briefly (Rhode & Strumpf 2004 [K]).

### 8.4 Hedge selection by channel
| Channel | Hedges that worked | Hedges that failed | Evidence |
|---|---|---|---|
| **Energy supply / inflationary war** | Long USD (up 65% of energy shocks, 5/5 regime Y, 4/4 zero-haven events); oil call spreads (cheaper than outrights when call skew is bid); energy equities for week one only; short duration | **TLT/duration** (10y fell in only 5/10 risk-off energy windows; +38bp in 21d of 2026); **JPY** (up 35%); gold in 2026 (-13.8% at 21d); EM oil importers' FX | `[computed]` `[Moderate]` |
| **Demand / trade / financial** | Duration (7/8 risk-off), JPY (73%), CHF (73%), gold (64%) | USD (36%); oil is a risk asset, not a hedge | `[computed]` `[Moderate]` |
| **US-policy credibility** (Apr 2025 "sell America") | CHF, JPY, gold | Treasuries (10y +28bp) and USD (-1.9%) together | `[V-DATA]` `[Weak]` (one episode) |
| **US terror / security, no supply loss** | Treasuries, gold, short transport/airlines | — | Rigobon-Sack, GPR paper `[Moderate]` |
| **Sanctions / reserve weaponization** | Gold (structural central-bank bid), physical-differential and freight trades | Exporter FX under capital controls (ruble over-recovered in 2022) | WGC [V], `[K][SC]` |
| **Elections / summits** | Own vol *before* attention rises; sell event vol after the result (vol crush) | Buying protection once the date is known (5-16% rich) | KPV `[Strong]` direction |
| Caveat: policy caps havens | — | CHF under an SNB floor (2011) | `[K high]` |

**Carry discipline.** Permanent geopolitical hedges bleed: crisis-sensitive assets earn a premium (Berkman), low EPU-beta beats high by 5.53%/yr (Brogaard-Detzel), and event-spanning puts cost 5-16% more (KPV). Buy protection when attention is low (low GPRT, low BGRI, flat OVX), use spreads when skew is bid, and fund carry by selling vol *after* spikes only with sizing that survives the next gap. Event pricing: `tradekit.py move --event-vol --base-vol` for the implied event move; an ATM straddle ≈ 0.8·σ√T·S is the expected *absolute* move, and 1 SD ≈ 1.25 x straddle. Structures: `options-volatility.md` §8, §10; tail budgets: `risk-sizing-execution.md` §8.

### 8.5 Weekend and gap rules `[Lore]`
- Size every open position for the gap, not the stop: assume 10-15%+ in oil and several percent in index futures across a closure (2026 had Brent single-day moves of ~6-16%; 8 Apr truce WTI futures -16.4%).
- Into a weekend with live escalation risk: cut to the size you can hold through the gap, or replace delta with options. Stops fill at the open, not the stop.
- First liquid prints of a weekend event: 24/7 crypto, Gulf equities (Tadawul trades Sun-Thu), Sunday 17:00-18:00 ET CME Globex and FX opens, then Asia. Thin markets: treat as noisy, not as the price.
- Pre-commit the plan for both de-escalation and escalation gaps before Friday's close.

---

## 9. News triage for traders

Early reports are often wrong; markets react within seconds; false news spreads "farther, faster, deeper" (Vosoughi, Roy & Aral 2018, Science [K]) `[Moderate]`; large moves **without** news reverse while moves with news drift (Chan 2003 [K][SC]); reactions to stale news partially reverse (Tetlock 2011 [K]) `[Moderate]`. No systematic statistic on early-report error rates exists — fog-of-war evidence is case-based.

| Tier | Sources | Use |
|---|---|---|
| 1, official | Government/ministry/military statements on official channels; central banks; IEA/OPEC/EIA; UKMTO and JMIC maritime advisories; named on-record officials | Actionable — but belligerents' claims are themselves propaganda |
| 1, wire | Reuters, Bloomberg, Dow Jones, AP, AFP with named or multiple sources | Two *independent* wires ≈ confirmation |
| 2, specialist / physical | Lloyd's List, TradeWinds, Argus, Platts; AIS/tanker tracking (Kpler, Vortexa); IMF PortWatch; flight tracking; satellite imagery | Ground truth: are ships transiting, are barrels lost? |
| 3, single-source | One anonymous official, one outlet's scoop, foreign state media | Small size only, with a pre-set reversal stop |
| 4, social / OSINT | Telegram, X, viral video, accounts rewriting wires | Never trade alone; alert to check tiers 1-2; assume AI-generated media is possible |

**Confirmation rule:** act on two independent tier-1 sources, or one tier-1 plus tier-2 physical/market corroboration. Two wires quoting the same anonymous official are one source. `[Lore]`

**Triage protocol** `[Lore]`: (1) classify type and supply relevance (§2); (2) check tier and source independence; (3) corroborate in markets and physical data — OVX, Brent spreads, Tadawul/Asian futures, USD/JPY, gold; a move confined to one asset on a tier-3/4 headline is a reversal candidate; (4) ask what was priced (GPRT trend, event-contract odds, skew) — anticipated events "sell the rumour, buy the fact"; (5) size for the gap; (6) pre-commit a fade rule (no tier-1 confirmation within N minutes and contradicting physical data → fade); (7) log the report, its later status and the market reaction to build your own error rates.

**Fog-of-war and fake-news cases** `[K][SC]` (magnitudes not re-verified):
| Date | Case | Market |
|---|---|---|
| 23 Apr 2013 | Hacked AP tweet: White House explosions | ~$130bn+ erased, recovered in minutes |
| 15 Nov 2022 | Przewodów: "Russian missiles hit Poland" (one US official) → Ukrainian air-defence missile | Havens bid briefly, reversed |
| 17 Oct 2023 | al-Ahli hospital: initial attribution and casualty figures contested | — |
| 22 May 2023 | AI-generated "Pentagon explosion" image via verified accounts | US equities dipped briefly |
| 7 Apr 2025 | Misattributed 90-day tariff-pause headline, called "fake news" by the White House | Multi-trillion-dollar intraday swing |
| 8 Apr / 9 Nov 2026 | Truce; presidential remark that strikes were "highly unlikely" | Brent's biggest one-day fall since 1991 (library: spot -11.6%, front futures -13.3%); Brent -5.8% to $92.57 (contract not stated in the source) |

**Timestamps and market hours.** Record the event time in ET and whether US cash markets were open. Library conventions: after-close news is dated the next day (or keep the date and pass `--same-day`); weekend events anchor to Friday; intraday events are partly priced on day 0. Telegraphed events carry pre-drift (Iraq 2003 +8.7%, Ukraine -5.5%, Apr 2024 Iran -1.6% over the 5 prior days) — check `--pre`. Russia's invasion began pre-dawn Kyiv time 24 Feb 2022 = US evening 23 Feb. **Latency reality:** machine-readable-news algos win the first move; discretionary edge is in second-order effects (sector rotation, physical differentials, importer FX), fading unverified spikes, and positioning before scheduled risk. `[Lore]`

---

## 10. Sector and country exposure map

| Channel / event | Winners | Losers | Evidence |
|---|---|---|---|
| Geopolitical risk generally (US industries 1985-2019) | Precious metals, petroleum, defense | Shipping, transportation (9/11: transport -13%, precious metals +7.4%) | GPR paper `[V]` `[Moderate]` `[US]` |
| War risk, Iraq 2003 | Gold, energy | Consumer discretionary, airlines, IT; Turkey, Israel, several European markets, oil importers | LWZ `[V]` `[Moderate]` |
| Energy-supply war (library) | XLE first week (+2.3% excess, fades to -1.1% at 21d); ITA (+0.5% at 21d, 58%) | EEM (-0.8% / -1.1%) | `[computed]` `[Weak]` |
| Gulf / Hormuz | US terms of trade, USD, energy exporters outside the Gulf | Asian importers: 84% of Hormuz crude goes to Asia, China/India/Japan/Korea 69%; Qatar LNG buyers (~20% of world LNG); EM importers with weak reserves (TRY, INR, PKR, EGP — verify current balances) | EIA `[V]`; FX list `[Lore]` |
| Food / fertilizer | Fertilizer producers outside the zone | Importers of Gulf urea, ammonia, sulfur; Russia+Ukraine ~25-30% of pre-2022 wheat exports; Russia/Belarus potash | `[K][SC]` |
| Russia-Ukraine 2022 | Commodities, USD | Countries closer to Ukraine (~1pp per 1,000 km), Russian assets (MOEX shut ~a month, MSCI deletion at ~zero), LME nickel (suspended 8 Mar 2022 after ~250% two-day spike) | `[K][SC]` `[Weak]` |
| Taiwan / chips | — | Semis, TWD, Taiwan CDS; TSMC makes most (~90% often cited) leading-edge logic; Bloomberg Economics: war ~$10tn (~10% world GDP), blockade ~5% (VEN) | `[K][SC]` |
| Tariffs | Domestic producers of protected goods | Importers (full pass-through margin squeeze), firms with China sales or sourcing (Huang et al. 2023 [K][SC]) | ARW, AKW `[V]` `[Strong]` |
| Defense / fiscal | European defense (2025 re-rating; NATO 5%) | Core sovereign bonds via term premium (Bund Mar 2025) | `[K][SC]` |
| EM generally | Exporters with buffers | EMs with high debt, low reserve adequacy, weak institutions (≥2x the sovereign-premium rise); banks when home country or counterparts are involved | IMF GFSR 2025 `[V]` `[Moderate]` |
| Incumbent conflict beneficiaries | Firms whose rents depend on the conflict (Angola diamonds fell when the war ended) | — | Guidolin-La Ferrara `[K][SC]` |

---

## 11. Failure modes / traps

1. **Selling the first print of a non-regime shock.** Day-1 drops ≥2% were above their day-1 close 21 days later in 8/9. Check a user's "exit everything" plan against §6 before agreeing.
2. **Assuming Treasuries hedge a war.** In energy-supply shocks yields rose in half of risk-off weeks; a 60/40 book has no hedge for an oil war. Run the scenario tree with a DV01 leg.
3. **Assuming the yen hedges a war.** Japan imports its energy: yen up in only 35% of energy shocks.
4. **Chasing an oil spike on threat alone.** Risk-premium-only spikes were up at 21d in 38% of cases; the escalation itself often removes the premium (Desert Storm -30%, Fordow -12%).
5. **Not naming the oil contract.** 2026 Brent spot vs front futures diverged by 15 percentage points at 21d (+70.9% vs +55.6%); WTI vs Brent, spot vs futures and continuous price vs total return (roll) all differ. Backtests on FRED spot before 2006 need `--align` (sparse data stretches "5 days" into weeks).
6. **Using GPR to size.** Spike size did not predict the equity hit; tariff and financial shocks barely register in GPR (look at EPU/TPU). Daily GPR lags weekends and is noisy; use the 7-day mean and dated vintages.
7. **Quoting a type median as a forecast.** n=2-7 per type, hindsight selection, overlapping windows; quote the pooled channel split and name the confounders (read the CSV's `confounders` field before quoting any 63d number).
8. **Ignoring the baseline.** 2026 GPR and EPU baselines are at the 97th-99th percentile; "2x the 1-year median" is now a top-1% reading.
9. **Trusting policy buffers to replace barrels.** ~6 mb/d of offsets vs ~16-17 mb/d lost; buffers depleted as of Nov 2026.
10. **Assuming central banks look through.** Post-2021 they hike through energy shocks (2022, Sep 2026).
11. **Trading tier-3/4 headlines at full size,** or treating two wires citing one official as confirmation.
12. **Relying on stops across a weekend.** Saturdays hosted three of the biggest recent shocks.
13. **Buying event protection after the date is known** (5-16% rich), or holding permanent hedges without pricing their carry.
14. **Reading local FX under capital controls** (ruble 2022) or the franc under an SNB floor as sentiment.
15. **US-only analysis.** The largest moves are in local markets (KOSPI/KRW, MOEX/RUB, gilts/GBP, Gulf and Israeli assets), which the library does not cover.

---

## 12. Toolkit hooks

```
# Uncertainty, oil/gold vol, safe-haven FX, curve, spreads (block "Geopolitics, uncertainty & safe havens":
# USEPUINDXD, EPUTRADE, EPUNATSEC, GEPUCURRENT, OVXCLS, GVZCLS, DEXJPUS, DEXSZUS)
python scripts/fetch.py macro
python scripts/fetch.py gpr                                   # monthly: date,GPR,GPRT,GPRA,GPRH,GPRHT,GPRHA
python scripts/fetch.py gpr --freq daily --out-xls gpr_daily.xls   # date,GPRD; raw xls keeps acts/threats, MA7
python scripts/fetch.py fred DCOILBRENTEU DGS10 DGS2 T10YIE DFII10 DEXJPUS DEXSZUS DTWEXBGS OVXCLS VIXCLS \
    USEPUINDXD KCRORO WUIGLOBALWEIGHTAVG --start 1985-01-01 --out fred.csv
python scripts/fetch.py search "national security uncertainty"
python scripts/fetch.py prices ^GSPC --years 41 --out spx.csv  # also GC=F, BZ=F, CL=F, DX-Y.NYB, XLE, ITA, EEM, TLT

# Analog study on the shipped library (--align forward-fills every series onto SPX's calendar: needed for
# sparse FRED oil spot before 2006). DEXJPUS/DEXSZUS are yen/francs per USD, so a rise = yen/franc WEAKER
# (the library inverted them, 1/DEXJPUS, so that + = haven stronger).
python scripts/eventkit.py study --assets SPX=spx.csv BRENT=fred.csv@DCOILBRENTEU GOLD=gold.csv \
    UST10=fred.csv@DGS10,level UST2=fred.csv@DGS2,level VIX=fred.csv@VIXCLS,level USDJPY=fred.csv@DEXJPUS \
    --events-file assets/geopolitical_events.csv --type war_onset military_strike sanctions \
    --horizons 1 5 21 63 --pre 5 --bench SPX --align SPX --out geo_study.csv
# Same --assets, plus a new event alongside the library (or append a CSV row with type/channel/regime flag):
#   --events 2026-11-20=NewEvent      (--events and --events-file can be combined)
#   --same-day                        anchor at the event date's close (news after the US close)

# Scenario tree on the user's book (prices in %, ,dv01 legs in bp); --max-loss gives the de-risking factor
python scripts/eventkit.py scenarios --file tree.csv --pos SPX=1000000 UST10=400,dv01 GOLD=100000 OILCALL=10000 --max-loss 60000

# Hedge pricing
python scripts/tradekit.py bs --S 80 --K 88 --days 45 --vol 0.55 --kind call    # oil call cost and Greeks
python scripts/tradekit.py move --S 5800 --days 30 --event-vol 0.28 --base-vol 0.18   # implied event move
python scripts/tradekit.py move --S 5800 --days 7 --straddle 120                       # straddle-implied move

# Post-shock trend/breadth/vol read and gap-aware sizing
python scripts/scanner.py regime --universe etf-core --fetch
python scripts/tradekit.py size --equity 1000000 --risk 0.5 --entry 80 --stop 68     # stop at the assumed gap, not the chart level
```
`--type` values: war_onset, military_strike, terror, oil_supply_political, trade_tariff, election_referendum, sanctions, coup_regime_change, nuclear_missile, sovereign_political_crisis, chokepoint_shipping, deescalation. Filter by channel or regime flag by copying the CSV and keeping the rows you want (`primary_channel`, `regime_change` columns).

---

## 13. Key sources

- Caldara & Iacoviello (2022), "Measuring Geopolitical Risk," AER 112(4) — https://www.matteoiacoviello.com/gpr.htm
- Caldara, Conlisk, Iacoviello & Penn (2025 WP), GPR and inflation — https://www.matteoiacoviello.com/research_files/GPR_INFLATION_PAPER.pdf
- Caldara, Iacoviello, Molligo, Prestipino & Raffo (2020), Trade Policy Uncertainty, JME 109 — https://www.matteoiacoviello.com/tpu.htm
- Baker, Bloom & Davis (2016), "Measuring Economic Policy Uncertainty," QJE 131(4) — https://doi.org/10.1093/qje/qjw024
- Rigobon & Sack (2003/2005), war risk and US markets, NBER w9609 — https://www.nber.org/papers/w9609
- Leigh, Wolfers & Zitzewitz (2003), "What Do Financial Markets Think of War in Iraq?" NBER w9587 — https://www.nber.org/papers/w9587
- Berkman, Jacobsen & Lee (2011), JFE 101(2) — https://ideas.repec.org/a/eee/jfinec/v101y2011i2p313-332.html
- Kelly, Pástor & Veronesi (2016), "The Price of Political Uncertainty," JF 71(5) — https://www.nber.org/papers/w19812
- Brogaard & Detzel (2015), Management Science 61(1) — https://ideas.repec.org/a/inm/ormnsc/v61y2015i1p3-18.html
- IMF GFSR April 2025, Ch. 2; blog Fendoglu, Qureshi & Suntheim — https://www.imf.org/en/Blogs/Articles/2025/04/14/how-rising-geopolitical-risks-weigh-on-asset-prices
- Kilian (2009), "Not All Oil Price Shocks Are Alike," AER 99(3) — https://www.aeaweb.org/articles?id=10.1257/aer.99.3.1053
- Hamilton (2011), "Historical Oil Shocks," NBER w16790 — https://www.nber.org/papers/w16790
- Amiti, Redding & Weinstein (2019), JEP 33(4) — https://www.aeaweb.org/articles?id=10.1257/jep.33.4.187
- Ranaldo & Söderlind (2010), "Safe Haven Currencies," RoF 14(3) — https://ideas.repec.org/a/oup/revfin/v14y2010i3p385-407.html
- Baur & Lucey (2010), "Is Gold a Hedge or a Safe Haven?" Fin. Review 45(2) — https://ideas.repec.org/a/bla/finrev/v45y2010i2p217-229.html
- Brune, Hens, Rieger & Wang (2015), "The war puzzle," Int. Rev. Econ. 62(1) [SC] — https://doi.org/10.1007/s12232-014-0215-1
- EIA, Strait of Hormuz flows and bypass (16 Jun 2025) — https://www.eia.gov/todayinenergy/detail.php?id=65504
- Wolfers & Zitzewitz (2004), "Prediction Markets," JEP 18(2) — https://www.aeaweb.org/articles?id=10.1257/0895330041371321
- Mellers et al. (2014), Good Judgment Project, Psych. Science 25(5) [K] — https://doi.org/10.1177/0956797614524255
- Event library: `assets/geopolitical_events.csv` (45 events, 1990-2026; computed with `eventkit.py study`, Nov 2026)
