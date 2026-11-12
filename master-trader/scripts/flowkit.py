#!/usr/bin/env python3
"""flowkit -- order-flow analytics: volume profile, delta/footprint, OFI, book imbalance.

Companion to tradekit.py / techkit.py. Standard library only.

Commands
  profile FILE   volume profile (POC, 70% value area, HVN/LVN) + VWAP with 1/2-sigma bands.
                 FILE = trades CSV (time,price,size[,side]) for exact volume-at-price, or
                 OHLCV bars (volume spread evenly across each bar's range -- an approximation).
  delta FILE     trades -> bars with buy/sell volume, delta, CVD, footprint diagonal imbalances,
                 stacked-imbalance zones, unfinished auctions, absorption and delta-divergence flags.
                 Needs aggressor side; without a side column the tick rule is used (less accurate).
  ofi FILE       L1 quotes (time,bid,bid_size,ask,ask_size) -> Cont-Kukanov-Stoikov order-flow
                 imbalance, price-impact slope, contemporaneous vs predictive R^2, queue imbalance,
                 microprice.
  book FILE      L2 snapshot (side,price,size) -> spread, microprice, depth imbalance by level and
                 by distance, large resting orders.

Data: `fetch.py trades BTC` and `fetch.py book BTC` give free crypto data with true aggressor side.
For futures use an MBO/MBP export with the exchange aggressor flag (e.g. CME via Databento/Rithmic).
Equities: aggressor side is inferred (~75-80% accurate) and ~half of volume prints off-exchange.
"""
from __future__ import annotations

import argparse
import csv
import re
import datetime as dt
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tradekit import out  # noqa: E402


# --------------------------------------------------------------------------- io
def parse_time(s: str) -> float:
    s = s.strip()
    try:
        x = float(s)
        return x / 1e9 if x > 1e17 else x / 1e6 if x > 1e14 else x / 1e3 if x > 1e11 else x  # ns / us / ms / s
    except ValueError:
        pass
    s = s.replace("Z", "+00:00")
    s = re.sub(r"(\.\d{6})\d+", r"\1", s)  # nanosecond ISO fractions -> microseconds
    t = dt.datetime.fromisoformat(s)
    if t.tzinfo is None:
        t = t.replace(tzinfo=dt.timezone.utc)
    return t.timestamp()


def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        r = csv.DictReader(fh)
        cols = {c.strip().lower(): c for c in r.fieldnames or []}
        return cols, list(r)


def col(cols, *names):
    for n in names:
        if n in cols:
            return cols[n]
    return None


# Side conventions -> +1 buy aggressor / -1 sell aggressor. Letters like A/B/ask/bid mean opposite things in
# different feeds, so they are only accepted under an explicit convention -- a wrong guess flips every delta.
SIDE_CONVENTIONS = {
    "aggressor": {"buy": 1, "b": 1, "1": 1, "+1": 1, "sell": -1, "s": -1, "-1": -1},   # fetch.py output, Kraken
    "databento": {"b": 1, "bid": 1, "a": -1, "ask": -1},          # trades: side = aggressor (Bid = buyer), N = none
    "cme": {"1": 1, "2": -1},                                     # MDP3 AggressorSide: 1 buy, 2 sell, 0 none
    "maker": {"buy": -1, "b": -1, "sell": 1, "s": 1},             # raw Coinbase: side = resting (maker) order
    "buyer-maker": {"true": -1, "1": -1, "false": 1, "0": 1},     # Binance m / isBuyerMaker
    "at-quote": {"ask": 1, "a": 1, "at_ask": 1, "bid": -1, "at_bid": -1},  # vendor "traded at ask/bid" labels
}
CURRENT_CONVENTION = "aggressor"


def load_trades(path, convention=None):
    convention = convention or CURRENT_CONVENTION
    cols, rows = read_rows(path)
    tc, pc = col(cols, "time", "timestamp", "ts", "ts_event", "date"), col(cols, "price", "px")
    vc = col(cols, "size", "qty", "quantity", "volume", "amount")
    sc = col(cols, "side", "aggressor", "aggressor_side", "taker_side", "m", "is_buyer_maker", "isbuyermaker")
    if not (pc and vc):
        return None
    mapping = SIDE_CONVENTIONS[convention]
    trades, unknown = [], {}
    for row in rows:
        try:
            t = parse_time(row[tc]) if tc else float(len(trades))
            p, v = float(row[pc]), float(row[vc])
        except (ValueError, TypeError):
            continue
        side = None
        if sc:
            s = str(row[sc]).strip().lower()
            side = mapping.get(s)
            if side is None and s not in ("", "n", "0", "none", "nan"):
                unknown[s] = unknown.get(s, 0) + 1
        trades.append([t, p, v, side])
    if unknown and sum(unknown.values()) > 0.5 * len(trades):
        vals = ", ".join(f"'{k}'" for k in list(unknown)[:6])
        sys.exit(f"side column has values {vals} that the '{convention}' convention does not define. Pass "
                 f"--side-convention one of: {', '.join(SIDE_CONVENTIONS)} (databento: A=sell/B=buy aggressor; "
                 "cme: 1 buy/2 sell; maker: raw Coinbase; buyer-maker: Binance m flag).")
    trades.sort(key=lambda x: x[0])  # stable: keeps file order (exchange sequence) within equal timestamps
    inferred = any(tr[3] is None for tr in trades)
    if inferred:  # tick rule: uptick = buy, downtick = sell, zero tick = previous sign
        last_p, last_s = None, 1
        for tr in trades:
            if tr[3] is None:
                if last_p is not None and tr[1] != last_p:
                    last_s = 1 if tr[1] > last_p else -1
                tr[3] = last_s
            last_p, last_s = tr[1], tr[3]
    return trades, inferred


def load_bars(path):
    cols, rows = read_rows(path)
    need = {k: col(cols, k, k[0]) for k in ("open", "high", "low", "close")}
    vcol = col(cols, "volume", "vol", "v")
    dcol = col(cols, "date", "time", "timestamp")
    if not all(need.values()) or not vcol:
        return None
    bars = []
    for row in rows:
        try:
            bars.append((row[dcol] if dcol else "", *(float(row[need[k]]) for k in ("open", "high", "low", "close")),
                         float(row[vcol])))
        except (ValueError, TypeError):
            continue
    return bars


def nice_tick(x):
    if x <= 0:
        return 1.0
    e = 10 ** math.floor(math.log10(x))
    for m in (1, 2, 2.5, 5, 10):
        if x <= m * e:
            return m * e
    return 10 * e


def fmt_p(p, tick):
    d = max(0, -int(math.floor(math.log10(tick)))) if tick < 1 else 0
    return f"{p:.{d}f}"


# --------------------------------------------------------------------------- profile
def value_area(levels, vols, share=0.70):
    """CBOT-style: start at POC, repeatedly add the larger of the next two levels above/below."""
    poc = max(range(len(vols)), key=lambda i: vols[i])
    total = sum(vols)
    lo = hi = poc
    acc = vols[poc]
    while acc < share * total and (lo > 0 or hi < len(vols) - 1):
        up = sum(vols[hi + 1:hi + 3]) if hi < len(vols) - 1 else -1
        dn = sum(vols[max(0, lo - 2):lo]) if lo > 0 else -1
        if up >= dn:
            step = min(2, len(vols) - 1 - hi)
            acc += sum(vols[hi + 1:hi + 1 + step])
            hi += step
        else:
            step = min(2, lo)
            acc += sum(vols[lo - step:lo])
            lo -= step
    return poc, lo, hi


def cmd_profile(a):
    tr = load_trades(a.file)
    pv = []  # (price, volume) samples
    last_price = None
    if tr and not load_bars(a.file):
        trades, _ = tr
        if a.last:
            trades = trades[-a.last:]
        pv = [(p, v) for _, p, v, _ in trades]
        last_price = trades[-1][1]
        src = f"{len(trades)} trades (exact volume at price)"
        lo_p, hi_p = min(p for p, _ in pv), max(p for p, _ in pv)
    else:
        bars = load_bars(a.file)
        if not bars:
            sys.exit("need a trades CSV (time,price,size) or OHLCV bars")
        if a.anchor:
            bars = [b for b in bars if b[0] >= a.anchor]
        if a.last:
            bars = bars[-a.last:]
        last_price = bars[-1][4]
        src = f"{len(bars)} bars (volume spread across each bar's range -- approximate)"
        lo_p, hi_p = min(b[3] for b in bars), max(b[2] for b in bars)
    tick = a.tick or nice_tick((hi_p - lo_p) / a.bins)
    base = math.floor(lo_p / tick) * tick
    n = int(math.floor((hi_p - base) / tick)) + 1
    vols = [0.0] * n
    pvs = vwap_num = vwap_den = 0.0
    if pv:
        for p, v in pv:
            vols[min(n - 1, int((p - base) / tick))] += v
            vwap_num += p * v
            vwap_den += v
        vwap = vwap_num / vwap_den
        var = sum(v * (p - vwap) ** 2 for p, v in pv) / vwap_den
    else:
        for _, o, h, l, c, v in bars:
            i0, i1 = int((l - base) / tick), min(n - 1, int((h - base) / tick))
            share = v / (i1 - i0 + 1)
            for i in range(i0, i1 + 1):
                vols[i] += share
            tp = (h + l + c) / 3
            vwap_num += tp * v
            vwap_den += v
        vwap = vwap_num / vwap_den
        var = sum(v * ((h + l + c) / 3 - vwap) ** 2 for _, o, h, l, c, v in bars) / vwap_den
    sd = math.sqrt(var)
    poc, va_lo, va_hi = value_area(list(range(n)), vols)
    price = lambda i: base + (i + 0.5) * tick
    # HVN / LVN: local extrema of a 3-level smoothed profile
    sm = [sum(vols[max(0, i - 1):i + 2]) / len(vols[max(0, i - 1):i + 2]) for i in range(n)]
    mean_v = statistics.mean(sm)
    hvn = [i for i in range(1, n - 1) if sm[i] >= sm[i - 1] and sm[i] >= sm[i + 1] and sm[i] > 1.3 * mean_v]
    lvn = [i for i in range(1, n - 1) if sm[i] <= sm[i - 1] and sm[i] <= sm[i + 1] and sm[i] < 0.5 * mean_v and va_lo - 5 <= i <= va_hi + 5]
    loc = ("above value (acceptance higher or a failed auction -- watch for return to VAH)" if last_price > price(va_hi) + tick / 2 else
           "below value (acceptance lower or a failed auction -- watch for return to VAL)" if last_price < price(va_lo) - tick / 2 else
           "inside value (rotational; edges of value are the reference)")
    f = lambda p: fmt_p(p, tick)
    out([
        ("Source", src),
        ("Bin size", f(tick)),
        ("POC", f(price(poc))),
        ("Value area (70%)", f"{f(price(va_lo) - tick / 2)} .. {f(price(va_hi) + tick / 2)}"),
        ("VWAP", f"{f(vwap)}  (+/-1sd {f(vwap - sd)} .. {f(vwap + sd)}; +/-2sd {f(vwap - 2 * sd)} .. {f(vwap + 2 * sd)})"),
        ("Last price", f"{f(last_price)} -> {loc}"),
        ("High-volume nodes", ", ".join(f(price(i)) for i in hvn[:8]) or "none"),
        ("Low-volume nodes", ", ".join(f(price(i)) for i in lvn[:8]) or "none"),
        ("Read", "HVN = accepted price (magnet/support-resistance); LVN = rejected price (fast travel); [Lore/untested]"),
    ], f"Volume profile: {a.file}")
    if a.show:
        mx = max(vols)
        print()
        for i in range(n - 1, -1, -1):
            tag = " POC" if i == poc else " VA" if va_lo <= i <= va_hi else ""
            print(f"  {f(price(i)):>12} {'#' * int(40 * vols[i] / mx):<40} {vols[i]:,.2f}{tag}")


# --------------------------------------------------------------------------- delta / footprint
def bar_key_fn(spec: str):
    s = spec.strip().lower()
    if s.endswith("t"):
        n = int(s[:-1])
        return ("count", n)
    if s.endswith("v"):
        return ("volume", float(s[:-1]))
    mult = {"s": 1, "m": 60, "h": 3600, "d": 86400}[s[-1]]
    return ("time", int(s[:-1]) * mult)


def build_bars(trades, spec):
    kind, n = bar_key_fn(spec)
    bars, cur, cnt, vacc, key = [], None, 0, 0.0, None
    for t, p, v, s in trades:
        if kind == "time":
            k = int(t // n)
            new = cur is None or k != key
            key = k
        elif kind == "count":
            new = cur is None or cnt >= n
        else:
            new = cur is None or vacc >= n
        if new:
            if cur:
                bars.append(cur)
            cur = {"t": t, "o": p, "h": p, "l": p, "c": p, "buy": 0.0, "sell": 0.0, "fp": {}}
            cnt, vacc = 0, 0.0
        cur["h"], cur["l"], cur["c"] = max(cur["h"], p), min(cur["l"], p), p
        if s > 0:
            cur["buy"] += v
        else:
            cur["sell"] += v
        cur["fp"].setdefault(p, [0.0, 0.0])[0 if s < 0 else 1] += v  # [bid-side (sells), ask-side (buys)]
        cnt += 1
        vacc += v
    if cur:
        bars.append(cur)
    return bars


def regrid(fp, tick):
    g = {}
    for p, (b, a_) in fp.items():
        k = round(math.floor(p / tick + 1e-9) * tick, 10)
        x = g.setdefault(k, [0.0, 0.0])
        x[0] += b
        x[1] += a_
    return g


def imbalances(g, tick, ratio, min_vol):
    """Diagonal imbalance: buy at p if ask[p] >= ratio * bid[p - tick]; sell at p if bid[p] >= ratio * ask[p + tick]."""
    buy, sell = [], []
    for p in sorted(g):
        b_below = g.get(round(p - tick, 10), [0.0, 0.0])[0]
        a_above = g.get(round(p + tick, 10), [0.0, 0.0])[1]
        if g[p][1] >= min_vol and g[p][1] >= ratio * max(b_below, 1e-12):
            buy.append(p)
        if g[p][0] >= min_vol and g[p][0] >= ratio * max(a_above, 1e-12):
            sell.append(p)
    return buy, sell


def stacks(levels, tick, k):
    zones, run = [], []
    for p in levels:
        if run and abs(p - run[-1] - tick) < tick * 1e-6:
            run.append(p)
        else:
            if len(run) >= k:
                zones.append((run[0], run[-1]))
            run = [p]
    if len(run) >= k:
        zones.append((run[0], run[-1]))
    return zones


def cmd_delta(a):
    tr = load_trades(a.file)
    if not tr:
        sys.exit("need a trades CSV: time,price,size[,side]")
    trades, inferred = tr
    bars = build_bars(trades, a.bar)
    if len(bars) < 3:
        sys.exit(f"only {len(bars)} bars -- use a smaller --bar")
    ranges = [b["h"] - b["l"] for b in bars]
    tick = a.tick or nice_tick(max(statistics.median(ranges), 1e-9) / 12)
    vols = [b["buy"] + b["sell"] for b in bars]
    cvd, events = 0.0, []
    look = a.lookback
    rows = []
    for i, b in enumerate(bars):
        vol = b["buy"] + b["sell"]
        d = b["buy"] - b["sell"]
        cvd += d
        b["cvd"], b["d"], b["v"] = cvd, d, vol
        g = regrid(b["fp"], tick)
        bi, si = imbalances(g, tick, a.ratio, a.min_vol * (statistics.median(vols) / max(1, len(g))))
        ts = dt.datetime.fromtimestamp(b["t"], dt.timezone.utc).strftime("%m-%d %H:%M:%S")
        f = lambda p: fmt_p(p, tick)
        for lo, hi in stacks(bi, tick, a.stack):
            events.append((ts, f"stacked BUY imbalance {f(lo)}-{f(hi)} (initiative buying; zone often acts as support)"))
        for lo, hi in stacks(si, tick, a.stack):
            events.append((ts, f"stacked SELL imbalance {f(lo)}-{f(hi)} (initiative selling; zone often acts as resistance)"))
        if i >= look:
            # unfinished auction: meaningful only at a swing extreme, with real two-sided volume at the extreme
            lvl_med = statistics.median(x[0] + x[1] for x in g.values())
            top, bot = g[max(g)], g[min(g)]
            swing_hi = b["h"] >= max(x["h"] for x in bars[i - look:i])
            swing_lo = b["l"] <= min(x["l"] for x in bars[i - look:i])
            if swing_hi and min(top) >= 0.25 * lvl_med:
                events.append((ts, f"unfinished auction at swing high {f(max(g))} (two-sided trade at the extreme; revisit common [Lore])"))
            if swing_lo and min(bot) >= 0.25 * lvl_med:
                events.append((ts, f"unfinished auction at swing low {f(min(g))} (two-sided trade at the extreme; revisit common [Lore])"))
            prev = bars[i - look:i]
            avg_v = statistics.mean(x["v"] for x in prev)
            avg_r = statistics.mean(x["h"] - x["l"] for x in prev) or 1e-12
            rng = b["h"] - b["l"]
            if vol >= 2 * avg_v and rng <= 0.6 * avg_r and abs(d) >= 0.2 * vol:
                if d < 0 and b["c"] >= b["o"]:
                    events.append((ts, f"ABSORPTION of selling: vol {vol / avg_v:.1f}x avg, delta {d:+,.2f}, price held (bullish if at support)"))
                elif d > 0 and b["c"] <= b["o"]:
                    events.append((ts, f"ABSORPTION of buying: vol {vol / avg_v:.1f}x avg, delta {d:+,.2f}, price held (bearish if at resistance)"))
            ph = max(range(i - look, i), key=lambda j: bars[j]["h"])
            pl = min(range(i - look, i), key=lambda j: bars[j]["l"])
            if b["h"] > bars[ph]["h"] and d < 0 and cvd < bars[ph]["cvd"]:
                events.append((ts, f"BEARISH delta divergence: new {look}-bar high {f(b['h'])} on negative delta {d:+,.2f} and CVD below the prior high (hypothesis only: may be passive bids, not hidden selling)"))
            if b["l"] < bars[pl]["l"] and d > 0 and cvd > bars[pl]["cvd"]:
                events.append((ts, f"BULLISH delta divergence: new {look}-bar low {f(b['l'])} on positive delta {d:+,.2f} and CVD above the prior low (hypothesis only: may be passive offers, not hidden buying)"))
        rows.append((ts, b, d, vol))
    print(f"\n== Delta / footprint: {a.file}  ({len(trades)} trades -> {len(bars)} bars of {a.bar}; "
          f"footprint tick {fmt_p(tick, tick)}; imbalance {a.ratio:.0f}x, stack {a.stack}) ==")
    if inferred:
        print("  WARNING: side column missing/partial -- aggressor inferred with the tick rule (expect misclassification)")
    print(f"  {'time':<16}{'open':>11}{'high':>11}{'low':>11}{'close':>11}{'volume':>11}{'delta':>11}{'delta%':>8}{'CVD':>12}")
    for ts, b, d, vol in rows[-a.show:]:
        f = lambda p: fmt_p(p, tick)
        print(f"  {ts:<16}{f(b['o']):>11}{f(b['h']):>11}{f(b['l']):>11}{f(b['c']):>11}{vol:>11,.2f}{d:>+11,.2f}"
              f"{(d / vol if vol else 0):>+8.0%}{b['cvd']:>+12,.2f}")
    tot_b, tot_s = sum(b["buy"] for b in bars), sum(b["sell"] for b in bars)
    px_chg = bars[-1]["c"] - bars[0]["o"]
    out([
        ("Session buy / sell volume", f"{tot_b:,.2f} / {tot_s:,.2f}  (buy share {tot_b / (tot_b + tot_s):.1%})"),
        ("Net delta vs price change", f"{tot_b - tot_s:+,.2f} vs {px_chg:+,.4g} -> "
                                      + ("aligned" if (tot_b - tot_s) * px_chg > 0 else "DIVERGENT (passive side winning)")),
    ], "Summary")
    print(f"\n== Events (last {a.events}) ==")
    for ts, e in events[-a.events:]:
        print(f"  {ts}  {e}")
    if not events:
        print("  none")
    print("\n  Read events in LOCATION context (value area, VWAP, prior day H/L, round numbers); alone they are noise.")
    print("  Evidence: order-flow imbalance has strong contemporaneous price impact but short predictive horizons;")
    print("  footprint patterns are practitioner lore/untested -- see references/order-flow.md.")
    if a.out:
        with open(a.out, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["time", "open", "high", "low", "close", "volume", "buy_volume", "sell_volume", "delta", "cvd"])
            for b in bars:
                w.writerow([dt.datetime.fromtimestamp(b["t"], dt.timezone.utc).isoformat(), b["o"], b["h"], b["l"], b["c"],
                            b["v"], b["buy"], b["sell"], b["d"], b["cvd"]])
        print(f"  wrote bars to {a.out} (open/high/low/close/volume columns work with techkit.py)")


# --------------------------------------------------------------------------- OFI
def cmd_ofi(a):
    cols, rows = read_rows(a.file)
    bc, bsc = col(cols, "bid", "bid_price", "bid_px"), col(cols, "bid_size", "bidsize", "bid_sz", "bid_qty")
    ac, asc = col(cols, "ask", "ask_price", "ask_px"), col(cols, "ask_size", "asksize", "ask_sz", "ask_qty")
    if not all((bc, bsc, ac, asc)):
        sys.exit("quotes CSV needs bid, bid_size, ask, ask_size columns")
    q = []
    for r in rows:
        try:
            q.append((float(r[bc]), float(r[bsc]), float(r[ac]), float(r[asc])))
        except (ValueError, TypeError):
            continue
    if len(q) < 4 * a.window:
        sys.exit(f"need at least {4 * a.window} quote updates")
    e = [0.0]
    for (pb0, qb0, pa0, qa0), (pb, qb, pa, qa) in zip(q, q[1:]):
        e.append((qb if pb >= pb0 else 0) - (qb0 if pb <= pb0 else 0) - (qa if pa <= pa0 else 0) + (qa0 if pa >= pa0 else 0))
    mids = [(b + a_) / 2 for b, _, a_, _ in q]
    W = a.window
    ofi, dmid, depth = [], [], []
    for k in range(0, len(q) - W, W):
        ofi.append(sum(e[k + 1:k + W + 1]))
        dmid.append(mids[k + W] - mids[k])
        depth.append(statistics.mean((q[j][1] + q[j][3]) / 2 for j in range(k, k + W)))

    def reg(x, y):
        mx, my = statistics.mean(x), statistics.mean(y)
        sxx = sum((u - mx) ** 2 for u in x)
        sxy = sum((u - mx) * (v - my) for u, v in zip(x, y))
        syy = sum((v - my) ** 2 for v in y)
        b = sxy / sxx if sxx else 0.0
        r2 = sxy * sxy / (sxx * syy) if sxx and syy else 0.0
        return b, r2

    beta, r2 = reg(ofi, dmid)
    beta_p, r2_p = reg(ofi[:-1], dmid[1:])
    pb, qb, pa, qa = q[-1]
    qi = qb / (qb + qa) if qb + qa else 0.5
    micro = (pa * qb + pb * qa) / (qb + qa) if qb + qa else (pa + pb) / 2
    hits = [1 if (q[j][1] / (q[j][1] + q[j][3]) - 0.5) * (mids[j + 1] - mids[j]) > 0 else 0
            for j in range(len(q) - 1) if mids[j + 1] != mids[j] and q[j][1] + q[j][3] > 0]
    out([
        ("Quote updates / windows", f"{len(q)} / {len(ofi)} windows of {W} events"),
        ("Impact slope (dMid per unit OFI)", f"{beta:.3e}   (Cont et al.: slope ~ 1/depth; avg depth {statistics.mean(depth):,.2f})"),
        ("Contemporaneous R^2", f"{r2:.1%}  (OFI explains same-window mid changes)"),
        ("Predictive R^2 (next window)", f"{r2_p:.1%}  (what you can actually trade on -- typically far smaller)"),
        ("Queue imbalance (last)", f"{qi:.2f}  (bid/(bid+ask) size at top; >0.5 leans up)"),
        ("Weighted mid (last)", f"{micro:.6g} vs mid {(pa + pb) / 2:.6g}  (size-weighted; not Stoikov's micro-price)"),
        ("Queue-imbalance hit rate", f"{statistics.mean(hits):.1%} of next mid moves in the imbalance direction ({len(hits)} moves)"
                                     if hits else "n/a"),
        ("Read", "seconds-horizon signal; after spread + fees + latency most retail cannot capture it"),
    ], f"Order-flow imbalance: {a.file}")


# --------------------------------------------------------------------------- book
def cmd_book(a):
    cols, rows = read_rows(a.file)
    sc, pc, vc = col(cols, "side"), col(cols, "price", "px"), col(cols, "size", "qty", "quantity", "volume")
    bids, asks = [], []
    for r in rows:
        try:
            side, p, v = r[sc].strip().lower(), float(r[pc]), float(r[vc])
        except (ValueError, TypeError, AttributeError):
            continue
        (bids if side.startswith("b") else asks).append((p, v))
    bids.sort(reverse=True)
    asks.sort()
    if not bids or not asks:
        sys.exit("need both bid and ask rows")
    pb, qb = bids[0]
    pa, qa = asks[0]
    mid = (pa + pb) / 2
    micro = (pa * qb + pb * qa) / (qb + qa)
    rows_out = [
        ("Best bid / ask", f"{pb} x {qb:,.4g}  /  {pa} x {qa:,.4g}"),
        ("Spread", f"{pa - pb:.6g} ({(pa - pb) / mid * 1e4:.2f} bps)"),
        ("Weighted mid", f"{micro:.8g} ({(micro - mid) / mid * 1e4:+.2f} bps vs mid; size-weighted, not Stoikov's micro-price)"),
    ]
    for n in (1, 5, 10, 20):
        if len(bids) >= n and len(asks) >= n:
            b, s = sum(v for _, v in bids[:n]), sum(v for _, v in asks[:n])
            rows_out.append((f"Depth imbalance top {n}", f"{(b - s) / (b + s):+.2f}  (bid {b:,.4g} / ask {s:,.4g})"))
    for bps in (10, 25, 50):
        b = sum(v for p, v in bids if p >= mid * (1 - bps / 1e4))
        s = sum(v for p, v in asks if p <= mid * (1 + bps / 1e4))
        if b + s:
            rows_out.append((f"Imbalance within {bps} bps", f"{(b - s) / (b + s):+.2f}"))
    med = statistics.median(v for _, v in bids + asks)
    walls_b = sorted(((p, v) for p, v in bids if v >= a.wall * med), key=lambda x: -x[1])[:3]
    walls_a = sorted(((p, v) for p, v in asks if v >= a.wall * med), key=lambda x: -x[1])[:3]
    fw = lambda ws: ", ".join(f"{p} ({v:,.4g}, {abs(p - mid) / mid * 1e4:.0f} bps)" for p, v in ws) or "none"
    rows_out += [
        (f"Large bids (>= {a.wall:.0f}x median)", fw(walls_b)),
        (f"Large asks (>= {a.wall:.0f}x median)", fw(walls_a)),
        ("Caveat", "displayed size can be cancelled in milliseconds; walls are information, not commitments "
                   "(placing orders you intend to cancel to mislead is spoofing -- illegal)"),
    ]
    out(rows_out, f"Order book: {a.file}")


# --------------------------------------------------------------------------- CLI
def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("profile")
    x.add_argument("file")
    x.add_argument("--bins", type=int, default=40, help="approximate number of price levels")
    x.add_argument("--tick", type=float, help="price bin size (overrides --bins)")
    x.add_argument("--anchor", help="bars only: start date for anchored profile/VWAP (YYYY-MM-DD)")
    x.add_argument("--last", type=int, help="use only the last N bars/trades")
    x.add_argument("--show", action="store_true", help="print the histogram")
    x.set_defaults(fn=cmd_profile)
    x = s.add_parser("delta")
    x.add_argument("file")
    x.add_argument("--bar", default="5m", help="bar spec: 30s, 1m, 5m, 1h (time) | 500t (trades) | 100v (volume)")
    x.add_argument("--tick", type=float, help="footprint price increment (default: auto)")
    x.add_argument("--ratio", type=float, default=3.0, help="diagonal imbalance ratio (300%% default)")
    x.add_argument("--stack", type=int, default=3, help="consecutive imbalanced levels for a stacked zone")
    x.add_argument("--min-vol", type=float, default=0.5,
                   help="min level volume for an imbalance, as a fraction of (median bar volume / levels in the bar)")
    x.add_argument("--lookback", type=int, default=10, help="bars for divergence/absorption baselines")
    x.add_argument("--show", type=int, default=12, help="bars to print")
    x.add_argument("--events", type=int, default=15)
    x.add_argument("--out", help="write bars (OHLCV + delta + CVD) CSV")
    x.set_defaults(fn=cmd_delta)
    for name in ("profile", "delta"):
        s.choices[name].add_argument("--side-convention", choices=sorted(SIDE_CONVENTIONS), default="aggressor",
                                     help="how to read the side column (default aggressor: buy/sell, b/s, 1/-1)")
    x = s.add_parser("ofi")
    x.add_argument("file")
    x.add_argument("--window", type=int, default=50, help="quote updates per aggregation window")
    x.set_defaults(fn=cmd_ofi)
    x = s.add_parser("book")
    x.add_argument("file")
    x.add_argument("--wall", type=float, default=5.0)
    x.set_defaults(fn=cmd_book)
    a = p.parse_args(argv)
    global CURRENT_CONVENTION
    CURRENT_CONVENTION = getattr(a, "side_convention", "aggressor")
    a.fn(a)


if __name__ == "__main__":
    main()
