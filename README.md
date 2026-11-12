# master-trader

A master-level trading skill for Claude, and a local web app built on top of it.

- **`master-trader/`** is the skill: operating principles and 11 workflows in `SKILL.md`, an
  evidence-graded reference library (`references/`, current to Nov 2026), and deterministic calculators
  (`scripts/`, Python standard library only). It covers single-stock deep dives, market regimes and macro,
  opportunity scanning and strategy selection, momentum, technical analysis, price action, order flow,
  options, geopolitical shocks, risk and sizing, backtest validation, trading psychology, and day trading
  with a paper portfolio.
- **`trader-ui/`** is the app: a single-page dashboard served by a small Python server on localhost. It
  imports the skill's toolkit; the skill never depends on the app.

This is analysis software, not investment advice. Free data sources are unofficial and often delayed, so
don't route live orders from it.

## Quick start

Requires Python 3.10 or newer. Nothing to install.

```bash
python trader-ui/server.py
```

Then open http://127.0.0.1:8765. The server binds to localhost only and caches data in `trader-ui/cache/`.

Tabs:
- Dashboard: market regime, plain-English macro read, FRED macro tables.
- Charts: daily or hourly, with a live quote and a rule-based next best action.
- Day Trading: intraday levels, VWAP, a bracket ticket, stocks in play, and intraday rule backtests.
- Stock: fundamentals, earnings reactions, reverse DCF and a price projection.
- Scanner: ranked setups with put positions for bearish ideas, plus the small-cap daily selection.
- Paper: a paper portfolio with bracket orders, filled from real minute bars.
- Strategy Lab, Options, Risk, Geopolitics, Order Flow.

## Using the skill

Copy `master-trader/` into your Claude skills folder (for Claude Code, `~/.claude/skills/master-trader/`), or
build a `.skill` package by zipping the folder without `evals/` and `__pycache__/`.

The toolkit also runs on its own:

```bash
python master-trader/scripts/fetch.py prices SPY --interval 5m --days 30 --prepost --out spy_5m.csv
```

```bash
python master-trader/scripts/daykit.py levels spy_5m.csv --symbol SPY --equity 50000
```

```bash
python master-trader/scripts/scanner.py smallcap
```

Every script prints its commands with `-h`.

| Script | What it does |
|---|---|
| `fetch.py` | Yahoo quotes, daily/hourly/minute bars, option chains, screener; FRED macro dashboard with a plain-English read; SEC EDGAR fundamentals; GPR index; Kraken/Coinbase trades and books |
| `tradekit.py` | sizing, Kelly, expectancy, ruin and drawdown Monte Carlo, Sharpe significance (PSR/DSR), Black-Scholes, implied vol, expected moves, market impact |
| `techkit.py` | indicators, trend template, momentum ranking, rule backtests, plain-English summary |
| `flowkit.py` | volume profile, VWAP, footprint/delta/CVD, order-flow imbalance, L2 book |
| `equitykit.py` | earnings reactions, reverse/forward DCF, price projection distributions |
| `eventkit.py` | geopolitical event studies, scenario-tree P&L |
| `scanner.py` | regime read, opportunity scan (with puts), walk-forward strategy tournament, small-cap selection |
| `daykit.py` | day-trading levels, intraday backtests, time-of-day profile, day-trade plan, journal review, stocks in play |
| `paperkit.py` | paper portfolio with bracket orders (JSON book, replayable) |

## Keys and data

- **FRED** (macro) needs a free API key. Set `FRED_API_KEY`, or put a file named `*fred*.txt` in the folder
  `TRADER_KEYS_DIR` points to. Without it, the macro panels are empty and everything else works.
- **Yahoo Finance, SEC EDGAR, Kraken, Coinbase** and the GPR index need no key. Yahoo is unofficial and can
  change or lag without notice.
- No paid service is used.

## Evals

`master-trader/evals/` holds the skill's test cases (prompt, input files, graders). They are kept out of
the packaged skill.
