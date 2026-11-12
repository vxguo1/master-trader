# Trader UI — build plan and status

Local web app over the `master-trader` toolkit (`F:\dev\skills\master-trader\scripts`). Run:

```
python F:\dev\skills\trader-ui\server.py      ->  http://127.0.0.1:8765
```

Binds to 127.0.0.1 only. Data is cached in `trader-ui/cache/`.

## Status (2026-11-12)

- **server.py — done and tested.** All 12 endpoints were exercised against live data (Yahoo, FRED,
  SEC EDGAR, Coinbase, GPR index). The run whitelist rejects injected values.
- **index.html — done and tested (2026-11-12).** All 9 tabs were exercised in the browser pane on live
  data, in dark and light themes, at 1366px and 375px widths, with error states (bad symbol, ticker
  outside the CIK map). `.claude/launch.json` has the `trader-ui` entry.
- Fixes made during testing:
  - server: `/api/run` flag regex now allows uppercase (`tradekit move/bs/iv` use `--S`/`--K`)
  - server: a Yahoo 404 becomes a readable "check the symbol" message, and ValueError returns a 400
  - UI: forms use `noValidate`, because native step checks silently blocked submits
  - UI: plot divs pin their height so responsive resizes don't squash them
- **Added 2026-11-12 (user requests):**
  - **Live prices.** Charts defaults to hourly bars (`/api/prices?interval=1h&range=5d|1mo|3mo|6mo|1y|2y`,
    exchange-local time, category x-axis, in-progress bar kept). `/api/quote` returns the live
    price, change, session state, quote age and any extended-hours print (cached 15 s). Live mode
    refreshes the quote every 30 s and the bars every 2 min, and patches the forming candle. The
    Stock tab header shows the live price too.
  - **Plain-English summary with a next best action.** `/api/summary` uses 3 years of daily bars
    plus the live price. It returns a stance, a bottom line, and an action (label, "if you own it",
    "if you don't", cautions), with up to 6 short "why" points. The rules come from
    `next_action()` in server.py and are rule-based, not personal advice. It shows on Charts and
    Stock.
  - The user chose Yahoo for prices (FRED has no intraday data and no stocks); FRED stays the
    macro source.
  - **Options tab symbol picker.** Symbol + Load price fills the spot (live quote) and Vol % (last
    month's realized vol; free data has no implied vol, so the user can type the option's IV). It
    also fills the expected-move form and rebuilds the current preset's strikes around the new spot
    (strike step scales with price, down to 0.001 for FX). Enter in the form loads a new symbol or
    recomputes, instead of reloading the page.
  - **The app depends on the skill, never the reverse.** The user wants the skill to be pure
    analysis. The quote, hourly-bar and summary logic lives in the skill's toolkit (`fetch.quote`,
    `fetch.yahoo_bars`, `techkit.summarize`/`next_action`). `server.py` only wraps those with
    caching, and the skill never mentions this app.
- **Added 2026-11-12 (session 3, user requests): day trading, puts, bracket orders, paper portfolio,
  small-cap selection, plain-English macro.** All browser-tested on live data:
  - **Day Trading tab** (`/api/day`, `/api/inplay`, `/api/day/backtest`): 1/5/15-minute candles with
    pre/after-hours in gray, VWAP with 1σ/2σ bands, prior-day/overnight/opening-range lines, the
    `daykit.levels` bottom line and next best action (in a trade / flat), a bracket ticket with "Paper trade
    this"; a stocks-in-play screen (threaded, ~1.3 s for 25 names); an intraday rule backtest (ORB, VWAP,
    first→last half-hour, noise band) with an equity curve. Live refresh every 60 s.
  - **Scanner tab:** "Put positions for bearish ideas" (long put + bear put spread from Yahoo's chain, sized to
    the risk budget), a Paper button on every idea, and the **daily selection: small-cap momentum (your 5
    criteria)** panel (`/api/smallcap`): pillar ticks, catalyst headline links, commentary and dilution
    flags, intraday plans for the leaders.
  - **Paper tab** (`/api/paper`, POST `/api/paper/init|order|update|close|cancel`): account cards, equity
    curve, bracket order form (stock long/short or bought put/call; market/limit/stop entry; stop-loss,
    take-profit or target R; qty or risk %; flatten time; TIF), positions with Close, working orders with
    Cancel, closed trades, activity log. Auto-update every 60 s while there are positions or orders. The book
    is `trader-ui/data/paper_book.json` (engine: the skill's `paperkit.py`).
  - **Dashboard:** the Macro flags panel opens with `fetch.macro_plain` (stance, bottom line, next best
    action, one plain line per gauge incl. oil, what to watch); the mechanical flags are folded away.
  - Server: POST bodies must be `application/json` (blocks cross-site form posts to the paper book).
  - Data fixes found in testing: Yahoo stores a running day total as some live-session bar volumes (repaired
    in `fetch.yahoo_bars`); off-hours bad prints are dropped from the day chart.
- Deliberate deviation from the spec below: no dual-axis charts. Revenue and YoY are stacked
  subplots sharing x, and the order-flow candles, delta and CVD are separate rows.
- Charts: Plotly 2.35.2 from `https://cdn.jsdelivr.net/npm/plotly.js-dist-min@2.35.2/plotly.min.js`.
  cdnjs does not host this version (404). Sparklines are inline SVG, not Plotly.

## API (all JSON; NaN/inf -> null)

GET
- `/api/prices?symbol=SPY&interval=1d|1h&years=2|range=1mo` -> symbol, interval, range, tz, partial,
  date, open, high, low, close, volume, sma20, sma50, sma200, bb_up, bb_lo, rsi14, atr14, text
  (`techkit indicators` on completed bars, ppy from bar spacing)
- `/api/quote?symbol=SPY` -> name, exchange, currency, price, prev_close, change, change_pct, time, tz,
  age_s, state (open|pre-market|after hours|closed), ext{price, change_pct, time}?, day/52w range, volume
- `/api/summary?symbol=SPY` -> stance, bottom_line, action{label, if_you_own, if_you_dont, caution},
  points[], note
- `/api/macro` -> sections[{name, rows[{id, label, last, date, chg1m, chg3m, chg1y, spark_d, spark_v} | {error}]}],
  flags[] (cached 30 min)
- `/api/regime?universe=etf-core,sectors` -> bench, trend, breadth, rv20, vol_pct, vol_regime, favour, tilt, n
- `/api/scan?universe=etf-core,sectors[&symbols=A,B]&equity&risk&top` -> regime, ranked[{sym, setup,
  side, grade, score, entry, stop, target, units, capped, micro, atr_pct, adv, also, cluster}], skipped, n
- `/api/select?symbols=SPY,QQQ,GLD,TLT[&short=1]` -> text (walk-forward tournament; slow, 20y fetch,
  cached 6 h)
- `/api/stock?ticker=NVDA&wacc=0.10&tg=0.03&sbc=1` -> entity, cik, rows (last 16 quarters: revenue,
  rev_yoy, rev_qoq, gm, op_margin, net_income, eps_diluted, fcf, fcf_margin, inv_days, dso, *_ttm ...),
  net_cash, price, price_date, realized_vol_1y, reactions[[release, timing, reaction_date, move, gap,
  next5d]], reaction_stats{n, mean_abs, median_abs, sd}, dcf{price, shares, fcf, net_cash, wacc, tg,
  implied_growth, mcap, fcf_yield, grid{wacc:{growth:value_per_share}}}
- `/api/events?types=war_onset,trade_tariff` -> text (eventkit study, aligned to SPX), rows[{date,
  label, type, regime_change, channel, SPX/GOLD/VIX/WTI/UST10: {pre, d1, d5, d21, d63, max_dd,
  days_to_trough, recover, vol_pre, vol_post | max_rise, max_fall}}], types[]
- `/api/geo` -> USEPUINDXD, OVXCLS, VIXCLS, GVZCLS, DCOILBRENTEU {d, v}; GPR {d, v, ma7}
- `/api/flow?symbol=BTC&exchange=coinbase&minutes=10&bar=30s` -> t, o, h, l, c, buy, sell, delta,
  cvd, profile{price, vol, poc, va_lo, va_hi, vwap}, text, meta

POST
- `/api/projection` {spot, days, iv, base_iv?, event_move?, iv_down?, iv_up?, scenarios[{name, prob,
  price}], levels[]} -> bins, market{hist, pct[5,10,25,50,75,90,95], mean, p_above}, mine{...}?, levels
- `/api/payoff` {spot, days, vol, r?, legs[{type: call|put|stock, strike, qty, premium?}]} -> grid,
  expiry, today, legs (with BS premium and greeks), greeks totals, net_premium
- `/api/run` {kit, cmd, args{flag: value}} with a whitelist: tradekit size, kelly, expectancy, ruin,
  drawdown, sharpe, bs, iv, move, impact; equitykit dcf; eventkit scenarios (also takes
  `tree: [{scenario, prob, ASSET...}]`) -> text

## Frontend spec (index.html, one file, dark trading-terminal theme, CSS variables)

Tabs load lazily on first open. Each panel has a spinner and an error box.

1. **Dashboard**:
   - Regime cards from `/api/regime` (trend, breadth, vol regime, favours).
   - Macro flags.
   - Macro tables per section, with an SVG sparkline and colored 1m/3m/1y changes.
   - SPY candles with SMA50/200.
2. **Charts**:
   - Symbol and years inputs.
   - Candlestick with SMA20/50/200 and Bollinger bands.
   - Volume subplot and RSI14 subplot.
   - Indicator text in a `<pre>`.
3. **Stock deep dive**:
   - Ticker input.
   - Header: entity, price/date, 1y realized vol.
   - Charts:
     - revenue bars with a YoY line on a secondary axis
     - margin lines (GM, OpM, FCF%)
     - net income and FCF bars
     - inventory days and DSO
   - Quarterly table.
   - Earnings-reaction bar chart plus stats, with an implied-move input. Client-side ratio =
     mean|move| / implied; benchmark exceedance about 42% (normal) or 37% (fat-tailed).
   - Reverse-DCF panel: editable WACC, terminal growth and SBC toggle; shows implied growth and
     the value grid.
   - Projection panel:
     - inputs: spot, days, IV (prefilled from realized vol), event move, skew vols
     - a scenario editor (bull/base/bear rows) and levels
     - output: overlaid histograms (market vs mine), a percentile table, and P(above level) with
       the gap column
4. **Scanner**:
   - Universe checkboxes (etf-core, sectors, megacap, futures, crypto, fx), custom symbols,
     equity and risk inputs.
   - Regime summary.
   - Ranked table with grade badges and cluster colors. Clicking a symbol opens it in Charts.
5. **Strategy Lab**: symbols input and a long/short toggle. Shows the `/api/select` text, with a
   warning that a run takes up to a minute.
6. **Options**:
   - Spot, days, vol and r inputs, plus a legs table (add/remove rows).
   - Presets: long call, bull call spread, put spread, iron condor, collar, straddle.
   - Payoff chart (expiry and today), greeks, net premium.
   - Expected-move calculator via `/api/run tradekit move`.
7. **Risk**: forms for size, kelly, expectancy, ruin, drawdown and sharpe, each sent to
   `/api/run`, with output in a `<pre>`.
8. **Geopolitics**:
   - GPR (7-day MA), EPU, and OVX vs VIX charts.
   - Event-type multi-select feeding `/api/events`: an SPX 21-day bar chart colored by
     regime_change, plus a table and the text output.
   - Scenario-tree editor sent to `/api/run eventkit scenarios`.
9. **Order flow**:
   - Symbol (BTC/ETH/SOL), exchange, minutes and bar inputs.
   - Candles with delta bars and a CVD line.
   - Volume profile (horizontal bars) with POC, value-area and VWAP lines.
   - Event text.

Footer: data sources and freshness. Yahoo is unofficial and may be delayed. This is analysis, not
personalized advice.

## After index.html

- Test every tab in the built-in browser pane at http://127.0.0.1:8765. Add a `.claude/launch.json`
  entry `trader-ui` (`python trader-ui/server.py`, port 8765).
- Check light/dark contrast and the empty and error states.
