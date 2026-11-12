# Technical Analysis: Evidence-Graded Toolkit and Professional Use

*Read when: a user asks whether an indicator, chart pattern, candlestick, Fibonacci/Elliott/Gann level, Ichimoku or "smart money" concept works; wants an indicator explained, parameterized or combined; shows a chart setup, a Bulkowski statistic or a TA-based trade plan for review; asks how professionals use TA (regime filters, multi-timeframe, levels for stops and targets); or wants to turn a discretionary chart idea into a testable rule.*

Depth elsewhere: Brooks-style bar reading, market/volume profile, order flow, Wyckoff and ICT/SMC in depth are in `price-action.md`. Momentum and breakout playbooks (trend template, stage analysis, relative strength) are in `momentum-trading.md`. Trend following as a strategy family is in `strategy-playbook.md`. Deflated Sharpe, PBO and walk-forward design are in `quant-research-validation.md`. Stop and sizing mechanics are in `risk-sizing-execution.md`.

Conventions:
- **Inline confidence:** [Strong] / [Moderate] / [Weak] / [Contested] / [Lore].
- **Table ratings:** SUPPORTED = peer-reviewed support that is out-of-sample or robust to data snooping, in at least one major asset class. MIXED = conflicting, period-dependent or decayed. UNSUPPORTED = tested and failed. UNTESTED = no peer-reviewed test located (practitioner lore only).
- **Verification tags on numbers:** [V] = checked against the primary source, abstract or full text. [NR] = from the literature but not re-verified, so check it before quoting a figure to a user.
- **Absence of tests:** "No test located" means none was found with keyword search unavailable. Treat it as a gap, not proof that no test exists.

## Contents
1. Core principles
2. Where TA has an edge and where it doesn't
3. Indicator reference (trend, oscillators, volatility, volume, breadth)
4. Chart and candlestick patterns
5. Fibonacci, Elliott, Gann, Ichimoku, Wyckoff, SMC: candid status
6. Using TA the way professionals do
7. Making TA testable (procedure + `techkit.py ruletest`)
8. Failure modes / traps
9. Toolkit hooks
10. Key sources

---

## 1. Core principles

- **Presume no edge in a single daily rule on a liquid developed-market instrument.** Simple MA, filter and breakout rules made real money in US equities until about the mid-1980s and in major FX through the 1980s. Those profits faded once costs, universe-wide data-snooping corrections and true out-of-sample tests were applied [Strong]. A user's 50/200 cross on the S&P 500 has to prove itself before it gets any credit.
- **TA edges are conditional, and they live where arbitrage is weak.** They persist in diversified futures trend, emerging-market and minor FX, small/young/hard-to-value/high-volatility stocks, monthly timing of the aggregate equity premium, and high-sentiment regimes [Moderate]. Before asking about the setup, ask why the edge has not been arbitraged away in this market.
- **Every published edge decays.** Adaptive-markets evidence (Neely, Weller & Ulrich 2009; Taylor 2014) shows profits shrinking after discovery and moving to new venues, asset classes and frequencies [Moderate]. Apply that to every result in this file too.
- **Count information sources, not indicators.** Almost every indicator transforms close, range, volume or breadth. RSI, stochastics, Williams %R, CCI and Bollinger %B all measure one thing: how stretched price is. Real confluence means agreement across *different* sources (§3.0).
- **Levels work because orders rest there.** Take-profit orders cluster *at* round numbers, which produces bounces. Stop orders cluster *just beyond* them, which produces acceleration through the level. The effect is real but small: about 4-6 percentage points of extra bounce frequency in FX (Osler 2000 [V]) [Strong for the mechanism, Moderate for the size].
- **Exits and risk rules matter more than entry patterns.** Whether candlestick patterns are profitable depends on the holding rule, not the pattern or the trend definition (Lu, Chen & Hsu 2015 [V]) [Moderate]. Stops add value only when returns are serially correlated (Kaminski & Lo 2014) [Moderate].
- **A pattern can carry information and still not make money.** Patterns can shift the return distribution (Lo, Mamaysky & Wang 2000) and still lose to simpler rules after costs (Chang & Osler 1999 [V]) [Moderate].
- **TA's strongest uses are risk, regime and execution.** In order of evidence: volatility-based sizing, then slow trend filters, then level-aware execution and stops, then conditional signals in high-uncertainty assets. Standalone oscillator or pattern alpha comes last.
- **If an idea can't be coded, don't believe it yet.** A discretionary idea earns confidence only once it becomes a deterministic rule, tested over its full parameter grid, net of costs, out of sample, with every trial counted (§7).

---

## 2. Where TA has an edge and where it doesn't

### 2.1 The decay story in developed markets

| Market / test | Finding | Status |
|---|---|---|
| DJIA daily, ~100 years. Universe of filter, MA, S/R, channel and OBV rules (7,846 rules [NR]) with White's Reality Check (Sullivan, Timmermann & White 1999 [V design]) | The best rule (short-term MA) stayed significant over 1897-1986 after the full snooping adjustment. It **did not continue out of sample over 1987-96**. S&P 500 futures were not significant [NR] | Decayed [Strong] |
| DJIA 1897-2011, False Discovery Rate control (Bajgrowicz & Scaillet 2012 [V]) | FDR flags more "winning" rules, but **the future best rules could not be picked in advance**, and **even in-sample profits vanish with low transaction costs** | Decayed [Strong] |
| Every DJIA member 1928-2012 (Taylor 2014 [V]) | Momentum-type rule profits are concentrated **mid-1960s to mid-1980s** and depend on being able to short | Episodic [Moderate] |
| S&P 500, 2,580 models, daily (Schulmeister 2009 [V]) | Profitability declined steadily from 1960 and has been **unprofitable since the early 1990s** | Decayed [Moderate] |
| Mature vs young US indexes, Reality Check + SPA (Hsu & Kuan 2005 [V]) | Significant in the NASDAQ Composite and Russell 2000, **not** in the DJIA or S&P 500 | Conditional [Moderate] |
| US tech and small-cap sectors 1995-2010 (Shynkevich 2012 [V]) | Predictable in the first half after snooping correction. **No portfolio beat buy-and-hold in the second half** | Decayed [Moderate] |
| S&P 500, genetic-algorithm rules (Allen & Karjalainen 1999; content [NR]) | No out-of-sample excess return after costs. The rules mostly sat in the market during low-volatility, rising periods: a volatility-regime effect, not timing skill | UNSUPPORTED [Moderate] |
| S&P 500, 6,402 rules (Aronson 2006 [NR]) | No rule was significant after data-mining correction | UNSUPPORTED [Weak] |
| US, Japanese and W. European indexes, recursive OOS (Griffioen, via Wikipedia [V]) | Not profitable after small costs | UNSUPPORTED [Weak] |
| Major FX, previously published rules, true OOS (Neely, Weller & Ulrich 2009 [V]) | 1970s-80s excess returns were **genuine, not data mining**. Filter and MA profits **had gone by the early 1990s** | Decayed [Strong] |
| Bessembinder & Chan 1998 [NR] | The break-even round-trip cost of the Brock-Lakonishok-LeBaron (BLL) rules was small (~0.39% [NR]), and returns declined over time | Decayed [Weak] |

**Default stance:** a single-asset daily rule on the DJIA, S&P 500 or a major FX pair has no edge until it is shown out of sample, net of costs, with all trials counted.

### 2.2 Where edges persist

| Setting | Evidence | Grade |
|---|---|---|
| **Diversified futures trend (time-series momentum, TSMOM)** | TSMOM is significant in all 58 liquid futures. It persists 1-12 months, then partially reverses. It does best in extreme markets, and speculators profit at hedgers' expense (Moskowitz, Ooi & Pedersen 2012 [V]). Trend following was consistently profitable in simulation back to 1880 (Hurst, Ooi & Pedersen 2017 [V]). In 28 commodity futures over 48 years, MA and channel rules were positive after costs in ≥22 of 28 markets, robust to data snooping, and positive in *all* parameterizations (Szakmary, Shen & Sharma 2010 [V]) | [Strong] that the effect exists; capacity and crowding are a concern since the GFC (AQR [V]) |
| **Emerging and minor FX** | Profitable rules migrated toward EM currencies, and adaptive rule selection beat static rules (Neely & Weller 2013 [V]). Across 30 developed and EM currencies, >21,000 rules and a stepwise test found substantial predictability out of sample (Hsu, Taylor & Wang 2016 [V]) | [Moderate]; [Contested] for majors (§2.4) |
| **Small, young, high-volatility, hard-to-value stocks** | MA timing on volatility-sorted portfolios beats buy-and-hold. For high-volatility portfolios, CAPM/FF3 alphas exceed momentum's, unexplained by sentiment, liquidity or default risk (Han, Yang & Zhou 2013 [V]). MA-ratio predictability shows up in small-cap, young and low-coverage stocks and in the dot-com NASDAQ (Detzel et al. 2021 [V]). Survival after publication has not been checked | [Moderate] |
| **Multi-horizon trend in the cross-section** | A trend factor built from many MA lengths more than doubles the Sharpe of the reversal and momentum factors. In 2008-09 it earned +0.75%/month while the market lost 2.03% and momentum lost 3.88% (Han, Zhou & Zhu 2016 [V]). The 21-day/200-day MA distance predicts returns (Avramov, Kaplanski & Subrahmanyam 2021 [NR]) | [Moderate] |
| **Aggregate equity-premium timing (monthly)** | MA, momentum and OBV-volume predictors show significant in- and out-of-sample power, matching or beating 14 macro variables. TA catches the premium's **decline near business-cycle peaks**, and macro variables catch the rise near troughs. Combining the two improves forecasts (Neely, Rapach, Tu & Zhou 2014 [V]) | [Moderate] |
| **High-sentiment regimes** | Hedge funds that use TA show better returns, lower risk and better timing when sentiment is high. The advantage shrinks or reverses when sentiment is low (Smith, Wang, Wang & Zychowicz 2016 [V]) | [Moderate] |
| Emerging equity markets (older studies) | MA rules had some power in Taiwan, Thailand and Mexico, weaker after costs (Ratner & Leal 1999 [NR]). BLL rules worked in Malaysia, Thailand and Taiwan (Bessembinder & Chan 1995 [NR]) | [Weak]; probably decayed |

### 2.3 Support/resistance: the microstructure evidence (the best foundation of any "discretionary" concept)

- **Osler 2000 (FRBNY EPR) [V, full text].** Six FX firms published daily S/R levels for USD/DEM, USD/JPY and USD/GBP from Jan 1996 to Mar 1998. These were tested on 1-minute quotes against 20 artificial support and 20 artificial resistance levels per day.
  - Rates bounced off published levels **60.8%** of the time vs **56.2%** for artificial levels.
  - Published levels beat artificial ones in all 16 firm-currency pairs, significantly at 5% in all but three.
  - Average excess bounce was 4.2 pp (mark), 5.6 pp (yen) and 4.0 pp (pound).
  - Predictive power lasted **at least five business days** after publication.
  - Firms' own "strength" ratings had **no consistent relationship** with bounce frequency.
  - Firms agreed on only ~30% of possible level matches.
  - More than 70% of published levels ended in 0, and 96% ended in 0 or 5, against 10% and 20% if chosen at random.
- **Osler 2003 (JF) [V]**, using actual dealer-bank order books. Take-profit orders cluster *at* round numbers, which reverses trends there. Stop-loss orders cluster *just beyond* round numbers, which makes trends accelerate after a level breaks.
- **Kavajecz & Odders-White 2004 (RFS) [V].** S/R levels coincide with peaks in limit-order-book depth, and MA levels carry information about where depth sits. Technical rules work because they *locate depth already on the book*.
- **Bhattacharya, Holden & Jacobsen 2012 (Mgmt Sci) [V]**, >100M stock trades. Liquidity demanders buy in excess one cent below round numbers and sell in excess one cent above. The imbalance scales with roundness (integers > half-dollars > ...) and is stronger when price *reaches* rather than *crosses* the number. This behaviour costs liquidity demanders nearly $1B/yr.
- **George & Hwang 2004 [NR].** Stocks near their 52-week high outperform because investors anchor on that high and underreact. This subsumes much of standard momentum and is the academic basis for treating prior highs as reference levels.

**What this means for advice:**
1. S/R is a **zone** around round numbers and prior swing points where resting orders are likely, not a line.
2. Expect a modestly higher bounce probability, never certainty. A ~5 pp edge is not a reason to size up.
3. Ignore "strong level" labels. Published strength ratings carried no information, and firms disagreed on 70% of levels.
4. When a level breaks cleanly, expect acceleration, because the stops beyond it get triggered.
5. Don't place stops one tick beyond the obvious round number or swing, which is where they cluster and get run. Place targets *just before* round numbers.

### 2.4 Conflicts to flag explicitly

- **FX:** Hsu, Taylor & Wang 2016 find continued profitability using a broader rule universe that includes EM currencies. Neely, Weller & Ulrich 2009 find that major-currency MA/filter profits were gone by the early 1990s. Both can hold: the decay is in majors and simple rules. [Contested]
- **Intraday:** Schulmeister 2009 [V] reports S&P 500 30-minute models averaging **7.2%/yr gross** over 1983-2007, with no clear decline across eight subperiods (weaker in 2001-07). Marshall, Cahan & Cahan 2008 [V] tested 7,846 rules on US equities intraday and found **none profitable after data-snooping adjustment**. The difference is that Schulmeister reports gross returns without a universe-wide correction. The defensible statement: **intraday TA profitability is unproven net of costs and snooping** [Contested].
- **Crypto:** Detzel et al. 2021 [V] find that price-to-MA ratios forecast daily Bitcoin returns in and out of sample. Hudson & Urquhart 2021 [V] tested ~15,000 rules and found significant predictability, robust to multiple testing, with break-even costs well above typical costs, **but no out-of-sample predictability for Bitcoin**, while other coins still showed it. Corbet et al. 2019, Grobys et al. 2020, Gerritsen et al. 2020 and Liu & Tsyvinski 2021 (crypto TSMOM) are all [NR]. Overall rating: MIXED-to-SUPPORTED, with decay in BTC as the market matured [Contested].
- Most of these disagreements trace to differences in rule universe, cost treatment, sample period and test statistic. Ask which of these the user's source used.

### 2.5 Why TA works when it does (use this to find the counterparty)

| Mechanism | Implication | Source |
|---|---|---|
| Slow information diffusion → underreaction, then overreaction | Trends persist 1-12 months, then partially reverse | MOP 2012 [V]; Hong & Stein 1999 [NR] |
| Rational learning about hard-to-value fundamentals | MA ratios matter most in young, small and opaque assets | Detzel et al. 2021 [V]; Zhu & Zhou 2009 [V]; Brown & Jennings 1989 [NR] |
| Volume reveals the quality of traders' information | Volume is a legitimate conditioning input | Blume, Easley & O'Hara 1994 [V] |
| Order clustering at salient prices | Bounces at round numbers, acceleration beyond | Osler 2003 [V]; K&OW 2004 [V]; BHJ 2012 [V] |
| Anchoring on salient highs | 52-week-high proximity and breakouts are informative | George & Hwang 2004 [NR] |
| Sentiment plus limits to arbitrage | TA pays more when mispricing is large and shorting is hard | Smith et al. 2016 [V]; Taylor 2014 [V] |
| Non-fundamental order flow; hedgers paying speculators | FX TA, CTA trend premium | Menkhoff & Taylor 2007 [V]; MOP 2012 [V] |

Where *not* to look: generic oscillator thresholds on the most liquid US large caps at daily horizons.

**Not known (as of Nov 2026):**
- Whether the high-volatility-stock MA edge survived after publication.
- Any post-2020 peer-reviewed reassessment of FX technical rules.
- How much crypto TA has decayed since 2022.
- Out-of-sample performance of the exact Connors RSI(2) rules since 2009.

---

## 3. Indicator reference

### 3.0 Collapse the zoo: five questions, one tool each

| Question | Raw input | Interchangeable tools (pick ONE per row) |
|---|---|---|
| 1. Trend: which way, how persistent? | Close vs its past | MA slope or price vs MA, MA cross, MACD, Donchian position, TSMOM/ROC, regression slope, Ichimoku, Supertrend, +DI/−DI |
| 2. Stretch: how far is price from its recent range? | Close vs range | RSI, stochastics, Williams %R, CCI, Bollinger %B, Keltner position, distance from MA |
| 3. Volatility: expanding or contracting? | Range / SD | ATR, Bollinger BandWidth, Keltner width, squeeze, realized vol |
| 4. Participation: is the move confirmed? | Volume, breadth | Relative volume, OBV, A/D line, CMF; breadth (A/D, % above MA, McClellan, NH−NL) |
| 5. Location: where do orders sit? | Prior prices | Round numbers, prior swings, 52-week high/low, widely watched MAs, VWAP/AVWAP, profile POC/value area |

ADX measures trend *strength*, not direction, so it sits between rows 1 and 3. Rule: confluence is agreement **across rows**. Two tools from the same row are one signal counted twice.

### 3.1 Trend

| Tool (defaults) | Construction | How a master reads it | Common misuse | Evidence |
|---|---|---|---|---|
| **SMA / EMA** (10/20, 50, 100/200 daily; 10/40 weekly; Faber's 10-month) | SMA = mean of the last n closes. EMA_t = α·P_t + (1−α)·EMA_{t−1}, α = 2/(n+1). Wilder smoothing uses α = 1/n | The slope is the trend. Price vs the 200-day is a regime label. The 50/200-day lines are widely watched, so order depth sits near them (K&OW 2004) | Optimizing the length; counting several MA lengths as separate confirmations; backtests filled at the same close that generated the signal (Zakamulin 2014 [NR]) | SUPPORTED as diversified or multi-horizon trend; MIXED → decayed on a single developed index |
| **Golden/death cross** (50/200 SMA) | 50-day crosses above (golden) or below (death) the 200-day | A slow regime marker with large lag | Using it as a timing signal; media "death cross" stories | MIXED/UNTESTED as a named rule: tested only as one setting inside generic MA universes (STW 1999; Bajgrowicz-Scaillet 2012) |
| **MACD** (12, 26, 9; Appel) | MACD = EMA12 − EMA26. Signal = EMA9(MACD). Histogram = MACD − signal (Aspray 1986) | A zero-line cross *is* a 12/26 EMA cross. Histogram slope on the higher timeframe shows the momentum of the trend (Elder) | Counting MACD and an MA cross as two confirmations; divergence calls with no trigger | MIXED (weak): Chong & Ng 2008, Chong, Ng & Liew 2014 [NR]; lower-tier journals, no snooping correction |
| **ADX / DMI** (14, Wilder) | +DM = H_t − H_{t−1} if it is > 0 and > (L_{t−1} − L_t), else 0; −DM is the mirror. Wilder-smooth +DM, −DM and TR. +DI = 100·sm(+DM)/sm(TR); −DI likewise. DX = 100·\|+DI − −DI\|/(+DI + −DI). ADX = Wilder(DX). Needs ~150 bars to stabilize | A **regime classifier**: ADX > 25 (many use 20) and rising → use trend tools; < 20 → use range tools; 20-25 is a gray zone | Reading ADX as direction. Trading DI crosses alone, which whipsaw: ChartSchool pairs them with price > 50-day SMA and puts the initial stop at the signal-day low [V] | UNTESTED |
| **Donchian channel** (Turtles: 20- and 55-day entries, 10- and 20-day exits) | Upper = highest high of N bars, lower = lowest low, mid = average | A breakout above the prior N-bar high is the entry; the opposite, shorter channel is the exit. Turtle rules [NR]: N = 20-day ATR, 1 unit = 1% of equity per N, stop at 2N; System 1 skips the signal after a winning breakout | Single-stock breakouts with no volatility sizing; judging the rule on one market | SUPPORTED in commodity futures (Szakmary 2010 [V]); MIXED in equities after 1990 |
| **TSMOM / ROC** (1-12 months; also 10/12/20 days) | ROC_n = 100·(C_t/C_{t−n} − 1); the signal is the sign of the return | The academic trend signal. Blend lookbacks (AQR's construction is commonly described as an equal-weighted 1/3/12-month blend, volatility-scaled [NR]) | One lookback on one market; forgetting the reversal beyond ~12 months | SUPPORTED (MOP 2012 [V]; Neely et al. 2014 MOM(9)/(12), specification [NR]) |
| **Regression slope** (× R², Clenow [NR]) | OLS slope of log price on time over N bars, annualized, × R² | Trend quality, for ranking | Treating it as different information from momentum | UNTESTED as a named tool; economically ≈ TSMOM |
| **Supertrend** (ATR 10, ×3; popular defaults [NR]) | Bands at (H+L)/2 ± m·ATR(n). The line ratchets with the trend and flips when the close crosses it | A volatility-scaled **trailing stop**. Use it as an exit | Using it as an entry signal with an edge of its own | UNTESTED |

### 3.2 Momentum oscillators

| Tool (defaults) | Construction | How a master reads it | Common misuse | Evidence |
|---|---|---|---|---|
| **RSI** (14, Wilder; 70/30 or 80/20) | RS = Wilder average gain ÷ average loss over n. RSI = 100 − 100/(1+RS) | **Regime-relative.** Cardwell/Brown range rules: bull markets hold RSI ~40-80, bear markets ~20-60. "Overbought" in a strong trend means continuation. Watch failure swings | Shorting RSI > 70 in an uptrend; treating divergence as a signal on its own | MIXED (weak): scattered single-market tests (e.g., Wong, Manzur & Chew 2003, Singapore [NR]) |
| **RSI(2)** (Connors) | RSI with n = 2 | How deep a short-horizon pullback is inside an uptrend; exact rules in §7.3 | Dropping the 200-day filter; adding tight stops | MIXED: practitioner backtests only, not peer-reviewed |
| **Stochastic** (14,3,3; 80/20; Lane) | %K = 100·(C − L_n)/(H_n − L_n). Fast %D = SMA3(%K). "Slow" = (14,3,3) | Where price sits in its n-bar range. Same information as %R and RSI | Stacking it with RSI and CCI; trading %K/%D crosses | UNTESTED/UNSUPPORTED: appears only inside rule universes that fail snooping tests (Marshall, Cahan & Cahan 2008 [V]) |
| **Williams %R** (14; −20/−80) | %R = −100·(H_n − C)/(H_n − L_n) | An inverted, unsmoothed fast stochastic. Use one or the other | Using it alongside stochastics | UNTESTED |
| **CCI** (20; ±100; Lambert 1980) | TP = (H+L+C)/3. CCI = (TP − SMA20(TP))/(0.015 × mean absolute deviation). The constant puts ~70-80% of values within ±100 | ±100 breakouts as trend entries, *or* extremes as reversion. These are opposite uses, so state which one is meant | Using both readings at once | UNTESTED |
| **Short-horizon ROC** (days to weeks) | As in §3.1 | At days-to-weeks, single stocks show **short-term reversal** (Jegadeesh 1990; Lehmann 1990 [NR]). At 1-12 months the effect is trend | Mixing the two horizons | See §3.1 |

### 3.3 Volatility

| Tool (defaults) | Construction | How a master reads it | Common misuse | Evidence |
|---|---|---|---|---|
| **ATR** (14, Wilder) | TR = max(H−L, \|H−C_{t−1}\|, \|L−C_{t−1}\|). ATR = Wilder(TR) | Stop distance of 2-3×ATR; size = risk ÷ (k·ATR); normalizing signals across assets. Chandelier exit = highest high(22) − 3·ATR(22) (LeBeau [NR]) | Using it as a directional signal; fixed-% stops that ignore ATR | N/A as a signal. As a volatility input for vol-managed portfolios: SUPPORTED [Strong] for momentum (Barroso & Santa-Clara 2015 [NR]); [Contested] for factors in general (Moreira & Muir 2017 [NR] find gains; Cederburg et al. 2020 find most fail out of sample) |
| **Bollinger Bands** (20, 2) | Mid = SMA20; bands = mid ± 2σ20 (population SD). %B = (P − Lower)/(Upper − Lower). BandWidth = (Upper − Lower)/Mid. **Squeeze** = BandWidth at a ~6-month (≈125-bar) low | Bollinger's own guidance: pair the bands with a volume or momentum confirmer; a band tag is not a signal by itself; price walking the band means trend | Selling upper-band tags in a trend; reading direction from a squeeze | MIXED (weak): no consistent advantage over plain MA envelopes (Leung & Chong 2003 [NR]); contrarian rules mostly unprofitable (Lento, Gradojevic & Wright 2007 [NR]); positive in China after 0.50% costs (Balsara et al. 2007) |
| **TTM Squeeze** (Carter) | ON when BB(20,2) sits inside KC(20, 1.5 ATR); "fires" when the bands exit. Histogram = regression-smoothed [C − (Donchian20 mid + SMA20)/2]. Carter's rule: buy the first fired dot if the histogram is > 0 and rising; moves last ~8-10 bars | Volatility clustering predicts the **size** of the next move, not its **direction**. Take direction from trend (row 1) | Treating the squeeze as directional | UNTESTED/LORE; the mechanism is consistent with GARCH-type clustering |
| **Keltner** (20, 2.0, 10) | Modern (Raschke): EMA20 ± 2×ATR(10). Original (Keltner 1960): 10-day SMA of typical price ± 10-day average range | A breakout signals unusual strength. With a flat EMA and low or falling ADX, the bands work as overbought/oversold levels | Combining it with Bollinger position as "two" signals | UNTESTED |

### 3.4 Volume

| Tool (defaults) | Construction | How a master reads it | Common misuse | Evidence |
|---|---|---|---|---|
| **Relative volume** (10-50 sessions) | RVOL = current V ÷ average V. Intraday, compare at the same time of day | A conditioning variable. Unusually high volume over a day or week precedes appreciation the following month (Gervais, Kaniel & Mingelgrin 2001 [NR]). Volume predicts whether momentum persists or reverses (Lee & Swaminathan 2000 [NR]) | Comparing intraday volume to full-day averages | SUPPORTED cross-sectionally as a conditioner; theory in Blume, Easley & O'Hara 1994 [V] |
| **OBV** (Granville 1963) | OBV_t = OBV_{t−1} + V_t if the close is up, − V_t if down | OBV trend and divergence vs price. OBV-based monthly MA rules were among the predictors in Neely et al. 2014 [V] (specification [NR]) | Trading divergences alone | MIXED (some monthly aggregate support) |
| **VWAP** | Σ(P·V)/ΣV from the session open, using typical price per bar | **An execution benchmark**: algos split parent orders along the intraday volume curve. Intraday bias: above or below VWAP; ±1/2σ bands as reversion targets | Treating it as tested S/R | SUPPORTED as an execution benchmark (Berkowitz, Logue & Noser 1988 [NR]); UNTESTED as a signal |
| **Anchored VWAP** | Same formula, anchored at an event bar (swing high/low, earnings, gap) | The average cost of participants since the event. Several AVWAPs converging marks a zone (Shannon). See `price-action.md` | Picking anchors after the fact to fit the chart | UNTESTED/LORE |
| **A/D line, CMF** (20; Chaikin) | Money-flow multiplier = [(C−L) − (H−C)]/(H−L). MFV = multiplier × V. A/D = cumulative MFV. CMF = ΣMFV_20 / ΣV_20, usually within ±0.5 | Use a ±0.05 buffer around zero to avoid whipsaw; pair with a price oscillator | It ignores gaps (no prior close in the formula), so it diverges from price on gap days | UNTESTED |
| **Volume / Market Profile** | Point of control (POC), value area of ~70% of activity, initial balance. Depth in `price-action.md` | Candidate levels | Reading every node as S/R | UNTESTED directly; indirect support from depth peaking at S/R (K&OW 2004 [V]) |

### 3.5 Breadth (equity-index regime context)

| Tool | Construction | How a master reads it | Common misuse | Evidence |
|---|---|---|---|---|
| **A/D line, new highs − new lows** | Cumulative (advances − declines); NH − NL | Confirms index highs. Index highs without A/D confirmation mean a narrowing rally | Calling a top on one divergence | UNTESTED (no peer-reviewed tests located) |
| **% of stocks above 50/200-day MA** | Share of index members above their MA | >70-80% = broad or overbought participation; <20-30% = washed out (thresholds [NR]); 50% crosses as regime signals | — | UNTESTED |
| **McClellan Oscillator / Summation Index** | RANA = (A−D)/(A+D), ×1000 at StockCharts. Osc = EMA19(RANA) − EMA39(RANA), smoothing constants 0.10/0.05. Summation Index = running sum of the oscillator | Zero-line bias. A **breadth thrust** is a surge from below −50 to above +50. −100 = selling plunge. Readings stuck within ±30 = low conviction. Divergences need confirmation, and not every thrust leads to an extended advance [V] | Mixing thresholds across scales: the non-ratio-adjusted Summation Index uses overbought/oversold ≈ ±1000-1250 (Wikipedia [V]) | UNTESTED |
| **Zweig Breadth Thrust** | 10-day EMA of A/(A+D) rises from < 0.40 to > 0.615 within 10 trading days [NR] | A rare, regime-context event | Quoting "always higher 12 months later": the claimed ~15-20 signals since the 1940s are unverified, and N is tiny | LORE |

---

## 4. Chart and candlestick patterns

### 4.1 What the evidence says

| Pattern class | Evidence | Rating |
|---|---|---|
| Classical (H&S, broadening, triangles, rectangles, double tops/bottoms) | Kernel-regression recognition on US stocks 1962-96: "several technical indicators do provide incremental information" (Lo, Mamaysky & Wang 2000) | MIXED: [Moderate] that they carry information, [Weak] that they make money |
| Head-and-shoulders in FX | Daily dollar rates 1973-94: profitable in real time and bootstrap-significant, but **not efficient**, because simpler trend rules dominate it (Chang & Osler 1999 [V]) | MIXED |
| Head-and-shoulders in US stocks | Algorithmically identified tops predict lower risk-adjusted returns, especially combined with a market position (Savin, Weller & Zvingelis 2007 [NR]) | MIXED |
| Candlesticks in large caps | DJIA stocks 1992-2002: no value (Marshall, Young & Rose 2006; content [NR]). Large Japanese stocks: not profitable (Marshall, Young & Cahan 2008 [NR]). DAX/Bund intraday: no predictive power (Fock, Klein & Zwergel 2005 [NR]). DJIA intraday: not profitable after costs (Duvinage, Mazza & Petitjean 2013 [NR]). Horton 2009: little value [NR] | Leans UNSUPPORTED |
| 3-day reversal candles | Eight patterns on S&P 500 stocks 1992-96 were positive (Caginalp & Laurent 1998, via secondary [V]). On DJIA stocks with 0.5% costs and snooping adjustment, they are **profitable under the Caginalp-Laurent holding rule and not under the Marshall-Young-Rose rule**, whatever the trend definition. Robust at 0.1% costs and across subperiods, stronger in volatile markets (Lu, Chen & Hsu 2015 [V]). Taiwan: some bullish reversals profitable after costs (Lu, Shiu & Liu 2012 [NR]) | MIXED. **The exit rule drives the result** |
| Cup-with-handle, flags, pennants | No rigorous study outside Bulkowski's own was located; O'Neil's claims are practitioner lore | UNTESTED/LORE |
| Trendlines | No academic test located; inherently subjective (kernel methods could make them testable) | UNTESTED |

Bulkowski ranks 103 candle patterns. His own glossary implies that only a small minority are "investment grade" [V].

### 4.2 Reading Bulkowski statistics correctly

Definitions from his glossary [V]:
- **Breakout** = a close or move outside the pattern boundary (for H&S, a pierce of the neckline).
- **Performance** = from the **open the day after breakout** to the **"ultimate high"**: the highest peak before a ≥20% decline. The downside mirror uses the ultimate low.
- **Busted** = moves less than 10% after breakout, then closes on the other side of the pattern.
- **Throwback/pullback** = price returns to the breakout level within 30 days.
- **Break-even failure** = fails to move at least 5%.
- **Bull/bear regimes** = defined by S&P 500 declines of ≥20%.

His site's own caveats [V]: the figures are "perfect trades" with no commissions or fees. Some classifications use judgment, and sample sizes are given only as "hundreds" per pattern. The statistics were updated 7/7/2022 for the 3rd edition of the *Encyclopedia of Chart Patterns*. Examples from that update (bull market, upward breakouts) [V]:
- Rounded top reversal: 61%.
- Bump-and-run bottom: 55%.
- Eve & Eve double bottom: 50%.
- Cup-with-handle: 54%.
- Ascending triangle: 43%.
- Downward-breakout reversals average ~16-18% declines (diamond top 17%, complex H&S top 17%).

**When a user quotes "cup-with-handle averages 54%", convert it before using it:**
1. The ultimate high is an **ex-post exit no trader can know in advance**. Re-measure with a realistic exit: a fixed horizon, a trailing stop or a measured-move target.
2. **Subtract the market's drift** over the same holding window. Bull-market samples embed beta. Better still, benchmark against random-entry stocks with the same exit rule.
3. **Deduct costs**: commission, spread, slippage, and gaps through stops.
4. Allow for **selection bias**: patterns were identified by hand, in US stocks only.
5. Work from his **failure-rate, busted and throwback statistics**. They are more useful for decisions (stop placement, planning a second entry) than the average rise.

What is left after these adjustments is typically much smaller than the headline number (inference from his definitions). Never present it as an expected trade return.

### 4.3 Best use: patterns define risk, not edge

- The **pattern boundary is the invalidation point**. Put the stop beyond it, adjusted for stop clustering (§6.5), and size from the stop distance.
- The **measured move is a target candidate**. Then pull the target in front of the nearest round number or opposing level.
- A **throwback is a planned second entry** with tighter risk.
- A **failed or busted pattern is information**. A failed breakout runs the stops beyond the boundary, then reverses. This is the defensible core of "springs" and "liquidity sweeps".
- Trade continuation patterns **in the direction of the higher-timeframe trend**.
- Ask "what is the exit rule?" before "what is the pattern?" (Lu, Chen & Hsu 2015).

---

## 5. Fibonacci, Elliott, Gann, Ichimoku, Wyckoff, SMC: candid status

| Method | Core claim / construction | Status | How to coach it |
|---|---|---|---|
| **Fibonacci** retracements 23.6/38.2/50/61.8/78.6%; extensions 127.2/161.8% | Markets retrace in natural ratios | UNSUPPORTED: no evidence that Fibonacci ratios appear more often than chance in DJIA trend durations or amplitudes (Batchelor & Ramyar 2006 [NR]). Osler 2000 lists the "50% rule" and 38.2/61.8 as common heuristics [V]. **Own test (12 Nov 2026) [computed]:** an Osler-style reaction test on daily SPY (25y), EUR/USD (20y), BTC (12y) and gold (25y) — mechanical ZigZag swings evaluated only after confirmation, bounce of ≥1 ATR within 10 bars vs ~20 random control levels per swing — found pooled Fib reaction rates of −4.5 to −0.2 pts vs random (all p > 0.19), and no consistent edge across 3 swing/reaction settings (±6 pts, sign flipping). The skill does not ship a Fibonacci tool | At most a **coordination device**: if many traders put orders there, a small Osler-type effect is possible, but it did not show up in daily data. Treat it as one more S/R candidate, never a law, never the only reason for a stop. If a user insists, prefer prior swing pivots, round numbers and volume nodes, which carry the documented order-clustering evidence |
| **Elliott Wave** (Elliott 1938; Frost & Prechter 1978) | 5-wave impulse + ABC correction, fractal. Wave 2 never retraces >100% of wave 1; wave 3 is never the shortest; wave 4 does not overlap wave 1 | UNSUPPORTED/UNTESTABLE as practiced. Counts get revised after the fact, so it is close to unfalsifiable | Require the count's **invalidation level and an alternate count before the trade**. A count changed after the fact was not a forecast |
| **Gann** (1×1 angles, Square of Nine, time cycles) | Geometric and time harmonics | UNSUPPORTED/LORE: no peer-reviewed support located | Do not treat it as evidence |
| **Ichimoku** (Hosoda 1969; 9/26/52) | Tenkan = 9-bar (H+L)/2. Kijun = 26-bar midpoint. Senkou A = (Tenkan+Kijun)/2, shifted +26. Senkou B = 52-bar midpoint, shifted +26. Chikou = close shifted −26. Price above the cloud = uptrend | UNTESTED/LORE. Every component is a Donchian midpoint, so it is a **multi-length channel-midpoint trend system** | Treat it as row 1 of §3.0. Test it with `donchian`/`sma` proxies. Cloud, Kijun and Tenkan are not three confirmations |
| **Wyckoff** | Composite Man; laws of supply/demand, cause/effect, effort/result. Accumulation phases A-E (SC, AR, ST, spring, SOS, LPS) and the distribution mirror (UTAD); P&F counts for targets | UNTESTED/LORE. The **spring** mechanically matches Osler's stop-run | Useful vocabulary for ranges, breakouts and failed breaks. Depth in `price-action.md` |
| **SMC / ICT** (order blocks, fair value gaps, liquidity sweeps, premium/discount, kill zones) | Institutional "footprints" | UNTESTED/LORE. Mostly relabelled gaps, S/R, failed breakouts and springs/upthrusts. The "institutional intent" story is unfalsifiable as usually taught. Defensible core: stops cluster just beyond obvious levels (Osler 2003 [V]) | Keep only the codable parts (e.g., sweep = wick through a swing point, then a close back inside) and demand a test. Depth in `price-action.md` |
| **Supply/demand zones** | The base before an explosive move; "fresh" zones hold | UNTESTED | One more S/R zone candidate |
| **Dow Theory** | Primary, secondary and minor trends; the averages must confirm; volume confirms; a trend persists until a definite reversal | MIXED: Hamilton's 1902-29 WSJ calls earned positive risk-adjusted returns (Brown, Goetzmann & Kumar 1998 [NR]); no out-of-sample test | Historical support for trend persistence, not a modern rule |
| **Market structure** (HH/HL, break of structure, change of character) | The first lower low ends an uptrend | UNTESTED as a standalone signal. In Lu-Chen-Hsu, the trend definition mattered less than the holding rule [V] | A trend definition. Code it with fractal/zig-zag swings and test it |
| **Market/volume profile, AVWAP** | Value area, POC, event-anchored average cost | UNTESTED directly; indirect support from depth clustering (K&OW 2004 [V]) | Candidate levels. See `price-action.md` |

---

## 6. Using TA the way professionals do

### 6.1 Hierarchy of uses (by strength of evidence)
1. **Risk and position sizing with volatility** (ATR/σ scaling). [Moderate-Strong, via the volatility-scaling literature]
2. **Slow, diversified trend filters.** [Strong]
3. **Execution and level-aware stop/target placement.** [Moderate]
4. **Conditional signals in high-uncertainty assets or regimes.** [Moderate]
5. **Discretionary patterns and oscillators as standalone alpha.** [Weak]

### 6.2 Who uses it, at what horizon
- **FX:** more than 90% of FX participants use TA (Osler 2000, citing Taylor & Allen 1992 and Lui & Mole 1998 [V]). About 90% of London chief dealers put some weight on it at intraday-to-one-week horizons, while fundamentals dominate at a year or more (Taylor & Allen 1992; content [NR]).
- **Fund managers:** in a 692-manager survey across five countries, ~87% put some importance on TA, and it is the preferred tool at horizons of weeks (Menkhoff 2010 [NR]).
- **Hedge funds:** about one-third use TA [NR]. They benefit when sentiment is high (Smith et al. 2016 [V]).
- **CTAs** run TSMOM across futures. AQR flags capacity concerns: more assets in the strategy and higher cross-market correlations since the credit crisis [V].
- **CMT Association:** three exam levels; 2,500+ charterholders in 137 countries (as of Nov 2026) [V]. The curriculum runs from charting to behavioral finance, quantitative testing and risk.
- **Pattern of use:** TA's weight rises as the horizon shortens. It is used as a **timing and risk overlay** on fundamental or macro views (entry, exit, stop, size), not as the thesis. Sell-side technical notes typically stress trend state, key levels and breadth confirmation rather than single-indicator signals (synthesis, [Lore]).

### 6.3 Regime and trend filters

| Filter | Rule | Use | Evidence |
|---|---|---|---|
| 200-day SMA | Long only above it (the Connors filter) | Gate mean-reversion longs; label the trend state | [Lore] as a filter. MA-timing outperformance is often concentrated in a few bear markets, and some studies fill at the signal close (Zakamulin 2014, 2017 [NR]) |
| 10-month SMA (Faber 2007 [NR]) | Monthly close above/below | Tactical asset allocation | [Weak-Moderate]; same caveats |
| TSMOM sign over 1/3/12 months | Blend of signs | Trend regime for any asset | [Strong] |
| ADX(14) | > 25 (or 20) and rising → trend tools; < 20 → range tools | Choose which kind of system to run | [Lore] |
| Volatility / information uncertainty | High-vol, young, small, low-coverage names | Where MA timing adds most | [Moderate] (HYZ 2013; Detzel 2021) |
| Sentiment | High vs low sentiment | TA adds more when mispricing is large and shorting is constrained | [Moderate] (Smith 2016) |
| Business cycle | Combine TA with macro | TA catches the premium's decline near peaks; macro catches troughs | [Moderate] (Neely 2014) |
| Weinstein stage / trend template | 30-week MA slope; Minervini's 8-point template (the toolkit checks 7; RS is not included) | Stock-selection filter. See `momentum-trading.md` | [Lore] |

A regime filter is itself a parameter. Count it as a trial, and test the system both with and without it.

### 6.4 Multi-timeframe alignment
- **Elder's Triple Screen** (Elder 1993 [NR]):
  - Higher timeframe, about **5×** the trading timeframe, sets direction (e.g., weekly MACD-histogram slope).
  - Middle timeframe: an oscillator times pullback entries in that direction.
  - Lowest timeframe: a trailing buy-stop handles execution.
- **Why it helps:** it diversifies across trend horizons and reduces noise. Combining short, intermediate and long trends beats any single horizon (Han, Zhou & Zhu 2016 [V]; TSMOM blends 1-12-month lookbacks, MOP 2012 [V]). It is not validated as a standalone edge [Weak].
- **Practice** [Lore]:
  - The higher timeframe gives permission, the trading timeframe gives the setup, and the lower timeframe gives the trigger and the stop.
  - When timeframes conflict, trade smaller or stand aside.
  - Never use a lower timeframe to override the higher one's invalidation point.
- **Trap:** adding timeframes until one agrees is multiple testing.

### 6.5 Levels for entries, stops and targets
1. **Map levels:**
   - Round numbers: 00 first, then 50. Over 70% of published FX levels ended in 0 (Osler 2000).
   - Prior swing highs and lows.
   - The 52-week high and low.
   - The 50- and 200-day MAs.
   - Session VWAP and event AVWAPs.
   - Gap edges.
2. **Make zones**, e.g., "a round number or prior swing within k×ATR". Use the same definition you would code (§7.1).
3. **Entries:**
   - Fade a zone only in a range regime (low ADX, flat MAs), with invalidation just past the zone.
   - In a trend regime, expect clean breaks to accelerate, because the stops beyond get hit. Prefer the throwback retest to chasing.
4. **Stops:** do not place them one tick beyond the obvious level, where the stop cluster gets run. Go beyond the cluster by a volatility buffer and **size down to keep risk constant** [Lore, derived from Osler 2003].
5. **Targets:** just before round numbers and opposing levels, where take-profit clusters reverse price (Osler 2003 [V]).
6. **Execution:** liquidity demanders pay up around round numbers (BHJ 2012 [V]). Use limit orders, and don't anchor market orders to round prices (inference).

### 6.6 Confluence vs indicator redundancy
- **Real confluence** comes from different rows of §3.0. Example: the trend is up (12-month TSMOM positive); price pulls back to a prior breakout level near the 50-day MA (location); volume is light on the pullback and rises on resumption (participation); the stop is sized in ATR (volatility).
- **Redundancy:**
  - RSI + stochastics + CCI.
  - MACD + an EMA cross.
  - Ichimoku cloud + Kijun + Tenkan.
  - Bollinger + Keltner position.
  - Several MA lengths on one chart.
- Every added filter cuts the trade count (less statistical power) and adds a free parameter (more snooping). Coaching heuristic [Lore]: one tool per question. If the setup needs a fifth confirmation, the first four were not saying much.

### 6.7 TA as an execution and risk tool; stop-loss theory
- **ATR stops and sizing:** stop = k×ATR (k ~ 2-3); size = risk ÷ (stop distance × multiplier). This is Turtle N-sizing [NR]; TSMOM implementations also scale by ex-ante volatility (MOP 2012 [V]).
- **Trailing exits** (chandelier, Supertrend, opposite Donchian channel) belong to trend systems.
- **VWAP** benchmarks execution quality.
- **Kaminski & Lo 2014** (*J. Financial Markets* 18:234-254) [V citation and abstract]. Applied to buy-and-hold on daily index futures, certain stop-loss policies **"can increase expected return while substantially reducing volatility"** at longer sampling frequencies [V]. The paper's framework result (from the full text [NR]): under a random walk, stops *reduce* expected return; they add value only when returns are serially correlated (momentum, regime switching). Lo & Remorov 2017 extend this to serial correlation, regime switching and costs [NR].

| Return dynamics at the holding horizon | Effect of a stop | Practice |
|---|---|---|
| Positive autocorrelation / trending (trend following, breakouts) | Can raise expected return and cut volatility | Use initial and trailing stops (2N, opposite channel, chandelier). Here the stop is part of the edge |
| Random walk | Lowers expected return slightly and only reshapes risk | Use the stop as a **risk-budget device**, not a source of alpha. Size so that a stop-out equals the planned 1R |
| Negative autocorrelation / mean-reverting (RSI(2), Bollinger reversion) | Tight stops exit just before the reversion. Connors found stops hurt his stock and index results [V] | Control risk with small size, the regime filter, a cap on concurrent positions, and at most a wide catastrophe stop [Lore]. Size for the fat left tail |

To decide, run the system with and without the stop and keep whichever survives out of sample. `techkit.py ruletest` has no stop parameter, so stop variants must be tested separately and counted as extra trials.

---

## 7. Making TA testable

### 7.1 Procedure: discretionary idea → codable rule → grid → costs → OOS → multiple-testing adjustment
1. **Name the mechanism and the counterparty** (§2.5). If you can't say why the edge exists in *this* market, expect noise.
2. **Write definitions that can be computed at the right edge of the chart:**
   - Swing point = N-bar fractal or zig-zag.
   - Level = round number or prior swing within k×ATR.
   - Pattern = a sequence of local extrema with tolerance bands (the Lo, Mamaysky & Wang kernel approach).
   - Trend = price vs MA, or the sign of the k-bar return.
3. **Fix entry, exit, stop, size and execution price before looking at any result.** The exit rule matters most.
4. **Start from the closest `techkit` baseline** (§7.2). Examples:
   - "Buy new highs" → `donchian`.
   - "Above the 200-day" → `sma`.
   - "Golden cross" → `cross 50,200`.
   - "Buy dips in uptrends" → `rsi2` or `bbrev`.
   - "Cloud trend" → `donchian`/`sma` proxy.

   The discretionary embellishments must **beat the plain baseline** to count for anything.
5. **Parameter grid:** run the default grid or a wider one. Accept only **broad plateaus** (e.g., MA 50-250 × exits 10-50 days), never isolated peaks. Szakmary's "all parameterizations positive" is the standard to aim for.
6. **Costs:**
   - Set `--cost-bps` to a realistic per-side cost (spread + commission + slippage) per unit of turnover.
   - Rerun at double that cost as a stress test.
   - Add borrow and funding costs for shorts outside the tool.
   - At short horizons, costs decide the outcome: even in-sample profits vanish at low costs (Bajgrowicz-Scaillet [V]).
7. **Out of sample:**
   - Hold out ≥30% (`--oos 0.3`).
   - Then walk forward across periods and **other markets**.
   - Run a **persistence test**: select the best rule in window t, evaluate it in t+1. Schulmeister's top-25 models persisting is the evidence to demand. Bajgrowicz-Scaillet's failure is the base case.
8. **Multiple testing:**
   - Log every variant, rule, market and filter tried, and pass the multiplier via `--extra-trials`.
   - Read the deflated Sharpe.
   - For large rule universes, use Reality Check, SPA, stepwise tests or FDR.
   - New signals face a t > 3 hurdle (Harvey, Liu & Zhu 2016 [NR]).
   - Depth: `quant-research-validation.md`.
9. **Benchmarks:** compare with buy-and-hold (the tool prints it) **and** with random entries using the same exits and exposure (build that separately). This is the benchmark Bulkowski's numbers lack.
10. **Regime split:** trend vs range, high vs low volatility, bull vs bear, high vs low sentiment. An edge that lives in one regime needs a regime filter, and that filter must be tested too.
11. **Accept only if** all of these hold:
    - The grid is a plateau.
    - Out-of-sample Sharpe is positive and has not collapsed.
    - The deflated Sharpe is supportive.
    - The result survives the cost stress.
    - It works in more than one market.

    Then haircut the result, size small, and watch for decay.

### 7.2 What `techkit.py ruletest` actually does

| `--rule` | Position logic (decided at the close of bar t) | Default grid | Notes |
|---|---|---|---|
| `sma` | Long if close > SMA(k); otherwise flat, or short with `--short` | 20, 50, 100, 150, 200, 250 | `--params 50 200` runs **two separate SMA tests**, not a cross |
| `cross` | Long if SMA(f) > SMA(s) | f ∈ {10, 20, 50} × s ∈ {100, 150, 200} | Pass fast,slow pairs: `--params 50,200` or `20,100 50,200`. Bare numbers (`--params 50 200`) are rejected with an error |
| `donchian` | Enter long on a close above the prior N-bar high (short below the prior N-bar low with `--short`). Exit on a close beyond the opposite **N/2**-bar channel | 20, 40, 55, 80, 100 | N = 20 matches Turtle System 1 (20/10). For 55, the tool exits on a 27-bar channel, not the Turtles' 20 |
| `tsmom` | Sign of the k-bar return | 21, 63, 126, 189, 252 | Use futures (excess-return) data. Lookback blends and cross-market portfolios must be built outside the tool |
| `rsi2` | **Long only.** Enter when close > SMA200 and RSI(2) < threshold; exit on a close > SMA5; no stop | Thresholds 5, 10, 15, 20, 25 | `--short` is ignored |
| `bbrev` | **Long only.** Enter on a close < SMA(k) − 2σ(k) (population SD); exit on a close ≥ SMA(k) | 10, 20, 30, 50 | `--short` is ignored |

Mechanics:
- **Fills:** by default (`--delay 1`) a position decided at bar t's close is first held from bar t+1's close, i.e. it fills at the next bar's close. `--delay 0` fills at the signal close (MOC-style, Connors' "near the close"); that is optimistic and defensible only for a real market-on-close process. Next-open fills are not modelled, and raising `--cost-bps` is no substitute, because the overnight gap has a systematic sign for reversal rules.
- **Bar frequency:** Sharpe, vol and vol targeting annualize with `--ppy` (default 252); set it for non-daily bars.
- **Costs:** charged per 1.0 of turnover (default 5 bps). A round trip costs 2×; a long-to-short flip costs 2× per flip.
- **Data length:** 260-bar warm-up; the tool warns below ~560 bars.
- **Volatility targeting:** `--vol-target 0.15` scales positions by 20-day realized volatility, capped at `--max-lev` (default 2).
- **Out-of-sample:** `--oos` (default 0.3) applies the best in-sample parameter to the final fraction of the data.
- **Robustness verdict:** "plateau" if ≥70% of the grid has positive Sharpe and the median Sharpe is ≥ 0.5× the best; otherwise "spiky".
- **DSR trials** = grid size × `--extra-trials`.

### 7.3 Connors RSI(2): exact rules and how to test them
Rules (ChartSchool RSI(2) [V]; original in Connors & Alvarez 2009 [NR]):
1. **Trend filter:** long only above the 200-day SMA; short only below it.
2. **Entry:** long when RSI(2) ≤ 5 (Connors found below 5 beat below 10). Short when RSI(2) ≥ 95.
3. **Execution:** near the close of the signal day (Connors' preference) or at the next open.
4. **Exit:** longs on a close above the 5-day SMA; shorts on a close below it.
5. **No stops.** Connors' tests found that stops hurt stock and index results.

Caveats (ChartSchool [V]):
- Signals can come early: RSI(2) stays pinned while price keeps falling.
- Drawdowns can be deep without stops.
- Earnings gaps disrupt single-stock trades.
- Curve fitting lowers future success.

Evidence: MIXED, practitioner-validated only. The underlying mechanism is short-horizon reversal (Jegadeesh 1990; Lehmann 1990 [NR]), documented in the cross-section. Index-level daily mean reversion depends on the regime. No peer-reviewed out-of-sample test of the exact rules was located, and performance since 2009 is unverified.

Testing protocol:
- `ruletest FILE --rule rsi2 --cost-bps 5 --oos 0.3`. Look for a plateau across thresholds 5-25. A spike at 5 alone is a red flag.
- Exposure is low, so judge it on Sharpe and max drawdown against buy-and-hold, not on CAGR. Read the `expos.` column.
- Trades are frequent, so rerun at double cost.
- Repeat on several indexes or ETFs, and pass the count via `--extra-trials`.
- The short side and any stop variant must be tested outside the tool and counted as trials. Kaminski-Lo predicts that stops hurt a mean-reversion edge.
- Tool RSI uses Wilder smoothing seeded with a simple mean, so values can differ slightly from charting platforms.

### 7.4 Reading `ruletest` output
- **"spiky"**: only a few parameters work, and the best one is probably fit to noise. Stop there or widen the idea.
- **"no parameter set makes money"**: there is no edge in this form.
- **Grid columns** are Sharpe, CAGR, vol, maxDD, trades, exposure and turnover/yr. Compare the buy-and-hold row on Sharpe *and* drawdown. A low-exposure rule can win on risk while losing on CAGR.
- **Significance block:** the PSR/DSR of the best parameter after the trial count. A strong in-sample Sharpe with a weak DSR means luck can't be ruled out.
- **OOS block:** expect out-of-sample below in-sample. A collapse toward 0 means the edge was mostly fit.
- **Few trades** means low power. `tradekit.py expectancy --p --win --loss --trades` gives the trades needed for t = 2 or 3.
- **A single `--params` value** (one-point grid) gives no robustness information. Use it only for a pre-registered specification or a cost stress *after* the full grid has been run.

### 7.5 Command set

```
python scripts/techkit.py indicators SPY.csv                                    # current state of every §3 tool + trend template + stage
python scripts/techkit.py ruletest SPY.csv --rule rsi2 --cost-bps 5 --oos 0.3   # Connors grid 5..25
python scripts/techkit.py ruletest SPY.csv --rule rsi2 --params 5 --cost-bps 10 --oos 0.3 --extra-trials 6   # cost stress; 6 = variants tried
python scripts/techkit.py ruletest SPY.csv --rule cross --params 50,200 --oos 0.3                            # golden cross as one rule
python scripts/techkit.py ruletest CL.csv --rule donchian --params 20 55 --short --vol-target 0.15 --cost-bps 3 --oos 0.3
python scripts/techkit.py ruletest ES.csv --rule tsmom --short --vol-target 0.15 --cost-bps 2 --oos 0.3
python scripts/techkit.py ruletest QQQ.csv --rule bbrev --cost-bps 5 --oos 0.3
```

---

## 8. Failure modes / traps

| Trap | How to catch it in a plan or backtest | Fix |
|---|---|---|
| **Overfitting / data snooping** | "Which settings did you try?" gets a vague answer; odd parameters (RSI 9, MA 137); a spiky grid | Count every trial; run the full grid; check DSR; demand a plateau (STW 1999; Bajgrowicz-Scaillet 2012) |
| **Assuming persistence** | The best rule from the past is assumed to stay best | Persistence test (t → t+1); walk-forward |
| **Cherry-picked charts** | Evidence is a few annotated textbook examples | Ask for **every** instance the rule flags over a fixed period and universe |
| **Hindsight pattern labeling** | Patterns or wave counts drawn on completed charts; the count changes after the move | Require identification that works at the right edge of the chart and an invalidation level set in advance |
| **Indicator stacking** | Several tools from one row of §3.0 called "confluence" | One tool per question; each extra filter must show added out-of-sample value |
| **Ignoring costs and turnover** | Zero or flat cost assumptions; high-turnover intraday or daily rules; shorts with no borrow cost | Realistic `--cost-bps`, double-cost stress test, borrow costs. Even in-sample profits can vanish at low costs |
| **Same-close / look-ahead fills** | Signal and fill on the same bar; stops assumed filled at intrabar highs and lows; survivorship-biased universes | Next-bar or MOC fills with slippage; point-in-time universes (Zakamulin [NR]) |
| **Decayed rule on an efficient market** | A single daily rule on the S&P/DJIA/EURUSD sold as an edge | Default to no edge (§2.1); move the test to the settings in §2.2 |
| **Regime blindness** | Fading "overbought" in a strong trend; mean reversion run through a trending regime; an MA-timing edge concentrated in one or two bear markets | Regime split; range-rule reading of RSI; a regime filter tested as its own trial |
| **Treating Bulkowski numbers as expected returns** | "This pattern averages 54%" | Run the §4.2 conversion |
| **Stop design that fights the dynamics** | Tight stops on mean-reversion; no stops on breakouts; stops one tick beyond round numbers | Match the stop to the autocorrelation (§6.7); add a buffer beyond clusters (§6.5) |
| **Crypto and intraday overconfidence** | "TA works in crypto" or "works intraday" cited as settled | The evidence conflicts (§2.4). Require a cost-inclusive out-of-sample test on that exact venue and timeframe |
| **Assuming a published edge is permanent** | A paper or book from decades ago cited as current | Assume decay after publication; haircut and monitor |
| **Low power on a single asset** | One market, few trades, a high Sharpe | Add markets; check the trade count with `tradekit.py expectancy` |
| **Unfalsifiable narratives** | "Institutions are accumulating", "smart money swept liquidity", Elliott counts | Turn the claim into a rule that could fail, or give it zero weight |

---

## 9. Toolkit hooks

- **Indicator readings:** `python scripts/techkit.py indicators FILE`. It prints SMA 20/50/150/200, EMA21, MACD 12/26/9, RSI14/RSI2, ADX14 with ±DI, ATR14 (Wilder), 20-day realized vol, Bollinger %B with a 6-month BandWidth percentile (squeeze flag at ≤10%), prior 20/55-day Donchian levels, 52-week high and low, 1/3/6-month and 12-1 returns, 50-day relative volume, the Minervini-style 7-point trend template, and an approximate Weinstein stage.
- **Rule backtests:** `python scripts/techkit.py ruletest FILE --rule sma|cross|donchian|tsmom|rsi2|bbrev [--params ...] [--cost-bps 5] [--short] [--vol-target 0.15] [--max-lev 2] [--oos 0.3] [--extra-trials k]` (details in §7.2-7.4).
- **Momentum ranking** of a watchlist: `python scripts/techkit.py rank FILE... --by voladj`. Depth in `momentum-trading.md`.
- **ATR-based position size:** `python scripts/tradekit.py size --equity E --risk 0.5 --entry P --atr A --atr-mult 2.5`. Here `--risk` is a percentage of equity; add `--multiplier` for futures.
- **Trade count and significance** of a discretionary setup log: `python scripts/tradekit.py expectancy --p --win --loss --trades`.
- **Significance of a quoted Sharpe** after k tries: `python scripts/tradekit.py sharpe --sr --n --ppy --skew --kurt --trials k --var-sr`. Kurtosis is raw, so normal = 3.
- **Full report on a user's equity curve:** `python scripts/tradekit.py perf FILE --trials k`.
- **Realized volatility estimators** (for a volatility regime): `python scripts/tradekit.py vol FILE`.
- **Mean-reversion diagnostics** (half-life, Hurst, variance ratios) before trusting a reversion rule: `python scripts/tradekit.py meanrev FILE`.
- **Execution cost of a level-based entry:** `python scripts/tradekit.py impact --qty --adv --price --daily-vol --spread-bps`.

---

## 10. Key sources

- Osler 2000, "Support for resistance," FRBNY EPR: https://www.newyorkfed.org/medialibrary/media/research/epr/00v06n2/0007osle.pdf
- Osler 2003, stop and take-profit clustering, JF 58(5): https://ideas.repec.org/a/bla/jfinan/v58y2003i5p1791-1819.html
- Kavajecz & Odders-White 2004, TA and limit-order depth, RFS 17(4): https://ideas.repec.org/a/oup/rfinst/v17y2004i4p1043-1071.html
- Bhattacharya, Holden & Jacobsen 2012, round numbers in equities, Mgmt Sci 58(2): https://ideas.repec.org/a/inm/ormnsc/v58y2012i2p413-431.html
- Sullivan, Timmermann & White 1999, Reality Check on technical rules, JF 54(5): https://ideas.repec.org/a/bla/jfinan/v54y1999i5p1647-1691.html
- Bajgrowicz & Scaillet 2012, FDR and persistence, JFE 106(3): https://ideas.repec.org/a/eee/jfinec/v106y2012i3p473-491.html
- Neely, Weller & Ulrich 2009, adaptive FX decay, JFQA 44(2): https://ideas.repec.org/p/fip/fedlwp/2006-046.html
- Hsu, Taylor & Wang 2016, FX predictability across 30 currencies, JIE 102: https://ideas.repec.org/a/eee/inecon/v102y2016icp188-208.html
- Moskowitz, Ooi & Pedersen 2012, time-series momentum, JFE 104(2): https://ideas.repec.org/a/eee/jfinec/v104y2012i2p228-250.html
- Szakmary, Shen & Sharma 2010, trend in commodity futures, JBF 34(2): https://ideas.repec.org/a/eee/jbfina/v34y2010i2p409-426.html
- Neely, Rapach, Tu & Zhou 2014, TA and the equity premium, Mgmt Sci 60(7): https://ideas.repec.org/a/inm/ormnsc/v60y2014i7p1772-1791.html
- Han, Yang & Zhou 2013, MA timing and volatility, JFQA 48(5): https://ideas.repec.org/a/cup/jfinqa/v48y2013i05p1433-1461_00.html
- Hsu & Kuan 2005, young vs mature markets, J. Fin. Econometrics 3(4): https://ideas.repec.org/a/oup/jfinec/v3y2005i4p606-628.html
- Marshall, Cahan & Cahan 2008, intraday rules, J. Empirical Finance 15(2): https://ideas.repec.org/a/eee/empfin/v15y2008i2p199-210.html
- Schulmeister 2009, daily vs 30-minute S&P rules, RFE 18(4): https://ideas.repec.org/a/eee/revfin/v18y2009i4p190-201.html
- Hudson & Urquhart 2021, crypto rules, Annals OR 297(1): https://ideas.repec.org/a/spr/annopr/v297y2021i1d10.1007_s10479-019-03357-1.html
- Lu, Chen & Hsu 2015, candlesticks and holding rules, JBF 61: https://ideas.repec.org/a/eee/jbfina/v61y2015icp172-183.html
- Kaminski & Lo 2014, "When do stop-loss rules stop losses?", J. Fin. Markets 18: https://ideas.repec.org/a/eee/finmar/v18y2014icp234-254.html
- Bulkowski, ThePatternSite glossary and rankings: https://www.thepatternsite.com/glossary.html
- ChartSchool, RSI(2) strategy (Connors rules): https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/rsi-2
