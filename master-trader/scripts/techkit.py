#!/usr/bin/env python3
"""techkit -- technical indicators, momentum screens and honest rule backtests.

Companion to tradekit.py (same folder). Standard library only.

Commands
  indicators FILE      latest trend/momentum/volatility/volume readings for an OHLC(V) CSV,
                       plus a trend-template and stage check
  rank FILE...         rank several symbols' CSVs by momentum (12-1, 6-1, 3m, vol-adjusted)
  ruletest FILE        backtest a classic TA/momentum rule with costs, fills at the NEXT bar's close (--delay 1),
                       a parameter-robustness grid, deflated Sharpe, and in/out-of-sample split
  summary FILE         plain-English bottom line + rule-based next best action (if you own it / if you don't)
                       from ~3 years of daily bars; --symbol S --live uses the live quote as the current price

Rules for ruletest: sma | cross | donchian | tsmom | rsi2 | bbrev
CSV needs columns: open, high, low, close (volume optional). Oldest row first.
"""
from __future__ import annotations

import argparse
import datetime as dt
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tradekit import max_drawdown, moments, out, pct, read_ohlc, sharpe_report  # noqa: E402


# --------------------------------------------------------------------------- indicator primitives
def sma(x, n):
    res = [None] * len(x)
    s = 0.0
    for i, v in enumerate(x):
        s += v
        if i >= n:
            s -= x[i - n]
        if i >= n - 1:
            res[i] = s / n
    return res


def ema(x, n):
    res = [None] * len(x)
    if len(x) < n:
        return res
    a = 2 / (n + 1)
    e = sum(x[:n]) / n
    res[n - 1] = e
    for i in range(n, len(x)):
        e = a * x[i] + (1 - a) * e
        res[i] = e
    return res


def wilder(x, n):
    """Wilder smoothing (RMA), seeded with a simple mean."""
    res = [None] * len(x)
    if len(x) < n:
        return res
    e = sum(x[:n]) / n
    res[n - 1] = e
    for i in range(n, len(x)):
        e = (e * (n - 1) + x[i]) / n
        res[i] = e
    return res


def rsi(c, n=14):
    ch = [0.0] + [c[i] - c[i - 1] for i in range(1, len(c))]
    g = wilder([max(v, 0) for v in ch[1:]], n)
    l = wilder([max(-v, 0) for v in ch[1:]], n)
    res = [None]
    for gi, li in zip(g, l):
        if gi is None:
            res.append(None)
        elif li == 0:
            res.append(100.0)
        else:
            res.append(100 - 100 / (1 + gi / li))
    return res


def true_range(h, l, c):
    tr = [h[0] - l[0]]
    for i in range(1, len(c)):
        tr.append(max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1])))
    return tr


def atr(h, l, c, n=14):
    return wilder(true_range(h, l, c), n)


def adx(h, l, c, n=14):
    pdm, mdm = [0.0], [0.0]
    for i in range(1, len(c)):
        up, dn = h[i] - h[i - 1], l[i - 1] - l[i]
        pdm.append(up if up > dn and up > 0 else 0.0)
        mdm.append(dn if dn > up and dn > 0 else 0.0)
    tr = true_range(h, l, c)
    s_tr, s_p, s_m = wilder(tr, n), wilder(pdm, n), wilder(mdm, n)
    pdi, mdi, dx = [], [], []
    for a, b, t in zip(s_p, s_m, s_tr):
        if t in (None, 0) or a is None:
            pdi.append(None); mdi.append(None); dx.append(None)
            continue
        p, m = 100 * a / t, 100 * b / t
        pdi.append(p); mdi.append(m)
        dx.append(100 * abs(p - m) / (p + m) if p + m else 0.0)
    valid = [v for v in dx if v is not None]
    adx_vals = wilder(valid, n)
    pad = len(dx) - len(valid)
    return [None] * pad + adx_vals, pdi, mdi


def rolling_std(x, n):
    res = [None] * len(x)
    for i in range(n - 1, len(x)):
        res[i] = statistics.pstdev(x[i - n + 1:i + 1])
    return res


def last(x):
    for v in reversed(x):
        if v is not None:
            return v
    return None


# --------------------------------------------------------------------------- indicators command
def cmd_indicators(a):
    d = read_ohlc(a.file)
    o, h, l, c = d["open"], d["high"], d["low"], d["close"]
    vol = _read_volume(a.file)
    n = len(c)
    if n < 60:
        sys.exit(f"only {n} bars -- indicators need at least 60 (200+ for the trend template); fetch more history")
    px = c[-1]
    s20, s50, s150, s200 = (last(sma(c, k)) for k in (20, 50, 150, 200))
    e21 = last(ema(c, 21))
    m12, m26 = ema(c, 12), ema(c, 26)
    macd = [x - y if x is not None and y is not None else None for x, y in zip(m12, m26)]
    sig = ema([v for v in macd if v is not None], 9)
    macd_v, sig_v = last(macd), last(sig)
    r14, r2 = last(rsi(c, 14)), last(rsi(c, 2))
    atr14 = last(atr(h, l, c, 14))
    adx14, pdi, mdi = adx(h, l, c, 14)
    bb_mid = sma(c, 20)
    bb_sd = rolling_std(c, 20)
    bw = [(4 * s / m) if s is not None and m else None for s, m in zip(bb_sd, bb_mid)]
    bw_hist = [v for v in bw[-126:] if v is not None]
    bw_rank = sum(1 for v in bw_hist if v <= bw_hist[-1]) / len(bw_hist) if bw_hist else None
    up, lo = bb_mid[-1] + 2 * bb_sd[-1], bb_mid[-1] - 2 * bb_sd[-1]
    pct_b = (px - lo) / (up - lo) if up != lo else None

    def ret(k, skip=0):
        if n > k + skip:
            return c[-1 - skip] / c[-1 - k] - 1
        return None

    hi52 = max(h[-252:])
    lo52 = min(l[-252:])
    don20h, don20l = max(h[-21:-1]), min(l[-21:-1])
    don55h = max(h[-56:-1]) if n > 56 else None
    rv20 = statistics.stdev([math.log(c[i] / c[i - 1]) for i in range(n - 20, n)]) * math.sqrt(a.ppy)

    def f(v, fmt="{:.2f}"):
        return "n/a" if v is None else fmt.format(v)

    rows = [
        ("Bars / last close", f"{n} / {px}"),
        ("SMA 20/50/150/200", f"{f(s20)} / {f(s50)} / {f(s150)} / {f(s200)}"),
        ("Price vs SMA50 / SMA200", f"{f(px / s50 - 1 if s50 else None, '{:+.1%}')} / {f(px / s200 - 1 if s200 else None, '{:+.1%}')}"),
        ("EMA21", f(e21)),
        ("MACD 12/26/9", f"{f(macd_v, '{:.3f}')} signal {f(sig_v, '{:.3f}')} hist {f(macd_v - sig_v if macd_v is not None and sig_v is not None else None, '{:+.3f}')}"),
        ("RSI14 / RSI2", f"{f(r14, '{:.1f}')} / {f(r2, '{:.1f}')}"),
        ("ADX14 (+DI/-DI)", f"{f(last(adx14), '{:.1f}')} ({f(last(pdi), '{:.1f}')}/{f(last(mdi), '{:.1f}')})  >25 trending, <20 range"),
        ("ATR14", f"{f(atr14)} ({f(atr14 / px if atr14 else None, '{:.2%}')} of price)"),
        ("Realized vol 20d", pct(rv20, 1)),
        ("Bollinger 20/2 %B", f(pct_b, '{:.2f}') + f"  bandwidth pct-rank (6m) {f(bw_rank, '{:.0%}')}" + ("  <- squeeze" if bw_rank is not None and bw_rank <= 0.1 else "")),
        ("Donchian 20 hi/lo (prior)", f"{don20h} / {don20l}" + ("  <- 20d breakout" if px > don20h else "  <- 20d breakdown" if px < don20l else "")),
        ("Donchian 55 hi (prior)", f(don55h) + ("  <- 55d breakout" if don55h and px > don55h else "")),
        ("52w high / low", f"{hi52} ({px / hi52 - 1:+.1%}) / {lo52} ({px / lo52 - 1:+.1%})"),
        ("Return 1m / 3m / 6m", f"{f(ret(21), '{:+.1%}')} / {f(ret(63), '{:+.1%}')} / {f(ret(126), '{:+.1%}')}"),
        ("Momentum 12-1", f(ret(252, 21), '{:+.1%}') + "  (skip last month: short-term reversal)"),
    ]
    if vol:
        av50 = sum(vol[-51:-1]) / 50 if len(vol) > 50 else None
        rows.append(("Relative volume (vs 50 bars)", f(vol[-1] / av50 if av50 else None, '{:.2f}x')))
        if av50 and vol[-1] < 0.5 * av50:
            rows.append(("WARNING", "last bar volume < 0.5x average -- possibly an in-progress (partial) bar; "
                                    "levels, ATR and breakout flags may change by the close"))
    out(rows, f"Indicators: {a.file}")

    if n >= 252 and s200 is not None and s150 is not None:
        s200_series = sma(c, 200)
        s200_prev = s200_series[-22]
        checks = [
            ("Price > SMA150 and SMA200", px > s150 and px > s200),
            ("SMA150 > SMA200", s150 > s200),
            ("SMA200 rising (1m)", s200_prev is not None and s200 > s200_prev),
            ("SMA50 > SMA150 > SMA200", s50 > s150 > s200),
            ("Price > SMA50", px > s50),
            (">= 30% above 52w low", px >= 1.3 * lo52),
            ("Within 25% of 52w high", px >= 0.75 * hi52),
        ]
        rows = [(k, "PASS" if v else "fail") for k, v in checks]
        passed = sum(v for _, v in checks)
        rows.append(("Score", f"{passed}/7 (relative-strength vs universe not checked -- use `rank`)"))
        out(rows, "Trend template (Minervini-style stage-2 screen)")
        s150_prev = sma(c, 150)[-22]
        slope = "rising" if s150 > s150_prev else "falling"
        stage = ("2 (advancing)" if px > s150 and slope == "rising" else
                 "4 (declining)" if px < s150 and slope == "falling" else
                 "1 or 3 (base / top) -- check context")
        out([("30-week MA slope", slope), ("Approx. Weinstein stage", stage)], "Stage analysis")


def _read_volume(path):
    import csv
    with open(path, newline="", encoding="utf-8-sig") as fh:
        r = csv.DictReader(fh)
        key = next((k for k in r.fieldnames or [] if k.strip().lower() in ("volume", "vol", "v")), None)
        if not key:
            return None
        res = []
        for row in r:
            try:
                res.append(float(row[key]))
            except (ValueError, TypeError):
                pass
        return res


# --------------------------------------------------------------------------- rank command
def cmd_rank(a):
    rows = []
    for fpath in a.files:
        c = read_ohlc(fpath)["close"]
        n = len(c)
        if n < 253:
            print(f"skip {fpath}: needs 253+ bars", file=sys.stderr)
            continue
        r121 = c[-22] / c[-253] - 1
        r61 = c[-22] / c[-127] - 1
        r3 = c[-1] / c[-64] - 1
        lr = [math.log(c[i] / c[i - 1]) for i in range(n - 252, n)]
        v = statistics.stdev(lr) * math.sqrt(252)
        hi = max(c[-252:])
        rows.append((os.path.basename(fpath), r121, r61, r3, v, r121 / v, c[-1] / hi - 1))
    rows.sort(key=lambda r: r[5 if a.by == "voladj" else 1], reverse=True)
    print(f"\n== Momentum rank (by {'12-1 / vol' if a.by == 'voladj' else '12-1'}) ==")
    print(f"  {'symbol':<22}{'12-1':>9}{'6-1':>9}{'3m':>9}{'vol':>8}{'12-1/vol':>10}{'vs 52wH':>9}")
    for r in rows:
        print(f"  {r[0]:<22}{r[1]:>+9.1%}{r[2]:>+9.1%}{r[3]:>+9.1%}{r[4]:>8.1%}{r[5]:>10.2f}{r[6]:>+9.1%}")
    print("  note: cross-sectional momentum needs a broad universe; a handful of names is a watchlist, not a factor")


# --------------------------------------------------------------------------- rule backtests
def signals(rule, c, h, l, p, allow_short):
    """Return target position for each bar (decided at close of bar t, held over t+1)."""
    n = len(c)
    pos = [0.0] * n
    if rule == "sma":
        m = sma(c, p[0])
        for i in range(n):
            if m[i] is not None:
                pos[i] = 1.0 if c[i] > m[i] else (-1.0 if allow_short else 0.0)
    elif rule == "cross":
        f, s = sma(c, p[0]), sma(c, p[1])
        for i in range(n):
            if s[i] is not None:
                pos[i] = 1.0 if f[i] > s[i] else (-1.0 if allow_short else 0.0)
    elif rule == "tsmom":
        k = p[0]
        for i in range(k, n):
            r = c[i] / c[i - k] - 1
            pos[i] = 1.0 if r > 0 else (-1.0 if allow_short else 0.0)
    elif rule == "donchian":
        ent, ex = p[0], max(2, p[0] // 2)
        cur = 0.0
        for i in range(ent, n):
            hh, ll = max(h[i - ent:i]), min(l[i - ent:i])
            xh, xl = max(h[i - ex:i]), min(l[i - ex:i])
            if cur == 0:
                if c[i] > hh:
                    cur = 1.0
                elif allow_short and c[i] < ll:
                    cur = -1.0
            elif cur > 0 and c[i] < xl:
                cur = 0.0
            elif cur < 0 and c[i] > xh:
                cur = 0.0
            pos[i] = cur
    elif rule == "rsi2":
        thr = p[0]
        r2, m200, m5 = rsi(c, 2), sma(c, 200), sma(c, 5)
        cur = 0.0
        for i in range(n):
            if None in (r2[i], m200[i], m5[i]):
                continue
            if cur == 0 and c[i] > m200[i] and r2[i] < thr:
                cur = 1.0
            elif cur > 0 and c[i] > m5[i]:
                cur = 0.0
            pos[i] = cur
    elif rule == "bbrev":
        k = p[0]
        m, sd = sma(c, k), rolling_std(c, k)
        cur = 0.0
        for i in range(n):
            if m[i] is None:
                continue
            if cur == 0 and c[i] < m[i] - 2 * sd[i]:
                cur = 1.0
            elif cur > 0 and c[i] >= m[i]:
                cur = 0.0
            pos[i] = cur
    return pos


def run_rule(c, pos, cost_bps, vol_target, max_lev, start, end, delay=1, ppy=252):
    """Position decided at close i is first held from close i+delay (delay=1: fill at the next bar's close)."""
    rets = [c[i] / c[i - 1] - 1 for i in range(1, len(c))]
    lr = [math.log(c[i] / c[i - 1]) for i in range(1, len(c))]
    strat, prev, turnover, trades, exposure = [], 0.0, 0.0, 0, 0
    for i in range(start, end - 1):
        w = pos[i - delay] if i - delay >= 0 else 0.0
        if vol_target and i >= 21:
            rv = statistics.stdev(lr[i - 20:i]) * math.sqrt(ppy)
            w = w * min(max_lev, vol_target / rv) if rv > 0 else 0.0
        dw = abs(w - prev)
        if (w != 0) and (prev == 0 or math.copysign(1, w) != math.copysign(1, prev)):
            trades += 1
        turnover += dw
        exposure += w != 0
        strat.append(w * rets[i] - dw * cost_bps / 1e4)  # return of bar i+1 earned by position set at close i
        prev = w
    return strat, turnover, trades, exposure


def stats(r, ppy=252):
    if len(r) < 20:
        return None
    m, sd, sk, ku = moments(r)
    eq = [1.0]
    for x in r:
        eq.append(eq[-1] * (1 + x))
    yrs = len(r) / ppy
    mdd, _ = max_drawdown(eq)
    return {
        "sharpe": m / sd * math.sqrt(ppy) if sd else 0.0,
        "cagr": eq[-1] ** (1 / yrs) - 1 if eq[-1] > 0 else -1.0,
        "vol": sd * math.sqrt(ppy), "mdd": mdd, "skew": sk, "kurt": ku, "n": len(r),
    }


DEFAULT_GRIDS = {
    "sma": [[k] for k in (20, 50, 100, 150, 200, 250)],
    "cross": [[f, s] for f in (10, 20, 50) for s in (100, 150, 200) if f < s],
    "tsmom": [[k] for k in (21, 63, 126, 189, 252)],
    "donchian": [[k] for k in (20, 40, 55, 80, 100)],
    "rsi2": [[t] for t in (5, 10, 15, 20, 25)],
    "bbrev": [[k] for k in (10, 20, 30, 50)],
}


def cmd_ruletest(a):
    d = read_ohlc(a.file)
    c, h, l = d["close"], d["high"], d["low"]
    n = len(c)
    grid = [list(map(int, g.split(","))) for g in a.params] if a.params else DEFAULT_GRIDS[a.rule]
    need = 2 if a.rule == "cross" else 1
    bad = [g for g in grid if len(g) != need or (need == 2 and g[0] >= g[1])]
    if bad:
        sys.exit(f"--params for '{a.rule}' must be " + ("fast,slow pairs with fast < slow, e.g. --params 20,100 50,200"
                                                       if need == 2 else "single integers, e.g. --params 50 100 200"))
    warm = 260
    if n < warm + 300:
        print(f"warning: only {n} bars -- results will be very noisy", file=sys.stderr)
    split = int(n * (1 - a.oos)) if a.oos else n
    res = []
    for p in grid:
        pos = signals(a.rule, c, h, l, p, a.short)
        r_is, to, tr, ex = run_rule(c, pos, a.cost_bps, a.vol_target, a.max_lev, warm, split, a.delay, a.ppy)
        s = stats(r_is, a.ppy)
        if s:
            res.append((p, s, to, tr, ex / max(1, len(r_is)), pos))
    if not res:
        sys.exit("not enough data for any parameter set")
    bh = stats([c[i] / c[i - 1] - 1 for i in range(warm + 1, split)], a.ppy)
    print(f"\n== Rule '{a.rule}' parameter grid ({'in-sample ' + pct(1 - a.oos, 0) if a.oos else 'full sample'}, "
          f"cost {a.cost_bps} bps/turnover, {'fill at next bar close' if a.delay == 1 else f'fill {a.delay} bars after signal' if a.delay else 'fill at SIGNAL close (optimistic)'}{', vol-target ' + pct(a.vol_target, 0) if a.vol_target else ''}) ==")
    print(f"  {'params':<12}{'Sharpe':>8}{'CAGR':>9}{'vol':>8}{'maxDD':>8}{'trades':>8}{'expos.':>8}{'turn/yr':>9}")
    for p, s, to, tr, ex, _ in res:
        yrs = s["n"] / a.ppy
        print(f"  {','.join(map(str, p)):<12}{s['sharpe']:>8.2f}{s['cagr']:>+9.1%}{s['vol']:>8.1%}{s['mdd']:>8.1%}{tr:>8}{ex:>8.0%}{to / yrs:>9.1f}")
    print(f"  {'buy&hold':<12}{bh['sharpe']:>8.2f}{bh['cagr']:>+9.1%}{bh['vol']:>8.1%}{bh['mdd']:>8.1%}")
    srs = [s["sharpe"] for _, s, *_ in res]
    best = max(res, key=lambda r: r[1]["sharpe"])
    med, top = statistics.median(srs), max(srs)
    share_pos = sum(1 for v in srs if v > 0) / len(srs)
    if top <= 0:
        verdict = "no parameter set makes money -- no edge here"
    elif share_pos >= 0.7 and med >= 0.5 * top:
        verdict = "plateau -- neighbouring params also work (good sign)"
    else:
        verdict = "spiky -- only a few params work; the best one is likely fit to noise"
    print(f"\n  Robustness: Sharpe {min(srs):.2f} .. {top:.2f}, median {med:.2f}, "
          f"{share_pos:.0%} of grid positive -> {verdict}")
    var_sr = statistics.variance(srs) if len(srs) > 1 else None
    bs = best[1]
    out(sharpe_report(bs["sharpe"], bs["n"], a.ppy, bs["skew"], bs["kurt"], len(res) * a.extra_trials,
                      max(var_sr or 0.0, 1e-4)), f"Best params {best[0]} -- significance after {len(res) * a.extra_trials} trials")
    if a.oos:
        r_oos, to, tr, ex = run_rule(c, best[5], a.cost_bps, a.vol_target, a.max_lev, split, n, a.delay, a.ppy)
        so = stats(r_oos, a.ppy)
        bho = stats([c[i] / c[i - 1] - 1 for i in range(split + 1, n)], a.ppy)
        if so:
            out([
                ("Out-of-sample bars", so["n"]),
                ("OOS Sharpe (best IS params)", f"{so['sharpe']:.2f}  vs in-sample {bs['sharpe']:.2f}"),
                ("OOS CAGR / maxDD", f"{so['cagr']:+.1%} / {so['mdd']:.1%}"),
                ("OOS buy&hold Sharpe", f"{bho['sharpe']:.2f}" if bho else "n/a"),
                ("Read", "expect OOS < IS; a collapse toward 0 means the edge was mostly fit"),
            ], "Out-of-sample check")
    print("\n  Caveats: single-asset tests are low-power; add more markets, include borrow/funding for shorts,"
          "\n  and treat any 'best' parameter as one draw from the grid, not a discovery.")


# --------------------------------------------------------------------------- plain-English summary
def words_pct(x):
    a = abs(x) * 100
    return f"{a:.0f}%" if a >= 9.5 else f"{a:.1f}%" if a >= 0.095 else f"{a:.2f}%"


def summarize(symbol, dates, high, low, close, quote=None):
    """Plain-English read of daily bars (oldest first, ~3 years; the last bar may be today's forming one), bottom
    line first, plus a rule-based next best action. Descriptive: it says what the price has done. `quote` is a
    fetch.quote() dict; its price replaces the last close when it is from the last bar's date."""
    c, hi, lo = list(close), list(high), list(low)
    n = len(c)
    if n < 60:
        raise ValueError(f"Only {n} daily bars for {symbol}: not enough history for a summary.")
    qt = quote or {}
    if qt.get("price") and qt.get("time") and qt["time"][:10] >= dates[-1][:10]:
        if qt["time"][:10] > dates[-1][:10]:  # the file stops before today's session: add it as a bar
            dates, c, hi, lo = [*dates, qt["time"][:10]], [*c, qt["price"]], [*hi, qt["price"]], [*lo, qt["price"]]
            n += 1
        c[-1] = qt["price"]
        hi[-1], lo[-1] = max(hi[-1], c[-1]), min(lo[-1], c[-1])
    span = max((dt.date.fromisoformat(dates[-1][:10]) - dt.date.fromisoformat(dates[0][:10])).days / 365.25, 1 / 365)
    ppy = max(240, min(370, round(n / span)))  # ~252 trading days for exchanges, ~365 for crypto
    px, cur = c[-1], qt.get("currency")

    def money(v):
        s = f"{v:,.{4 if abs(v) < 2 else 2}f}"  # FX and sub-$2 prices need more decimals
        return f"${s}" if cur in (None, "USD") else f"{s} {cur}"

    def rel(g, what):
        return f"right at its {what}" if abs(g) < 0.005 else f"{words_pct(g)} {'above' if g > 0 else 'below'} its {what}"

    lr = [math.log(c[i] / c[i - 1]) for i in range(1, n)]
    pts = []
    chg = qt["change_pct"] if qt.get("change_pct") is not None else c[-1] / c[-2] - 1
    typical = statistics.median(abs(x) for x in lr[-61:-1]) or 1e-9
    ratio = abs(chg) / typical
    size = "a quiet day" if ratio < 0.5 else "a normal-sized move" if ratio < 1.5 else \
        "a big move" if ratio < 2.5 else "an unusually large move"
    live = qt.get("state") == "open"
    pts.append(f"{symbol} is {'at' if live else 'closed at'} {money(px)}, {'up' if chg >= 0 else 'down'} "
               f"{words_pct(chg)} {'today' if live else 'on the day'}: {size} for it "
               f"(a typical day is about {words_pct(typical)}).")

    lt, s200 = None, None  # long-term: price vs the 200-day average, and which way that average is heading
    if n >= 220:
        s200, s200_prev = statistics.mean(c[-200:]), statistics.mean(c[-220:-20])
        gap, rising = px / s200 - 1, s200 > s200_prev
        where = f"{rel(gap, '200-day average')} ({money(s200)})"
        if gap >= 0 and rising:
            lt = "up"
            pts.append(f"Long-term trend: up. It is {where}, and that average is still rising.")
        elif gap < 0 and not rising:
            lt = "down"
            pts.append(f"Long-term trend: down. It is {where}, and that average is falling.")
        elif gap < 0:
            lt = "weakening"
            pts.append(f"Long-term trend: weakening. It is {where}. The average is still rising from earlier gains "
                       "but will turn down if prices stay here.")
        else:
            lt = "improving"
            pts.append(f"Long-term trend: improving. It is {where}, though that average is still falling from "
                       "earlier losses.")
    else:
        pts.append("Not enough history for a long-term trend read (that needs about 200 trading days).")

    s50 = statistics.mean(c[-50:])  # recent weeks: the 50-day average; within 0.5% counts as sideways
    g50 = px / s50 - 1
    mt = "flat" if abs(g50) < 0.005 else "up" if g50 > 0 else "down"
    pts.append(f"Recent weeks: {dict(up='firm', down='softer', flat='sideways')[mt]}. "
               f"It is {rel(g50, '50-day average')} ({money(s50)}).")

    hi52 = max(hi[-ppy:])
    dd = px / hi52 - 1
    hi_where = "at or near its 52-week high" if dd > -0.01 else \
        f"{words_pct(dd)} below its 52-week high of {money(hi52)}" + (", a deep drop" if dd < -0.2 else "")
    if n > ppy:
        r1y = px / c[-1 - ppy] - 1
        pts.append(f"Over the past year it is {'up' if r1y >= 0 else 'down'} {words_pct(r1y)}, and it sits {hi_where}.")
    else:
        pts.append(f"It sits {hi_where}.")

    r14 = rsi(c, 14)[-1]  # only mention extremes; silence means normal
    if r14 is not None and r14 >= 70:
        pts.append(f"It has climbed fast lately (RSI {r14:.0f}, 'overbought'). Pauses often follow, but strong "
                   "trends can stay overbought for weeks.")
    elif r14 is not None and r14 <= 30:
        pts.append(f"It has fallen fast lately (RSI {r14:.0f}, 'oversold'). Bounces often follow, but that alone "
                   "is not a reliable buy signal.")
    rv = [statistics.stdev(lr[i - 20:i]) * math.sqrt(ppy) for i in range(20, len(lr) + 1)]
    pr = sum(1 for v in rv if v <= rv[-1]) / len(rv)
    if pr >= 0.8:
        pts.append(f"Price swings are bigger than usual right now (higher than {pr:.0%} of the past "
                   f"{span:.0f} years), so expect a bumpier ride.")
    elif pr <= 0.2:
        pts.append("Price swings are unusually small right now. Calm stretches can end abruptly.")

    lvl = money(s200) if s200 else ""
    stance, bl = {
        ("up", "up"): ("uptrend", "Uptrend, and it is holding. Nothing here signals a change yet."),
        ("up", "flat"): ("uptrend, pausing", "Uptrend that has gone sideways in recent weeks. The long-term trend is still up."),
        ("up", "down"): ("uptrend, dipping", f"Long-term uptrend with a short-term dip. The 200-day average ({lvl}) is "
                                             "the level trend-followers watch if the dip deepens."),
        ("down", "down"): ("downtrend", "Downtrend, still in force. No sign of a turn yet."),
        ("down", "flat"): ("downtrend, pausing", "Long-term downtrend that has gone sideways lately. No sign of a turn yet."),
        ("down", "up"): ("downtrend, bouncing", "Long-term downtrend, but it has bounced recently. The bigger trend stays "
                                                f"down unless it gets back above its 200-day average ({lvl})."),
        ("weakening", "down"): ("uptrend breaking down", "An uptrend that is breaking down: it has fallen below both its "
                                "50-day and 200-day averages. Not a confirmed downtrend yet, but the direction lately is down."),
        ("weakening", "flat"): ("unsettled", f"It slipped below its long-term average and has steadied. Getting back above "
                                             f"{lvl} (the 200-day average) would repair the uptrend."),
        ("weakening", "up"): ("unsettled", f"It slipped below its long-term average but is recovering. Getting back above "
                                           f"{lvl} (the 200-day average) would repair the uptrend."),
        ("improving", "up"): ("downtrend turning up", "A downtrend that is turning up: it is back above both its 50-day "
                              "and 200-day averages. Not a confirmed uptrend yet, but the direction lately is up."),
        ("improving", "flat"): ("unsettled", "Back above its long-term average, but recent weeks have stalled. "
                                             "The trend is unsettled."),
        ("improving", "down"): ("unsettled", "Back above its long-term average, but recent weeks have been weaker. "
                                             "The trend is unsettled."),
    }.get((lt, mt), ("not enough history", "Too little history for a trend call. Recent weeks have been "
                     + dict(up="firm.", down="softer.", flat="sideways.")[mt]))
    if dd < -0.2:
        bl += f" It is {words_pct(dd)} off its 52-week high, a sharp drop."
    action = next_action(stance, lt, px, s50, s200, hi, lo, c, money, pr >= 0.8, qt.get("type"))
    return {"symbol": symbol, "name": qt.get("name") or symbol, "price": px, "stance": stance, "bottom_line": bl,
            "action": action, "points": pts, "as_of": qt.get("time") or dates[-1],
            "note": "Rule-based read of the price trend only. It does not know your goals, account or upcoming "
                    "news, and it is not personal advice or a forecast."}


def next_action(stance, lt, px, s50, s200, hi, lo, c, money, vol_hi, kind):
    """Mechanical next step from the trend state (trend-following rules: trade with the 200-day trend, wait for
    confirmation at turns, define the exit before entering, risk a fixed 0.5% per position)."""
    a14 = atr(hi, lo, c, 14)[-1]
    m50, m200, low20 = money(s50), money(s200) if s200 else "n/a", money(min(lo[-20:]))

    def sizing():  # currency-agnostic: position as a share of the account for a fixed 0.5% risk to the exit
        stop = px - 2 * a14 if a14 else None
        if not stop or stop <= 0:
            return ""
        dist = 1 - stop / px
        w = min(0.005 / dist, 0.25)
        return (f" If you buy at today's price, set the exit first: twice its average daily range lower, about "
                f"{money(stop)} ({words_pct(dist)} down). To lose no more than 0.5% of your account if that exit "
                f"hits, keep the position to about {w:.0%} of your account"
                + (" (capped at 25% so one position can't dominate)." if w >= 0.25 else "."))

    table = {
        "uptrend": ("Hold, or buy on pullbacks",
                    f"Hold. Trend-followers keep it while it stays above the 200-day average ({m200}).",
                    f"Buying now is following the trend. A calmer entry is a pullback toward the 50-day average ({m50})."
                    + sizing()),
        "uptrend, pausing": ("Hold; wait to add", "Hold. The long-term trend is intact.",
                             f"Wait for it to break out of the sideways range, or buy a pullback toward the 200-day "
                             f"average ({m200})." + sizing()),
        "uptrend, dipping": ("Hold; wait to add",
                             f"Hold while it stays above the 200-day average ({m200}). A close below it weakens the case.",
                             f"Wait for it to get back above its 50-day average ({m50}) before buying."),
        "downtrend": ("Avoid; reduce if you own it",
                      f"Consider reducing. Downtrends tend to persist, and a rally toward the 50-day average ({m50}) "
                      "is a common place to lighten up.",
                      f"Stay out until it gets back above its 200-day average ({m200})."),
        "downtrend, pausing": ("Avoid; reduce if you own it",
                               "Keep a firm exit level. The long-term trend is still down.",
                               f"Stay out until it gets back above its 200-day average ({m200})."),
        "downtrend, bouncing": ("Wait: a bounce is not a turn yet",
                                "Use the bounce to reassess. The long-term trend is still down.",
                                f"Wait. A close above the 200-day average ({m200}) would be the first real sign of a turn."),
        "uptrend breaking down": ("Reduce risk; don't buy the dip yet",
                                  f"Decide your exit now. A close below the recent low ({low20}) would extend the breakdown.",
                                  f"Don't try to catch the fall. Wait for it to steady and get back above its 50-day "
                                  f"average ({m50})."),
        "downtrend turning up": ("Watch; a small starter position is an option", "Hold.",
                                 f"This is an early turn. Trend-followers sometimes start small and add only once the "
                                 f"200-day average ({m200}) itself starts rising." + sizing()),
        "not enough history": ("Wait", "Not enough history for a rule-based call.",
                               "Not enough history for a rule-based call."),
    }
    if stance == "unsettled" and lt == "weakening":
        row = ("Wait for confirmation", f"Hold with a set exit. Getting back above the 200-day average ({m200}) would "
               "repair the trend.", f"Wait for a close above the 200-day average ({m200}).")
    elif stance == "unsettled":
        row = ("Wait for confirmation", f"Hold. An exit just below the 200-day average ({m200}) keeps losses contained.",
               f"Wait for it to clear its 50-day average ({m50}) again.")
    else:
        row = table[stance]
    caution = []
    if vol_hi:
        caution.append("Prices are swinging more than usual, so use smaller positions than normal.")
    if kind == "EQUITY":
        caution.append("Check the next earnings date first: these rules ignore news and earnings.")
    return {"label": row[0], "if_you_own": row[1], "if_you_dont": row[2], "caution": " ".join(caution)}


def cmd_summary(a):
    import csv
    with open(a.file, newline="", encoding="utf-8-sig") as fh:
        r = csv.DictReader(fh)
        cols = {k.strip().lower(): k for k in r.fieldnames or []}
        if not all(k in cols for k in ("date", "high", "low", "close")):
            sys.exit(f"summary needs date, high, low and close columns; found {list(cols)}")
        rows = [(x[cols["date"]], float(x[cols["high"]]), float(x[cols["low"]]), float(x[cols["close"]]))
                for x in r if x[cols["close"]] not in ("", None)]
    if rows and len(rows[0][0]) > 10:
        sys.exit("summary reads daily bars; this file looks intraday (fetch.py prices SYMBOL --years 3)")
    q = None
    if a.live:
        import fetch
        try:
            q = fetch.quote(a.symbol)
        except Exception as e:  # noqa: BLE001 -- fall back to the file's last close
            print(f"  (live quote unavailable: {e}; using the file's last close)")
    try:
        s = summarize(a.symbol or os.path.basename(a.file).split(".")[0], [x[0] for x in rows],
                      [x[1] for x in rows], [x[2] for x in rows], [x[3] for x in rows], q)
    except ValueError as e:
        sys.exit(str(e))
    act = s["action"]
    print(f"\n== {s['symbol']}: {s['stance']} (as of {s['as_of']}) ==")
    print(f"  Bottom line: {s['bottom_line']}")
    print(f"  Next best action (rule-based): {act['label']}")
    print(f"    If you own it: {act['if_you_own']}")
    print(f"    If you don't:  {act['if_you_dont']}")
    if act["caution"]:
        print(f"    Caution: {act['caution']}")
    print("  Why:")
    for p_ in s["points"]:
        print(f"    - {p_}")
    print(f"  {s['note']}")


# --------------------------------------------------------------------------- CLI
def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("indicators")
    x.add_argument("file")
    x.add_argument("--ppy", type=int, default=252, help="bars per year for annualizing realized vol")
    x.set_defaults(fn=cmd_indicators)
    x = s.add_parser("rank")
    x.add_argument("files", nargs="+")
    x.add_argument("--by", choices=["mom", "voladj"], default="voladj")
    x.set_defaults(fn=cmd_rank)
    x = s.add_parser("ruletest")
    x.add_argument("file")
    x.add_argument("--rule", required=True, choices=sorted(DEFAULT_GRIDS))
    x.add_argument("--params", nargs="*", help="override grid, e.g. --params 50 200  or  20,100 50,200")
    x.add_argument("--cost-bps", type=float, default=5.0, help="cost per 1.0 of turnover, in bps")
    x.add_argument("--short", action="store_true", help="allow short side")
    x.add_argument("--vol-target", type=float, help="annual vol target, e.g. 0.15")
    x.add_argument("--max-lev", type=float, default=2.0)
    x.add_argument("--oos", type=float, default=0.3, help="fraction held out for out-of-sample (0 = none)")
    x.add_argument("--delay", type=int, default=1,
                   help="bars between signal close and fill close (1 = next bar's close; 0 = signal close, optimistic)")
    x.add_argument("--ppy", type=int, default=252, help="bars per year for annualization (e.g. 252 daily, 52 weekly)")
    x.add_argument("--extra-trials", type=int, default=1,
                   help="multiply trial count by this if you tried other rules/markets before this run")
    x.set_defaults(fn=cmd_ruletest)
    x = s.add_parser("summary", help="plain-English bottom line + rule-based next best action from daily bars")
    x.add_argument("file", help="daily bars CSV, ~3 years (fetch.py prices SYMBOL --years 3)")
    x.add_argument("--symbol", help="ticker for the text and for --live")
    x.add_argument("--live", action="store_true", help="use the live Yahoo quote as the current price (needs --symbol)")
    x.set_defaults(fn=cmd_summary)
    a = p.parse_args(argv)
    if a.cmd == "summary" and a.live and not a.symbol:
        p.error("--live needs --symbol")
    a.fn(a)


if __name__ == "__main__":
    main()
