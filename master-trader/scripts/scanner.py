#!/usr/bin/env python3
"""scanner -- the orchestrator: find opportunities across a universe and decide which strategies to run.

Companion to tradekit / techkit / flowkit / eventkit / fetch (same folder). Standard library only.

Commands
  regime     trend / volatility / breadth read of the market (benchmark + universe) and which strategy
             families it favours.
  scan       score every instrument in a universe against a menu of setups (trend, cross-sectional
             momentum, 52-week-high, breakout, volatility squeeze, RSI(2) pullback in an uptrend, trend
             short), filter for liquidity, adjust for regime, cluster correlated names, and print a ranked
             opportunity list with entry / stop / R-target / size and an evidence grade per setup.
  select     walk-forward strategy tournament: for each rule family (sma, cross, donchian, tsmom, rsi2,
             bbrev) pick parameters on a rolling training window and trade the next window out of sample;
             compare "pick the best" vs "ensemble all parameters", deflate for the number of families
             tried, and allocate inverse-vol weights to the families that survive. Several files ->
             family-level verdicts across instruments (more robust than per-instrument winners).

  smallcap   your small-cap momentum day-trading selection: today's US-listed gainers (Yahoo's screener) scored
             on five criteria -- up >= 10% on the day, relative volume >= 5x, a news catalyst, price $2-$20,
             float < 20M shares -- with dilution red flags and, for the leaders, the intraday levels and a sized
             bracket ticket from daykit.

scan --puts adds put expressions for the bearish candidates (a long put and a bear put spread from the listed
chain, sized so the premium is the risk budget).

Universes (--universe): etf-core, sectors, megacap, futures, crypto, fx -- or --symbols / --symbols-file,
or pass CSV FILES directly. --fetch pulls daily bars via fetch.py (Yahoo, unofficial) into --data-dir.

Everything here is a SCREEN, not a verdict: every setup and every universe you scan is another trial.
Confirm candidates with techkit ruletest / indicators, size with tradekit size, and read the references.
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tradekit import _expected_max_sr, _psr, out, pct, read_ohlc  # noqa: E402
from techkit import DEFAULT_GRIDS, atr, rolling_std, rsi, run_rule, signals, sma, stats  # noqa: E402

UNIVERSES = {
    "etf-core": "SPY QQQ IWM DIA EFA EEM FXI EWJ TLT IEF SHY HYG LQD TIP GLD SLV USO UNG DBA DBC UUP FXE FXY".split(),
    "sectors": "XLK XLF XLE XLV XLI XLY XLP XLU XLB XLRE XLC SMH ITA KRE XBI".split(),
    "megacap": ("AAPL MSFT NVDA AMZN GOOGL META TSLA AVGO BRK-B JPM LLY V UNH XOM MA COST HD PG JNJ NFLX "
                "ORCL AMD CRM WMT BAC").split(),
    "futures": "ES=F NQ=F RTY=F CL=F BZ=F NG=F GC=F SI=F HG=F ZN=F ZB=F ZC=F ZS=F ZW=F 6E=F 6J=F 6B=F".split(),
    "crypto": "BTC-USD ETH-USD SOL-USD BNB-USD XRP-USD ADA-USD DOGE-USD AVAX-USD LINK-USD".split(),
    "fx": "EURUSD=X USDJPY=X GBPUSD=X AUDUSD=X USDCAD=X USDCHF=X NZDUSD=X USDMXN=X".split(),
}

# evidence grade -> weight in the composite score (see references: momentum-trading, strategy-playbook,
# technical-analysis). Grades are about the setup family, not about this particular chart.
SETUPS = {
    "trend_long": ("Moderate", 1.0, "price > SMA200 with positive 12-1 momentum (time-series momentum)"),
    "xs_momentum": ("Moderate", 1.0, "top-decile vol-adjusted 12-1 momentum vs the universe"),
    "near_52w_high": ("Moderate", 0.8, "within 5% of the 52-week high in a stage-2 trend"),
    "breakout_55": ("Moderate", 0.8, "close above the prior 55-bar high (Donchian), volume-confirmed if available"),
    "squeeze": ("Weak", 0.4, "Bollinger bandwidth in its lowest decile (6m) inside an uptrend"),
    "rsi2_pullback": ("Weak", 0.5, "RSI(2) < 10 while above SMA200 (short-term pullback in an uptrend; decayed)"),
    "trend_short": ("Moderate", 0.8, "price < SMA200, negative 12-1 momentum, close below the prior 55-bar low"),
    "breakdown_55": ("Moderate", 0.7, "close below the prior 55-bar low (Donchian), volume-confirmed if available"),
    "xs_momentum_short": ("Moderate", 0.7, "bottom-decile vol-adjusted 12-1 momentum vs the universe (losers keep losing; "
                                           "the short leg crashes in sharp rebounds)"),
    "rsi2_rally_short": ("Weak", 0.4, "RSI(2) > 90 while below SMA200 (short-term rally in a downtrend; decayed)"),
}
LONG_FAMILIES = {"trend_long", "xs_momentum", "near_52w_high", "breakout_55", "squeeze", "rsi2_pullback"}


# --------------------------------------------------------------------------- data
def resolve_universe(a):
    syms = []
    if a.universe:
        for u in a.universe:
            if u not in UNIVERSES:
                sys.exit(f"unknown universe '{u}'; choose from {', '.join(UNIVERSES)}")
            syms += UNIVERSES[u]
    if a.symbols:
        syms += a.symbols
    if a.symbols_file:
        with open(a.symbols_file, encoding="utf-8-sig") as fh:
            syms += [s.strip().split(",")[0] for s in fh if s.strip() and not s.startswith("#")]
    return list(dict.fromkeys(syms))


def load_universe(a):
    """Return {name: dict(o,h,l,c,v,dates)} from FILES or fetched symbols."""
    data = {}
    files = list(a.files or [])
    syms = resolve_universe(a)
    if syms:
        os.makedirs(a.data_dir, exist_ok=True)
        if a.fetch:
            import fetch  # noqa: PLC0415
        for s in syms:
            path = os.path.join(a.data_dir, s.replace("^", "").replace("=", "_").replace("/", "_") + ".csv")
            if a.fetch:
                try:
                    rows = fetch.yahoo_history(s, a.years)
                    if rows and len(rows[-1]) > 7:
                        rows.pop()  # drop today's still-trading bar
                    with open(path, "w", newline="") as fh:
                        w = csv.writer(fh)
                        w.writerow(["date", "open", "high", "low", "close", "volume"])
                        for r in rows:
                            f = r[6] / r[4] if r[4] else 1.0  # split/dividend-adjust OHLC
                            w.writerow([r[0], r[1] * f, r[2] * f, r[3] * f, r[6], int(r[5])])
                except Exception as e:  # noqa: BLE001
                    print(f"  skip {s}: {e}", file=sys.stderr)
                    continue
            if os.path.exists(path):
                files.append(path)
            else:
                print(f"  skip {s}: no data at {path} (use --fetch)", file=sys.stderr)
    for f in files:
        try:
            d = read_ohlc(f)
        except SystemExit as e:
            print(f"  skip {f}: {e}", file=sys.stderr)
            continue
        d["v"] = _volume(f, len(d["close"]))
        d["ppy"] = _bars_per_year(f)
        name = os.path.splitext(os.path.basename(f))[0]
        d["mult"] = FUT_MULT.get(name.replace("_F", "=F").upper(), 1.0)
        data[name] = d
    if not data:
        sys.exit("no instruments loaded -- pass CSV files, or --universe/--symbols with --fetch")
    return data


FUT_MULT = {"ES=F": 50, "NQ=F": 20, "RTY=F": 50, "YM=F": 5, "CL=F": 1000, "BZ=F": 1000, "NG=F": 10000,
            "GC=F": 100, "SI=F": 5000, "HG=F": 25000, "ZN=F": 1000, "ZB=F": 1000, "ZF=F": 1000, "ZC=F": 50,
            "ZS=F": 50, "ZW=F": 50, "6E=F": 125000, "6J=F": 12500000, "6B=F": 62500, "6A=F": 100000}


def _bars_per_year(path):
    """Estimate bars per year from the last ~2 years of dates (252 for stocks, ~365 for crypto)."""
    import datetime as _dt  # noqa: PLC0415
    with open(path, newline="", encoding="utf-8-sig") as fh:
        r = csv.DictReader(fh)
        key = next((k for k in r.fieldnames or [] if k.strip().lower() in ("date", "time", "timestamp")), None)
        if not key:
            return 252
        ds = [row[key][:10] for row in r if row.get(key)]
    try:
        tail = ds[-504:]
        days = (_dt.date.fromisoformat(tail[-1]) - _dt.date.fromisoformat(tail[0])).days
        return max(200, min(370, round(len(tail) / days * 365))) if days > 60 else 252
    except ValueError:
        return 252


def _volume(path, n):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        r = csv.DictReader(fh)
        key = next((k for k in r.fieldnames or [] if k.strip().lower() in ("volume", "vol")), None)
        if not key:
            return None
        vals = []
        for row in r:
            try:
                vals.append(float(row[key] or 0))
            except ValueError:
                vals.append(0.0)
    return vals if len(vals) == n and any(vals) else None


# --------------------------------------------------------------------------- features
def features(d):
    h, l, c, v = d["high"], d["low"], d["close"], d.get("v")
    n = len(c)
    Y = int(d.get("ppy", 252))  # bars per year: 252 equities/futures, ~365 crypto
    M = max(1, round(Y / 12))
    if n < max(260, Y + M + 2):
        return None
    s50, s200 = sma(c, 50), sma(c, 200)
    a14 = atr(h, l, c, 14)
    r2 = rsi(c, 2)
    mid, sd = sma(c, 20), rolling_std(c, 20)
    bw = [(4 * s / m) if s is not None and m else None for s, m in zip(sd, mid)]
    bwh = [x for x in bw[-126:] if x is not None]
    lr = [math.log(c[i] / c[i - 1]) for i in range(n - Y, n) if c[i - 1] > 0]
    vol = statistics.stdev(lr) * math.sqrt(Y)
    m121 = c[-1 - M] / c[-1 - Y] - 1
    f = {
        "px": c[-1], "atr": a14[-1], "s50": s50[-1], "s200": s200[-1], "s200_prev": s200[-22],
        "rsi2": r2[-1], "vol": vol, "m121": m121, "m121_va": m121 / vol if vol else 0.0,
        "hi52": max(h[-Y:]), "lo52": min(l[-Y:]),
        "don55h": max(h[-56:-1]), "don55l": min(l[-56:-1]),
        "bw_rank": (sum(1 for x in bwh if x <= bwh[-1]) / len(bwh)) if bwh else None,
        "rets60": [c[i] / c[i - 1] - 1 for i in range(n - 60, n)],
    }
    f["dollar_adv"] = (sum(c[i] * v[i] for i in range(n - 50, n)) / 50) if v else None
    f["rel_vol"] = (v[-1] / (sum(v[-51:-1]) / 50)) if v and sum(v[-51:-1]) > 0 else None
    tt = [f["px"] > f["s200"], f["s50"] > f["s200"], f["s200"] > f["s200_prev"], f["px"] > f["s50"],
          f["px"] >= 1.3 * f["lo52"], f["px"] >= 0.75 * f["hi52"]]
    f["template"] = sum(tt)
    return f


def regime_read(data, bench):
    feats = {k: features(v) for k, v in data.items()}
    feats = {k: v for k, v in feats.items() if v}
    breadth = sum(1 for f in feats.values() if f["px"] > f["s200"]) / max(1, len(feats))
    b = feats.get(bench) if bench else None
    note = ""
    if b is None and feats:
        bench = max(feats, key=lambda k: (feats[k]["dollar_adv"] or 0))
        b = feats[bench]
        note = "" if b["dollar_adv"] else " (no volume data -- benchmark chosen arbitrarily; pass --bench)"
    trend = "up" if b["px"] > b["s200"] and b["s200"] > b["s200_prev"] else \
        "down" if b["px"] < b["s200"] and b["s200"] < b["s200_prev"] else "mixed"
    c = data[bench]["close"]
    Y = int(data[bench].get("ppy", 252))
    lr = [math.log(c[i] / c[i - 1]) for i in range(1, len(c))]
    rv20 = statistics.stdev(lr[-20:]) * math.sqrt(Y)
    rv_hist = sorted(statistics.stdev(lr[i - 20:i]) * math.sqrt(Y) for i in range(max(20, len(lr) - 3 * Y), len(lr), 5))
    vol_pct = sum(1 for x in rv_hist if x <= rv20) / len(rv_hist)
    volr = "high" if vol_pct >= 0.8 else "low" if vol_pct <= 0.3 else "normal"
    if trend == "up" and breadth >= 0.6:
        favour = "trend/momentum longs, breakouts, pullback-buying; trend shorts only on laggards"
        tilt = {"long": 1.25, "short": 0.5}
    elif trend == "down" and breadth <= 0.4:
        favour = "trend shorts, defensive/low-vol, cash; long momentum and breakouts fail more often (momentum-crash risk on rebounds)"
        tilt = {"long": 0.5, "short": 1.25}
    else:
        favour = "mixed: smaller size, prefer mean-reversion at extremes and strong relative-strength leaders"
        tilt = {"long": 0.75, "short": 0.75}
    if volr == "high":
        favour += "; high vol -> cut size (vol targeting), widen stops, expect more false breakouts"
        tilt = {k: v * 0.75 for k, v in tilt.items()}
    tilt = {k: max(0.5, min(1.5, v)) for k, v in tilt.items()}  # bounded risk dial, never an on/off switch
    return {"bench": bench + note, "trend": trend, "breadth": breadth, "rv20": rv20, "vol_pct": vol_pct,
            "vol_regime": volr, "favour": favour, "tilt": tilt, "feats": feats}


# --------------------------------------------------------------------------- scan
def cmd_regime(a):
    data = load_universe(a)
    r = regime_read(data, a.bench)
    out([
        ("Benchmark", f"{r['bench']}: trend {r['trend']} (price vs rising/falling SMA200)"),
        ("Breadth", f"{r['breadth']:.0%} of {len(r['feats'])} instruments above SMA200"),
        ("Volatility", f"{r['bench']} 20d realized {pct(r['rv20'], 1)} = {r['vol_pct']:.0%} percentile of 3y -> {r['vol_regime']}"),
        ("Favours", r["favour"]),
        ("Next", "confirm with fetch.py macro (rates/credit/VIX) and references/macro-regimes.md section 2"),
    ], "Market regime (price-based)")


def scan(data, a):
    """Regime read + ranked candidates (one per symbol) + correlation clusters."""
    reg = regime_read(data, a.bench)
    feats = reg["feats"]
    skipped = []
    if a.min_price or a.min_adv:
        for k in list(feats):
            f = feats[k]
            priced = not (k.upper().endswith(("-USD", "_X", "=X")))  # min price is an equity concept
            if (priced and f["px"] < a.min_price) or (f["dollar_adv"] is not None and f["dollar_adv"] < a.min_adv):
                skipped.append(k)
                feats.pop(k)
    if not feats:
        sys.exit("nothing left after filters")
    va = sorted(f["m121_va"] for f in feats.values())
    def xs_pct(x):
        return sum(1 for y in va if y <= x) / len(va)
    cands = []
    for k, f in feats.items():
        px, at = f["px"], f["atr"] or px * 0.02
        hits = []
        up = f["px"] > f["s200"] and f["m121"] > 0
        if up:
            hits.append(("trend_long", min(1.0, abs(f["m121_va"]) / 1.5), px, px - 3 * at))
        if xs_pct(f["m121_va"]) >= 0.9 and f["m121"] > 0 and len(feats) >= 10:
            hits.append(("xs_momentum", xs_pct(f["m121_va"]), px, px - 3 * at))
        if f["px"] >= 0.95 * f["hi52"] and f["template"] >= 5:
            hits.append(("near_52w_high", f["template"] / 6, max(px, f["hi52"]), max(px, f["hi52"]) - 2.5 * at))
        if px > f["don55h"] and (f["rel_vol"] is None or f["rel_vol"] >= 1.2):
            hits.append(("breakout_55", min(1.0, (px - f["don55h"]) / at), px, f["don55h"] - 1.0 * at))
        if up and f["bw_rank"] is not None and f["bw_rank"] <= 0.1:
            hits.append(("squeeze", 1 - f["bw_rank"], px + 0.5 * at, px - 2 * at))
        if up and f["rsi2"] is not None and f["rsi2"] < 10:
            hits.append(("rsi2_pullback", (10 - f["rsi2"]) / 10, px, px - 2.5 * at))
        down = f["px"] < f["s200"] and f["m121"] < 0
        if down and px < f["don55l"]:
            hits.append(("trend_short", min(1.0, abs(f["m121_va"]) / 1.5), px, f["don55l"] + 1.0 * at))
        if px < f["don55l"] and (f["rel_vol"] is None or f["rel_vol"] >= 1.2):
            hits.append(("breakdown_55", min(1.0, (f["don55l"] - px) / at), px, f["don55l"] + 1.0 * at))
        if xs_pct(f["m121_va"]) <= 0.1 and f["m121"] < 0 and len(feats) >= 10:
            hits.append(("xs_momentum_short", 1 - xs_pct(f["m121_va"]), px, px + 3 * at))
        if down and f["rsi2"] is not None and f["rsi2"] > 90:
            hits.append(("rsi2_rally_short", (f["rsi2"] - 90) / 10, px, px + 2.5 * at))
        for setup, strength, entry, stop in hits:
            grade, w, _ = SETUPS[setup]
            side = "long" if setup in LONG_FAMILIES else "short"
            score = w * (0.5 + 0.5 * strength) * reg["tilt"][side]
            mult = data[k].get("mult", 1.0)
            risk_ps = abs(entry - stop)
            risk_budget = a.equity * a.risk / 100 * reg["tilt"][side]  # regime dial scales risk, not just rank
            shares = math.floor(risk_budget / (risk_ps * mult)) if risk_ps > 0 else 0
            cap = max(0, math.floor(a.equity * a.max_weight / (entry * mult))) if entry > 0 else shares
            capped = shares > cap
            shares = min(shares, cap)
            cands.append({"sym": k, "setup": setup, "side": side, "grade": grade, "score": score,
                          "entry": entry, "stop": stop, "target": entry + (2 if side == "long" else -2) * risk_ps,
                          "units": shares, "capped": capped, "micro": shares == 0 and mult > 1, "atr_pct": at / px, "adv": f["dollar_adv"], "rets": f["rets60"]})
    # one row per symbol: keep its best-scoring setup, list the others
    best = {}
    for cnd in sorted(cands, key=lambda x: -x["score"]):
        if cnd["sym"] not in best:
            best[cnd["sym"]] = dict(cnd, also=[])
        else:
            best[cnd["sym"]]["also"].append(cnd["setup"])
    ranked = sorted(best.values(), key=lambda x: -(x["score"] + 0.1 * len(x["also"])))[:a.top]
    # correlation clusters among the shortlist
    clusters, cid = {}, 0
    for i, x in enumerate(ranked):
        if x["sym"] in clusters:
            continue
        cid += 1
        clusters[x["sym"]] = cid
        for y in ranked[i + 1:]:
            if y["sym"] not in clusters and _corr(x["rets"], y["rets"]) > a.cluster_corr:
                clusters[y["sym"]] = cid
    shorts = sorted((x for x in best.values() if x["side"] == "short"), key=lambda x: -x["score"])
    return {"reg": reg, "ranked": ranked, "clusters": clusters, "skipped": skipped, "feats": feats, "shorts": shorts}


def put_plan(sym, entry, stop, target, risk_budget, dte=35):
    """Bearish expressions from the listed chain: a long put near the entry and a bear put spread from the entry to
    the target, sized so the premium paid is the risk budget. Prices at the ask/bid (what a market order pays)."""
    import datetime as _dt  # noqa: PLC0415
    import fetch  # noqa: PLC0415
    ch = fetch.option_chain(sym, (_dt.date.today() + _dt.timedelta(days=dte)).isoformat())
    puts = sorted((x for x in ch["puts"] if x["bid"] > 0 and x["ask"] > 0), key=lambda x: x["strike"])
    if not puts:
        return {"error": f"no two-sided put quotes for {ch['expiry']}"}
    days = (_dt.date.fromisoformat(ch["expiry"]) - _dt.date.today()).days
    k1 = min(puts, key=lambda x: abs(x["strike"] - entry))
    below = [x for x in puts if x["strike"] < k1["strike"]]
    k2 = min(below, key=lambda x: abs(x["strike"] - target)) if below else None

    def spr(x):
        return (x["ask"] - x["bid"]) / ((x["ask"] + x["bid"]) / 2)
    res = {"expiry": ch["expiry"], "days": days, "spot": ch["spot"], "k1": k1["strike"], "iv": k1["iv"],
           "oi": k1["oi"], "spread_pct": spr(k1)}
    cost = k1["ask"]
    res["long_put"] = {"strike": k1["strike"], "premium": cost, "contracts": math.floor(risk_budget / (cost * 100)),
                       "breakeven": k1["strike"] - cost, "at_target": max(0.0, k1["strike"] - target) - cost,
                       "max_loss": cost}
    if k2:
        debit = k1["ask"] - k2["bid"]
        width = k1["strike"] - k2["strike"]
        if 0 < debit < width:
            res["spread"] = {"long": k1["strike"], "short": k2["strike"], "debit": debit,
                             "mid_debit": k1["mid"] - k2["mid"], "max_gain": width - debit, "rr": (width - debit) / debit,
                             "contracts": math.floor(risk_budget / (debit * 100)), "breakeven": k1["strike"] - debit,
                             "short_oi": k2["oi"], "short_spread_pct": spr(k2)}
    warn = []
    if k1["oi"] < 100 or spr(k1) > 0.10:
        warn.append(f"costly to trade (open interest {k1['oi']:,}, bid-ask {spr(k1):.0%} of the price)")
    if res["long_put"]["contracts"] == 0:
        warn.append(f"one long put costs {cost * 100:,.0f}, more than the {risk_budget:,.0f} risk budget"
                    + ("; the spread fits" if res.get("spread", {}).get("contracts") else "; raise the risk or skip"))
    res["warn"] = warn
    return res


def cmd_scan(a):
    r = scan(load_universe(a), a)
    reg, ranked, clusters, skipped, feats = r["reg"], r["ranked"], r["clusters"], r["skipped"], r["feats"]
    print(f"\n== Regime: {reg['bench']} trend {reg['trend']}, breadth {reg['breadth']:.0%} > SMA200, "
          f"vol {reg['vol_regime']} ({pct(reg['rv20'], 0)}) ==\n  favours: {reg['favour']}")
    print(f"\n== Opportunities: {len(ranked)} of {len(feats)} instruments "
          f"({len(skipped)} removed by liquidity filters; {len(SETUPS)} setups screened) ==")
    print(f"  {'#':>2} {'symbol':<10}{'setup':<15}{'side':<6}{'grade':<9}{'score':>6}{'entry':>11}{'stop':>11}"
          f"{'2R tgt':>11}{'units':>7}{'ATR%':>6}{'$ADV':>8}{'clu':>4}  also")
    for i, x in enumerate(ranked, 1):
        adv = f"{x['adv'] / 1e6:,.0f}m" if x["adv"] else "n/a"
        print(f"  {i:>2} {x['sym']:<10}{x['setup']:<15}{x['side']:<6}{x['grade']:<9}{x['score']:>6.2f}"
              f"{x['entry']:>11.4g}{x['stop']:>11.4g}{x['target']:>11.4g}{str(x['units']) + ('*' if x['capped'] else '') + ('(m)' if x.get('micro') else ''):>7}{x['atr_pct']:>6.1%}"
              f"{adv:>8}{clusters[x['sym']]:>4}  {', '.join(x['also'])}")
    n_clusters = len(set(clusters.values()))
    print(f"\n  units = {a.risk}% of {a.equity:,.0f} x regime dial {reg['tilt']['long']:.2f} long / {reg['tilt']['short']:.2f} short, risked to the stop per idea (* = capped at {a.max_weight:.0%} of equity; futures in contracts; 0(m) = one contract is too big, use the micro or skip). {n_clusters} independent clusters "
          f"(60-day return correlation > {a.cluster_corr}) -- size each cluster as ONE bet.")
    print("  Setup definitions and evidence: " + "; ".join(f"{k} [{v[0]}]" for k, v in SETUPS.items()))
    print("  This is a screen: confirm each candidate (techkit indicators/ruletest, catalysts, liquidity), then plan it.")
    if a.puts:
        shorts = r["shorts"][:a.put_top]  # the best bearish setups, ranked or not: puts are asked for explicitly
        if shorts and not any(x["side"] == "short" for x in ranked):
            print(f"\n  (None made the top {a.top}: the regime dial ranks shorts lower. Listing the best {len(shorts)} anyway.)")
        print(f"\n== Put positions for the {len(shorts)} bearish candidates (listed chain ~{a.put_dte} days out; "
              f"premium = the risk budget: {a.equity * a.risk / 100 * reg['tilt']['short']:,.0f} = {a.risk:g}% x short dial "
              f"{reg['tilt']['short']:.2f}) ==")
        if not shorts:
            print("  No bearish candidates in this scan (the regime may not favour shorts).")
        for x in shorts:
            budget = a.equity * a.risk / 100 * reg["tilt"]["short"]
            try:
                pp = put_plan(x["sym"], x["entry"], x["stop"], x["target"], budget, a.put_dte)
            except Exception as e:  # noqa: BLE001 -- futures, FX and crypto have no Yahoo chain
                pp = {"error": str(e)}
            x["puts"] = pp
            if "error" in pp:
                print(f"  {x['sym']:<9} no puts: {pp['error']}")
                continue
            lp = pp["long_put"]
            print(f"  {x['sym']:<9} spot {pp['spot']:,.2f}, expiry {pp['expiry']} ({pp['days']}d), IV {(pp['iv'] or 0):.0%}")
            print(f"    Buy put {lp['strike']:g} at {lp['premium']:.2f}: {lp['contracts']} contracts, breakeven {lp['breakeven']:,.2f}, "
                  f"at the {x['target']:,.2f} target (at expiry) {lp['at_target']:+.2f}/share; max loss = premium")
            sp = pp.get("spread")
            if sp:
                print(f"    Bear put spread {sp['long']:g}/{sp['short']:g} at {sp['debit']:.2f} (mid {sp['mid_debit']:.2f}): "
                      f"{sp['contracts']} contracts, max gain {sp['max_gain']:.2f} = {sp['rr']:.1f}x the debit, breakeven {sp['breakeven']:,.2f}")
            print(f"    Exit if {x['sym']} closes above {x['stop']:,.2f} (the setup's stop) -- the put's premium is the most you lose, "
                  "the stop tells you when the idea is wrong." + (" Caution: " + "; ".join(pp["warn"]) if pp["warn"] else ""))
        print("  Prices at the ask (and the short leg at the bid) from Yahoo's delayed chain; check your broker's live quotes."
              "\n  Long puts lose to time decay and falling volatility: options-volatility.md section 8 has the structure matrix.")
    if a.out:
        with open(a.out, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["rank", "symbol", "setup", "side", "grade", "score", "entry", "stop", "target", "units",
                        "atr_pct", "dollar_adv", "cluster", "also"])
            for i, x in enumerate(ranked, 1):
                w.writerow([i, x["sym"], x["setup"], x["side"], x["grade"], round(x["score"], 3), x["entry"], x["stop"],
                            x["target"], x["units"], round(x["atr_pct"], 4), x["adv"], clusters[x["sym"]], "|".join(x["also"])])
        print(f"  wrote {a.out}")


VOLUME_CURVE = [(0, 0.0), (15, 0.09), (30, 0.15), (60, 0.234), (120, 0.372), (180, 0.483), (240, 0.58),
                (300, 0.685), (360, 0.817), (390, 1.0)]  # cumulative share of a US session's volume (SPY hourly, 2024-26)


def volume_fraction(now=None):
    """Share of a normal day's volume done by now (US Eastern). 1.0 outside the session (compare whole days)."""
    import datetime as _dt  # noqa: PLC0415
    try:
        from zoneinfo import ZoneInfo  # noqa: PLC0415
        t = now or _dt.datetime.now(ZoneInfo("America/New_York"))
    except Exception:  # noqa: BLE001
        t = now or _dt.datetime.now(_dt.timezone(_dt.timedelta(hours=-5)))
    m = t.hour * 60 + t.minute - 570
    if t.weekday() >= 5 or m <= 0 or m >= 390:
        return 1.0
    for (m0, f0), (m1, f1) in zip(VOLUME_CURVE, VOLUME_CURVE[1:]):
        if m <= m1:
            return max(0.05, f0 + (f1 - f0) * (m - m0) / (m1 - m0))
    return 1.0


def smallcap_screen(a):
    """Today's gainers scored on the five criteria; returns dict(rows, meta)."""
    import fetch  # noqa: PLC0415
    lo, hi = a.price
    base = fetch.yahoo_screen(min_change=min(a.min_change, a.min_change * 0.5) if a.near else a.min_change,
                              price_lo=lo * (0.8 if a.near else 1), price_hi=hi * (1.2 if a.near else 1))
    state = base[0]["state"] if base else None
    frac = volume_fraction() if state == "REGULAR" else 1.0
    rows = []
    for q in base:
        avg = q["avg_vol_3m"] or q["avg_vol_10d"]
        rvol = q["volume"] / (avg * frac) if avg else None
        rows.append(dict(q, rvol=rvol))
    rows.sort(key=lambda r: -(r["rvol"] or 0))
    for r in rows[:a.deep]:  # float and news only for the most active names (two requests each)
        try:
            r.update(fetch.key_stats(r["symbol"]))
        except Exception as e:  # noqa: BLE001
            r["float_err"] = str(e)
        try:
            items = fetch.news(r["symbol"])
        except Exception as e:  # noqa: BLE001
            items, r["news_err"] = [], str(e)
        fresh = [n for n in items if n["age_h"] is not None and n["age_h"] <= a.news_hours]
        r["catalyst"] = next((n for n in fresh if not n["list"]), None)
        r["list_only"] = bool(fresh) and r["catalyst"] is None
        r["dilution"] = [n["title"] for n in items if n["dilution"] and n["age_h"] is not None and n["age_h"] <= 24 * 30]
        r["headlines"] = items[:4]
    for r in rows:
        fl = r.get("float") or None
        p = {"up": r["change_pct"] >= a.min_change / 100, "rvol": (r["rvol"] or 0) >= a.min_rvol,
             "news": r.get("catalyst") is not None, "price": lo <= (r["price"] or 0) <= hi,
             "float": fl is not None and fl < a.max_float}
        r["pillars"], r["met"] = p, sum(p.values())
        r["checked"] = "catalyst" in r
    rows.sort(key=lambda r: (-r["met"], -(r["rvol"] or 0)))
    return {"rows": rows, "state": state, "volume_fraction": frac, "n": len(base)}


def cmd_smallcap(a):
    import datetime as _dt  # noqa: PLC0415
    res = smallcap_screen(a)
    rows, state = res["rows"], res["state"]
    full = [r for r in rows if r["met"] == 5]
    four = [r for r in rows if r["met"] == 4]
    print(f"\n== Small-cap momentum selection: {res['n']} US-listed gainers checked (market {state or 'n/a'}) ==")
    names = ", ".join(r["symbol"] for r in full[:6])
    if full:
        bl = f"{len(full)} stock{'s' if len(full) > 1 else ''} meet all five criteria today: {names}."
    elif four:
        bl = f"No stock meets all five criteria today; {len(four)} meet four: {', '.join(r['symbol'] for r in four[:6])}."
    else:
        bl = "No stock meets four or more of the five criteria today."
    print(f"\n  Bottom line: {bl}")
    print("  Next best action: " + ("Watch, then trade only the levels' setup -- these are the market's most dangerous "
                                    "trades (thin floats, halts, dilution). Risk 0.25% or less per trade."
                                    if full or four else "Stand aside: nothing in play on your criteria."))
    if state == "PRE":
        print("  Before the open, Yahoo's screener still shows yesterday's session: re-run after 09:30, or run "
              "`daykit.py inplay --symbols ...` on a pre-market watchlist.")
    if res["volume_fraction"] < 1:
        print(f"  Relative volume is time-adjusted: a normal day has done ~{res['volume_fraction']:.0%} of its volume by now.")
    print(f"\n  {'symbol':<7}{'price':>8}{'day':>8}{'RVOL':>8}{'float':>9}  {'up':<3}{'vol':<4}{'news':<5}{'$':<3}{'flt':<4}{'met':>4}  catalyst / flags")
    for r in rows[:a.top]:
        p = r["pillars"]
        fl = r.get("float")
        flt = f"{fl / 1e6:.1f}m" if fl else ("?" if r["checked"] else "-")
        tick = lambda ok: "Y" if ok else "."  # noqa: E731
        news = tick(p["news"]) if r["checked"] else "?"
        flags = []
        if r.get("catalyst"):
            c = r["catalyst"]
            src = f"{c['publisher']}, commentary: find the source news" if c.get("commentary") else c["publisher"]
            flags.append(f"\"{c['title'][:70]}\" ({src}, {c['age_h']:.0f}h)")
        elif r.get("list_only"):
            flags.append("only gainer-list mentions, no real news found")
        elif r["checked"]:
            flags.append(f"no headline in {a.news_hours:g}h")
        if r.get("dilution"):
            flags.append("DILUTION/LISTING RISK: " + r["dilution"][0][:60])
        if not r["checked"]:
            flags.append("float/news not checked (raise --deep)")
        print(f"  {r['symbol']:<7}{r['price']:>8.2f}{r['change_pct']:>+8.0%}{(r['rvol'] or 0):>8.1f}{flt:>9}  "
              f"{tick(p['up']):<3}{tick(p['rvol']):<4}{news:<5}{tick(p['price']):<3}{tick(p['float']) if r['checked'] else '?':<4}"
              f"{r['met']:>4}  {'; '.join(flags)}")
    lead = (full + four)[:a.plans]
    if lead:
        import daykit  # noqa: PLC0415
        for r in lead:
            try:
                raw, _, _ = fetch_bars(r["symbol"])
                lv = daykit.levels(daykit.bars_from_rows(raw), (570, 960), equity=a.equity, risk=a.risk, bp=a.bp,
                                   symbol=r["symbol"])
            except Exception as e:  # noqa: BLE001
                print(f"\n  {r['symbol']}: no intraday plan ({e})")
                continue
            print(f"\n  {r['symbol']} intraday: {lv['bottom_line']}\n    Next: {lv['action']['label']} -- {lv['action']['flat']}")
            if lv.get("vwap") is not None:
                print(f"    VWAP {lv['vwap']:,.2f}, high {lv['hod']:,.2f}, low {lv['lod']:,.2f}, prior close {lv.get('pdc', float('nan')):,.2f}")
    print(f"\n  Criteria (yours): up >= {a.min_change:g}% on the day; relative volume >= {a.min_rvol:g}x; news in the last "
          f"{a.news_hours:g}h (gainer roundups don't count); price ${a.price[0]:g}-${a.price[1]:g}; float < {a.max_float / 1e6:g}M shares.")
    print("  Evidence: [Lore] -- a practitioner screen with no published test. What is known: stocks with extreme one-day"
          "\n  gains and heavy retail attention tend to do worse afterwards (Bali-Cakici-Whitelaw 2011; Barber-Odean 2008),"
          "\n  so any edge is in the first minutes and in execution, not in holding. Expect wide spreads, trading halts"
          "\n  (limit up-limit down pauses) that jump stops, and share offerings into the spike. Yahoo data is ~15 min delayed;"
          "\n  float figures can be stale. Prove it in the paper portfolio before risking money.")
    print(f"  Checked {_dt.datetime.now().strftime('%Y-%m-%d %H:%M')} local time.")


def fetch_bars(sym):
    import fetch  # noqa: PLC0415
    return fetch.yahoo_bars(sym, "5m", days=20, prepost=True)


def _corr(x, y):
    n = min(len(x), len(y))
    x, y = x[-n:], y[-n:]
    mx, my = statistics.mean(x), statistics.mean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy) if sxx and syy else 0.0


# --------------------------------------------------------------------------- select (walk-forward tournament)
def tournament(d, rules, a):
    c, h, l = d["close"], d["high"], d["low"]
    n = len(c)
    tr, te, warm = int(a.train * a.ppy), int(a.test * a.ppy), 260
    if n < warm + tr + te:
        return None
    res = {}
    for rule in rules:
        grid = DEFAULT_GRIDS[rule]
        poss = [signals(rule, c, h, l, p, a.short) for p in grid]
        wf_best, wf_ens, picks = [], [], []
        s = warm
        while s + tr + te <= n:
            train_sr = []
            for pos in poss:
                r, *_ = run_rule(c, pos, a.cost_bps, None, 1.0, s, s + tr, a.delay, a.ppy)
                st = stats(r, a.ppy)
                train_sr.append(st["sharpe"] if st else -9)
            k = max(range(len(grid)), key=lambda i: train_sr[i])
            picks.append(tuple(grid[k]))
            tests = [run_rule(c, pos, a.cost_bps, None, 1.0, s + tr, s + tr + te, a.delay, a.ppy)[0] for pos in poss]
            wf_best += tests[k]
            wf_ens += [sum(t[j] for t in tests) / len(tests) for j in range(len(tests[0]))]
            s += te
        full = [stats(run_rule(c, pos, a.cost_bps, None, 1.0, warm, n, a.delay, a.ppy)[0], a.ppy) for pos in poss]
        mode = max(set(picks), key=picks.count)
        res[rule] = {"best": stats(wf_best, a.ppy), "ens": stats(wf_ens, a.ppy), "ens_r": wf_ens,
                     "is_best": max(f["sharpe"] for f in full if f), "stability": picks.count(mode) / len(picks),
                     "mode": mode, "windows": len(picks)}
    bh = [c[i] / c[i - 1] - 1 for i in range(warm + tr + 1, n)]
    return res, stats(bh, a.ppy)


def cmd_select(a):
    data = load_universe(a)
    rules = a.rules or list(DEFAULT_GRIDS)
    agg = {r: [] for r in rules}
    for name, d in data.items():
        t = tournament(d, rules, a)
        if not t:
            print(f"  skip {name}: needs {260 + int((a.train + a.test) * a.ppy)}+ bars", file=sys.stderr)
            continue
        res, bh = t
        for r in rules:  # per-instrument significance, deflated for the families compared on THIS instrument
            x = res[r]
            e = x["ens"]
            sr_p = e["sharpe"] / math.sqrt(a.ppy)
            var_p = statistics.variance([res[q]["ens"]["sharpe"] for q in rules]) / a.ppy if len(rules) > 1 else 1e-4
            x["psr"] = _psr(sr_p, 0.0, e["n"], e["skew"], e["kurt"])
            x["dsr"] = _psr(sr_p, _expected_max_sr(len(rules), max(var_p, 1e-6)), e["n"], e["skew"], e["kurt"])
            x["bh"] = bh
        print(f"\n== {name}: walk-forward ({a.train:g}y train -> {a.test:g}y test, rolling; {a.cost_bps} bps; "
              f"fill at {'next' if a.delay == 1 else 'signal'} close; {'long/short' if a.short else 'long/flat'}) ==")
        print(f"  {'rule':<10}{'IS best SR':>11}{'WF pick SR':>11}{'WF ens SR':>10}{'ens CAGR':>10}{'ens maxDD':>10}"
              f"{'stability':>10}  usual pick")
        for r in rules:
            x = res[r]
            agg[r].append(x)
            print(f"  {r:<10}{x['is_best']:>11.2f}{x['best']['sharpe']:>11.2f}{x['ens']['sharpe']:>10.2f}"
                  f"{x['ens']['cagr']:>+10.1%}{x['ens']['mdd']:>10.1%}{x['stability']:>10.0%}  {x['mode']}")
        print(f"  {'buy&hold':<10}{'':>11}{'':>11}{bh['sharpe']:>10.2f}{bh['cagr']:>+10.1%}{bh['mdd']:>10.1%}")
        gap = statistics.mean(res[r]["is_best"] - res[r]["best"]["sharpe"] for r in rules)
        print(f"  optimism gap (in-sample best minus walk-forward pick): {gap:+.2f} Sharpe on average")
    # family-level decision: judged per instrument (no pooling of different markets into one long series),
    # against buy & hold, and deflated for the number of families compared
    k = max(len(v) for v in agg.values())
    print(f"\n== Strategy selection across {k} instrument(s): walk-forward ensembles vs buy & hold ==")
    print(f"  {'rule':<10}{'med SR':>8}{'med SR-B&H':>11}{'% beat B&H':>11}{'med DD cut':>11}{'med PSR':>9}{'med DSR':>9}  verdict")
    elig, overlay = {}, {}
    for r in rules:
        xs = agg[r]
        if not xs:
            continue
        med = statistics.median(x["ens"]["sharpe"] for x in xs)
        exc = [x["ens"]["sharpe"] - x["bh"]["sharpe"] for x in xs]
        beat = sum(1 for e in exc if e > 0) / len(xs)
        ddcut = statistics.median(1 - x["ens"]["mdd"] / x["bh"]["mdd"] if x["bh"]["mdd"] else 0 for x in xs)
        mpsr = statistics.median(x["psr"] for x in xs)
        mdsr = statistics.median(x["dsr"] for x in xs)
        vol = statistics.median(x["ens"]["vol"] for x in xs)
        if med > 0 and statistics.median(exc) > 0 and beat >= 0.6 and mpsr >= 0.9 and mdsr >= 0.6:
            verdict = "ELIGIBLE: timing edge vs B&H"
            elig[r] = vol
        elif med > 0 and mpsr >= 0.8 and ddcut >= 0.3 and statistics.median(exc) > -0.15:
            verdict = "RISK OVERLAY: similar SR, much smaller drawdowns"
            overlay[r] = vol
        else:
            verdict = "drop"
        print(f"  {r:<10}{med:>8.2f}{statistics.median(exc):>+11.2f}{beat:>11.0%}{ddcut:>11.0%}{mpsr:>9.0%}{mdsr:>9.0%}  {verdict}")
    chosen = elig or overlay
    if chosen:
        inv = {r: 1 / v for r, v in chosen.items() if v > 0}
        tot = sum(inv.values())
        print(f"\n  Allocation (inverse-vol across {'eligible' if elig else 'overlay'} families, each run as an ensemble of its parameters):")
        for r, w in sorted(inv.items(), key=lambda x: -x[1]):
            print(f"    {r:<10}{w / tot:>6.0%}")
        print("  Re-run quarterly; demote a family whose live Sharpe falls >1 SE below its walk-forward Sharpe")
        print("  (references/strategy-orchestration.md). Per-instrument results above say WHERE each family works.")
    else:
        print("\n  No family beats buy & hold or meaningfully cuts drawdown out of sample after costs here --")
        print("  the honest answer is buy & hold, cash, or a different market/strategy menu.")
    print(f"  Thresholds: timing edge needs median SR > B&H in >=60% of instruments, median PSR >= 90%, median DSR >= 60%;")
    print(f"  DSR deflates for the {len(rules)} families compared on each instrument, not for screens run before this one.")


# --------------------------------------------------------------------------- CLI
def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)

    def common(x):
        x.add_argument("files", nargs="*", help="OHLCV CSV files (name = file stem)")
        x.add_argument("--universe", nargs="*", help=f"built-in lists: {', '.join(UNIVERSES)}")
        x.add_argument("--symbols", nargs="*", help="tickers (Yahoo symbols)")
        x.add_argument("--symbols-file", help="text/CSV file, one ticker per line")
        x.add_argument("--fetch", action="store_true", help="download daily bars for the symbols first")
        x.add_argument("--years", type=float, default=6, help="history to fetch")
        x.add_argument("--data-dir", default="scan_data", help="where fetched CSVs are cached")
        x.add_argument("--bench", help="benchmark name for the regime read (default: most liquid instrument)")

    x = s.add_parser("regime", help="trend / vol / breadth regime read")
    common(x)
    x.set_defaults(fn=cmd_regime)
    x = s.add_parser("scan", help="ranked opportunity list")
    common(x)
    x.add_argument("--equity", type=float, default=100000)
    x.add_argument("--risk", type=float, default=0.5, help="%% of equity risked per idea, for the units column")
    x.add_argument("--max-weight", type=float, default=0.25, help="max notional per idea, fraction of equity")
    x.add_argument("--min-price", type=float, default=5.0)
    x.add_argument("--min-adv", type=float, default=20e6, help="min average daily $ volume (skipped if no volume)")
    x.add_argument("--top", type=int, default=20)
    x.add_argument("--cluster-corr", type=float, default=0.7)
    x.add_argument("--out", help="write the ranked list to CSV")
    x.add_argument("--puts", action="store_true", help="add put positions (long put, bear put spread) for bearish candidates")
    x.add_argument("--put-dte", type=int, default=35, help="days to the put expiry (first listed on or after)")
    x.add_argument("--put-top", type=int, default=5, help="how many bearish candidates get put positions")
    x.set_defaults(fn=cmd_scan)
    x = s.add_parser("smallcap", help="small-cap momentum selection on five criteria (today's gainers)")
    x.add_argument("--min-change", type=float, default=10.0, help="%% up on the day")
    x.add_argument("--min-rvol", type=float, default=5.0, help="relative volume (time-adjusted in the session)")
    x.add_argument("--price", type=float, nargs=2, default=[2.0, 20.0], metavar=("LO", "HI"))
    x.add_argument("--max-float", type=float, default=20e6, help="float shares")
    x.add_argument("--news-hours", type=float, default=24.0, help="a catalyst must be this recent")
    x.add_argument("--near", action="store_true", help="also list near misses outside the change/price bands")
    x.add_argument("--deep", type=int, default=25, help="check float and news for this many of the most active names")
    x.add_argument("--top", type=int, default=20)
    x.add_argument("--plans", type=int, default=3, help="intraday levels + ticket for this many leaders")
    x.add_argument("--equity", type=float, default=100000)
    x.add_argument("--risk", type=float, default=0.25, help="%% of equity per trade (small caps: keep it small)")
    x.add_argument("--bp", type=float, default=4.0)
    x.set_defaults(fn=cmd_smallcap)
    x = s.add_parser("select", help="walk-forward strategy tournament")
    common(x)
    x.add_argument("--rules", nargs="*", choices=sorted(DEFAULT_GRIDS))
    x.add_argument("--train", type=float, default=3.0, help="training window, years")
    x.add_argument("--test", type=float, default=1.0, help="out-of-sample window, years")
    x.add_argument("--cost-bps", type=float, default=5.0)
    x.add_argument("--delay", type=int, default=1)
    x.add_argument("--ppy", type=int, default=252)
    x.add_argument("--short", action="store_true")
    x.set_defaults(fn=cmd_select, years=20)
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
