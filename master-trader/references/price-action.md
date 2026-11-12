# Price Action Trading: Levels, Bar-by-Bar Reading, Auction and Order Flow

*Read when: a user trades from raw charts (intraday or swing; index futures, equities, FX, crypto) and asks about support/resistance or key levels, where to put stops and targets around levels, trend vs range reading, Al Brooks terms or setups (H2/L2, wedge, measured move, always in, MTR), opening range or gaps, VWAP, Market Profile / value area / the 80% rule, DOM/footprint/delta/tape reading, Wyckoff/VSA or ICT/SMC (FVG, order blocks, liquidity sweeps, kill zones); or when reviewing a discretionary setup, playbook, journal or backtest for testability, costs and sample size.*

Tags: grade **[Strong] / [Moderate] / [Weak] / [Contested] / [Lore]**, then source type **PR** peer-reviewed · **WP** working paper / central-bank staff report · **IT** independent test, quant blog or forum backtest · **VEN** vendor or author selling related products · **PL** practitioner lore (books, courses, education sites), then the mechanism rating **SUPPORTED / MIXED / UNSUPPORTED / UNTESTED**. **(math)** = arithmetic, exact under its stated assumptions.

Depth elsewhere: indicator, chart-pattern, candlestick and Fibonacci statistics are in `technical-analysis.md`; momentum and breakout playbooks (52-week highs, trend templates) are in `momentum-trading.md`; sizing, stop theory and execution cost are in `risk-sizing-execution.md`; backtest validation and the deflated Sharpe are in `quant-research-validation.md`; dealer gamma and the intraday flow calendar are in `market-forces-flows.md` (§4, §11); journaling and the coaching conversation are in `trader-psychology-process.md`. Do not duplicate them here; point there.

**Contents:** 1 Core principles · 2 What is actually evidenced · 3 Reading the chart: market phase decision guide · 4 Brooks bar-by-bar toolkit · 5 Key-level playbook · 6 Auction market theory / Market Profile · 7 Order flow and tape · 8 Wyckoff/VSA and ICT/SMC · 9 Quantify your setup · 10 Base rates · 11 Failure modes / traps · 12 Toolkit hooks · 13 Key sources

---

## 1. Core principles

- **Levels work because orders are anchored to them.** Take-profits cluster *at* round numbers and published levels, and stops cluster *just beyond* them [Moderate · PR · SUPPORTED, FX]. A level is therefore a place where a reaction (absorption) or a cascade (triggered stops) is more likely. It is not a magic line. *Why:* this tells you which side of the level the stop and the target belong on.
- **Phase first, setup second.** The same bar pattern is a buy in a bull channel and a trap at the top of a range. Brooks himself says a High 2 alone is not a setup. *Why:* most bad price-action trades are correctly drawn patterns in the wrong context.
- **The vocabulary is useful; the numbers are untested.** Brooks's, Dalton's, Wyckoff's and ICT's probabilities are self-described estimates or unsourced [Lore · PL · UNTESTED]. *Why:* treat every "80%" as a hypothesis the trader must measure on their own instrument, never as a statistic.
- **Every setup is a trader's equation.** EV = p·R − (1−p) − cost, in R units (math). *Why:* if a trader cannot state p, R and cost, they do not have a setup yet.
- **Costs decide short-horizon edges.** A +0.2R gross edge on an 8-tick stop disappears with about 2 ticks of all-in round-trip cost (math). *Why:* tight-stop scalps need either a much larger edge or a wider frame.
- **Order-flow edges live for seconds to minutes.** OFI explains contemporaneous price change linearly [Strong · PR · SUPPORTED], but the predictive window of imbalances shrank to about 5 minutes in large NYSE stocks by the early 2000s [Moderate · PR · SUPPORTED]. *Why:* use the tape to time entries at levels planned in advance, not to forecast.
- **Data quality caps what order flow can show.** CME futures carry the true aggressor side. US equity trade direction is inferred (76–81% accurate) on a tape where about half the volume is off-exchange (2025). Unregulated crypto venues report mostly wash volume. *Why:* the same footprint chart means different things in different markets.
- **Time of day is real structure.** U-shaped volatility and volume, first-half-hour → last-half-hour momentum and same-half-hour periodicity across days are among the best-documented intraday facts [Strong · PR · SUPPORTED]. *Why:* opening-range and session-open tactics ride a genuine spike in volatility and imbalance; midday chop is predictable too.
- **The base rate is failure.** 97% of persistent Brazilian futures day traders lost money, about 0.3% of Taiwanese day traders predictably outperform, and 74–89% of EU retail CFD accounts lose (§10). *Why:* gate live size on demonstrated, cost-inclusive expectancy over an adequate sample.
- **A new name is not a new edge.** FVG, order block, liquidity sweep, spring and failed breakout reduce to a few mechanisms. *Why:* translate the term (§8), then apply one testing standard (§9).

---

## 2. What is actually evidenced

| Finding | Key numbers | Grade | Trading implication |
|---|---|---|---|
| Round-number order clustering (FX) | About 9,700 stop-loss and take-profit orders at one dealing bank, 1 Sep 1999 – 11 Apr 2000 (43% USD/JPY, 33% EUR/USD, 24% GBP/USD). 8.7% of orders sit at levels ending 00 versus about 1% if uniform; declining clusters at 50, then other 0s, then 5s; no special clustering at 25/75 (Osler 2003) | [Moderate · PR · SUPPORTED] | Big figures and 50s are focal. Quarters (25/75) are not special in this data |
| Take-profits *at* the number → reversals | 9.3% of take-profits vs 4.4% of stops execute exactly at 00 (bootstrap p ≈ 1.1%). When the rate rises to a 00, about 10.5% of take-profit sells trigger versus about 2.8% of stop-loss buys | [Moderate · PR · SUPPORTED] | The first touch of a round number favors a reaction |
| Stops *just beyond* → cascades | Stop-loss buys: 14.4% at levels ending 01–10 vs 7.4% at 90–99 (sells mirror this below the number). After a cross, the triggered orders are same-direction stops. Rates trend unusually fast at stop clusters, with a larger and longer response than to take-profit clusters, significant for **hours, not days** (Osler 2005). Osler does *not* claim stops cause most large moves | [Moderate · PR · SUPPORTED] | A clean break tends to extend. Level-break trades are intraday-to-short-swing trades |
| Published S/R levels | Levels from six FX firms predicted intraday trend interruptions better than 10,000 sets of arbitrary levels (1-minute quotes, 9am–4pm NY). Power varied by firm and currency, firms disagreed, and it lasted at least 5 business days (Osler 2000) | [Moderate · PR · SUPPORTED] | Widely watched levels matter even when "wrong" |
| Round numbers in equities | Over 100M trades: liquidity demanders buy just below and sell just above round numbers, monotonic in roundness (whole > half > ...), costing them close to $1bn a year (Bhattacharya, Holden & Jacobsen 2012). Stock limit orders cluster at whole, then half, then quarter numbers (Osborne 1960; Niederhoffer 1965; Harris 1991, via Osler). In FX, rates *move away* from round numbers fast; stock prices *linger* at limit-order clusters | [Moderate · PR · SUPPORTED] | Whole and half dollars are real order magnets in stocks |
| S/R bounce | On stock tick data, prices bounce off identified S/R more often than they cross it, beyond chance; read as self-fulfilling (Garzarelli et al. 2014) | [Moderate · PR · SUPPORTED] | Default expectation at a tested level is a bounce, until the break is decisive |
| Order-flow imbalance → price | ΔP is linear in OFI at the best quotes, slope ∝ 1/depth; robust to intraday seasonality, across time scales and 50 NYSE stocks; the volume-impact relation is noisier (Cont, Kukanov & Stoikov 2014) | [Strong · PR · SUPPORTED] | Price moves when net aggressive flow exceeds the depth in front of it |
| Shrinking imbalance horizon | Predictive window of lagged imbalances: about 30 min (1996) → 10 min (1999) → about 5 min later (150 large NYSE stocks); convergence between 5 and 60 min (Chordia, Roll & Subrahmanyam 2005) | [Moderate · PR · SUPPORTED] | Tape reading is an execution skill. Today's window is probably shorter still (inference) |
| Intraday U-shape | Equity volatility and volume are U-shaped (some markets reverse-J); FX has strong intraday periodicity (Wood, McInish & Ord 1985; Admati & Pfleiderer 1988; Andersen & Bollerslev 1997) | [Strong · PR · SUPPORTED] | Opportunity and risk concentrate at the open and close. This is the real basis for "kill zones" |
| First half-hour → last half-hour | SPY 1993–2013: the first half-hour return (from the prior close) predicts the last half-hour; R² 1.6% in-sample, about 1.2% out-of-sample; stronger on high-volume days and in recessions (Gao, Han, Li & Zhou 2018). Present in 60+ futures 1974–2020, reverting over the following days, stronger when dealer gamma is negative (Baltussen et al. 2021) | [Strong · PR · SUPPORTED] | Small but real. Early-session direction is a legitimate bias input; see `market-forces-flows.md` §4 for gamma |
| Half-hour periodicity | A half-hour's return continues at exact daily lags (same half-hour on later days) for 40+ days, strongest at open and close; short-lag reversal within the day from bid-ask bounce (Heston, Korajczyk & Sadka 2010) | [Moderate · PR · SUPPORTED] | Time-of-day effects are persistent. Very short-lag intraday "momentum" is partly bounce noise |
| Opening-range breakout (peer-reviewed) | ORB on crude-oil futures: returns significantly above zero, success rate above a fair game; in-sample bootstrap, one market (Holmberg, Lönnbark & Lundström 2013). Follow-up thesis: success depends heavily on volatility | [Moderate · PR · SUPPORTED (limited scope)] | ORB is a credible family; condition on volatility |
| ORB (vendor) | 5-min ORB on "Stocks in Play" (high relative volume, usually news), 7,000+ US stocks, 2016–2023: top 20 gave >1,600% net, Sharpe 2.81, annualized alpha 36% (Zarattini, Barbon & Aziz 2024). QuantConnect re-implementation: Sharpe 2.396 vs 0.836 for SPY [IT]. QQQ/TQQQ ORB 2016–2023: 1,484% vs 169%, slippage not addressed on the summary page (Zarattini & Aziz 2023) | [Weak · WP/VEN · MIXED] | Promising, but the authors sell products, it covers a single period, and there is no independent peer-reviewed replication |
| VWAP trend rule | QQQ long above / short below VWAP, Jan 2018 – Sep 2023: $25k → $192,656 net of commissions (+671%), Sharpe about 2.1. Several public QuantConnect replications reportedly found much weaker results (Zarattini & Aziz) | [Weak · WP/VEN · MIXED] | Do not cite as proof that VWAP is an edge |
| Gaps | US indices 1928–2018: price moves *in the gap's direction* on the gap day, and gaps do *not* reliably fill (Plastun, Sibande, Gupta & Wohar 2020). An earlier multi-market study found US equity gaps not inconsistent with efficiency, with only FX gaps giving abnormal profits (Caporale & Plastun 2017). Weekend gaps in DJIA/Nasdaq/DAX, 5-min data 2013–2023: the reliable-fill assumption is challenged, with directional patterns at medium-to-large gaps, especially in the DAX (JRFM 2025) | [Contested · PR · MIXED] | Default to gap-and-go on the day. "Gaps always fill" is lore |

**No rigorous test was found for** [UNTESTED]: prior-day high/low, Globex high/low or anchored VWAP as S/R in futures or crypto; pullback depth (38/50/62%) as a continuation predictor; HH/HL structure rules; multi-timeframe alignment; intraday inside-bar breakouts; NR4/NR7 hit rates; Brooks's probabilities; Market Profile predictions; Wyckoff/VSA signals; ICT concepts; retail footprint/CVD patterns net of costs. It is also not established whether Osler's 1999–2000 clustering asymmetries persist in today's algorithmic FX and crypto markets.

---

## 3. Reading the chart: market phase decision guide

Brooks's cycle: **breakout (spike) → channel → trading range → breakout**. Most climaxes end in trend-channel overshoots, and most reversals lead to trading ranges rather than opposite trends [Lore · PL · UNTESTED]. The phase read is the context filter for every setup below.

| Phase | Bar overlap | Tails | Consecutive trend bars | Pullbacks | Swing structure | Take | Avoid |
|---|---|---|---|---|---|---|---|
| **Breakout / spike** | Little or none | Small; closes near bar extremes | Several in a row | None, or one small bar | New extreme, no test | With-trend entries on the first small pause; "always in" flips this way | Fading on "overbought"; waiting for a deep pullback that may not come |
| **Tight (micro) channel** | Low | Small | Most bars | At most 1–2 tiny; most bars touch the trend line | Persistent HH/HL (or LH/LL) | H1/H2 (L1/L2) with trend | Early reversal attempts (Brooks: most trend-reversal attempts fail) |
| **Broad channel** | Moderate | Both ends | Mixed | Deeper, often two-legged | HH/HL with overlap | H2/L2 with trend; fade channel-line overshoots on a wedge / third push | Breakout entries in the trend's direction right at the channel line |
| **Trading range** | Heavy | Prominent at the extremes | Trend bars lack follow-through | Legs reverse | Flat; failed new highs and lows | Fade the extremes; failed breakouts; second entries; targets toward the middle or other side | Buying highs and selling lows; stop entries in the middle third |
| **Tight trading range / barbwire** | ≥ 2–3 heavily overlapping bars, dojis | Both ends | None | n/a | None | Nothing: wait for a breakout *with* follow-through | Stop entries (reversals too small to pay after costs) |
| **Breakout mode / compression** | Contracting ranges (NR4/NR7, ID/NR4, inside bars, triangle) | Small | None | n/a | Converging | Bracket both sides with stop orders; direction is unknown | Predicting direction from the compression itself |
| **Climax / reversal attempt** | Outsized bars late in a trend; channel-line overshoot | Large rejection tail possible | Climactic | n/a | Trend line broken? Extreme tested? | Expect two-sided trading, i.e. a range first. MTR only after a trend-line break *and* a test of the extreme | Assuming an immediate opposite trend |

**Objective proxies** (test definitions to make a read measurable, not evidence): trend bar = body ≥ 50% of range and close in the top/bottom 25%; tail length in ATR units (ATR 14, Wilder); overlap = share of a bar's range inside the prior bar's range, averaged over the last 10 bars; trend filter = slope of a 20-period EMA plus a count of consecutive higher lows; ADX14 above 25 suggests trending and below 20 suggests ranging (the toolkit's convention). Record pullback depth as a variable rather than a rule, because no study supports 38/50/62% thresholds.

**Phase-read procedure (run before naming a setup):**
1. **Higher timeframe** (one or two steps up): trend or range, and the nearest higher-timeframe levels.
2. **Current phase** from the table above. If two phases fit, assume the more two-sided one (smaller targets, fewer stop entries) as a conservative default.
3. **Location:** distance to the nearest key level (§5) in ticks or ATR. A with-trend setup straight into a major level has a worse trader's equation.
4. **Time of day:** open and close windows versus midday (§2 U-shape).
5. **Allowed setups:** pick only the setup families the phase permits and reject the rest.
6. **Trader's equation with costs** (§4): take the trade only if an honest p exceeds (1 + c)/(1 + R).
7. **Invalidation:** write down the price or bar behavior that would show the phase read was wrong.

**Market structure (HH/HL, BOS, CHoCH)** [Lore · PL · UNTESTED]: these restate the Dow rule. An uptrend is intact while higher lows hold, and the first lower low is the earliest warning. Brooks's MTR adds a confirmation step (trend-line break, then a test of the extreme). Teach them as *state descriptions* that set the context filter, not as signals with stand-alone edge.

**Multi-timeframe alignment** [Lore · PL · UNTESTED]: plausibly linked to documented intraday momentum (Gao et al.; Baltussen et al.) but never tested directly. Default: the higher timeframe sets bias and levels, the lower timeframe sets only entry and stop. Tag trades as aligned or counter-trend so the user can measure the difference.

**Contraction → expansion** [Moderate · PR · MIXED-to-SUPPORTED, conditional on volatility] (Holmberg et al. 2013; consistent with volatility clustering). Crabel's tools are [Lore · PL · UNTESTED]:
- NR4/NR7 = the narrowest daily range of the last 4/7 days. ID/NR4 = an inside day that is also an NR4. Both flag compression, not direction, so bracket both sides with stops.
- **Stretch:** a preset distance above and below the open or opening range, where the buy and sell stops go. One common computation is the 10-day average of min(high − open, open − low).
- An "early entry" retracement rule (3/8–1/2 re-entry, stop beyond 5/8) comes from one blog summary and is unverified against the book.
- NR7 has no reliable published hit rate.

**Bar anatomy:** read *who won the bar* (close location, body/range ratio, tail versus ATR) and *whether follow-through came* (the next bar). Isolated candlestick statistics are in `technical-analysis.md`. A pattern *at a level* has a plausible mechanism (rejection where take-profits cluster) but is UNTESTED as a combination.

---

## 4. Brooks bar-by-bar toolkit

Status: the vocabulary is descriptive and internally consistent; every probability Brooks quotes is [Lore · PL · UNTESTED]; the trader's equation is arithmetic.

| Term | Meaning | How a master uses it |
|---|---|---|
| Signal bar / entry bar | Signal bar = the last bar of the setup (it becomes the signal bar once the order fills); entry bar = the bar in which the trade is entered | Judge the signal bar by body, close and tails in context. A bull reversal bar ideally closes near its high with a lower tail |
| Stop entry | A buy stop 1 tick above the signal bar's high (sell stop 1 tick below its low) | The market must prove direction before you are in. Costs at least 1 tick of slippage in futures |
| Trend bar / doji | Meaningful body / small or no body (neither side in control) | Count consecutive trend bars for strength; dojis and overlap signal two-sided trade |
| High 1, High 2 (H3, H4) | In a bull flag or near a range bottom, the first (then second, ...) bar whose high exceeds the prior bar's high during the correction | H2 is usually the end of a two-legged pullback. Low 1/Low 2 are the bear mirror |
| Second entry | A second entry within a few bars of the first, on the same logic | Re-entry on the same logic after a quick failure; log first and second entries separately to see whether the second really is better (UNTESTED) |
| Wedge / three pushes | Three-push move with converging lines; any three-push pattern trades like a wedge | A reversal or fade candidate, especially at a channel-line overshoot |
| Measured move | A leg roughly equal to the prior leg or to the range height; a breakout "measuring gap" projects a similar move | A target tool, not an entry signal |
| Trading range / breakout mode | Sideways, neither side in control / a setup where a breakout either way should get follow-through | Ranges: fade extremes. Breakout mode: bracket both sides |
| Barbwire / tight trading range | ≥ 3 overlapping bars incl. a doji / ≥ 2 heavily overlapping bars whose reversals are too small to trade with stop entries | Stand aside. Beginners should wait for a clear breakout |
| Micro channel | Tight channel where most bars touch the trend and channel lines, with none or 1–2 small pullbacks | Strongest trend state. Do not fade the first reversal bar |
| Spike and channel | A breakout spike followed by a lower-momentum, two-sided channel | Momentum fades and trade turns two-sided: favor pullback entries over breakout entries inside the channel |
| Climax | Too far, too fast, then reverses; most end in channel overshoots | Expect a trading range next, not an instant new trend |
| Failure / trap; failed failure | A move that stops traders out before target, often reversing as they exit / a failed trap that resumes the original breakout direction | The core of the range playbook. Know the price that invalidates the fade |
| Always in | The side you would hold if forced to be in the market; usually needs a spike to flip. Brooks's forum calls it a theoretical concept, not a strategy | A bias label that decides which side's setups to take |
| Major trend reversal (MTR) | Bull → bear (or the reverse) that breaks the trend channel and then *tests the old extreme*; tops are double-top variants, bottoms double-bottom variants | Needs both the break and the test; even then expect a range more often than a new trend |

**Trader's equation (math):**
```
Gross EV (R)  = p·R − (1 − p)·1                   break-even  p* = 1/(1 + R)
Net EV (R)    = p·R − (1 − p) − c                 break-even  p* = (1 + c)/(1 + R)
c (in R)      = (slippage ticks + commission in tick-equivalents, round trip) / stop distance in ticks
```
- **Brooks's defaults:** if uncertain, assume a 40–50% win rate and target at least 2R. If confident, assume 60% and 1R is acceptable. An equidistant stop and target hovers near 50%. Both 40% @ 2R and 60% @ 1R give +0.2R gross.
- **Cost example (illustrative):** with an 8-tick stop and 2 ticks of all-in round-trip cost, c = 0.25R, so +0.2R becomes −0.05R. With a 20-tick stop, c = 0.10R and the edge halves to +0.1R. Break-even at 60% @ 1R with c = 0.1R rises to 55%.
- **Coaching rule:** make the user restate every setup as (p, R, c). Check p > (1 + c)/(1 + R), then run `tradekit.py expectancy`.

**Brooks's own numbers and their status** [Lore · PL · UNTESTED; inconsistent across his materials]:

| Claim | Figure quoted |
|---|---|
| Channel breakout succeeds | about 30% (about 70% reverse within a few bars) |
| Wedge or parallel-channel breakout attempts fail | > 60% |
| Almost any setup | 40–60% |
| Strong breakouts get follow-through | about 80% |
| Trading-range breakout attempts fail | 80% (also 75%, and 50% for the first breakout, in other Q&A) |
| Trend-reversal attempts fail | 80% |

- In a course transcript Brooks also notes that what counts as a breakout is itself undefined. On the channel figure he says, "Have I tested it? No. It's just my guideline." (Brooks Trading Course transcript).
- The only measured statistics in that transcript are monthly-chart historical counts.
- No independent or out-of-sample test of H2/L2, wedges, measured moves, MTR or breakout-failure rates was found. H2/L2 detector scripts exist on TradingView, but no published backtest uses them. A TradingView "debunking" post and a base.report breakout study surfaced in search but were not read; their methods are unknown.
- **How to teach "80% of breakouts fail":** as a base-rate heuristic for *established ranges*: fade the extremes, do not buy highs or sell lows. Osler (reflection plus cascades) and Garzarelli (bounces) give a plausible mechanism, but neither measures Brooks's figure.

**Setup cards.** All entries are stop orders 1 tick beyond the signal bar, and 1R = entry-to-stop distance. Every card is UNTESTED until the user measures it (§9).

**H2 buy / L2 sell (with-trend pullback)**
- *Context:* bull trend or channel (or a range bottom). Not after a buying climax: per Brooks, an H2 on its own is not a setup.
- *Trigger:* a two-legged pullback, then a bull signal bar closing in its top third.
- *Stop:* below the signal bar or the pullback low.
- *Target:* the prior extreme or a measured move. If uncertain, demand ≥ 2R.
- *Avoid:* barbwire, H2 directly under range resistance or a key level, late in a climactic leg.
- *Testable form:* price above a rising 20-EMA, ≥ N consecutive higher lows before the pullback, two legs down, signal-bar close in the top third. Cancel if not filled in N bars.

**Wedge / three-push reversal**
- *Context:* the third push into a channel-line overshoot late in a trend, or at a range extreme.
- *Trigger:* a reversal signal bar after the third push.
- *Stop:* beyond the third-push extreme.
- *Target:* expect a two-sided correction rather than a new trend (most reversals become ranges), so take a range-sized first target and size it per the trader's equation.
- *Avoid:* fading a micro channel; wedges against a fresh spike.

**Failed breakout / trap (and the failed failure)**
- *Context:* an established range or major level; the breakout bar is weak (tails, overlap, no follow-through) and price closes back inside.
- *Trigger:* a reversal signal bar back inside. Take a second entry if the first is stopped within a few bars.
- *Stop:* beyond the breakout (sweep) extreme.
- *Target:* the range middle, then the opposite side.
- *Exit rule:* if price re-breaks the extreme with follow-through (failed failure), the original breakout direction usually resumes: exit, do not average.
- *Mechanism:* stops beyond the level were triggered but absorbed (Osler). This is the same event as a Wyckoff spring/UTAD and an ICT sweep.

**Measured move:** a target only. Leg 2 ≈ leg 1, or breakout ≈ range height. Log the actual extension in leg-1 units so the user learns their market's distribution.

**Always-in flip:** a strong spike with consecutive trend bars that closes beyond structure. Switch the setup bias to that side and stop taking the other side's reversal setups until a new spike.

**MTR**
- *Sequence:* trend-line or channel break, then a test of the old extreme (a higher high/lower high in a bull trend, or the mirror), then a reversal signal bar on the test.
- *Stop:* beyond the test extreme.
- *Target:* the first target is range-sized, because most reversals become ranges. Hold a runner only if a spike in the new direction follows.

**Other bar-by-bar schools** [Lore · PL · UNTESTED]:
- **Volman** (*Understanding Price Action*, 5-min EUR/USD): DD (double doji break), FB (first break), SB (second break), BB (block break), RB (range break), IRB (inside range break), ARB (advanced range break). The core logic is build-up/compression followed by a breakout, with "double pressure" before the break. The abbreviations are community shorthand matching the chapter titles; exact rules were not verified against the book.
- **Beggs (YTC):** five setups chosen by market environment: BPB, PB, TST, BOF, CPB. The expansions (breakout pullback, pullback, test, breakout failure, complex pullback) are believed correct but not confirmed from the primary text.

---

## 5. Key-level playbook

| Level | Why it is a focal point | Evidence | Practical notes |
|---|---|---|---|
| Round numbers (00 > 50 > other 0s > 5s) | Take-profits sit at them, stops just beyond | [Moderate · PR · SUPPORTED] in FX (1999–2000 data) and equities (whole > half dollar) | Index-futures and crypto round numbers are plausible by the same logic but UNTESTED |
| Published S/R (bank/vendor levels) | Many traders anchor orders to the same list | [Moderate · PR · SUPPORTED] (Osler 2000) | Effect lasted ≥ 5 business days; varied by source |
| Prior-day high / low / close | A salient anchor for stops and targets | [Lore · UNTESTED] | Define RTH vs ETH explicitly (futures) and the "day" boundary (crypto) |
| Overnight (Globex) high / low | The nearest untested references at the cash open (practitioner view) | [Lore · UNTESTED] | Often paired with open types (§6) |
| Opening range (first 5/15/30/60 min) | Captures the opening volatility and imbalance spike | [Moderate · PR] crude oil; [Weak · VEN] equities | Condition on volatility and relative volume ("Stocks in Play") |
| VWAP / anchored VWAP | Execution benchmark; average cost of participants since the anchor | VWAP trend rule [Weak · VEN · MIXED]; AVWAP as S/R [Lore · UNTESTED] | `flowkit.py profile` (VWAP ±1/2σ bands; `--anchor` for AVWAP on bars) |
| Weekly / monthly high-low, swing extremes, 52-week high | Higher-timeframe stop and take-profit pools | [Lore] as S/R; 52-week-high momentum evidence is in `momentum-trading.md` / `technical-analysis.md` | `techkit indicators` gives Donchian 20/55 and the 52-week high/low |
| Prior value area / POC | Where yesterday's volume was accepted | [Lore · UNTESTED] (§6) | Profile definition choices change results |
| Prior close across a gap | Gap reference | Gap-day momentum [Contested · PR · MIXED] | Do not assume a fill |

```
VWAP_t = Σ(typical_i × volume_i) / Σ volume_i,  i from the session open (or the anchor bar for AVWAP) to t;  typical = (H + L + C)/3 on bars
```

**Reaction vs break: decision procedure.**
1. **Pre-mark levels** before the session and rank them by confluence (e.g. a round number at the prior-day high). Confluence is [Lore], but it is consistent with more orders being anchored there.
2. **Read the approach.** Fading momentum (smaller bodies, overlap, tails into the level, absorption on the tape) favors a **reaction**: take-profits and responsive liquidity. Strong momentum (consecutive trend bars, closes at extremes, no overlap) raises the odds of a **break**.
3. **A break is confirmed** by a decisive close beyond the level plus a follow-through bar. That favors a stop-driven extension: join on the first pullback or retest, and expect the move to play out within hours (Osler).
4. **A pierce that closes back inside within 1–3 bars** is a failed cascade (stops absorbed). Fade it with the stop beyond the sweep extreme (§4 failed-breakout card).
5. **Plan both scenarios** in advance, each with its own trigger, stop and target. Do not predict which one comes.

**Where stops and targets should and should not go (given order clustering):**
- **Do not park a stop in the crowd.** Just beyond a round number or obvious swing point is where same-direction stops cluster (FX stop buys: 14.4% at 01–10 above a 00). A stop there fills inside the cascade, with slippage. Put the stop where the thesis is invalidated. If that coincides with the crowd zone, add a volatility buffer (e.g. a fraction of ATR 14) and cut size so the dollar risk stays at 1R (inference from Osler).
- **Take profits in front of the number.** Take-profits cluster at 00 and rates tend to reverse there. In FX, rates spend *less* time at round numbers, so a target a few ticks in front fills more reliably than one at or beyond it (inference).
- **Breakout stop-entries just beyond a level are joining the cascade.** Expect slippage, and model it in c.
- **Fading at a level:** a resting limit order competes with the take-profit cluster and gets filled on the breaks that matter most. Prefer entering on a rejection bar's stop entry, or accept the adverse selection knowingly (inference).
- **Holding period:** cascades last hours, not days. Level-break trades are intraday-to-short-swing; multi-day holds need trend/momentum evidence (`momentum-trading.md`).

**Gap playbook:** default to momentum in the gap direction on the gap day (Plastun et al.). Fade only if intraday structure fails, e.g. an open-rejection-reverse or an opening-range break against the gap. Have the user measure their own fill rates by gap size in ATR units, because modern index-futures fill probabilities by gap size are not available in peer-reviewed form.

**Per-market notes:**

| Market | Level conventions | Data caveats |
|---|---|---|
| Index futures | RTH vs ETH sets prior-day H/L/C, overnight H/L and the profile; the cash open sets the opening range | CME aggressor flag makes order flow the most meaningful here (§7) |
| US equities | Premarket gaps; whole/half-dollar levels; Stocks in Play screen (Zarattini et al. via CXO: open > $5, 14-day average volume ≥ 1M shares, 14-day ATR > $0.50) | About half of volume is off-exchange (2025); trade direction is inferred |
| Spot FX | Big figures and 50s (best evidence, but 1999–2000 data); London and NY opens | No centralized volume; tick volume is only a proxy |
| Crypto | Trades 24/7, so "prior day", "open" and "weekly close" are conventions (e.g. a UTC boundary) and must be stated | Unregulated-venue volume is mostly wash trading; round-number effects are UNTESTED |

---

## 6. Auction market theory / Market Profile

Status: a rich *descriptive* framework [Lore · PL · UNTESTED]. No peer-reviewed test exists of the value area, POC, day types, open types or revisit claims. As an 80% figure, the 80% rule is [Lore · IT · UNTESTED-to-UNSUPPORTED]. Steidlmayer reportedly said the method had become subjective once trading hours were extended (a paraphrased forum claim).

| Term | Definition (standard practitioner reading) |
|---|---|
| TPO | Time-price opportunity: one letter per 30-minute period at each price traded (Steidlmayer, CBOT) |
| POC | The price with the most activity (TPO count or volume) |
| Value area (VA) | The central ~70% of activity around the POC, by analogy with ±1 SD |
| Initial balance (IB) | The range of the first two 30-minute periods |
| Range extension | Trading beyond the IB; its size and direction classify the day |
| Excess / tail | Single-print tail at an extreme = rejected prices; the auction found the other side quickly |
| Single prints | Levels with one TPO, left by a fast one-sided move. They separate the two value areas of a double-distribution day. "They get filled" is UNTESTED |
| Poor high / poor low | An extreme without excess (flat, several TPOs at the high or low, no tail), read as an unfinished auction. "It gets revisited" is UNTESTED |
| Balance / imbalance | Rotating inside accepted value / moving to find new value |

| Day type | Recognition (IB width, extension) | Common practitioner use (unsourced here; UNTESTED) |
|---|---|---|
| Normal | Wide IB, little extension | Fade IB extremes |
| Normal variation | Extension of about 1× IB | Trade the extension side after acceptance |
| Trend | Narrow IB, one-way extension, open and close at opposite extremes | Do not fade; buy or sell pullbacks |
| Double-distribution trend | Two value areas separated by single prints | Single prints act as the reference |
| Neutral (center / extreme) | Extension on both sides; closes in the middle / at an extreme | Center: fade both edges. Extreme: respect the close side |
| Non-trend | Narrow, low-activity day with little extension | Small size or stand aside |

Day-type definitions come from practitioner summaries (NexusFi, LuxAlgo), not checked against Dalton's text.

| Open type | What happens | Common practitioner use (unsourced here; UNTESTED) |
|---|---|---|
| Open-drive | Moves directionally at once and does not return | Highest conviction: go with it, stop beyond the open |
| Open-test-drive | Probes a reference (prior high/low, swing), reverses through the open, then drives | The failed probe's extreme is the stop reference |
| Open-rejection-reverse | Trades one way, meets opposite activity, returns through the opening range | Lower conviction; expect rotation |
| Open-auction | Rotates around the open | Range-day tactics |

Practitioners disagree where test-drive ends and rejection-reverse begins. Open types encode early-session imbalance, which ties to documented first-half-hour predictability [Strong · PR] (Gao et al.). The open-type taxonomy itself is untested.

**The 80% rule.**
- *Definition:* if the market opens outside the prior value area and then trades back inside it for two consecutive 30-minute periods, it has about an 80% chance of traversing to the other side of value.
- *Origin:* traced to Dalton Capital's *Profile Reports* (1987–1991), with no study behind the number.
- *Tests:*
  - One NexusFi member's TradeStation backtest found completion closer to **62%**, with no methodology shown [IT].
  - A separate unsourced claim puts it at 73–80% on ES/NQ.
  - Results depend on TPO vs volume value area, RTH vs ETH, and how "acceptance" is defined.
- *Completion rate is not edge (math):* at 62% completion with R = 1, EV = +0.24R gross. If the stop is twice the distance to target (R = 0.5), EV = 0.62 × 0.5 − 0.38 = −0.07R.
- **Test protocol to require:**
  - RTH TPO value area; an open outside the prior VA; two consecutive 30-minute closes inside.
  - Target = the opposite VA edge; stop = beyond the re-entry extreme.
  - Costs included; 3-year out-of-sample period; report expectancy in R, not just the completion %.

**How to use Market Profile:** as a context map. Ask where value is, whether the market is accepting or rejecting it, and whether today is balanced or imbalanced. Excess and tails are the same phenomenon as Osler's reflecting barriers and Garzarelli's bounces, and that is the defensible core. Do not quote 80%.

---

## 7. Order flow and tape

**Mechanism (Cont, Kukanov & Stoikov 2014)** [Strong · PR · SUPPORTED]:
```
For each top-of-book update n (Pb, qb = best bid price/size; Pa, qa = best ask):
 e_n = 1{Pb_n ≥ Pb_n-1}·qb_n − 1{Pb_n ≤ Pb_n-1}·qb_n-1 − 1{Pa_n ≤ Pa_n-1}·qa_n + 1{Pa_n ≥ Pa_n-1}·qa_n-1
OFI_k = Σ e_n over interval k        ΔP_k ≈ β·OFI_k + ε,   β ∝ 1 / average depth at the best quotes
```
In words: OFI is net limit, cancel and market-order flow at the inside. The same aggressive flow moves a thin book further than a deep one. **Absorption** = heavy aggressive volume (or OFI) with little ΔP, which means large and often refilling depth on the other side. This is Wyckoff's "effort without result".

| Tool | Shows | Cannot show | Evidence |
|---|---|---|---|
| DOM (depth of market) | Displayed resting orders near the inside | Hidden/iceberg size; intent (displayed size can be cancelled) | Book resiliency [Contested · PR/WP · MIXED]: spreads recover fast and depth slowly, with depth refilled mainly by human liquidity providers (Clapham et al. 2021); another study finds the book fails to replenish after large trades in > 60% of cases (Xu et al.) |
| Time & sales | Executed prints: price, size, time, aggressor side if the feed carries it | In US equities, direction is inferred, and many prints are off-exchange | See the data table below |
| Footprint / cluster | Bid-hit vs ask-lift volume per price per bar | Only as good as aggressor classification | [Lore · UNTESTED] net of costs |
| Cumulative delta (CVD) | Running aggressive buys − sells | Noisy where signing is inferred; divergences have no peer-reviewed support | [Lore · UNTESTED] |
| Absorption | Big aggressive volume, no progress | Whether the passive side is one player or many | Mechanism consistent with CKS [Strong]; as a signal UNTESTED |
| Icebergs / hidden liquidity | Repeated prints at one price exceeding displayed size | Retail iceberg-detection accuracy is unquantified | [Weak · WP]: hidden depth can be inferred from public data, and other traders react to it; it goes with more book liquidity, higher volume and smaller impact; icebergs impose adverse selection on displayed orders (Frey & Sandås, Xetra) |

**Horizon rule:** imbalance predictability decays within minutes (Chordia, Roll & Subrahmanyam 2005). Use the tape to *time* an entry or exit at a level planned in advance, or to abort a trade. Do not hold a swing trade on a delta reading.

**Data quality by market:**

| Market | Aggressor side | Volume coverage | Verdict |
|---|---|---|---|
| CME futures | True: MDP 3.0 Trade Summary AggressorSide (tag 5797: 0 none, 1 buy, 2 sell). Trades against implied orders and the first trade after a Velocity Logic re-open can have no aggressor; normalized feeds set implied trades' side to None | Single venue | Best case for footprint and delta |
| US equities | Inferred: on Nasdaq trades, the quote rule is 76.4% accurate, tick 77.66%, Lee-Ready 81.05%. All rules do poorly inside the quotes, biasing large trades, high-volume periods and ECN trades (Ellis, Michaely & O'Hara 2000) [Moderate · PR]. Bulk volume classification underperformed a standard tick rule against a near-perfect CME benchmark (a result usually attributed to Andersen & Bondarenko 2015; Chakrabarty, Pascual & Shkilko 2015 used equity data); its accuracy is [Contested] | Off-exchange (TRF) = **50.6% of consolidated volume in 2025**, a record; dark ATSs about 14–18%, most of the rest wholesaler/bilateral; Nov 2024 was the first month with more volume off-exchange than on (Cboe, Rosenblatt, Nasdaq) | A single-exchange footprint misses about half the volume; CVD is noisy |
| Spot FX | None centralized | Tick-volume proxies only | Order-flow and VSA readings are proxies |
| Crypto | Venue-specific | Of the 29 exchanges studied (regulated and unregulated), wash trading averaged > 70% of reported volume on the unregulated ones and was absent on regulated ones (Cong, Li, Tang & Yang 2023; WP figure 77.5% mean / 79.1% median) [Moderate · PR · SUPPORTED] | Use regulated or major-venue data only; the sample predates publication, so re-check venues |

**Spoofing: illegal to do; learn to recognize it.**
- **Law:** Dodd-Frank added CEA §4c(a)(5)(C), which prohibits bidding or offering with intent to cancel before execution. It requires intent beyond recklessness; a partial fill does not excuse it, and a single instance can suffice. Exposure, per a 2015 law-firm article (verify current figures): criminally, up to 10 years and $1m per count; civilly (CFTC), penalties of the greater of $1m or 3× the gain per violation. The first criminal prosecution was *U.S. v. Coscia*.
- **Recognition:** large displayed orders away from the inside that cancel as price approaches, repeatedly. Do not "trade the size" on the book at face value. Weight *executed* volume and absorption over resting size.
- **Coaching boundary:** never explain how to place or time non-bona-fide orders, or how to move price deliberately to trigger others' stops. Both are prosecuted as manipulation, civilly and criminally.

---

## 8. Wyckoff/VSA and ICT/SMC

**Wyckoff** [Lore · PL · UNTESTED]
- **Three laws:** supply/demand; cause and effect (the horizontal point-and-figure count of a range projects the move, UNTESTED); effort vs result (a volume–price divergence warns of a turn).
- **Five steps:**
  1. Assess the trend and position.
  2. Pick relative-strength (or weakness) leaders.
  3. Require a big enough cause for the price objective.
  4. Confirm readiness with the nine buying/selling tests.
  5. Time the entry with a market turn, then trail a stop.
- **Accumulation:** PS → SC (selling climax) → AR (sets the range top) → ST (secondary test, lower volume) → **Spring** (dip below the range low, back inside, trapping sellers) → Test → SOS → LPS (higher low, low volume) → BU. Phases: A stop of the prior trend, B build the cause, C spring/test, D demand dominates, E markup.
- **Distribution:** PSY → BC → AR → ST → **UTAD** (traps breakout buyers) → SOW → LPSY → markdown.
- **Composite Man:** a heuristic of one large operator running campaigns.
- **Evidence:** peer-reviewed Wyckoff work is very sparse; the one named paper is in a low-tier journal and is preliminary. Critics say the schematics can rationalize almost any price action after the fact. Pruden & Belletante's proposed forward test has no reported outcome.

**VSA (Tom Williams)** [Lore · PL · UNTESTED]
- **No demand:** an up bar, narrow spread, volume below the prior two bars.
- **No supply:** a down bar, narrow spread, low volume.
- **Stopping volume:** a heavy-volume bar that halts a decline, ideally followed by a low-volume **test** (high volume on the test means it failed).
- **Upthrust:** a wide-spread up move on high volume that closes on its low or back under resistance.
- In spot FX these readings rest on tick volume.

**Make it mechanical before trusting it:** spring = a close back inside the range within N bars after trading ≥ X ticks below the range low, on volume above the 20-bar average. Stop below the spring low; target the range midpoint or top. Then test it (§9).

**ICT / Smart Money Concepts** (originator Michael Huddleston). Concepts are [Lore · PL · UNTESTED]; specific fill-rate and "institutional" claims are UNSUPPORTED.
- **FVG:** a three-candle imbalance where candle 1's high does not overlap candle 3's low (bullish; mirror for bearish), with displacement in candle 2. Fill-probability claims of 80–92% are unsourced.
- **Order block:** commonly the last opposing candle before a strong displacement; it has no rigorous definition.
- **OTE:** the 62–79% retracement of an impulse leg, with 70.5% as the "sweet spot", i.e. the classical 0.618–0.786 band. Claims that institutional orders cluster there are assertions.
- **Kill zones:** e.g. London about 2–5 AM ET and the New York open. Times vary by source, with no official definition.
- **Vendor backtests:** e.g. about 1,247 EUR/USD and XAU/USD FVG-retest and sweep trades, 2019–2024 [Weak · VEN], promotional and not reviewed.
- **Unverified:** a reported 2026 preprint concluding that the concepts do not work as literally taught could not be traced to a primary source.

**Random baseline for FVGs (simulation run this session):** in a driftless Gaussian random walk with bars built from 20–240 sub-steps, **24–30% of bars complete a 3-bar FVG** (about 12–15% per direction). An unverified search-summary figure of about 29.8% is consistent with this. An FVG's mere existence is therefore noise-level common; any FVG rule must beat random entries under the same filter.

**Translation table:**

| ICT / SMC / Wyckoff term | Older concept | Evidenced or tested mechanism | Status |
|---|---|---|---|
| Liquidity pool (buy-side / sell-side) | Stops above swing highs and below lows; round numbers | Stops cluster just beyond levels (Osler 2003) | Mechanism [Moderate · PR · SUPPORTED, FX]; "engineered by smart money" UNSUPPORTED |
| Liquidity sweep / stop hunt | Brooks failed breakout; Wyckoff spring/UTAD; stop run | Cascades from stop clusters (Osler 2005); failure = stops absorbed; bounce effect (Garzarelli) | Pattern UNTESTED; mechanism partly SUPPORTED |
| Fair value gap | Brooks breakout / measuring gap; classic "imbalance" | None direct; 24–30% of random-walk bars produce one | UNTESTED; fill rates UNSUPPORTED |
| Order block | Supply/demand zone; last opposing bar before a breakout | Levels as order anchors (Osler 2000; Garzarelli), indirectly | UNTESTED |
| OTE (62–79%) | Fibonacci 0.618–0.786 pullback | None; pullback depth untested (Fibonacci statistics in `technical-analysis.md`) | UNTESTED |
| Kill zones | Session opens; time-of-day | U-shape, FX periodicity, first-half-hour momentum [Strong] | Timing basis SUPPORTED; exact windows UNTESTED |
| BOS / CHoCH | Dow HH/HL; Brooks trend-line break + test (MTR) | None | UNTESTED (state description) |
| Displacement | Spike; consecutive trend bars | OFI exceeding depth (CKS) | Mechanism SUPPORTED; as a signal UNTESTED |
| "Sweep → FVG → OTE entry" | Brooks failed breakout + L2/H2; Wyckoff UTAD → LPSY (spring → LPS) | Failed stop cascade, then a pullback entry | UNTESTED |
| Effort vs result (Wyckoff/VSA) | Absorption | Volume or OFI without price impact = deep opposite depth (CKS) | Mechanism SUPPORTED; signal UNTESTED |

Real stop cascades arise mechanically from order clustering. *Deliberately* moving price to trigger stops with manipulative orders is illegal; never teach it as a technique.

---

## 9. Quantify your setup

**Template (enforce before any live size):**
1. **Context filter**, objective: trend/range state (20-EMA slope, HH/HL count, ADX threshold), time-of-day window, and key-level proximity in ticks or ATR.
2. **Trigger**, an exact bar condition. Example: bull signal bar closing in the top third, range ≤ 1 ATR, second leg down (H2), within 2 ticks of the prior-day low.
3. **Entry:** stop order 1 tick beyond the signal bar; cancel if not filled within N bars.
4. **Stop:** 1 tick beyond the signal bar or swing; record initial risk = 1R.
5. **Targets and management:** e.g. half off at 1R or the measured move, stop to breakeven after X, time stop at the session end.
6. **Costs:** commission plus realistic slippage, at least 1 tick per side on stop entries in futures.
7. **Evaluation:**
   - win rate, average win and loss in R, expectancy, MAE/MFE distribution;
   - results by context bucket and by time of day;
   - a **random-entry baseline** under the same filter and exits;
   - an in-sample / out-of-sample split by time, then walk-forward.
   - Count every variant tried as a trial (deflated Sharpe in `quant-research-validation.md`).

**Sample-size math** (math; expectancy rows computed with `tradekit.py expectancy` this session):

| Question | Assumption | Trades needed |
|---|---|---|
| Win rate 55% vs 50% | 95% CI half-width ±5 pp: n ≈ 1.96²·0.25/0.05² | ≈ 384 (only ~50% power); ≈ 780 for 80% power |
| Win rate ±10 pp | same formula | ≈ 96 |
| Mean R > 0 at t = 2 | n ≈ (2·σ_R / E[R])², σ_R = 1.2R, E[R] = +0.2R | ≈ 144 |
| Same, smaller edge | σ_R = 1.2R, E[R] = +0.1R | ≈ 576 |
| Brooks "uncertain" default | 40% @ 2R: +0.2R, σ 1.47R | 216 (t = 2), 486 (t = 3) |
| Brooks "confident" default | 60% @ 1R: +0.2R, σ 0.98R | 97 (t = 2), 217 (t = 3) |
| Thin scalp | 55% @ 1R: +0.1R, σ 0.995R | 396 (t = 2), 891 (t = 3) |

- 30 trades (a common rule of thumb) detects only very large edges or obvious failure, not a Brooks-style +0.2R. A "30+ positive-EV samples before live" threshold attributed to SMB comes from a low-authority site and is unverified.
- No authoritative prop-firm standard for per-setup samples was found; the figures above are standard statistics.

**SMB PlayBook-style training loop** [Lore · PL; the structure follows SMB, and the replay specifics are standard practice, unsourced]:
1. **Playbook:** each A+ setup is documented (chart, catalyst, context, entry, exit, stats in R and MAE/MFE). The head trader reviews and annotates it before it is shared with the desk.
2. **Replay:** bar by bar with the right side hidden. Predict the next bar and log the reason.
3. **Journal:** a screenshot per trade with the setup label, context, the trader's-equation estimate made *before* entry, the outcome and MAE/MFE.
4. **Review cadence:** daily, weekly, monthly. A "good trade" is graded by process (rules, sizing, risk, own setup), not by outcome.
5. **Promote or demote setups** weekly by measured expectancy. Add size only for setups with stable expectancy across conditions.
6. **Progression:** simulator → minimum size → scale only after the sample thresholds above.

*Why objective logs:* learning among day traders is slow and biased, and 74% of day-trading volume comes from traders with a history of losses (Barber et al. 2020). SMB's "Stocks in Play" focus matches the later finding that restricting ORB to high-relative-volume names improved results.

---

## 10. Base rates for intraday discretionary traders

| Dataset | Sample | Finding | Caveats |
|---|---|---|---|
| Brazil, mini-Ibovespa futures (Chague, De-Losso & Giovannetti 2019) | 19,646 individuals who started day trading in 2013–2015; 1,551 (7.9%) persisted > 300 sessions | 97% of persistent traders lost money; 1.1% earned more than the minimum wage; 0.5% more than a bank teller's starting salary | One market; possibly a difficult period |
| Taiwan, all trades 1992–2006 (Barber, Lee, Liu, Odean & Zhang 2020) | About 360,000 day traders in an average year | About 15% earn abnormal returns, but only about 1,000 (~0.3%) *predictably* outperform; aggregate performance negative; losers more likely to quit, but learning slow | All day traders, not price-action traders specifically |
| EU retail CFDs (ESMA, Mar 2018) | National regulators' account analyses | 74–89% of accounts lose money; average loss per client €1,600–€29,000 → 2018 leverage caps, negative-balance protection and risk warnings | Leverage-heavy product |

The convergent conclusion is [Strong]; each dataset alone is [Moderate]. No study isolates *discretionary price-action* traders, and prop-firm evaluation pass rates were not researched.

**Using the base rates without lecturing:**
- State them once, with numbers, when a plan implies living off day trading or scaling before proof. Then move straight to the gate: cost-inclusive positive expectancy over the §9 sample, simulator → minimum size.
- Mechanical ORB and intraday-momentum rules show positive results while most individuals lose. The gap is likely in execution, costs, selectivity and discipline. This is an inference that the cited studies do not test directly.
- For the coaching conversation itself, see `trader-psychology-process.md` §15.

---

## 11. Failure modes / traps

- **Quoting lore percentages as statistics** (Brooks's 80%, the Profile 80% rule, ICT fill rates). Catch: ask "measured by whom, on what data, with what definition?"
- **Setup without context:** an H2 after a climax, breakout buys in the middle of a range, fading a micro channel. Catch: require the phase label (§3) on every journal entry.
- **Ignoring costs on tight stops.** Catch: compute c = cost ticks / stop ticks; if c ≥ the gross edge, the setup is dead.
- **Stops at the obvious tick beyond a round number or swing**, then blaming "stop hunts". Catch: compare stop placement with the nearest round number and swing extreme.
- **Trading DOM size at face value** (spoofed or cancelled orders). Catch: did the size *execute*?
- **Equity footprint/CVD treated as CME-quality,** or crypto volume taken from unregulated venues. Catch: ask the feed and venue.
- **Holding a level-break trade for days on intraday cascade logic.** Catch: the holding period must match the evidence (hours).
- **"Gaps always fill", "single prints always fill", "poor highs always get revisited".** All untested or contradicted.
- **Hindsight labeling:** Wyckoff phases, order blocks and MTRs assigned after the move. Catch: demand time-stamped, pre-entry screenshots.
- **Small or cherry-picked samples:** 20–30 trades, or a gallery of winners. Catch: run `expectancy --trades N` and report the t-stat.
- **Tuning until it works:** stretch size, OR length, VA definition, kill-zone hours. Catch: count trials and deflate (`quant-research-validation.md`).
- **Inconsistent RTH/ETH or crypto day boundaries** between level marking and backtest.
- **Timeframe shopping:** switching timeframes until one confirms the trade. Treat each switch as a trial.
- **Assuming Osler's 1999–2000 numbers hold exactly** in today's algorithmic FX or in crypto. The mechanism is plausible; the magnitudes are unverified.
- **FVG or other pattern presence treated as a signal** without a random baseline (24–30% of random-walk bars have an FVG).
- **Trusting vendor backtests** (Concretum, Backtrex, course sellers) without slippage, period and conflict checks.
- **Any request to spoof, layer or deliberately run stops.** Refuse the technique; explain recognition and the law.

---

## 12. Toolkit hooks

Run these instead of doing mental math:

- **Setup expectancy and sample size:** `python scripts/tradekit.py expectancy --p 0.4 --win 2 --loss 1 --trades 100`. It gives EV in R, break-even win rate, σ per trade, trades needed for t = 2/3 and the t-stat at the trades observed. This example gives +0.2R, σ 1.47R, 216/486 trades and t = 1.36 at 100 trades. To net out costs, subtract c from the win and add it to the loss, e.g. `--win 1.9 --loss 1.1` for c = 0.1R.
- **Size from the level-based stop:** `python scripts/tradekit.py size --equity 50000 --risk 0.5 --entry 5000 --stop 4995 --multiplier 50 --target 5010`. It gives units, cash at risk, R:R and a notional/leverage warning; this example is 1 contract, $250 risk, 2R, with a 5× notional warning. Use `--atr X --atr-mult k` for a volatility stop when a buffer beyond the crowd zone is needed (§5).
- **Drawdown/ruin for a setup's stats:** `python scripts/tradekit.py ruin --p 0.4 --b 2 --risk 1 --trades 250 --limit 20`. This session it gave P(drawdown ≥ 20%) ≈ 8.9% and a median max drawdown of 12.5% for a +0.2R setup at 1% risk.
- **Swing levels and phase proxies:** `python scripts/techkit.py indicators FILE` reports Donchian 20/55 highs and lows (prior bars), 52-week high/low, ATR14, ADX14 (> 25 trending, < 20 range), a Bollinger squeeze flag (bandwidth rank ≤ 10%) and relative volume. It is bar-agnostic: on intraday CSVs, "52w" means 252 bars, and you must pass `--ppy` (bars per year) so the 20-bar realized vol annualizes correctly. It does **not** compute VWAP, profile or delta — use `flowkit.py` for those (next bullet). Prior-day H/L/C from intraday bars, overnight H/L, the opening range and pivots are not automated; read them from the data directly.
- **Value, VWAP and order flow:** `python scripts/flowkit.py profile FILE` gives POC, the 70% value area, HVN/LVN and VWAP with ±1/2σ bands (exact volume-at-price from a trades CSV; approximate from OHLCV bars; `--anchor YYYY-MM-DD` for an anchored profile/VWAP on bars, `--last N` for the most recent N bars/trades, `--show` for the histogram). `python scripts/flowkit.py delta TRADES.csv --bar 1m` builds bars with buy/sell volume, delta and CVD, and flags stacked imbalances, absorption, delta divergences and unfinished auctions at swing extremes. Free crypto tape with true aggressor side: `python scripts/fetch.py trades BTC`.
- **Mechanical proxies for level logic:** `python scripts/techkit.py ruletest FILE --rule donchian --params 20 55 --short --cost-bps 5 --oos 0.3` tests breakout-of-level logic; `--rule bbrev` tests range-fade logic. Both fill at the next bar's close (`--delay 1`; next-open fills are not modelled) and apply costs, a parameter grid, DSR and an OOS split; pass `--ppy` on intraday bars so Sharpe and vol annualize correctly. Brooks, Profile, Wyckoff and ICT setups are *not* built-in rules. Test them outside the toolkit, then feed per-trade R into `expectancy`, or a returns series into `python scripts/tradekit.py perf FILE --trials N`.
- **Several setups or variants tried:** `python scripts/tradekit.py sharpe --sr ... --n ... --trials N --var-sr ...` gives PSR/DSR. Kurtosis is raw (normal = 3).

---

## 13. Key sources

- Osler 2003, "Currency Orders and Exchange Rate Dynamics" (round-number clustering), J. Finance 58(5) — https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr125.pdf
- Osler 2005, "Stop-loss orders and price cascades in currency markets," JIMF (NY Fed SR150) — https://www.newyorkfed.org/research/staff_reports/sr150.html
- Osler 2000, "Support for Resistance," FRBNY Economic Policy Review 6(2) — https://www.newyorkfed.org/research/epr/00v06n2/0007osle
- Bhattacharya, Holden & Jacobsen 2012, round-number trading in equities, Management Science 58(2) — https://pubsonline.informs.org/doi/10.1287/mnsc.1110.1364
- Garzarelli et al. 2014, support/resistance memory, Scientific Reports — https://arxiv.org/abs/1110.5197
- Cont, Kukanov & Stoikov 2014, "The Price Impact of Order Book Events," J. Fin. Econometrics — https://arxiv.org/abs/1011.6402
- Chordia, Roll & Subrahmanyam 2005, speed of convergence to efficiency, JFE — https://escholarship.org/content/qt8wb6140g/qt8wb6140g.pdf
- Gao, Han, Li & Zhou 2018, "Market Intraday Momentum," JFE — https://econpapers.repec.org/RePEc:eee:jfinec:v:129:y:2018:i:2:p:394-414
- Baltussen, Da, Lammers & Martens 2021, "Hedging Demand and Market Intraday Momentum," JFE — https://www3.nd.edu/~zda/intramom.pdf
- Heston, Korajczyk & Sadka 2010, intraday return periodicity, J. Finance — https://arxiv.org/abs/1005.3535
- Holmberg, Lönnbark & Lundström 2013, ORB in crude-oil futures, Finance Research Letters — https://econpapers.repec.org/RePEc:eee:finlet:v:10:y:2013:i:1:p:27-33
- Zarattini, Barbon & Aziz 2024, ORB on Stocks in Play [VEN] — https://ideas.repec.org/p/chf/rpseri/rp2498.html
- Plastun, Sibande, Gupta & Wohar 2020, price gaps 1928–2018, NAJEF — https://repository.up.ac.za/handle/2263/78336
- Ellis, Michaely & O'Hara 2000, trade-classification accuracy, JFQA — https://ideas.repec.org/a/cup/jfinqa/v35y2000i04p529-551_00.html
- Cong, Li, Tang & Yang 2023, crypto wash trading, Management Science — https://nber.org/papers/w30783
- Barber, Lee, Liu, Odean & Zhang 2020, "Learning, Fast or Slow," RAPS — https://econpapers.repec.org/RePEc:oup:rasset:v:10:y:2020:i:1:p:61-93
- Chague, De-Losso & Giovannetti 2019, Brazilian day traders, SSRN — https://papers.ssrn.com/abstract=3423101
- ESMA 2018, CFD product intervention (74–89% of accounts lose) — https://www.esma.europa.eu/node/84933
- Brooks, price-action glossary and course transcript [PL] — https://www.brookstradingcourse.com/price-action-trading-terms-glossary/ ; https://www.brookstradingcourse.com/?p=51932
- Dalton, Jones & Dalton, *Mind Over Markets* (1990; Wiley ed. 2013) [PL] — https://www.oreilly.com/library/view/mind-over-markets/9781118659762/
