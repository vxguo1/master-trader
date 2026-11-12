# Market Forces: Microstructure, Dealer Hedging, Systematic Flows and Positioning

*Read when: a user asks why price moved without news, what "flows" are coming (opex, quarter-end, rebalances, CTA or vol-control selling, LETF into the close, buyback blackout), how to read GEX/0DTE/gamma levels, whether crowding or sentiment (COT, margin debt, short interest, put/call, AAII, FMS, crypto funding/OI) is a signal, how liquidity spirals and squeezes work, intraday timing (open, close, overnight, FOMC), crypto liquidation cascades, or when reviewing a plan or backtest that leans on any of these.*

## Contents
1. Core principles
2. Force map (master table)
3. Microstructure basics: spreads, impact, order flow, venues, the close
4. Dealer options hedging: gamma regime, vanna/charm, opex, 0DTE
5. Systematic flows: CTA, vol-control, LETF, pensions, buybacks, index, passive, inelastic markets
6. Flow calendar and checklist
7. Positioning and sentiment gauges
8. Reading positioning: signal vs noise decision guide
9. Liquidity and funding spirals
10. Squeezes, crowding, reflexivity
11. Intraday patterns
12. Crypto microstructure
13. Failure modes / traps
14. Toolkit hooks
15. Key sources

---

## 1. Core principles

- **Flow moves price in proportion to its size relative to depth, not to its "information".** Kyle's lambda, OFI and the square-root law all say impact = flow / depth. A forced $5bn sale in a thin book moves price more than a well-informed $500m one. *Why it matters:* always ask "how big vs ADV and depth, and over what window?" before attributing a move to news.
- **Forced, rules-based flow is forecastable; discretionary flow is not.** CTAs, vol-control funds, LETFs, pensions, index funds and buyback desks trade on price, volatility, calendar and index rules with public inputs. *Why:* this is the only part of "flow" an outsider can estimate ahead of time.
- **Positioning is fuel; price and volatility are the trigger.** Record margin debt, crowded longs or high perp OI say little about *timing*. They tell you the *amplitude* once a trigger (trend break, vol spike, margin hike) fires. *Why:* stops users shorting "because everyone is long".
- **Dealer gamma sign is a regime variable, not a price target.** Long dealer gamma dampens and mean-reverts; short dealer gamma amplifies and trends [Strong for direction]. Vendor "flip levels" are model inferences with large error [Contested]. *Why:* use it to choose fade-vs-follow tactics, never as support/resistance to the point.
- **Liquidity is pro-cyclical and disappears exactly when needed.** Market liquidity and funding liquidity reinforce each other (Brunnermeier-Pedersen) [Strong]. Depth can fall to under 1% of normal (May 2010). *Why:* size and stops must assume stress-time depth, not calm-time depth.
- **Concave impact explains market structure.** Impact grows with sqrt(Q/V), so big flows get worked over time and concentrated into auctions. *Why:* the close (and its 3:50pm ET imbalance) is the cleanest real-time read of mechanical flow.
- **Contrarian value is asymmetric and extreme-only.** Pessimism and capitulation extremes near bottoms have better support than euphoria near tops. Mid-range readings are noise [Moderate].
- **Spirals end when an unconstrained balance sheet steps in or forced sellers are exhausted.** Central banks, buybacks, real money, or OI collapsed / CTAs max short / vol-control at minimum exposure. *Why:* tells you when the same gauges flip from "danger" to "exhaustion".
- **Every flow estimate is dated and model-based.** Desk numbers (Goldman, JPM, Nomura) mostly reach us through secondary aggregators, flows net against each other, and they are widely front-run. *Why:* treat a "$33bn pension selling" headline as a conditional tilt, never a certainty.

---

## 2. Force map (master table)

| Force | Mechanism | Observable indicator | Data source | Typical magnitude (dated) | Evidence |
|---|---|---|---|---|---|
| Order-flow imbalance | Net adds/cancels/market orders at best quotes move price linearly; slope ~ 1/depth | OFI, top-of-book depth | Exchange L2/L3 feeds | Explains most short-horizon price change (Cont et al. 2014) | [Strong] |
| Metaorder impact | Square-root law: Y*sigma_d*sqrt(Q/V), Y ~ 1 | Order %ADV, daily vol | Own fills, TAQ | ~20 bp x Y for 1% ADV at 2% daily vol | [Strong] |
| Off-exchange internalization | Wholesalers internalize retail (PFOF); lit depth understates calm liquidity | TRF share of volume | Cboe, Rosenblatt, FINRA OTC | 50.6% of US vol (2025, record); 50.1% (Jul 2026); ATS 17.74% (2025) | [Strong] (measured) |
| Closing-auction concentration | Passive, index, LETF flow routed to the close | NYSE/Nasdaq imbalance messages | Exchange feeds, Rosenblatt | 6.18% (Apr 2025) to 9.31% (Mar 2025) of US vol; 7.54% (May 2026) | [Strong] (measured) |
| Dealer gamma sign | Long gamma: hedge against moves; short gamma: hedge with moves | GEX estimate, intraday return autocorrelation | SpotGamma, SqueezeMetrics, Cboe open-close | Vendor level error 30-50% claimed (self-published 2026) | [Strong] direction; [Contested] levels |
| Expiry pinning | Long-gamma MM re-hedging pulls price to big strikes | Clustering at strikes on expiry | OI by strike | Documented on monthly expiries | [Strong] |
| Vanna/charm into opex | Falling IV / time decay shrink dealer short hedges, forcing buying | IV trend into opex, put OI | Vendor models | None quantified peer-reviewed | [Lore] |
| 0DTE | Same-day gamma; balanced customer flow nets out | 0DTE share, customer net side | Cboe | 66.2% of SPX vol (Jul 2026, record); ~65% (Q3 2026); MM hedging <= ~0.2% of SPX liquidity (Cboe, May 2025) | [Contested] |
| CTA / trend | Time-series momentum signals on 1/3/12m lookbacks | Trend sign flips, desk trigger levels | Futures prices; desk notes (secondary) | Up to ~$70bn/wk equity selling est. (GS, ~8 Apr 2025); ~$48bn S&P futures sold over Apr 2025 | [Strong] signal; [Weak] $ estimates |
| Vol-control / risk parity | Exposure = target vol / realized vol, lagged | Realized vol (1-3m EWMA) | Price data | Vol-control equity alloc ~95% to ~52% (start-2025 to Apr 2025, GS via secondary) | [Strong] mechanism; [Weak] size |
| Leveraged/inverse ETF rebalance | AUM*(L^2-L)*r, always with the day's move, into the close | Day's return by 3:50pm, LETF AUM | Issuer AUM files | ~$2-9bn per 1% index move (2024 estimates; MS ~$7bn on ~$117bn AUM, Sep 2024) | [Strong] arithmetic; [Contested] price impact |
| Pension / balanced rebalancing | Fixed weight bands force selling winners at month/quarter-end | QTD stock vs bond relative return | Desk estimates (secondary) | ~$33bn US pension equity selling, Sep 2026 QE (GS, 98th pct since 2000); ~$165bn global, Jun 2026 (JPM) | [Weak] estimates; [Moderate] front-running cost |
| Buybacks | Corporate bid; absent in blackouts; 10b-18 limits | Blackout calendar, authorizations | GS buyback desk (secondary) | ~98% of S&P in blackout mid-Apr 2026; $410bn authorizations 2026 YTD (Apr 2026) | [Weak] |
| Index events | Forced trades at the effective-date close | Add/delete lists, recon prelim lists | S&P DJI, FTSE Russell, exchanges | Nasdaq close 4.59bn sh / $334.0bn (Jun 2026 Russell recon) | [Moderate]; index effect shrinking |
| Inelastic aggregate market | Mandate-bound holders absorb little; M = value change per $ flow | Fund flows into equities | Fund flow data | M ~ 5 (Gabaix-Koijen) vs M ~ 1 (Bouchaud) | [Contested] magnitude |
| Margin leverage | Margin calls force sales in drawdowns | FINRA debit balances | FINRA monthly | $1.502tn record (Jun 2026); ~$1.45tn (Aug 2026, secondary) | [Moderate] fuel; [Weak] timing |
| Aggregate short interest | Informed shorts; covering fuel at stock level | SI % float, days-to-cover, borrow cost | FINRA (2x monthly), lending data | Strongest known aggregate return predictor (Rapach et al. 2016) | [Strong] |
| Funding/liquidity spiral | Losses raise margins and haircuts, forcing sales and widening spreads | Depth vs 20d median, margin hikes, repo/basis moves | CME, NY Fed, OFR | E-mini buy depth <1% of morning (6 May 2010); basis trade ~$830bn (Sep 2025) | [Strong] |
| Crypto perp leverage | Liquidation engines and ADL create cascades | OI, funding, liquidations | CoinGlass, Amberdata, Kaiko, Velo | >$19bn liquidated, OI ~$175bn to ~$125bn (10-11 Oct 2025) | [Moderate] mechanism; [Weak] totals |
| Crypto real-money flows | Spot ETF and stablecoin issuance as slow bid | Daily ETF net flow, stablecoin supply | Farside, SoSoValue, DefiLlama | BTC ETF cum. ~$57.6bn (25 Sep 2026); 2026 YTD ~-$0.9bn (6 Nov 2026); stablecoins $308.0bn (13 Aug 2026) | [Weak] as predictor |

---

## 3. Microstructure basics

### Formulas (use these, not intuition)
```
Roll implied spread      s = 2*sqrt(-Cov(dp_t, dp_{t-1}))    (undefined if Cov >= 0)
Kyle impact              dp = lambda * net_order_flow,  lambda = sqrt(Sigma0) / (2*sigma_u),  depth = 1/lambda
OFI (best quotes)        bid adds - bid cancels - sell market orders, minus the same on the ask side; dp ~ OFI / depth
Square-root law          impact ~ Y * sigma_daily * sqrt(Q / V),  Y of order 1 (toolkit default 0.5-1)
Amihud illiquidity       ILLIQ = mean_d( |r_d| / dollar_volume_d )
```
- Roll (1984) [Strong]: a spread from trade prices only. Glosten-Milgrom (1985) [Strong]: the spread widens with the informed share. Kyle (1985) [Strong]: more noise trading means deeper markets, and insiders trade gradually.
- Spread components (Huang & Stoll 1997, large NYSE stocks, 1992 data): order processing largest, adverse selection smallest [Moderate; dated sample].
- Inventory: dealers shade quotes away from inventory (Ho & Stoll 1981). Spreads widen after large inventories or MM trading losses (Comerton-Forde et al. 2010) [Moderate].
- Returns to liquidity provision (short-term reversal) rise sharply with the VIX: liquidity evaporates because intermediaries withdraw (Nagel 2012) [Strong].
- OFI beats trade imbalance for short-horizon price changes (Cont, Kukanov & Stoikov 2014) [Strong]. The square-root law holds across markets (Toth et al. 2011) [Strong].
- Concavity: 10% of ADV costs ~3.2x what 1% costs, not 10x. That is why large flows are sliced and pushed into auctions.

### Informed vs uninformed flow
- PIN (Easley et al. 1996) [Moderate]. VPIN "toxicity" was claimed to spike before the May 2010 flash crash (Easley, Lopez de Prado & O'Hara 2012). Andersen & Bondarenko (2014) call that an artifact of trade-classification and volume-clock choices [Contested]. Do not use VPIN as a crash alarm.
- Retail identification: the BJZZ sub-penny price-improvement flag in TAQ. Retail order imbalance predicts returns over the following weeks (Boehmer, Jones, Zhang & Zhang 2021) [Moderate]. Read it as positive predictive sign, i.e. not contrarian at the stock level (sign from the paper; not re-verified this pass).
- Attention-driven herding (Robinhood "top-bought" events) is followed by negative returns (Barber et al. 2022) [Moderate]. Crowd *attention spikes* are contrarian; routine retail imbalance is not.
- Do not infer informed flow in the seconds after macro releases. Depth is mechanically withdrawn and spreads are wide (Fleming & Remolona 1999) [Strong].

### Venues, PFOF, tick size (US equities)
| Metric | Value | As of | Source |
|---|---|---|---|
| Off-exchange (TRF) share | 50.6% (+361 bp y/y, record) | FY2025 | Cboe 2025 Year in Review — https://www.cboe.com/insights/posts/2025-u-s-equities-year-in-review |
| Off-exchange share | 50.61%; dark pools (ATS) 17.74% | FY2025 | Rosenblatt LTBL #75 — https://www.rblt.com/market-structure-reports/let-there-be-light-us-edition-75 |
| Off-exchange share | 50.1% (+126 bp m/m) | Jul 2026 | TradersUnion on Cboe data (secondary) |
| Monthly record | 51.8% in a January (year unclear, 2025 or 2026) | — | Bloomberg Law (secondary) |
| ATS share range | ~14-17%, roughly flat | 2019-2025 | Nasdaq; Caplight |
| EDGX retail | +51.3% y/y, 30.4% of EDGX volume | FY2025 | Cboe |

- The rise is single-dealer/wholesaler internalization, not dark pools. In calm markets lit depth *understates* liquidity. In stress, wholesalers widen or route out, lit depth binds, and impact goes nonlinear (inference) [Moderate].
- Regulation: on 12 Jun 2025 the SEC withdrew 14 proposals, including the Order Competition Rule and Reg Best Execution. PFOF routing stays the status quo as of late 2026. FINRA 5310 best execution still applies.
- Rule 612 half-penny tick and Rule 610 access-fee cap amendments (adopted Sep 2024): compliance was relieved to 2 Nov 2026, then reportedly pushed to Nov 2027 (secondary reports, Jun 2026; the SEC order was not seen this session). Do not assume half-penny ticks are live.
- Options: retail is a very large share of US options volume, routed through a few wholesalers (Bryzgalova, Pavlova & Sikorskaya 2023) [Moderate; exact share not re-verified].

### Auctions and the close
- **NYSE (verified this session from the NYSE closing fact sheet):** MOC/LOC entry until 3:50pm ET. Imbalance publication starts 3:50:00pm, updated every second. After 3:50pm only orders offsetting the imbalance are accepted, and cancels are for legitimate errors only. Cancels are rejected after 3:58pm.
- **Nasdaq:** Nasdaq's own documents conflict on whether the MOC cutoff and NOII start are 3:50 or 3:55pm ET. Check the current Closing Cross spec before relying on a minute.
- Closing share of total US volume (Rosenblatt): 9.31% (Mar 2025, rebalance month), 6.18% (Apr 2025), 7.54% (May 2026).
- Records: NYSE close 3.57bn sh / $230.5bn (Mar 2026 rebalance day). NYSE close averaged 605.5m sh/day (Q1 2026). Nasdaq Closing Cross 4.59bn sh / $334.0bn (Jun 2026 Russell recon) vs 2.51bn / $102.5bn (Jun 2025).
- Buybacks avoid the open and close: the 10b-18 safe harbor excludes the opening print and the last 10 minutes (30 for less-active stocks), and caps volume at 25% of ADTV.
- Opening-auction share and the first/last-30-minute share of volume: no current primary figure found.

---

## 4. Dealer options hedging

### Regime table
| Dealer net gamma | Hedging behavior | Expect | Tactics | Evidence |
|---|---|---|---|---|
| Long (positive GEX) | Sell rallies, buy dips | Lower realized vol, intraday reversal, pinning to big strikes into expiry, end-of-day reversal | Fade extensions toward large strikes; sell rich short-dated premium cautiously; breakouts likely to fail | Ni, Pearson, Poteshman & White 2021 [Strong]; EOD-reversal WP [Moderate] |
| Short (negative GEX) | Buy rallies, sell dips | Higher realized vol, trend days, intraday momentum, level breaks accelerate | Follow first-half-hour direction into the last half-hour; widen stops; cut size | Baltussen, Da, Lammers & Martens 2021 (60+ futures) [Strong]; Barbon & Buraschi WP [Moderate] |

- Effects are strongest in illiquid underlyings (Barbon & Buraschi) [Moderate].

### GEX: how it is built and why it is fragile
```
GEX ($ per 1% move) ~ sum over strikes of  sign * Gamma * OI * 100 * S^2 * 0.01
sign: +1 calls, -1 puts under the SqueezeMetrics heuristic (dealers long calls, short puts)
```
Standard vendor construction; conventions vary.
- The dealer-sign assumption is unobservable. Vendors themselves say GEX "is all inference from assumptions, not an observed dealer book", and their estimates disagree [Contested].
- A self-published 2026 MPRA paper claims 30-50% error and systematic failure in four configurations [Weak]. A secondary summary of Jonsson & Nyberg (2025) says GEX changes predict next-day S&P returns, weaker after 2020 [Weak; original not verified]. There is no independent peer-reviewed replication of vendor levels.
- **Confirm the regime from realized behavior before trusting a vendor sign:**
  1. Intraday return autocorrelation or variance ratio on 5-30 min bars (autocorrelation < 0 or variance ratio < 1 suggests mean reversion and long gamma; autocorrelation > 0 or variance ratio > 1 suggests momentum and short gamma).
  2. Correlation of the first half-hour with the last half-hour (section 11).
  3. Realized vol vs implied vol: realized well below implied fits long gamma.

### Opex, pinning, vanna/charm
- Pinning: optionable stocks cluster at strikes on expiration dates, consistent with long-gamma MM re-hedging (Ni, Pearson & Poteshman 2005) [Strong].
- "Vanna/charm rally into opex, release after": falling IV and time decay shrink dealer short-delta hedges on customer-long puts, so dealers buy; monthly opex removes the support. This is a practitioner hypothesis with no peer-reviewed quantification [Lore]. Use it as a reason to watch, not a reason to trade.

### 0DTE
| Metric | Value | As of |
|---|---|---|
| SPX 0DTE share of SPX volume | 55% (record at the time) | Q1 2025 |
| | 63% / ~60% | Feb / Mar 2026 |
| | 66.2% (record) | Jul 2026 |
| SPX ADV / 0DTE ADV | 4.9m / 3.2m (~65%, record 0DTE) | Q3 2026 |
| 0DTE monthly ADV record | 3.4m | Sep 2026 |
| Net MM 0DTE hedging | <= ~0.2% of SPX daily liquidity; customer flow "extremely balanced" | Cboe, May 2025 |

Sources: Cboe Market Metrics Sep 2026; Cboe Jul 2026 volume release; SIFMA Insights Apr 2026; FOW May 2025; Cboe "0DTEs Decoded". Caveat: Cboe is the venue operator.

**Volatility effect is [Contested]:**
- *Dampens:* realized vol ~60 annualized bp lower on 0DTE days, identified from the Tue/Thu expiry introductions (SSRN, via Quantpedia). Dim, Eraker & Vilkov (2024) find higher 0DTE OI gamma goes with lower intraday vol.
- *Amplifies:* Brogaard, Han & Won (2023) find +1 SD of 0DTE volume raises S&P daily vol ~14%. UBS: it drives intraday but not necessarily close-to-close vol.
- Master view: 0DTE is a *conditional* amplifier. It matters when customer flow goes one-sided (panic put buying, call frenzy), which Cboe's daily averages mask.

### Expected move from options (apply the correction)
- ATM straddle ~ 0.8 * sigma*sqrt(T)*S, so the straddle approximates the expected *absolute* move. **1 SD ~ 1.25 x straddle** (not 0.8 x straddle).
- Run `python scripts/tradekit.py move --S <spot> --days <d> --straddle <price>`.

---

## 5. Systematic flows

### CTA / trend: trigger reconstruction
Time-series momentum is real across asset classes and a century of data (Moskowitz, Ooi & Pedersen 2012; Hurst, Ooi & Pedersen 2017) [Strong]. Desk "trigger levels" are these thresholds re-expressed as prices [Moderate].
1. Pull daily closes for the index future (ES, NQ, etc.).
2. Compute signs of the 1m (21d), 3m (63d) and 12m (252d) returns, and price vs the 50/100/200d SMA. Use `techkit.py indicators FILE`, and `techkit.py ruletest FILE --rule tsmom` or `--rule sma` for the current signal state.
3. A trigger price for an N-day lookback is the close N days ago (the return sign flips there); for an MA rule it is the MA value. List the nearest triggers above and below spot.
4. Position scales with blended signal x (target vol / realized vol). A vol spike cuts CTA size even with no sign change.
5. Flow is largest when a long medium-term uptrend with full positioning breaks. It exhausts as positioning reaches max short, then the same models flip to buyers. April 2025 example (GS via secondary): ~$70bn/week of selling estimated around 8 Apr, models flipped to buyers in all scenarios by ~21 Apr, ~$48bn of S&P futures sold over the month [Weak].
6. Trend followers can lose in choppy reversals: the SocGen trend indices were in the red in Q1 2025.

### Vol-control and risk parity
```
exposure_t = min(max_leverage, target_vol / realized_vol_t)      realized vol: EWMA, 1-3 month lookback
Example: 10% target, realized 10% -> 100%; realized 20% -> 50% (sell half)
```
- Mechanism [Strong] (it is the rule). Lags [Moderate, inference]: selling trails the vol spike by the lookback, and re-leveraging trails the calm. That fits the "slow grind back" rallies after vol shocks.
- Magnitude: vol-control equity allocation ~95% at start-2025 to ~52% after the Apr 2025 spike (GS via Tickmill) [Weak]. In Aug 2024 the VIX spike "was associated with immediate deleveraging pressures" (BIS Bulletin 90) [Moderate].
- Current CTA and vol-control/risk-parity AUM: no reliable 2026 primary figure. Say so if asked.

### Leveraged and inverse ETFs
```
rebalance_$ = AUM * (L^2 - L) * r_day     (always in the direction of the day's move, executed near the close)
2x: 2*AUM*r    -1x: 2*AUM*r    3x: 6*AUM*r    -3x: 12*AUM*r
```
(Cheng & Madhavan 2009) [Strong arithmetic].
- Per-1% estimates scale with AUM and are all dated: $1.04bn on ~$20bn AUM (Dec 2011, Fed FEDS 2013-48); ~$7bn on ~$117bn AUM (MS, Sep 2024); ~$2bn (Elm Wealth, Nov 2024); ~$9bn (Nomura, undated). No 2026 estimate found.
- Price impact is [Contested]: an EFMA 2024 paper finds late-day effects economically insignificant after controls, while desks (e.g. JPM) flag billions sold into down closes.
- Single-stock LETFs make this name-specific. On a big single-name day, size that name's LETF AUM x (L^2-L) x r against its closing-auction volume.

### Pension / balanced-fund rebalancing
- Rule [Moderate]: when equities beat bonds strongly over the month or quarter, fixed-weight holders sell equities into month/quarter-end, and vice versa.
- Dated estimates (all secondary) [Weak]: GS ~$33bn US pension equity selling into Sep 2026 QE (98th percentile since 2000); JPM ~$165bn global equity selling for Jun 2026, incl. ~$60bn from GPIF (splits differ by write-up); GS ~$23bn for Apr 2026 month-end.
- Calendar and threshold rebalancing is predictable and front-run, costing ~8 bp/yr, ~$16bn/yr (Harvey, Mazzoleni & Melone 2025; model-based; checked this session against press coverage and the authors' CFA blog) [Moderate]. Implication: the predictable part is partly priced *before* the date. Do not assume the final-day print carries it.
- Scale check (inference): with M ~ 5, $33bn implies ~$165bn of value impact, under 0.3% of an assumed ~$60tn+ US market cap (assumption, unsourced). It is meaningful only when it aligns with other one-way flows.

### Buybacks
- Blackouts are company policy, not law. They typically cover the run-up to earnings until shortly after the report [Lore]. Timing and volume limits come from 10b-18 (no open, no last 10/30 min, <=25% ADTV).
- Dated (GS desk via secondary) [Weak]: ~98% of S&P companies in blackout mid-Apr 2026, window reopening ~28 Apr. 2026 YTD authorizations $410bn, the most active on record to that point. May 2026 execution ran 1.2x 2025 YTD ADTV. Buyback volume typically falls ~35% at blackout start (Bloomberg-sourced, date uncertain).
- Use: the corporate bid is weakest in peak-blackout weeks. A shock during peak blackout lacks one of the main non-margin-constrained buyers.

### Index events and passive share
- **S&P 500 quarterly rebalances:** effective at the close on the third Friday of Mar/Jun/Sep/Dec (convention; coincides with quad witching).
- **Russell:** semi-annual from 2026. June is the full recon; Dec 2026 rank day was 30 Oct 2026, effective after the close **Fri 11 Dec 2026**, reconstituted indexes trade Mon 14 Dec. December style changes are limited to adds, deletes and R1000/R2000 moves (FTSE Russell, verified this session — https://www.lseg.com/en/insights/ftse-russell/looking-ahead-to-the-december-2026-russell-us-indexes-reconstitution). Expect a record-scale closing cross (Jun 2026: $334bn).
- The S&P inclusion "index effect" has shrunk dramatically since the 1990s (Greenwood & Sammon, NBER WP 30748) [Moderate]. Announcement-to-effective drift is mostly arbitraged.

| Passive milestone | Value | As of |
|---|---|---|
| US index equity funds > active equity funds | $4.271tn vs $4.246tn | Aug 2019 |
| All US funds: passive > active | $13.252tn vs $13.244tn | end-2023 |
| Passive share of US fund assets | ~55% | end-2025 |
| Index funds' share of total US market cap | ~19% (11% in 2015) | 2025 |
| Passive share (BI) | ~13% of US market, >20% of S&P 500 | Jan 2025 |
| ICI index-fund share / broad incl. non-fund passive | 18% / 30-35% | end-2023 |

Fund-asset share and market-cap share are different numbers. Users conflate them.

### Inelastic markets
- Gabaix & Koijen: M ~ 5, so $1 of flow into equities raises aggregate value by ~$5. The efficient-markets benchmark is M ~ 0. The mechanism is mandate-bound marginal holders (NBER WP 28967). The authors call it "a hypothesis".
- Bouchaud's microstructural reconciliation: M of order unity, rising with volatility and falling with the traded fraction of cap (arXiv 2108.00242). Magnitude is [Contested]; directional inelasticity is [Moderate].
- Use M for *aggregate* flows only. Do not apply 5x to single-stock trades; use the square-root law there.

---

## 6. Flow calendar and checklist

### Daily
1. **Pre-open:** overnight futures move (and where it happened: the European open ~2-3am ET carries the overnight drift), macro calendar times, and any one-way flow estimates published by desks.
2. **Gamma regime:** vendor GEX sign plus your own realized-behavior check (section 4). Note big-OI strikes and today's 0DTE share.
3. **CTA proximity:** distance of spot to the nearest 1m/3m/12m and MA trigger levels (section 5).
4. **Vol-control pressure:** 1m realized vol vs the prior week. A rising realized vol means lagged de-risking is still coming.
5. **Around 3:50pm ET:** NYSE imbalance (Nasdaq per current spec) plus the LETF estimate = AUM x (L^2-L) x day's return. The two should agree in sign on big days.
6. **Crypto:** funding, OI change vs price change, liquidation heat, prior-day spot ETF flow (Farside/SoSoValue).
7. **Stress tape:** top-of-book depth in ES/ZN/BTC vs its 20-day median, spreads, Amihud (section 9).

### Weekly
- CFTC COT (Tuesday positions, released Friday): Leveraged Funds and Asset Managers nets vs a multi-year range.
- AAII survey: only ±2 SD extremes matter.
- Spot BTC/ETH ETF weekly net flows; stablecoin supply change (DefiLlama).
- FINRA OTC transparency (2-4 week lag): ATS/non-ATS shifts in names you trade.
- Desk flow notes: CTA scenarios, buyback-desk blackout percentage.

### Monthly
- **Monthly opex (third Friday):** pinning into it in long gamma, hedge release after [Lore for vanna/charm].
- **Month-end rebalancing:** compare MTD stock vs bond returns. A large equity outperformance means selling pressure into the last days.
- FINRA margin debt (published with a lag of about a month): use the trend and y/y, not the level, as fuel.
- BofA FMS: cash level vs the sell (<=4.0%) and buy (~4.5-5%+) thresholds (secondary; thresholds vary by report).
- FINRA short interest (twice monthly): aggregate trend and single-name squeeze screens.

### Quarterly / annual
- **Quad witching and S&P rebalance:** third Friday of Mar/Jun/Sep/Dec. Record closing auctions cluster here.
- **Quarter-end pension rebalance:** QTD relative return. Note that it is front-run before the date (HMM 2025).
- **Buyback blackout:** roughly the weeks before earnings season through the reports. Bid weakest at peak (e.g. ~98% mid-Apr 2026).
- **Russell recon:** June (full) and December (semi-annual from 2026; next effective **11 Dec 2026**).
- **FOMC days:** pre-FOMC drift window (24h before) [Contested persistence]; liquidity withdrawal at the release.

### When flows are mechanically predictable (and when not)
| Flow | Predictable inputs | Timing precision | What breaks it |
|---|---|---|---|
| LETF rebalance | AUM, day's return | Very high (last minutes) | Intraday creations/redemptions; netting with other closing flow |
| Index adds/deletes | Published lists, effective date | Very high (one close) | Pre-positioning by arbs absorbs much of it |
| Vol-control | Realized vol path | Medium (lagged days to weeks) | Unknown lookbacks, caps, AUM |
| CTA | Price vs lookbacks/MAs | Medium (levels known, sizes not) | Signal blends differ by fund; vol scaling |
| Pension rebalance | MTD/QTD relative returns | Low-medium (window, not day) | Discretion within bands, front-running, netting |
| Buybacks | Earnings calendar | Low (company-specific) | Policy differences, ASR programs |
| Dealer hedging | OI by strike, vendor GEX | Low (sign unobservable) | Wrong dealer-sign assumption |
| Crypto liquidations | Visible OI, funding, liquidation levels | Low-medium (levels visible, trigger random) | Self-reported data, ADL, oracle failures |

---

## 7. Positioning and sentiment gauges

| Gauge | Cadence / lag | Evidence and horizon | Grade | Latest dated reading |
|---|---|---|---|---|
| CFTC COT (TFF categories) | Weekly; Tue data, Fri release | Hedging pressure predicts futures returns (de Roon, Nijman & Veld 2000); multi-week | [Moderate] | — |
| Aggregate short interest | FINRA, twice monthly | Strongest known aggregate predictor, in and out of sample (Rapach, Ringgenberg & Zhou 2016). High aggregate SI predicts *lower* market returns (sign from paper; not re-verified) | [Strong] | — |
| Stock-level put/call (opening buys) | Daily; needs open-close data (Cboe DataShop) | Low-P/C stocks beat high-P/C next day/week: informed flow (Pan & Poteshman 2006) | [Moderate] | — |
| Index total put/call | Daily | Noisy; distorted by 0DTE | [Weak] | — |
| AAII bull-bear | Weekly | 13/26-week relation (1987-2008) vanished 2001-08 (CXO); ~useless at 1 month (SF Fed via Option Alpha); bearish >2 SD extremes (4.1% of weeks) followed by +0.3%/+0.7%/+0.6% excess at 3/6/12m (LPL); +7.4% avg 6m after pessimism since 1990 (Schaeffer's, Sep 2025) | [Contested] | — |
| Baker-Wurgler composite | Monthly | High sentiment means low future returns for speculative, hard-to-arbitrage stocks (2006) | [Strong] (cross-section) | — |
| BofA Global FMS cash | Monthly | "Cash Rule" sell signal at <=4.0%; buy threshold reported as 4.5% or 5%+; one report: ACWI -2.4% avg next month after sells since 2011 (secondary) | [Weak] | 3.9% (May 2026), 4.1% (Jun), 3.6% (Jul), 3.5% (Aug 2026) (secondary) |
| FINRA margin debt | Monthly, ~1 month lag | Fuel for forced selling; weak timing | [Weak] timing | $1.502tn record (Jun 2026, ~+49% y/y); ~$1.417tn (Jul 2026, single source calls it the largest monthly drop on record); ~$1.45tn (Aug 2026, 247wallst) |
| Net investor credit / margin vs market | Monthly | Record-low net credit ~-$1.06tn; margin growth beat the market by 28 pts, widest gap since Oct 2007 (secondary) | [Weak] | Jun-Jul 2026 |
| PB gross/net leverage | Press only | Crowding and degrossing risk | [Weak] | Not found for late 2026; OFR Hedge Fund Monitor / Form PF are public proxies |
| Crypto funding / OI | Real time | No peer-reviewed predictor test found | [Weak] | — |

---

## 8. Reading positioning: signal vs noise decision guide

Run these steps in order whenever a user cites crowding or sentiment as a trade reason.

1. **Grade and horizon.** Look up the gauge above. If the user's horizon is shorter than the gauge's evidenced horizon (e.g. AAII for a 2-week trade, margin debt for next month), call it **noise for timing**.
2. **Is it extreme vs its own history?** Use percentile or z-score over a long window, e.g. outside the 10th-90th percentile or beyond ±2 SD. Mid-range readings are noise. One extreme gauge is weak; three independent ones agreeing (survey + positioning + options) is stronger [Lore].
3. **Who is crowded, and are they forced?** Crowding matters when the crowded holders are *levered or rule-bound*: margin accounts, perp longs, short-gamma dealers, vol-control, CTAs, shorts in a small float. Unlevered long-only crowding is mostly noise.
4. **Fuel or trigger?** Positioning is fuel. Require a trigger before acting: a trend-level break (CTA trigger), a realized-vol jump (vol-control), margin or haircut hikes, funding or repo spikes, or a catalyst outside liquid hours. **Fuel without trigger = risk-sizing input, not an entry.**
5. **Has the forced flow already happened?** Look for CTAs near max short, vol-control near minimum exposure, OI collapsed, funding negative, short interest covered, record ETF outflows done. If yes, the same gauge **flips to a contrarian/exhaustion signal**. This is the highest-value use of positioning data [Moderate].
6. **Apply the asymmetry.** Bearish extremes near bottoms have better contrarian support than bullish extremes near tops. Euphoria and record leverage can persist for months [Moderate].
7. **Check the sign convention.** Some "positioning" data is *informed* and should be followed, not faded: aggregate short interest, stock-level opening put/call, retail order imbalance over weeks. Faded: attention-herding spikes, survey extremes, crowded levered longs after a trigger.
8. **Translate into action.**
   - Signal + trigger: trade the forced flow with price confirmation.
   - Fuel only: cut leverage, use defined-risk structures, widen stops.
   - Exhaustion: scale into the reversal with tight invalidation.
   - Noise: say so explicitly and drop it from the thesis.

**Quick matrix**
| Crowding extreme? | Forced/levered holders? | Trigger fired? | Read |
|---|---|---|---|
| No | — | — | Noise |
| Yes | No | — | Mostly noise; mild contrarian at multi-month horizons |
| Yes | Yes | No | Fuel: reduce size and leverage, no directional entry |
| Yes | Yes | Yes, flow under way | Signal: expect amplitude; trade with the forced flow |
| Yes (already unwound) | Exhausted | After the fact | Contrarian / exhaustion signal |

---

## 9. Liquidity and funding spirals

- **Brunnermeier & Pedersen (2009)** [Strong]: margin spirals (vol up, margins up, forced selling, liquidity down, vol up) and loss spirals. Liquidity dries up suddenly, co-moves across assets and links to flight to quality.
- Broker-dealer leverage is pro-cyclical (Adrian & Shin 2010) [Strong]. Intermediary capital is a priced factor, and the primary-dealer capital ratio is a trackable stress gauge (He, Kelly & Manela 2017) [Strong].
- Liquidity risk premium: high-liquidity-beta stocks earned ~7.5%/yr more (Pastor & Stambaugh 2003); see also Acharya & Pedersen (2005). The characteristic liquidity premium has diminished (Ben-Rephael, Kadan & Wohl 2015) [Contested].

| Episode | Trigger | Spiral channel | Key stat | Lesson |
|---|---|---|---|---|
| Aug 2007 quant quake | Rapid unwind of a large quant L/S book | Crowding + deleveraging contagion (Khandani & Lo 2011) | Losses across similar strategies | Crowded factor books share an exit |
| 6 May 2010 flash crash | 75,000 E-mini (~$4.1bn) sell algo at 9% of volume, price-blind | Depth collapse | E-mini buy depth ~$58m, <1% of the morning; stub quotes at $0.01 / $100,000 (CFTC-SEC 2010) | Participation-rate algos with no price limit are dangerous |
| 15 Oct 2014 UST flash rally | No clear news | Liquidity vacuum | Rapid drop and full reversal in minutes (bp not re-verified) | Even the deepest market gaps |
| Feb 2018 Volmageddon | Short-VIX ETP daily rebalancing | Mechanical feedback (Augustin et al. 2021) | Record one-day VIX % jump; XIV terminated | Predictable rebalancing plus short vol = convex blow-up |
| Sep 2019 repo spike | Funding shortage | Funding liquidity (Anbil et al. 2020) | — | Watch repo as a trigger |
| Mar 2020 dash for cash | Customer selling > dealer balance sheet | Basis-trade unwind (Barth & Kahn 2021) | UST depth at GFC-nadir levels 12-17 Mar; Fed bought $775bn UST + $291bn MBS, 15-31 Mar 2020 | Safe assets can be illiquid; a central bank ended it |
| Sep 2022 UK LDI | Collateral calls on levered LDI | Textbook margin spiral | BoE long-gilt purchases announced 28 Sep 2022 | Leverage in "safe" mandates |
| 5 Aug 2024 yen carry | Carry unwind, >= $250bn yen loans (BIS) | Vol-driven deleveraging | VIX >65 intraday (from 23 on 2 Aug), close 38.57; Nikkei -12.4%, worst since 1987 | VIX rising far faster than spot falls is the deleveraging signature |
| Apr 2025 tariff shock | Macro shock | CTA + vol-control selling | Vol-control equity ~95% to ~52% (GS, secondary) | Mechanical sellers have a known lag, and flip |
| 10-11 Oct 2025 crypto | 100% China tariff headline, Friday evening US | Liquidations + ADL | >$19bn liquidated; OI ~$175bn to ~$125bn | Off-hours shocks plus perp leverage |

**Treasury basis trade:** ~$830bn as of Sep 2025, about double its early-2020 peak and ~35% of hedge funds' long UST exposure (Fed FEDS Note, 22 Jun 2026). OFR (19 Aug 2026): HF long cash UST $2.0tn vs short futures $1.4tn. The trade reportedly plateaued in 2026 (Reuters via secondary). Ignore an aggregator figure of $4.1tn: it has no primary source.

**Stress-detection checklist** (any 3 = treat as stress regime; cut size, use stress depth in impact estimates). Indicators are [Moderate, inference from the episodes]; the "any 3" and 25% thresholds are untested defaults [Lore]:
1. Top-of-book depth in ES/ZN/BTC below ~25% of its 20-day median (threshold is a default, not tested).
2. Bid-ask spreads widening; Amihud impact rising.
3. VIX rising faster than the spot decline implies (BIS Aug 2024 signature).
4. Swap spreads or the cash-futures basis moving sharply.
5. Repo or crypto funding spikes.
6. CME/exchange margin hikes (the funding-liquidity trigger).
7. Dealer gamma negative and realized intraday momentum present.

**Spiral end conditions:** an unconstrained balance sheet steps in (central bank, buybacks, real money), or forced sellers are exhausted (OI collapsed, CTAs short, vol-control at minimum).

---

## 10. Squeezes, crowding, reflexivity

- **Mechanism:** forced demand (covering, margin calls, dealer delta hedging of short calls, lending recalls) meets a small available float, and the price rise forces more buying. A gamma squeeze is the short-gamma regime around short-dated OTM calls (section 4).
- **VW, Oct 2008:** Porsche's disclosed control (shares plus cash-settled options) plus Lower Saxony's stake left little free float against heavy short interest. VW was briefly the world's most valuable company (Allen, Haas, Nowak & Tengulov 2021) [Strong; exact percentages not re-verified].
- **GameStop, Jan 2021** (SEC Staff Report, Oct 2021; paraphrased, verify wording) [Moderate]:
  - Short interest exceeded 100% of float.
  - Short covering was a *small* fraction of buying; social-media-driven long buying sustained the rise.
  - Options-MM hedging was not found to be the primary driver.
  - Broker restrictions followed NSCC margin calls: a funding channel.
  - *Lesson:* do not assume every squeeze is short covering or gamma.
- **Reflexivity (Soros 1987, 2013)** [Lore/theory]: beliefs move fundamentals through financing and collateral values, which validate the beliefs and produce boom-bust. Operationally: look for the price-to-collateral-to-funding loop.

**Squeeze-risk screen** (higher on more items):
1. SI % float and days-to-cover.
2. Cost-to-borrow and utilization.
3. Short-dated OTM call OI vs float and ADV.
4. Retail-attention spike.
5. LETF / single-stock LETF AUM.
6. Free-float constraints (locked holders, index inclusion).

The loop is reflexive only while forced flow dominates. Once SI is covered or call OI collapses, the same gauges signal *exhaustion*. A squeeze chased after covering is a long into vanished demand.

---

## 11. Intraday patterns

- **U-shaped volume and volatility** (Admati & Pfleiderer 1988; Jain & Joh 1988) [Strong]. The close's share keeps rising (section 3).
- **Intraday momentum:** the first half-hour return (from the prior close) predicts the last half-hour on SPY, stronger on high-vol, high-volume and news days (Gao, Han, Li & Zhou 2018) [Strong]. It holds across 60+ futures and is conditional on negative dealer gamma (Baltussen et al. 2021).
- **End-of-day reversal** in single stocks when MMs are long gamma near the close (Notre Dame WP) [Moderate].
- **Intraday periodicity:** a half-hour's return predicts the same half-hour on subsequent days (Heston, Korajczyk & Sadka 2010) [Moderate].
- **Overnight vs intraday:**
  - US equity returns historically accrue overnight (Cliff, Cooper & Gulen 2008) [Moderate].
  - Momentum earns overnight; most other anomalies earn intraday (Lou, Polk & Skouras 2019) [Moderate].
  - The overnight drift concentrates around the European open (~2-3am ET), linked to dealer inventory from closing imbalances (Boyarchenko, Larsen & Whelan 2023) [Moderate].
  - Persistence through 2024-2026 was not checked.
- **News:** at scheduled releases, depth collapses and spreads widen immediately, then volume and vol surge (Fleming & Remolona 1999) [Strong]. Pre-FOMC drift: S&P +49 bp on average in the 24h before scheduled announcements, 1994-2011 (Lucca & Moench 2015). Post-2015 persistence is debated [Contested].
- **Opening-range breakout:** no peer-reviewed support retrieved [Lore]. Demand the user's own cost-inclusive OOS test.
- Overnight (GTH) index options set records in 2026 (Cboe via TradersUnion). Overnight sessions are gaining liquidity, but books are still thinner.

**Intraday template** [Moderate, inference]:
1. Overnight gap plus first-30-minute direction sets the bias.
2. Midday is thin and noisy: lower conviction, smaller size.
3. Negative gamma: expect last-30-minute continuation of the day's direction.
4. Positive gamma: expect a fade and a pin toward big strikes.
5. From 3:50pm ET, read the closing imbalance plus the LETF estimate for the final print.

---

## 12. Crypto microstructure

- **Perpetuals:** no expiry; longs pay shorts funding proportional to the perp-spot premium. Perps are ~93% of crypto futures volume (MDPI 2026).
- Perp deviations from no-arbitrage are far larger than in FX. Funding carry earned high but decaying Sharpe ratios and is **not riskless** (He & Manela, arXiv 2212.06888) [Moderate].
- Venue risk is real: Hyperliquid carry underperformed Binance when perps traded at a discount, and the discount move swamped funding income (Robot Wealth) [Weak].
- **10-11 Oct 2025 cascade:**
  - Liquidations: >$19bn in ~24h (FTI).
  - Open interest: -$19.2bn (-14.08%) in 40 minutes (Amberdata); ~$175bn to ~$125bn in under a day (CoinShares).
  - Venue failures: Hyperliquid OI fell ~60%, and ADL closed some of the best-hedged shorts. A Binance oracle/pricing failure contributed (The Defiant).
  - Disputed: claims of >$50bn true losses or 10-20x undercounting are single-source [Contested]. All liquidation totals are exchange self-reported.
- **Cascade-risk signature** [Lore/Moderate]:
  1. OI rising faster than price.
  2. Persistently elevated positive funding.
  3. Thin weekend or off-hours books.
  4. A high share of OI on venues with ADL or immature oracles.
  5. A macro shock outside US equity hours.
- **Exhaustion signal:** after a cascade, collapsed OI plus negative funding is the crypto analogue of CTAs at max short.
- **Fragmentation:** large, recurrent cross-exchange deviations, especially across capital-control borders (e.g. the Korean premium), much smaller within countries (Makarov & Schoar 2020) [Moderate]. Price discovery increasingly happens in perps before spot (practitioner) [Weak].

| Slow "real money" flow | Value | As of |
|---|---|---|
| Stablecoin supply | $315bn; peak $322.4bn (17 May 2026); $308.0bn (13 Aug 2026); USDT ~59%, USDC ~23% | end-Q1 to Aug 2026 |
| USDC vs USDT adjusted transfer volume | $18.3tn vs $13.3tn | FY2025 |
| US spot BTC ETF cumulative net inflow | peak ~$63bn (Oct 2025), ~$53bn (Feb 2026), ~$57.6bn with $108.4bn net assets (25 Sep 2026) | dated as shown |
| Spot BTC ETF weekly flow | -$1.28bn (IBIT -$1.21bn), worst since June; 2026 YTD ~-$914m | week to ~6 Nov 2026 |
| Spot ETH ETF | ~-$365m, sixth straight outflow week | week to ~6 Nov 2026 |
| Prior-year comparison | record monthly outflow ~$3.5bn | Nov 2025 |

- Tether issuance after declines was associated with later BTC rises (Griffin & Shams 2020); Tether disputes this [Contested].
- Persistent ETF outflows (Oct-Nov 2026) remove a structural bid and raise sensitivity to perp-driven moves (inference).
- No peer-reviewed test of funding or OI as return or crash predictors was found. Present them as risk gauges, not alpha.

---

## 13. Failure modes / traps

- **GEX levels as precise support/resistance.** Ask which vendor, what dealer-sign assumption, and whether realized intraday behavior confirms the regime. If not confirmed, ignore the level.
- **Raw CBOE total put/call as sentiment.** It is 0DTE-polluted. Use opening-volume or longer-dated P/C, skew, or dealer-positioning data instead.
- **Shorting "record margin debt" or "crowded longs" with no trigger.** Fuel is not timing. Require a trigger (section 8 step 4).
- **Treating desk flow estimates as certain.** They are model outputs via secondary sources, they net against each other (pension selling vs buybacks vs LETF), and they are front-run. Convert to "tilt plus risk", never "will drop X%".
- **Aggregate short interest read as contrarian.** At the market level, high SI has been bearish (informed). Only single-name small-float squeezes are the contrarian case.
- **Backtests of closing or intraday strategies** filled at the official close with no imbalance or auction-impact cost, or using 3:59pm prices for "MOC" decisions made after the 3:50pm cutoff. Check order-entry timing against the cutoffs and add sqrt-law cost.
- **Lit depth = liquidity.** With >50% of volume off-exchange (2025-2026), calm-time lit depth understates liquidity, and stress-time depth can drop to a few percent of normal. Size for stress.
- **Reading informed flow into post-release prints** in the first seconds after macro data.
- **Stale data treated as live:**
  - COT is Tuesday data published Friday.
  - FINRA short interest and margin debt lag by weeks.
  - FINRA OTC transparency lags 2-4 weeks.
  - Vendor GEX history may be rebuilt with revised OI (look-ahead).
- **Applying M ~ 5 to a single stock**, or the square-root law to aggregate market flows. Use the right tool for the scale.
- **Front-running calendar flows on the day.** HMM (2025) show they are predicted and front-run. Edge, if any, sits earlier and is crowded.
- **Assuming 0DTE always amplifies, or always dampens.** The evidence is split. Condition on one-sided customer flow.
- **Trusting crypto liquidation totals** as complete, or funding carry as riskless (basis and venue risk, ADL).
- **Chasing a squeeze after covering.** Check whether SI or call OI has already collapsed.
- **Presenting any dated number as "current".** Every share, AUM or estimate in this file carries its date. Repeat the date to the user.

---

## 14. Toolkit hooks

- **Cost of a flow or order (square-root law):** `python scripts/tradekit.py impact --qty <shares> --adv <ADV> --price <px> --daily-vol 0.02 --spread-bps <bps> --y 0.7 --edge-bps <edge>`. For stress regimes, rerun with ADV cut to stress levels and a higher daily vol.
- **Expected move from a straddle (1 SD = 1.25 x straddle):** `python scripts/tradekit.py move --S <spot> --days <d> --straddle <price>`. From IV: `--vol 0.16`. Event isolation: `--event-vol <iv> --base-vol <iv>`.
- **Per-option gamma and vanna** (building blocks of GEX; aggregate GEX needs OI by strike outside the toolkit): `python scripts/tradekit.py bs --S <spot> --K <strike> --days <d> --vol <iv> --kind call|put`.
- **Realized vol for the vol-control exposure (target/realized):** `python scripts/tradekit.py vol FILE --window 21` (Yang-Zhang/EWMA). Exposure = target / realized.
- **Regime confirmation (reversal vs momentum)** on intraday bars: `python scripts/tradekit.py meanrev FILE --log`. Variance ratio <1 fits long gamma / mean reversion; >1 fits short gamma / momentum.
- **CTA trigger state:** `python scripts/techkit.py indicators FILE` (SMA, 12-1 momentum, Donchian). `python scripts/techkit.py ruletest FILE --rule tsmom --vol-target 0.15 --cost-bps 2 --oos 0.3`, or `--rule sma --params 50 200`.
- **Cross-asset trend ranking** (who CTAs are long/short): `python scripts/techkit.py rank FILE1 FILE2 ... --by voladj`.
- **Leverage survival in crowded or levered trades:** `python scripts/tradekit.py ruin --p <p> --b <b> --risk <pct> --trades <n> --limit 30` (risk and limit in %). Stress-sized stops: `python scripts/tradekit.py size --equity <E> --risk <pct> --entry <px> --atr <atr> --atr-mult 3`.
- **Order flow on trade data:** `python scripts/flowkit.py delta TRADES.csv --bar 1m` (buy/sell volume, delta, CVD, stacked imbalances, absorption, divergences), `flowkit.py profile FILE` (POC/value area/VWAP), `flowkit.py ofi QUOTES.csv` (Cont-Kukanov-Stoikov OFI, contemporaneous vs predictive R²), `flowkit.py book BOOK.csv` (depth imbalance, microprice). Free crypto tape and books: `python scripts/fetch.py trades BTC`, `fetch.py book BTC`. Depth on order-flow strategy: `order-flow.md`.
- No toolkit command computes GEX, LETF rebalance or COT z-scores. Do that arithmetic explicitly from the formulas above and show the work.

---

## 15. Key sources

- Kyle (1985), "Continuous Auctions and Insider Trading," *Econometrica* 53(6) — https://doi.org/10.2307/1913210
- Glosten & Milgrom (1985), *JFE* 14(1) — https://doi.org/10.1016/0304-405X(85)90044-3
- Cont, Kukanov & Stoikov (2014), "The Price Impact of Order Book Events," *J. Fin. Econometrics* 12(1); arXiv:1011.6402
- Toth et al. (2011), "Anomalous Price Impact...," *Physical Review X* 1, 021006 (square-root law)
- Ni, Pearson, Poteshman & White (2021), "Does Option Trading Have a Pervasive Impact on Underlying Stock Prices?" *RFS* 34(4)
- Baltussen, Da, Lammers & Martens (2021), "Hedging Demand and Market Intraday Momentum," *JFE* 142(1) — https://www3.nd.edu/~zda/intramom.pdf
- Cboe, "0DTEs Decoded" (May 2025) — https://www.cboe.com/insights/posts/0-dt-es-decoded-positioning-trends-and-market-impact ; Market Metrics Sep 2026 — https://www.cboe.com/insights/posts/market-metrics-that-matter-derivatives-september-2026-volume-highlights
- Moskowitz, Ooi & Pedersen (2012), "Time Series Momentum," *JFE* 104(2)
- Cheng & Madhavan (2009), "The Dynamics of Leveraged and Inverse ETFs," *J. Investment Management* 7(4)
- Gabaix & Koijen, "In Search of the Origins of Financial Fluctuations: The Inelastic Markets Hypothesis," NBER WP 28967 — https://conference.nber.org/conf_papers/f141240.pdf ; Bouchaud — https://www.arxiv.org/abs/2108.00242
- Harvey, Mazzoleni & Melone (2025), "The Unintended Consequences of Rebalancing" (WP)
- Rapach, Ringgenberg & Zhou (2016), "Short Interest and Aggregate Stock Returns," *JFE* 121(1)
- Pan & Poteshman (2006), "The Information in Option Volume for Future Stock Prices," *RFS* 19(3)
- Baker & Wurgler (2006), "Investor Sentiment and the Cross-Section of Stock Returns," *JF* 61(4)
- Brunnermeier & Pedersen (2009), "Market Liquidity and Funding Liquidity," *RFS* 22(6) — https://doi.org/10.1093/rfs/hhn098
- BIS Bulletin No 90 (27 Aug 2024), Aug 2024 market turbulence — https://www.bis.org/publ/bisbull90.pdf
- Fed FEDS Note (22 Jun 2026), hedge-fund Treasury exposures / basis trade — https://www.federalreserve.gov/econres/notes/feds-notes/decomposing-hedge-funds-u-s-treasury-exposures-20260622.html
- Gao, Han, Li & Zhou (2018), "Market Intraday Momentum," *JFE* 129(2); Lucca & Moench (2015), "The Pre-FOMC Announcement Drift," *JF* 70(1)
- He & Manela, perpetual futures pricing and funding — https://arxiv.org/html/2212.06888v5 ; FTI Consulting on the Oct 2025 crash — https://www.fticonsulting.com/insights/articles/crypto-crash-october-2025-leverage-met-liquidity
- Rosenblatt "Let There Be Light" #75 (2025 venue shares) — https://www.rblt.com/market-structure-reports/let-there-be-light-us-edition-75 ; NYSE closing auction fact sheet — https://www.nyse.com/publicdocs/nyse/NYSE_Auctions_Closing_Process_Fact_Sheet.pdf
