# master-trader

A master-level trading skill for Claude.

`master-trader/` holds operating principles and 11 workflows in `SKILL.md`, an evidence-graded reference
library (`references/`, current to Nov 2026), and deterministic calculators (`scripts/`, Python standard
library only). It covers:
- single-stock deep dives, market regimes and macro;
- opportunity scanning and strategy selection;
- momentum, technical analysis, price action and order flow;
- options, geopolitical shocks, risk and sizing;
- backtest validation and trading psychology;
- day trading, with a paper portfolio.

A local web dashboard built on this toolkit, Mekiki, lives in its own repo,
[vxguo1/mekiki](https://github.com/vxguo1/mekiki). The app imports the skill; the skill never
depends on the app.

This is analysis software, not investment advice. Free data sources are unofficial and often delayed, so
don't route live orders from it. Requires Python 3.10 or newer; nothing to install.

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

- **FRED** (macro) needs your own free API key; none ships with the skill. See
  [Getting a FRED key](#getting-a-fred-key). Without it, the macro panels are empty and everything else works.
- **Yahoo Finance, SEC EDGAR, Kraken, Coinbase** and the GPR index need no key. Yahoo is unofficial and can
  change or lag without notice.
- No paid service is used.

### Getting a FRED key

The key is free and takes about two minutes.

1. Create an account at [fredaccount.stlouisfed.org](https://fredaccount.stlouisfed.org/login/secure/) and
   sign in.
2. Open [API Keys](https://fredaccount.stlouisfed.org/apikeys) and choose **Request API Key**.
3. Describe your use in a sentence (for example "personal market research"), accept the terms and submit.
   The key is a 32-character string of letters and digits.
4. Give the key to the toolkit in one of two ways:
   - Set the environment variable `FRED_API_KEY`. On Windows run `setx FRED_API_KEY your_key_here` and open
     a new terminal. On macOS or Linux add `export FRED_API_KEY=your_key_here` to your shell profile.
   - Or save the key as the only line of a text file with `fred` in its name, such as
     `~/.keys/fred_apikey.txt`. To use a different folder, point `TRADER_KEYS_DIR` at it.
5. Check that it works:

   ```bash
   python master-trader/scripts/fetch.py macro
   ```

   A dated macro dashboard means the key was found. "No FRED key found" means it was not.

Keep the key out of anything you commit or share. Each person who uses the toolkit needs their own.

## Evals

`master-trader/evals/` holds the skill's test cases (prompt, input files, graders). They are kept out of
the packaged skill.
