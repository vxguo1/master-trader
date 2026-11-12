# Day Trading

*Read when: a user day trades or wants to (intraday stocks, ETFs, index futures, crypto), asks for levels, an
opening-range or VWAP plan, a stocks-in-play or small-cap momentum list, bracket orders, a daily loss limit, the
PDT rule, paper trading, or a review of their day-trade journal.* Evidence tags: [Strong] peer-reviewed or official,
[Moderate] working paper or preliminary official, [Weak] secondary or community backtest, [Lore] vendor or
practitioner claim. Research cut-off 12 Nov 2026.

## Contents
1. What a day trader is up against
2. Where intraday edges are documented, and what survives costs
3. Rules and account mechanics (US, Nov 2026)
4. The session map: times, volume curve, levels, day types
5. The daily routine (with toolkit commands)
6. Setup rule cards
7. Small-cap momentum selection (five criteria)
8. Risk rules for day trading
9. Bracket orders
10. From paper to live
11. Journal review
12. Toolkit hooks
13. Sources

---

## 1. What a day trader is up against

- **Base rates are brutal and stable across markets.** Brazil futures: 97% of persistent day traders lost money
  [Strong]. Taiwan: under 1% predictably profitable after fees [Strong]. India (SEBI census data):
  - Equity cash, FY23: 71% of individual intraday traders lost, and 80% of those with more than 500 trades a year [Strong].
  - F&O: 93% lost over FY22-24; 87.7% lost in FY26 [Strong].
  - **Only 0.5% of traders active every year FY22-26 were profitable in all five years; 65.6% lost in every year** [Strong].
  - Costs equalled 57% of losers' losses (cash segment).
- **No credible 2022-26 US account-level day-trader P&L study exists.** The "72% lost (FINRA)" figure is
  unverified; do not quote it.
- **Prop-firm evaluations:** Topstep (vendor disclosure, 2025) reported 16.8% of evaluations passed, 33% of
  funded traders paid out, and 0.71% of sim-funded traders moved to a live account [Lore]. Fees, not trading,
  drive that business.
- **Costs are the first-order problem.** Intraday edges are measured in basis points. A 2 bp round trip eats most
  published ORB and VWAP edges on liquid ETFs (§2); small caps cost 20-100+ bp round trip.
- Use these to set the gate (§10), not to sneer. Say them once, with numbers, then move to the plan.

## 2. Where intraday edges are documented, and what survives costs

| Effect | Evidence | Net of realistic costs | Grade |
|---|---|---|---|
| First half-hour → last half-hour (market intraday momentum) | SPY 1993-2013, R² ~1-2% (Gao, Han, Li, Zhou 2018); hedging-demand channel (Baltussen et al. 2021) | Small; on SPY hourly bars 2024-26 the toolkit found corr −0.03 (t −0.8): **not present in that window** | [Strong] historical, unproven now |
| Half-hour periodicity | Same half-hour continues at daily lags (Heston, Korajczyk, Sadka 2010) | Too small to trade alone | [Moderate] |
| Opening-range breakout (crude oil) | Holmberg, Lönnbark, Lundström 2013 | One market, in-sample | [Moderate] |
| ORB on QQQ / stocks in play | Zarattini & Aziz 2023; Zarattini, Barbon & Aziz 2024 (vendor) | **Independent replications: gross edge reproduces, net ≈ 0.** NQ 2015-26 +0.13R gross → +0.002R net; SPX, Dow, DAX, FTSE negative net (Krueger 2026). QQQ 2004-24 turns negative with 2c/4c slippage (Girlando) | [Weak] net |
| VWAP trend (long above / short below) | Zarattini & Aziz 2023 (vendor), QQQ 2018-23 | QuantConnect reproduction: out-of-sample Sharpe ~0.7, **break-even below ~1 bp round trip** | [Weak] |
| SPY noise-band momentum | Zarattini, Aziz & Barbon 2024 (vendor) | No independent net-of-cost replication found | [Lore] until replicated |
| Overnight vs intraday returns | Equity premium earned overnight; momentum overnight, other anomalies intraday (Lou, Polk, Skouras 2019) | Hard to monetise after costs | [Moderate] |
| Round-number clustering | Take-profits at the number, stops just beyond | A location effect, not a strategy | [Strong] |

Reading the table: the published intraday edges are real but tiny, and they need institutional costs. A retail day
trader's plausible edges are **selection** (trade only in-play names on news), **execution** (limit orders,
avoiding the open's spread), and **discipline** (small losses, no tilt). Those cannot be backtested from bars, so
they must be proven in the journal (§10-11).

## 3. Rules and account mechanics (US, Nov 2026)

- **The pattern-day-trader rule is gone, with a transition.** The SEC approved SR-FINRA-2025-017 on 14 Apr 2026,
  effective **4 Jun 2026** (FINRA RN 26-10) [Strong].
  - Removed: the PDT label (4+ day trades in 5 business days), the **$25,000 minimum** and 4x day-trading buying power.
  - Replaced by **intraday margin** (Rule 4210(d)(2)): normal maintenance margin applied to intraday exposure.
    A deficit must be met promptly, within 15 business days at most.
  - Repeatedly missing deficits by the 5th day brings a 90-day freeze. Deficits below 5% of equity or $1,000 don't count.
  - The $2,000 margin minimum stays.
  - **Brokers may keep the old rules until 20 Oct 2027.** Always ask which regime the user's broker applies.
- **Cash accounts** were never under PDT. Reg T still applies:
  - **Free-riding** (selling before paying with settled funds) brings a 90-day freeze.
  - **Good-faith violations** (buying with unsettled proceeds, then selling before they settle) trigger broker restrictions.
  - Settlement is **T+1** (since 28 May 2024), so settled cash turns over about once a day.
- **Fees on sales:** SEC Section 31 is **$20.60 per $1M** of sales (from 4 Apr 2026). FINRA TAF is $0.000195/share
  (max $9.79), **$0 from 1 Oct to 31 Dec 2026**, back on 1 Jan 2027 and held at 2026 rates through 2028 [Strong].
- **Tick size:** still $0.01. The half-penny tick and the lower access-fee cap were **postponed to Nov 2027**
  (SEC order 34-105656) [Strong]. Round-lot tiers changed on 3 Nov 2025, so a "round lot" is smaller for
  high-priced stocks.
- **Overnight equity trading:** five exchanges are approved, but none trades overnight yet; the target is 6 Dec
  2026, limit orders only [Weak; unverified go-live]. Today overnight volume (~0.9%) runs on ATSs with wide
  spreads: off-hours prints are thin and sometimes bad ticks (`levels` ignores outliers).
- **Micro futures (CME):**
  - MES is $5 per S&P point (tick 0.25 = $1.25); MNQ is $2 per Nasdaq-100 point (tick 0.25 = $0.50).
  - Hours run Sunday 6 pm to Friday 5 pm ET, with a daily 5-6 pm ET break.
  - All-in costs are about $0.60-1.25 per side.
  - Futures are CFTC/NFA accounts: no PDT and no securities intraday-margin rule; margins are broker house terms.
- **Short selling:** needs a borrow (hard-to-borrow fees on small caps). **Rule 201 (SSR)** restricts short sales
  to above the national best bid after a stock falls 10% from the prior close, for that day and the next [Strong].
- **Halts:** limit up-limit down (LULD) pauses trading for 5 minutes when price leaves its band. Low-priced, thin
  stocks halt often, and a stop does not protect you through a halt.
- **Taxes:** short-term gains, wash sales and trader tax status are outside this skill. Tell the user to ask a tax professional.

## 4. The session map: times, volume curve, levels, day types

**Clock (ET):**
- 04:00-09:30 pre-market (thin; levels form).
- 08:30 US data (CPI, jobs, claims).
- 09:30 open (widest spreads, biggest volume).
- 10:00 data (ISM, sentiment, JOLTS).
- 11:30-14:00 midday lull.
- 14:00 FOMC (8 times a year) and minutes.
- 15:50 closing-auction imbalances published.
- 16:00 close.
- Futures trade around the clock: the cash open still sets the opening range.

**Volume curve** (SPY, 2024-26): about 23% of the day's volume trades in the first hour, 9-11% per hour at midday,
and 19% in the last half-hour. Volatility follows the same U. `timeofday` prints it for any symbol. Relative
volume must be compared at the same time of day; `levels` and `inplay` do this.

**Levels to mark before the open** (`order-flow.md` §6 has the order-flow versions):
- Prior day high, low and close.
- Overnight (pre-market) high and low.
- The opening range, 5, 15 and 30 minutes.
- Session VWAP and its 1-2σ bands.
- Round numbers.
- The prior day's value area.

Location beats signal: a breakout through the prior day's high on heavy volume is a different trade from a
breakout in the middle of yesterday's range.

**Day types** (`levels` reads these mechanically; [Lore] taxonomy, useful as a filter):
- **Trend day:** price stays on one side of VWAP, moves at least 60% of its daily ATR, crosses VWAP 3 times or fewer.
  Fade nothing; trail.
- **Range / balance day:** 5+ VWAP crosses or price stuck inside the opening range. Breakouts fail more often;
  either stand aside or mean-revert at the edges.
- **Gap day:** the open is more than 1 ATR from the prior close. Ranges widen; cut size. `backtest --rule gap`
  shows how often gaps of each size filled and drifted in that symbol.

## 5. The daily routine (with toolkit commands)

**Pre-market (08:00-09:25 ET)**
1. Macro and calendar: `fetch.py macro` (plain-English block first); scheduled data, FOMC and earnings.
2. Watchlist: `daykit.py inplay --universe megacap --symbols <your list>` (gap, pre-market relative volume, ATR,
   liquidity). For small caps after the open: `scanner.py smallcap` (§7).
3. For each name: `fetch.py prices SYM --interval 5m --days 30 --prepost`, then `daykit.py levels FILE --equity E`.
4. Write the plan before the bell: the setup, trigger, stop, target and size for each name, the daily loss limit
   and the max trade count (`daykit.py plan`).

**Session**
5. No trades in the first opening range, 5 minutes by default (`levels` says "Wait until 09:35").
6. Enter only with a bracket (§9). Size from the stop, never from conviction.
7. Stop for the day at the daily loss limit or the max trade count, whichever comes first.
8. Flatten day trades by 15:55 unless the plan says otherwise. Holding overnight converts a day trade into gap risk.

**After the close**
9. `paperkit.py trades --csv t.csv` then `daykit.py journal t.csv`: expectancy by setup, hour and trade number,
   and after a loss vs after a win.
10. One change per week at most, decided from the journal, never mid-session.

## 6. Setup rule cards

Each card gives rules, evidence and what the toolkit can test. "Test" means `daykit.py backtest FILE --rule ...`.
Yahoo's 5-minute bars span about 2 months (40 sessions): far too few to prove an edge. Hourly bars span 2
years (~500 sessions) and support 60-minute ranges and the first-hour → last-half-hour test.

**Opening-range breakout (ORB)**
- **Range:** high and low of the first N minutes (5 in the vendor studies; 15 and 30 common).
- **Entry:**
  - `break` mode: buy-stop above the high or sell-stop below the low after the range completes; the first touch wins.
  - `candle` mode (Zarattini & Aziz): trade in the direction of the range's own move, enter at the next bar.
- **Stop:** the other side of the range. If that is wider than half an ATR, use 10% of the daily ATR (the
  stocks-in-play variant).
- **Target:** the papers used 10R, which is effectively hold to the close. A 2R bracket target raises the hit
  rate and cuts the payoff; test both.
- **Filters:** relative volume at least 1, price and VWAP on the same side, a catalyst for single stocks.
- **Evidence:** [Weak] net of costs (§2). **Test:** `--rule orb --or 5 --mode break|candle --target-r 2|10 --grid`.
  The grid deflates the best of 16 variants (DSR).

**VWAP trend**
- Long while above VWAP, short below, decided at each bar's close and filled at the next open.
- Flips often on range days, so costs decide it: break-even is below ~1 bp round trip. [Weak]
- **Use instead as a filter:** take ORB longs only above VWAP. **Test:** `--rule vwap`.

**First half-hour → last half-hour (intraday momentum)**
- If the return from the prior close to 10:00 is positive, go long from 15:30 to the close (short if negative).
- Documented on SPY [Strong historically]; strongest on high-volume, high-volatility and news days.
- The toolkit's 2024-26 hourly test found no effect. Treat it as a lean, not a trade.
- **Test:** `--rule imom` (hourly bars use the first hour).

**Noise-band momentum** (Zarattini, Aziz & Barbon)
- **Bands:** the open (or prior close) ± the 14-day average absolute move from the open at each time of day.
- **Entry:** checked every 30 minutes; enter on a close outside the band.
- **Exit:** at max(band, VWAP) for longs, min(band, VWAP) for shorts.
- [Lore] until replicated net. **Test:** `--rule noise` (needs 15+ sessions of history).

**Gap behaviour (study, not a rule)**
- `--rule gap` buckets gaps by ATR and reports how often each bucket filled, the open-to-close drift, and how
  often price kept going.
- Use it to decide "fade or go" per symbol, then trade the decision with a bracket at a level.

**Stocks in play** (screen for all of the above)
- Filters: price above $5, 14-day average volume at least 1M, ATR at least $0.50, relative volume at least 1 at
  the same time of day, plus a catalyst. `daykit.py inplay`. [Weak, vendor]
- The single most defensible day-trading habit: trade names with a reason to move today and leave the rest.

## 7. Small-cap momentum selection (five criteria)

The user's daily selection (`scanner.py smallcap`) scores today's US-listed gainers on five criteria:

| # | Type | Indicator | Default threshold |
|---|---|---|---|
| 1 | Demand | Up on the day | ≥ 10% |
| 2 | Demand | Relative volume (time-adjusted) | ≥ 5x |
| 3 | Demand | News catalyst | a real headline within 24 h (gainer roundups don't count) |
| 4 | Demand | Price | $2-$20 |
| 5 | Supply | Float | < 20M shares |

**How the toolkit measures them**
- Yahoo's screener gives today's gainers (OTC excluded) and quote volume against the 3-month average. During the
  session that average is scaled by the share of a normal day's volume done by now.
- Float and short interest come from Yahoo key statistics. Float figures can lag share issuance by weeks.
- Headlines come from Yahoo Finance search:
  - "List" articles (top gainers, stocks to watch) are excluded.
  - Commentary sites (Zacks, Simply Wall St., MarketBeat...) are flagged: find the original release.
  - **Dilution red flags** in the last 30 days (offering, registered direct, warrants, ATM, shelf, reverse split,
    going concern, delisting notice) are shown on the row.

**Why the criteria make sense:** a small float plus a news-driven demand shock means few shares must absorb heavy
buying, so price can move far and fast. **Evidence: [Lore].** There is no published test of this screen. What
is known cuts the other way for holders:
- Stocks with extreme one-day gains underperform afterwards (the MAX effect, Bali, Cakici & Whitelaw 2011) [Strong].
- Attention-grabbing stocks are net bought by retail and then do worse (Barber & Odean 2008) [Strong].

So any edge is in the first minutes to hours, in execution, and in avoiding the traps.

**The traps, and the checks**
- **Dilution:**
  - Companies sell stock into spikes: at-the-market programs, registered directs, warrant exercises.
  - Check the dilution flag, recent 8-K/424B filings and whether an S-3 shelf is effective.
  - A stock with a reverse split and a going-concern note is a supply machine, whatever its float says.
- **Halts:** LULD pauses jump stops. Size as if the stop may fill 5-10% worse.
- **Spreads:** a 5-cent spread on a $3 stock costs 1.7% round trip. Use limit orders; check `daykit plan`'s
  cost-per-R line.
- **Short-sale restriction:** after a 10% drop, shorts can only sell above the bid. It affects exits for shorts.
- **Late-day fades:** first-day runners often give back gains after the morning. `levels` says "Late day: manage,
  don't start breakouts" after 15:30.

**How to trade it, if at all**
- Watch list only until the opening range forms. Then act only on a `levels` setup: break of the range with VWAP
  agreeing, or the first pullback that holds VWAP.
- Bracket every trade with risk at most 0.25%; at most 2 attempts per name per day.
- Prove it in the paper portfolio over 100+ trades before real money.

## 8. Risk rules for day trading

Conventions, not evidence, except where tagged:
- **Risk per trade:** 0.25-0.5% of equity to the stop (0.25% for small caps and unproven setups). Size =
  risk ÷ stop distance (`daykit plan`, `paperkit order --risk-pct`).
- **Daily loss limit:** 1-2% of equity, or 3-4 full losses, whichever comes first. Then stop: losses cluster
  after losses (tilt; `trader-psychology-process.md` §4, §10).
- **Max trades per day:** fixed in the plan (e.g. 4). The journal's "trade number of the day" table usually shows
  why: later trades are worse.
- **Costs per R:** if round-trip costs exceed ~15% of the risk, the stop is too tight for the instrument.
  Widen the stop and shrink the size, or skip it.
- **No averaging down; no moving the stop away.** Moving a stop toward profit is allowed.
- **Buying power:** under intraday margin, leverage follows maintenance margin (≈4x on large caps at most; less
  for volatile names). Never let one trade's notional exceed what a 10% adverse gap could absorb.
- **Flat by the close** unless a swing plan says otherwise. Overnight gaps jump stops: `paperkit` fills a gapped
  stop at the open, as real markets do.
- **Total open risk ("heat")** at most ~2% of equity intraday, 6% for swing books (`paperkit` defaults: 1% per trade,
  6% heat).

## 9. Bracket orders

A bracket is one entry order with two exits attached, a stop-loss and a take-profit, that cancel each other (OCO)
when either fills.
- **Entry types:** market (fills now, pays the spread); limit (buy at or below a price: pullbacks); stop (buy at or
  above a price: breakouts; fills worse in fast markets).
- **Stop-loss type:**
  - A stop-market order fills through gaps and halts, at a worse price.
  - A stop-limit can fail to fill at all.
  - Day traders use stop-market and size for slippage.
- **Placement:** the stop goes where the setup is wrong (the other side of the range, below VWAP or the last swing),
  just beyond round numbers, never at a round dollar amount of loss.
- **Take-profit:** a fixed R (2R is a common bracket default), a level (prior day high, VWAP band), or none with
  a trailing stop. Fixed targets cap the right tail that breakout systems live on: test it (§6).
- **Server-side vs platform-side:** confirm the broker holds the OCO on its servers, so it survives a disconnect.
- **Time exit:** a day bracket should be cancelled and flattened at a set time (15:55).
- **Options:** brackets usually trigger on the underlying's price. For a long put the stop is *above* the stock
  price; the premium is the maximum loss. `scanner.py scan --puts` gives put and bear-put-spread versions of
  bearish setups, sized so the premium is the risk budget.

## 10. From paper to live

1. **Paper first**, with the same brackets, sizes and limits as the live plan (`paperkit.py`; fills from real
   1-minute bars, stop wins ties, gaps fill at the open).
2. **Gate to go live:**
   - At least 100 trades on one setup (`expectancy` says how many the observed edge needs: often 150-350+).
   - Net expectancy above 0 after costs.
   - Max drawdown inside the plan.
   - No daily-limit breaches in the last 20 sessions.
3. **Paper is kinder than reality:** no queue position, no partial fills, no halts, no emotions. Haircut paper
   expectancy by a third before deciding.
4. **Go live at minimum size** (1 share, 1 micro contract) for 50 trades; compare live vs paper slippage
   per trade.
5. **Scale** in steps only after each step's sample holds up; scale down after a 1.5x-expected drawdown.

## 11. Journal review

`daykit.py journal FILE` reads any CSV with entry time, symbol, side, entry, exit and qty (plus stop, risk or r,
setup, exit time and fees when present). It reports:
- expectancy in R or currency, with the sample needed to prove it;
- green-day share, best and worst day, and daily-limit breaches (`--daily-loss`);
- the longest losing streak;
- tables by entry hour, setup, weekday, trade number of the day, after a win vs after a loss, and holding time;
- the biggest leaks (setups with at least 5 trades and negative expectancy).

Use `trader-psychology-process.md` §14 to turn a pattern into an intervention. Act only on groups with dozens of
trades and a reason.

## 12. Toolkit hooks

| Task | Command |
|---|---|
| Intraday bars (with pre/after-hours) | `fetch.py prices SYM --interval 1m|5m|15m|30m|1h --days N [--prepost]` |
| Day map, plain-English read, bracket ticket | `daykit.py levels FILE --equity E [--risk 0.5] [--date D]` |
| Intraday rule tests | `daykit.py backtest FILE --rule orb|vwap|imom|noise|gap [--grid]` |
| Time-of-day profile | `daykit.py timeofday FILE` |
| Plan, costs per R, daily limit, ticket | `daykit.py plan --equity E --entry X --stop Y [--target Z]` |
| Journal review | `daykit.py journal FILE [--daily-loss N]` |
| Stocks in play | `daykit.py inplay --universe megacap --symbols ...` |
| Small-cap five-criteria selection | `scanner.py smallcap [--min-change 10 --min-rvol 5 --price 2 20 --max-float 20e6]` |
| Puts for bearish setups | `scanner.py scan --universe ... --fetch --puts` |
| Option chain | `fetch.py options SYM --dte 30 --type put` |
| Paper portfolio with brackets | `paperkit.py init / order / update / status / close / cancel / trades --csv` |

Data notes:
- Yahoo minute bars are delayed (~15 min for some feeds) and unofficial.
- During the live session Yahoo sometimes stores a running day total as a bar's volume. `fetch` repairs these
  against the quote's volume (and says so) before relative volume or VWAP is computed.
- Off-hours bad prints are ignored for levels.
- Not for live order routing.

## 13. Sources

- FINRA RN 26-10 and SEC Release 34-105226 (PDT replaced by intraday margin) — https://www.finra.org/rules-guidance/notices/26-10
- SEC Order 34-105656 (tick size and access fee postponed to Nov 2027) — https://www.sec.gov/files/rules/exorders/2026/34-105656.pdf
- SEC fee rate advisory 2026-2; FINRA SR-FINRA-2026-021 (TAF holiday) and SR-FINRA-2026-020
- SEC T+1 (press release 2024-62); FINRA "Frequent Intraday Trading" (Jun 2026)
- SEBI: intraday cash study (Jul 2024), F&O studies (Sep 2024, Jul 2025, Aug 2026) — https://www.sebi.gov.in
- Gao, Han, Li & Zhou 2018, JFE; Baltussen, Da, Lammers & Martens 2021, JFE; Heston, Korajczyk & Sadka 2010, JF
- Holmberg, Lönnbark & Lundström 2013, FRL; Zarattini & Aziz 2023; Zarattini, Barbon & Aziz 2024; Zarattini, Aziz & Barbon 2024 (Concretum, vendor)
- Krueger 2026, ORB replication with costs — https://www.mql5.com/en/blogs/post/776235 ; QuantConnect VWAP and stocks-in-play reproductions
- Bali, Cakici & Whitelaw 2011, "Maxing out", JFE; Barber & Odean 2008, "All that glitters", RFS
- Beckmeyer, Branger & Gayda 2023 (retail 0DTE losses, SSRN 4404704); Fu, Li, Musto & Pearson 2025 (SEC DERA)
- Chague, De-Losso & Giovannetti 2019; Barber, Lee, Liu & Odean 2014 / 2020
