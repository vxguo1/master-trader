#!/usr/bin/env python3
"""daykit -- day-trading analysis on intraday bars for the master-trader toolkit.

Standard library only. Bars: CSV date,open,high,low,close,volume with 'YYYY-MM-DD HH:MM' bar START times in
exchange-local time, oldest first -- what `fetch.py prices SYMBOL --interval 5m` writes.

Commands
  levels     the day-trading map for the latest (or --date) session: prior-day high/low/close, overnight
             high/low, gap in ATRs, opening ranges, session VWAP with 1/2-sigma bands, relative volume at this
             time of day, share of the daily ATR used, a rule-based day-type read, a plain-English bottom line,
             the next best action and a sized bracket ticket.
  backtest   intraday rules over every session in the file, flat by the close, next-bar fills, costs:
             orb (opening-range breakout: 'break' = stop orders at the range, 'candle' = direction of the
             opening range), vwap (long above / short below VWAP), imom (first half-hour -> last half-hour),
             noise (noise-band momentum), gap (gap-size study: fill rate, open-to-close drift).
  timeofday  volume, volatility and return by time of day, plus the first->last half-hour correlation.
  plan       day-trade plan from entry and stop: size with a buying-power cap, cost per R, breakeven win rate,
             daily loss limit in R, and a bracket ticket (entry + stop-loss + take-profit, one cancels the other).
  journal    day-trading journal review: expectancy, by hour / setup / weekday / trade number of the day,
             after a loss vs after a win, daily P&L, loss-limit breaches, the biggest leaks.
  inplay     "stocks in play" screen: gap, relative volume, ATR and liquidity filters, opening-range and VWAP
             position (fetches 5-minute bars incl. pre-market from Yahoo).

Sessions: --session 09:30-16:00 (US cash hours, the default; also the usual RTH for index futures levels).
Crypto or other 24-hour markets: --session 00:00-24:00.
Research on delayed, unofficial data: not for live order routing.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tradekit import moments, out, sharpe_report  # noqa: E402

Z95 = 1.645  # one-sided 95%


# --------------------------------------------------------------------------- bars and sessions
def parse_dt(s: str) -> dt.datetime:
    s = s.strip().replace("T", " ")
    for fmt, n in (("%Y-%m-%d %H:%M:%S", 19), ("%Y-%m-%d %H:%M", 16)):
        try:
            return dt.datetime.strptime(s[:n], fmt)
        except ValueError:
            continue
    raise ValueError(f"can't read time '{s}' (want YYYY-MM-DD HH:MM)")


def load_bars(path: str) -> list[list]:
    """[[datetime, o, h, l, c, v], ...] oldest first."""
    with open(path, newline="", encoding="utf-8-sig") as fh:
        r = csv.DictReader(fh)
        cols = {k.strip().lower(): k for k in r.fieldnames or []}
        tkey = next((cols[k] for k in ("date", "datetime", "time", "timestamp") if k in cols), None)
        keys = [next((cols[a] for a in al if a in cols), None) for al in
                (("open", "o"), ("high", "h"), ("low", "l"), ("close", "c"), ("volume", "vol", "v"))]
        if not tkey or None in keys[:4]:
            sys.exit(f"{path}: need date,open,high,low,close[,volume] columns; found {list(cols)}")
        bars = []
        for row in r:
            try:
                bars.append([parse_dt(row[tkey])] + [float(row[k]) for k in keys[:4]]
                            + [float(row[keys[4]] or 0) if keys[4] else 0.0])
            except (ValueError, TypeError):
                continue
    if not bars:
        sys.exit(f"{path}: no bars")
    bars.sort(key=lambda b: b[0])
    if len(bars) > 1 and all(b[0].hour == 0 and b[0].minute == 0 for b in bars):
        sys.exit(f"{path}: these look like daily bars; daykit needs intraday bars (fetch.py prices S --interval 5m)")
    return bars


def bars_from_rows(rows) -> list[list]:
    """fetch.yahoo_bars rows [ts, label, o, h, l, c, v] -> daykit bars."""
    return [[dt.datetime.strptime(r[1], "%Y-%m-%d %H:%M"), r[2], r[3], r[4], r[5], float(r[6])] for r in rows]


def bar_minutes(bars) -> int:
    d = sorted(int((b[0] - a[0]).total_seconds() // 60) for a, b in zip(bars, bars[1:])
               if a[0].date() == b[0].date() and b[0] > a[0])
    return max(1, d[len(d) // 2]) if d else 5


def parse_session(s: str) -> tuple[int, int]:
    try:
        a, b = s.split("-")
        f = [int(x.split(":")[0]) * 60 + int(x.split(":")[1]) for x in (a, b)]
    except (ValueError, IndexError):
        sys.exit(f"--session must look like 09:30-16:00, got '{s}'")
    if not 0 <= f[0] < f[1] <= 1440:
        sys.exit("--session start must be before its end within one day (use 00:00-24:00 for 24h markets)")
    return f[0], f[1]


def mod(t: dt.datetime) -> int:
    return t.hour * 60 + t.minute


def hhmm(m: int) -> str:
    return f"{m // 60:02d}:{m % 60:02d}"


def split_sessions(bars, sess):
    """Sessions in date order: {'date', 'bars' (inside the session), 'pre' (bars since the previous session ended:
    after-hours + overnight + pre-market)}. Also returns the bars after the last session (still pending)."""
    s, e = sess
    out_, pending = [], []
    for b in bars:
        m = mod(b[0])
        if s <= m < e:
            if not out_ or out_[-1]["date"] != b[0].date():
                out_.append({"date": b[0].date(), "bars": [], "pre": pending})
                pending = []
            out_[-1]["bars"].append(b)
        else:
            pending.append(b)
    for S in out_:
        S["o"], S["h"] = S["bars"][0][1], max(b[2] for b in S["bars"])
        S["l"], S["c"] = min(b[3] for b in S["bars"]), S["bars"][-1][4]
        S["v"] = sum(b[5] for b in S["bars"])
    return out_, pending


def daily_atr(sessions, i, n=14):
    """Wilder-style true range averaged over the n sessions before sessions[i] (simple mean)."""
    trs = []
    for k in range(max(1, i - n), i):
        pc = sessions[k - 1]["c"]
        trs.append(max(sessions[k]["h"], pc) - min(sessions[k]["l"], pc))
    return (sum(trs) / len(trs), len(trs)) if trs else (None, 0)


def vwap_series(bars):
    """[(vwap, sd)] per bar, cumulative from the first bar; equal weights when there is no volume (TWAP)."""
    res, sv, spv, spv2 = [], 0.0, 0.0, 0.0
    novol = not any(b[5] for b in bars)
    for b in bars:
        tp, v = (b[2] + b[3] + b[4]) / 3, 1.0 if novol else b[5]
        sv, spv, spv2 = sv + v, spv + tp * v, spv2 + tp * tp * v
        vw = spv / sv if sv else tp
        res.append((vw, math.sqrt(max(0.0, spv2 / sv - vw * vw)) if sv else 0.0))
    return res, novol


def opening_range(bars, s, n):
    orb = [b for b in bars if mod(b[0]) < s + n]
    if not orb:
        return None
    return {"n": n, "hi": max(b[2] for b in orb), "lo": min(b[3] for b in orb), "open": orb[0][1],
            "close": orb[-1][4], "complete": any(mod(b[0]) >= s + n for b in bars), "end": hhmm(s + n)}


def cum_volume(bars, upto_min):
    return sum(b[5] for b in bars if mod(b[0]) <= upto_min)


def rel_volume(sessions, i, bars_today, upto_min, n=14):
    """Today's volume through upto_min vs the average of the prior n sessions through the same minute."""
    prior = [cum_volume(sessions[k]["bars"], upto_min) for k in range(max(0, i - n), i)]
    prior = [p for p in prior if p > 0]
    today = cum_volume(bars_today, upto_min)
    return (today / (sum(prior) / len(prior)), len(prior)) if prior and today else (None, len(prior))


def clean_ext(bars, atr_v):
    """Drop thin off-hours bars whose high/low sits more than 1.5 daily ATRs from the median close (bad prints)."""
    med = statistics.median(b[4] for b in bars)
    tol = 1.5 * atr_v if atr_v else 0.05 * med
    good = [b for b in bars if b[2] <= med + tol and b[3] >= med - tol]
    return good, len(bars) - len(good)


def round_levels(p):
    if p <= 0:
        return None, None
    step = 10 ** (math.floor(math.log10(p)) - 1)  # 757 -> 10s, 7,600 -> 100s, 45 -> 1s
    lo = math.floor(p / step) * step
    return lo, lo + step


def fmt(x, d=None):
    if x is None:
        return "n/a"
    d = d if d is not None else (4 if abs(x) < 10 else 2)
    return f"{x:,.{d}f}"


# --------------------------------------------------------------------------- levels
def levels(bars, sess=(570, 960), date=None, ors=(5, 15, 30), primary=5, equity=None, risk=0.5, bp=4.0,
           target_r=2.0, price=None, symbol=""):
    s, e = sess
    bm = bar_minutes(bars)
    sessions, pending = split_sessions(bars, sess)
    if not sessions:
        raise ValueError("no bars inside the session window; check --session")
    if date:
        idx = next((k for k, S in enumerate(sessions) if S["date"].isoformat() == date), None)
        if idx is None:
            raise ValueError(f"no session on {date}; the file covers {sessions[0]['date']} .. {sessions[-1]['date']}")
        pending = []
    else:
        idx = len(sessions) - 1
    pre_open = not date and pending and pending[-1][0].date() > sessions[-1]["date"] and mod(pending[-1][0]) < s
    if pre_open:
        today, prev, overnight = None, sessions[idx], pending
        atr_v, natr = daily_atr(sessions, idx + 1)
        last_bar = pending[-1]
    else:
        today = sessions[idx]
        prev = sessions[idx - 1] if idx > 0 else None
        overnight = today["pre"]
        atr_v, natr = daily_atr(sessions, idx)
        last_bar = today["bars"][-1]
    px = price if price is not None else last_bar[4]
    lm = mod(last_bar[0])
    r = {"symbol": symbol, "bar_minutes": bm, "session": f"{hhmm(s)}-{hhmm(e)}", "time": last_bar[0].strftime("%Y-%m-%d %H:%M"),
         "price": px, "atr": atr_v, "atr_days": natr, "cautions": [], "points": []}
    if prev:
        r.update(pdh=prev["h"], pdl=prev["l"], pdc=prev["c"], prev_date=prev["date"].isoformat())
    if overnight:
        good, bad = clean_ext(overnight, atr_v)
        if good:
            r.update(onh=max(b[2] for b in good), onl=min(b[3] for b in good))
        if bad:
            r["cautions"].append(f"Ignored {bad} off-hours bar(s) with prints far from the rest (likely bad ticks).")
    r["round"] = round_levels(px)
    if pre_open:
        r.update(date=pending[-1][0].date().isoformat(), phase="pre-open", ors=[], vwap=None)
        if prev:
            r["gap"] = px / prev["c"] - 1
            r["gap_atr"] = (px - prev["c"]) / atr_v if atr_v else None
        return _read(r, sess, primary, equity, risk, bp, target_r)
    tb = today["bars"]
    r["date"] = today["date"].isoformat()
    r["open"], r["hod"], r["lod"] = today["o"], today["h"], today["l"]
    if prev and not (s == 0 and e == 1440):  # a 24-hour market opens where it closed: no gap to speak of
        r["gap"] = today["o"] / prev["c"] - 1
        r["gap_atr"] = (today["o"] - prev["c"]) / atr_v if atr_v else None
        r["gap_filled"] = (today["l"] <= prev["c"]) if today["o"] > prev["c"] else (today["h"] >= prev["c"])
    r["ors"] = [x for x in (opening_range(tb, s, n) for n in ors if n >= bm and n % bm == 0) if x]
    vw, novol = vwap_series(tb)
    r["vwap"], r["vwap_sd"], r["twap"] = vw[-1][0], vw[-1][1], novol
    r["vwap_crosses"] = sum(1 for k in range(1, len(tb)) if (tb[k][4] - vw[k][0]) * (tb[k - 1][4] - vw[k - 1][0]) < 0)
    r["atr_used"] = (today["h"] - today["l"]) / atr_v if atr_v else None
    r["rvol"], r["rvol_days"] = rel_volume(sessions, idx, tb, lm) if not novol else (None, 0)
    end = lm + bm
    r["phase"] = ("closed" if end >= e or date else "opening range forming" if end < s + primary
                  else "last half-hour" if end > e - 30 else "open")
    if date is None and pending and r["phase"] != "closed":
        r["phase"] = "closed"  # after-hours bars exist: the session is over
    first = next((b for b in tb if mod(b[0]) + bm >= s + 30), None)
    if prev and first and mod(first[0]) + bm <= lm + bm:
        r["first_half_hour"] = first[4] / prev["c"] - 1
    return _read(r, sess, primary, equity, risk, bp, target_r)


def _read(r, sess, primary, equity, risk, bp, target_r):
    """Rule-based day-type read, bottom line, next best action and bracket ticket."""
    s, e = sess
    px, atr_v, sym = r["price"], r["atr"], r["symbol"] or "It"
    gap_txt = ""
    if r.get("gap") is not None:
        gap_txt = f"{'up' if r['gap'] > 0 else 'down'} {abs(r['gap']):.1%} from yesterday's close"
        if r.get("gap_atr") is not None:
            gap_txt += f" ({abs(r['gap_atr']):.1f}x its normal daily range)"
    r["ticket"] = None
    if r["phase"] == "pre-open":
        r["day_type"] = "pre-open"
        r["bottom_line"] = f"{sym} is trading {gap_txt} before the open, at {fmt(px)}."
        r["action"] = {"label": "Wait for the open",
                       "in_trade": "Overnight positions face the open's gap risk; decide before 09:30 whether to keep them.",
                       "flat": f"Mark yesterday's high {fmt(r.get('pdh'))}, low {fmt(r.get('pdl'))} and close {fmt(r.get('pdc'))}. "
                               f"Let the first {primary} minutes set the opening range, then trade only a clean break of it."}
        if r.get("gap_atr") is not None and abs(r["gap_atr"]) >= 1:
            r["cautions"].append("Big gap (at least one normal day's range): expect a wide, fast open; trade smaller.")
        return r
    orp = next((o for o in r["ors"] if o["n"] >= primary and o["complete"]), None)
    above_vw = px > r["vwap"]
    if r["phase"] == "opening range forming" or orp is None:
        r["day_type"] = "opening range forming"
        r["bottom_line"] = f"{sym} opened {gap_txt}; the first {primary} minutes are still setting the range. Price {fmt(px)}."
        r["action"] = {"label": f"Wait until {hhmm(s + primary)}", "in_trade": "Hold your plan's stop; don't add during the opening swing.",
                       "flat": "No trade until the opening range is complete."}
        return r
    hi, lo = orp["hi"], orp["lo"]
    used = r.get("atr_used")
    if px > hi and above_vw:
        bias = "long"
    elif px < lo and not above_vw:
        bias = "short"
    elif lo <= px <= hi:
        bias = "inside"
    else:
        bias = "mixed"
    trendish = used is not None and used >= 0.6 and r["vwap_crosses"] <= 3
    if bias in ("long", "short") and trendish:
        r["day_type"] = f"trend day {'up' if bias == 'long' else 'down'} (so far)"
    elif r["vwap_crosses"] >= 5 or bias == "inside":
        r["day_type"] = "range / balance day (so far)"
    else:
        r["day_type"] = "undecided"
    side_txt = {"long": f"above its {orp['n']}-minute opening range ({fmt(hi)}) and above VWAP, the day's average price ({fmt(r['vwap'])})",
                "short": f"below its {orp['n']}-minute opening range ({fmt(lo)}) and below VWAP, the day's average price ({fmt(r['vwap'])})",
                "inside": f"inside its {orp['n']}-minute opening range ({fmt(lo)}-{fmt(hi)})",
                "mixed": f"outside its opening range ({fmt(lo)}-{fmt(hi)}) but on the other side of VWAP ({fmt(r['vwap'])})"}[bias]
    vol_txt = ((" on more than 100x normal volume for this time of day" if r["rvol"] > 100 else
                f" on {r['rvol']:.1f}x normal volume for this time of day") if r.get("rvol") else "")
    r["bottom_line"] = f"{sym} at {fmt(px)} is {side_txt}{vol_txt}. It opened {gap_txt}." if gap_txt else \
        f"{sym} at {fmt(px)} is {side_txt}{vol_txt}."
    if r.get("rvol") is not None and r["rvol"] < 0.8:
        r["cautions"].append("Light volume for this time of day: breakouts tend to follow through less [Weak].")
    if used is not None and used >= 1.0:
        r["cautions"].append(f"The day has already moved {used:.1f}x its normal range: late to chase a breakout.")
    if r.get("gap_atr") is not None and abs(r["gap_atr"]) >= 1:
        r["cautions"].append("Big opening gap: wider swings than usual; trade smaller.")
    if r.get("twap"):
        r["cautions"].append("No volume in this data: VWAP is a time-weighted average and relative volume is unknown.")
    late = r["phase"] in ("last half-hour", "closed")
    if r["phase"] == "closed":
        r["action"] = {"label": "Session closed", "in_trade": "Day trades should be flat; anything held is now an overnight position with gap risk.",
                       "flat": f"Plan tomorrow from today's high {fmt(r['hod'])}, low {fmt(r['lod'])} and close {fmt(px)}."}
        r["day_type"] = r["day_type"].replace(" (so far)", "")
        r["bottom_line"] = (f"{sym} closed the session at {fmt(px)}, a {r['day_type']}; "
                            f"day range {fmt(r['lod'])}-{fmt(r['hod'])}.")
        return r
    if late:
        fh = r.get("first_half_hour")
        lean = (f" The first half-hour was {'up' if fh > 0 else 'down'} {abs(fh):.2%}; the intraday-momentum rule "
                f"(Gao et al.: documented on SPY, small, untested on single stocks) leans {'long' if fh > 0 else 'short'} into the close.") if fh else ""
        r["action"] = {"label": "Late day: manage, don't start breakouts",
                       "in_trade": "Tighten stops to the last swing or VWAP and be flat by the close.",
                       "flat": "No new breakout trades this late." + lean}
        return r
    if bias == "long":
        entry, etype = px, "market/limit near"
        stop = lo
    elif bias == "short":
        entry, etype = px, "market/limit near"
        stop = hi
    else:
        up_ok = px <= hi
        r["action"] = {"label": "Stand aside: inside the range" if bias == "inside" else "Mixed: wait for price and VWAP to agree",
                       "in_trade": "Keep the stop where your plan put it; chop eats tight stops.",
                       "flat": (f"Buy-stop above {fmt(hi)} only if it's also above VWAP; sell-stop below {fmt(lo)} only if also below VWAP."
                                if up_ok else "Wait for a break that VWAP agrees with.")}
        return r
    d = 1 if bias == "long" else -1
    risk_ps = abs(entry - stop)
    note = f"stop at the other side of the {orp['n']}-minute range"
    if atr_v and risk_ps > 0.5 * atr_v:
        stop = entry - d * 0.1 * atr_v
        risk_ps = abs(entry - stop)
        note = "stop at 10% of the daily ATR (the opening range is too wide for a range stop) [Weak, vendor study]"
    target = entry + d * target_r * risk_ps
    t = {"side": bias, "entry_type": etype, "entry": entry, "stop": stop, "target": target, "target_r": target_r,
         "flatten": hhmm(e - 5), "stop_note": note}
    if equity:
        qty = math.floor(equity * risk / 100 / risk_ps) if risk_ps > 0 else 0
        cap = math.floor(equity * bp / entry) if entry > 0 else qty
        t.update(qty=min(qty, cap), capped=qty > cap, risk_cash=min(qty, cap) * risk_ps, notional=min(qty, cap) * entry)
    r["ticket"] = t
    size = f", {t['qty']:,} shares ({risk}% risk)" if equity else ""
    r["action"] = {"label": "Long bias: buy strength, not dips" if d > 0 else "Short bias: sell weakness, not rips",
                   "in_trade": f"Stop {fmt(stop)} ({note}); take profit near {fmt(target)} ({target_r:g}R); flat by {hhmm(e - 5)}.",
                   "flat": f"{'Buy' if d > 0 else 'Sell short'} near {fmt(entry)} with a bracket: stop {fmt(stop)}, "
                           f"target {fmt(target)}{size}. Skip it if price is back inside the range first."}
    return r


def print_levels(r):
    print(f"\n== {r['symbol'] or 'Session'} {r['date']} ({r['session']}, {r['bar_minutes']}-min bars) -- {r['phase']}, last bar {r['time']} ==")
    print(f"\n  Bottom line: {r['bottom_line']}")
    a = r["action"]
    print(f"  Next best action: {a['label']}\n    If you're in a trade: {a['in_trade']}\n    If you're flat: {a['flat']}")
    for c in r["cautions"]:
        print(f"    caution: {c}")
    rows = [("Price", fmt(r["price"]))]
    if r.get("pdc") is not None:
        rows.append(("Prior day H / L / C", f"{fmt(r['pdh'])} / {fmt(r['pdl'])} / {fmt(r['pdc'])}  ({r['prev_date']})"))
    if r.get("onh") is not None:
        rows.append(("Overnight / pre-mkt H / L", f"{fmt(r['onh'])} / {fmt(r['onl'])}"))
    if r.get("gap") is not None:
        g = f"{r['gap']:+.2%}" + (f" = {r['gap_atr']:+.2f} ATR" if r.get("gap_atr") is not None else "")
        if "gap_filled" in r:
            g += ", filled" if r["gap_filled"] else ", not filled"
        rows.append(("Gap", g))
    if r.get("atr"):
        rows.append(("Daily ATR", f"{fmt(r['atr'])} ({r['atr_days']} sessions)"
                     + (f"; today's range used {r['atr_used']:.0%}" if r.get("atr_used") is not None else "")))
    if r.get("open") is not None:
        rows.append(("Open / high / low", f"{fmt(r['open'])} / {fmt(r['hod'])} / {fmt(r['lod'])}"))
    for o in r.get("ors", []):
        rows.append((f"Opening range {o['n']}m", f"{fmt(o['lo'])} - {fmt(o['hi'])}" + ("" if o["complete"] else f"  (forming until {o['end']})")))
    if r.get("vwap") is not None:
        sd = r["vwap_sd"]
        rows.append(("VWAP" if not r.get("twap") else "TWAP (no volume)",
                     f"{fmt(r['vwap'])}  bands 1sd {fmt(r['vwap'] - sd)}-{fmt(r['vwap'] + sd)}, 2sd {fmt(r['vwap'] - 2 * sd)}-{fmt(r['vwap'] + 2 * sd)}"
                     f"; price {(r['price'] - r['vwap']) / sd if sd else 0:+.1f} sd; {r['vwap_crosses']} crosses"))
    if r.get("rvol") is not None:
        rows.append(("Relative volume", f"{r['rvol']:.2f}x the {r['rvol_days']}-day average to this time"))
    if r.get("round") and r["round"][0] is not None:
        rows.append(("Round numbers", f"{fmt(r['round'][0])} / {fmt(r['round'][1])}"))
    rows.append(("Day type", r.get("day_type", "")))
    out(rows, "Levels")
    t = r.get("ticket")
    if t:
        rows = [("Side", t["side"]), ("Entry", f"{fmt(t['entry'])} ({t['entry_type']})"), ("Stop-loss", f"{fmt(t['stop'])} -- {t['stop_note']}"),
                ("Take-profit", f"{fmt(t['target'])} ({t['target_r']:g}R)"), ("Flatten", f"{t['flatten']} if neither leg fills")]
        if "qty" in t:
            rows += [("Quantity", f"{t['qty']:,}{' (capped by buying power)' if t['capped'] else ''}"),
                     ("Risk / notional", f"{t['risk_cash']:,.0f} / {t['notional']:,.0f}")]
        out(rows, "Bracket ticket (one cancels the other)")
        print("  The published ORB rules held to the close (10R target); a 2R take-profit trades payoff for hit rate -- "
              "test both with `backtest --rule orb --target-r 2|10`.")
    print("\n  Rule-based read on delayed data, not personal advice. Confirm the live price before any order.")


def cmd_levels(a):
    bars = load_bars(a.file)
    try:
        r = levels(bars, parse_session(a.session), a.date, a.ors, a.primary, a.equity, a.risk, a.bp, a.target_r,
                   a.price, a.symbol or os.path.splitext(os.path.basename(a.file))[0].split("_")[0].upper())
    except ValueError as e:
        sys.exit(str(e))
    print_levels(r)


# --------------------------------------------------------------------------- backtests
def _close_trade(tr, d, entry, exit_, risk_ps, cost_bps, day, t_in, t_out, why):
    gross = d * (exit_ / entry - 1)
    net = gross - 2 * cost_bps / 1e4
    rr = (d * (exit_ - entry) - 2 * cost_bps / 1e4 * entry) / risk_ps if risk_ps else None
    tr.append({"day": day, "side": d, "entry": entry, "exit": exit_, "t_in": t_in, "t_out": t_out, "ret": net,
               "R": rr, "risk_ps": risk_ps, "why": why})


def _orb_day(S, s, p, atr_v):
    bars = [b for b in S["bars"] if p["flat"] is None or mod(b[0]) < p["flat"]]
    orb = [b for b in bars if mod(b[0]) < s + p["or"]]
    rest = [b for b in bars if mod(b[0]) >= s + p["or"]]
    if not orb or not rest:
        return [], "no bars"
    hi, lo = max(b[2] for b in orb), min(b[3] for b in orb)
    if p["mode"] == "candle":
        o0, c0 = orb[0][1], orb[-1][4]
        if c0 == o0:
            return [], "doji"
        d = 1 if c0 > o0 else -1
        k0, entry, breakout = 0, rest[0][1], False
    else:
        k0 = next((k for k, b in enumerate(rest) if b[2] >= hi or b[3] <= lo), None)
        if k0 is None:
            return [], "no break"
        b = rest[k0]
        if b[2] >= hi and b[3] <= lo:
            return [], "ambiguous"  # both sides in one bar: can't know which came first
        d = 1 if b[2] >= hi else -1
        entry, breakout = (max(b[1], hi) if d > 0 else min(b[1], lo)), True
    if d < 0 and not p["short"]:
        return [], "short skipped"
    stop = entry - d * p["stop_atr"] * atr_v if p["stop_atr"] and atr_v else (lo if d > 0 else hi)
    risk_ps = abs(entry - stop)
    if risk_ps <= 0:
        return [], "zero risk"
    target = entry + d * p["target_r"] * risk_ps
    tr = []
    for k in range(k0, len(rest)):
        b = rest[k]
        first = k == k0
        if not first:
            if (d > 0 and b[1] <= stop) or (d < 0 and b[1] >= stop):
                _close_trade(tr, d, entry, b[1], risk_ps, p["cost"], S["date"], rest[k0][0], b[0], "stop (gap)")
                return tr, "ok"
            if (d > 0 and b[1] >= target) or (d < 0 and b[1] <= target):
                _close_trade(tr, d, entry, b[1], risk_ps, p["cost"], S["date"], rest[k0][0], b[0], "target (gap)")
                return tr, "ok"
        if (d > 0 and b[3] <= stop) or (d < 0 and b[2] >= stop):  # stop first when both are touched: conservative
            _close_trade(tr, d, entry, stop, risk_ps, p["cost"], S["date"], rest[k0][0], b[0], "stop")
            return tr, "ok"
        if not (first and breakout) and ((d > 0 and b[2] >= target) or (d < 0 and b[3] <= target)):
            _close_trade(tr, d, entry, target, risk_ps, p["cost"], S["date"], rest[k0][0], b[0], "target")
            return tr, "ok"
    _close_trade(tr, d, entry, rest[-1][4], risk_ps, p["cost"], S["date"], rest[k0][0], rest[-1][0], "close")
    return tr, "ok"


def _vwap_day(S, s, p):
    bars = [b for b in S["bars"] if p["flat"] is None or mod(b[0]) < p["flat"]]
    vw, _ = vwap_series(bars)
    tr, pos, entry, t_in = [], 0, None, None
    for k in range(len(bars) - 1):
        want = 1 if bars[k][4] > vw[k][0] else (-1 if p["short"] else 0)
        if want != pos:
            fill, t = bars[k + 1][1], bars[k + 1][0]
            if pos:
                _close_trade(tr, pos, entry, fill, None, p["cost"], S["date"], t_in, t, "flip")
            pos, entry, t_in = want, fill, t
    if pos:
        _close_trade(tr, pos, entry, bars[-1][4], None, p["cost"], S["date"], t_in, bars[-1][0], "close")
    return tr, "ok"


def _imom_day(S, s, e, prev_c, p, bm):
    bars = S["bars"]
    sig = next((b for b in bars if mod(b[0]) + bm >= s + p["signal_min"]), None)
    k_tr = next((k for k, b in enumerate(bars) if mod(b[0]) >= e - p["trade_min"]), None)
    if sig is None or k_tr is None or mod(sig[0]) >= mod(bars[k_tr][0]) or prev_c is None:
        return [], "no bars"
    x = sig[4] / prev_c - 1
    if x == 0 or (x < 0 and not p["short"]):
        return [], "flat signal"
    d = 1 if x > 0 else -1
    tr = []
    _close_trade(tr, d, bars[k_tr][1], bars[-1][4], None, p["cost"], S["date"], bars[k_tr][0], bars[-1][0], "close")
    return tr, "ok"


def _noise_day(S, s, p, prev_c, sigma, bm):
    bars = [b for b in S["bars"] if p["flat"] is None or mod(b[0]) < p["flat"]]
    o = bars[0][1]
    up_base, dn_base = max(o, prev_c), min(o, prev_c)
    vw, _ = vwap_series(bars)
    check = max(p["check"], bm)
    tr, pos, entry, t_in = [], 0, None, None
    for k in range(len(bars) - 1):
        tau = mod(bars[k][0]) - s
        if (tau + bm) % check or tau not in sigma:
            continue
        c, ub, lb = bars[k][4], up_base * (1 + sigma[tau]), dn_base * (1 - sigma[tau])
        want = pos
        if pos == 0:
            want = 1 if c > ub else (-1 if c < lb and p["short"] else 0)
        elif pos > 0 and c < max(ub, vw[k][0]):
            want = -1 if c < lb and p["short"] else 0
        elif pos < 0 and c > min(lb, vw[k][0]):
            want = 1 if c > ub else 0
        if want != pos:
            fill, t = bars[k + 1][1], bars[k + 1][0]
            if pos:
                _close_trade(tr, pos, entry, fill, None, p["cost"], S["date"], t_in, t, "band/VWAP stop")
            pos, entry, t_in = want, fill, t
    if pos:
        _close_trade(tr, pos, entry, bars[-1][4], None, p["cost"], S["date"], t_in, bars[-1][0], "close")
    return tr, "ok"


def run_backtest(bars, sess, rule, p):
    """-> dict(trades, daily[(date, ret)], days, skipped{reason: n}, bench_intraday[], bench_cc[])."""
    s, e = sess
    bm = bar_minutes(bars)
    sessions, _ = split_sessions(bars, sess)
    sessions = [S for S in sessions if len(S["bars"]) >= 3]
    trades, daily, skipped, b_in, b_cc = [], [], {}, [], []
    moves = []  # noise rule: per session {tau: |c/o - 1|}
    for i, S in enumerate(sessions):
        moves.append({mod(b[0]) - s: abs(b[4] / S["o"] - 1) for b in S["bars"]})
        if i == 0:
            continue
        prev_c = sessions[i - 1]["c"]
        atr_v, _ = daily_atr(sessions, i)
        if rule == "orb":
            tr, why = _orb_day(S, s, p, atr_v)
        elif rule == "vwap":
            tr, why = _vwap_day(S, s, p)
        elif rule == "imom":
            tr, why = _imom_day(S, s, e, prev_c, p, bm)
        elif rule == "noise":
            if i < 15:
                continue
            sigma = {}
            for tau in moves[i]:
                xs = [moves[k][tau] for k in range(i - 14, i) if tau in moves[k]]
                if len(xs) >= 10:
                    sigma[tau] = sum(xs) / len(xs)
            tr, why = _noise_day(S, s, p, prev_c, sigma, bm)
        else:
            raise ValueError(rule)
        if why != "ok":
            skipped[why] = skipped.get(why, 0) + 1
        day = 0.0
        for t in tr:
            lev = p["lev"]
            if t["R"] is not None and p["risk"]:
                lev = min(p["max_lev"], p["risk"] / 100 / (t["risk_ps"] / t["entry"]))
            t["eq_ret"] = lev * t["ret"]
            day += t["eq_ret"]
        trades += tr
        daily.append((S["date"], day))
        b_in.append(S["c"] / S["o"] - 1)
        b_cc.append(S["c"] / prev_c - 1)
    return {"trades": trades, "daily": daily, "skipped": skipped, "bench_intraday": b_in, "bench_cc": b_cc,
            "sessions": len(sessions), "bar_minutes": bm}


def _sharpe(xs):
    if len(xs) < 2:
        return 0.0
    sd = statistics.stdev(xs)
    return statistics.mean(xs) / sd * math.sqrt(252) if sd else 0.0


def summarize_bt(res):
    tr, daily = res["trades"], [x for _, x in res["daily"]]
    if not daily:
        return None
    has_r = bool(tr) and all(t["R"] is not None for t in tr)
    unit = [t["R"] for t in tr] if has_r else [t["ret"] for t in tr]
    eq, peak, mdd = 1.0, 1.0, 0.0
    for x in daily:
        eq *= 1 + x
        peak = max(peak, eq)
        mdd = max(mdd, 1 - eq / peak)
    wins = [u for u in unit if u > 0]
    losses = [u for u in unit if u <= 0]
    m = statistics.mean(unit) if unit else 0.0
    sd = statistics.stdev(unit) if len(unit) > 1 else 0.0
    need = math.ceil((Z95 * sd / m) ** 2) if m > 0 and sd > 0 else None
    md = statistics.mean(daily)
    sdd = statistics.stdev(daily) if len(daily) > 1 else 0.0
    return {"days": len(daily), "trades": len(tr), "traded_days": sum(1 for x in daily if x != 0), "has_r": has_r,
            "win": len(wins) / len(unit) if unit else 0.0, "avg_win": statistics.mean(wins) if wins else 0.0,
            "avg_loss": statistics.mean(losses) if losses else 0.0, "exp": m, "sd": sd,
            "pf": sum(wins) / -sum(losses) if losses and sum(losses) < 0 else float("inf"),
            "total": eq - 1, "sharpe": _sharpe(daily), "t": md / (sdd / math.sqrt(len(daily))) if sdd else 0.0,
            "mdd": mdd, "worst_day": min(daily), "need": need, "unit": unit, "daily": daily}


def print_bt(res, rule, p, label=None):
    st = summarize_bt(res)
    if not st:
        sys.exit("no sessions to test")
    u = "R" if st["has_r"] else "%"
    f = (lambda x: f"{x:+.2f}R") if st["has_r"] else (lambda x: f"{x * 100:+.3f}%")
    desc = {"orb": f"{p['or']}-min opening range, mode '{p['mode']}', stop {'%g x ATR' % p['stop_atr'] if p['stop_atr'] else 'other side of the range'}, target {p['target_r']:g}R, else flat at the close",
            "vwap": "long above VWAP" + (" / short below" if p["short"] else "") + ", decided at each bar close, filled at the next open",
            "imom": f"first {-(-p['signal_min'] // res['bar_minutes']) * res['bar_minutes']} min (from prior close) sets the "
                    f"direction for the last {-(-p['trade_min'] // res['bar_minutes']) * res['bar_minutes']} min",
            "noise": f"noise-band breakout checked every {p['check']} min, exit at max(band, VWAP); 14-session sigma"}[rule]
    print(f"\n== Backtest '{rule}'{' -- ' + label if label else ''}: {desc} ==")
    print(f"  {res['sessions']} sessions of {res['bar_minutes']}-min bars; costs {p['cost']:g} bps per side; "
          f"sizing {'risk %g%% to the stop, leverage cap %gx' % (p['risk'], p['max_lev']) if st['has_r'] and p['risk'] else 'leverage %gx' % p['lev']}"
          f"{'; long only' if not p['short'] else ''}")
    rows = [("Days / trades", f"{st['days']} / {st['trades']} (traded on {st['traded_days']} days)"),
            ("Win rate", f"{st['win']:.0%}  avg win {f(st['avg_win'])}, avg loss {f(st['avg_loss'])}"),
            (f"Expectancy per trade ({u})", f"{f(st['exp'])}  profit factor {st['pf']:.2f}"),
            ("Equity: total / max DD / worst day", f"{st['total']:+.1%} / {st['mdd']:.1%} / {st['worst_day']:+.2%}"),
            ("Daily Sharpe (ann.) / t-stat", f"{st['sharpe']:.2f} / {st['t']:.2f}"),
            ("Intraday buy&hold Sharpe (open->close)", f"{_sharpe(res['bench_intraday']):.2f}"),
            ("Buy&hold Sharpe (close->close)", f"{_sharpe(res['bench_cc']):.2f}")]
    if st["need"]:
        verdict = "enough" if st["trades"] >= st["need"] else "NOT enough"
        rows.append(("Trades to show the edge > 0 (95%)", f"about {st['need']:,}; you have {st['trades']:,} -> {verdict}"))
    else:
        rows.append(("Edge", "expectancy <= 0 after costs: no edge in this sample"))
    if res["skipped"]:
        rows.append(("Days without a trade", ", ".join(f"{k} {v}" for k, v in sorted(res["skipped"].items()))))
    out(rows)
    n = len(res["daily"])
    if n >= 40:
        cut = int(n * 0.7)
        halves = []
        for name, part in (("first 70%", res["daily"][:cut]), ("last 30%", res["daily"][cut:])):
            ds = {d for d, _ in part}
            tu = [t["R"] if st["has_r"] else t["ret"] for t in res["trades"] if t["day"] in ds]
            halves.append(f"{name}: {len(tu)} trades, {f(statistics.mean(tu)) if tu else 'n/a'}/trade, "
                          f"Sharpe {_sharpe([x for _, x in part]):.2f}")
        print("  Stability: " + " | ".join(halves))
    return st


def cmd_backtest(a):
    bars = load_bars(a.file)
    sess = parse_session(a.session)
    base = {"or": a.or_min, "mode": a.mode, "target_r": a.target_r, "stop_atr": a.stop_atr, "cost": a.cost_bps,
            "short": not a.long_only, "flat": None, "risk": a.risk, "max_lev": a.max_lev, "lev": a.lev,
            "signal_min": a.signal_min, "trade_min": a.trade_min, "check": a.check}
    if a.flatten:
        base["flat"] = parse_session(a.flatten + "-24:00")[0]
    if a.rule == "gap":
        return gap_study(bars, sess)
    bm = bar_minutes(bars)
    if a.rule == "orb" and (a.or_min < bm or a.or_min % bm):
        sys.exit(f"--or {a.or_min} must be a multiple of the {bm}-minute bar size")
    res = run_backtest(bars, sess, a.rule, base)
    st = print_bt(res, a.rule, base)
    if a.grid and a.rule == "orb":
        grid = [(n, m, t) for n in (5, 15, 30, 60) if n >= bm and n % bm == 0 for m in ("break", "candle") for t in (2.0, 10.0)]
        rows = []
        for n, m, t in grid:
            q = dict(base, **{"or": n, "mode": m, "target_r": t})
            sg = summarize_bt(run_backtest(bars, sess, "orb", q))
            if sg:
                rows.append(((n, m, t), sg))
        print(f"\n  Grid ({len(rows)} variants):  {'OR':>4} {'mode':<7}{'tgt':>5}{'trades':>8}{'win':>6}{'exp R':>8}{'Sharpe':>8}{'maxDD':>8}")
        for (n, m, t), sg in rows:
            print(f"  {'':>12}{n:>4} {m:<7}{t:>5.0f}{sg['trades']:>8}{sg['win']:>6.0%}{sg['exp']:>+8.2f}{sg['sharpe']:>8.2f}{sg['mdd']:>8.1%}")
        srs = [sg["sharpe"] for _, sg in rows]
        best = max(rows, key=lambda r: r[1]["sharpe"])
        sk, ku = moments(best[1]["daily"])[2:4]
        pos = sum(1 for x in srs if x > 0) / len(srs)
        print(f"  {pos:.0%} of variants positive; median Sharpe {statistics.median(srs):.2f}, best {max(srs):.2f} {best[0]}")
        if len(srs) > 1:
            out(sharpe_report(best[1]["sharpe"], best[1]["days"], 252, sk, ku, len(srs) * a.extra_trials,
                              max(statistics.variance(srs), 1e-4)), f"Best variant after {len(srs) * a.extra_trials} trials")
    print("\n  Fills: next-bar opens (orb 'break' fills at the range level or a worse open; stop wins when stop and target"
          "\n  share a bar). Daily costs, borrow and halts are simplified. Yahoo minute bars span ~2 months: a few dozen"
          "\n  sessions cannot prove a day-trading edge -- use hourly bars (2 years) or longer vendor/broker history.")
    return st


def gap_study(bars, sess):
    sessions, _ = split_sessions(bars, sess)
    buckets = [(-9, -1), (-1, -0.5), (-0.5, -0.2), (-0.2, 0.2), (0.2, 0.5), (0.5, 1), (1, 9)]
    stats_ = {bk: [] for bk in buckets}
    for i in range(1, len(sessions)):
        S, pc = sessions[i], sessions[i - 1]["c"]
        atr_v, _ = daily_atr(sessions, i)
        if not atr_v:
            continue
        g = (S["o"] - pc) / atr_v
        bk = next(b for b in buckets if b[0] <= g < b[1])
        filled = S["l"] <= pc if S["o"] > pc else S["h"] >= pc
        stats_[bk].append((filled, S["c"] / S["o"] - 1, math.copysign(1, S["c"] - S["o"]) == math.copysign(1, S["o"] - pc)))
    print(f"\n== Gap study: {len(sessions) - 1} sessions, gap = (open - prior close) / daily ATR ==")
    print(f"  {'gap (ATR)':<14}{'days':>6}{'filled':>8}{'open->close':>13}{'kept going':>12}")
    for bk in buckets:
        xs = stats_[bk]
        if not xs:
            continue
        lab = f"{bk[0]:+g} .. {bk[1]:+g}".replace("-9", "<").replace("+9", ">")
        print(f"  {lab:<14}{len(xs):>6}{sum(x[0] for x in xs) / len(xs):>8.0%}"
              f"{statistics.mean(x[1] for x in xs):>+13.2%}{sum(x[2] for x in xs) / len(xs):>12.0%}")
    print("  filled = touched the prior close during the session; kept going = closed beyond the open in the gap's direction."
          "\n  A descriptive study, not a rule: small buckets are noise, and fills are not trades (no stop, no costs).")


# --------------------------------------------------------------------------- time of day
def cmd_timeofday(a):
    bars = load_bars(a.file)
    s, e = parse_session(a.session)
    bm = bar_minutes(bars)
    sessions, _ = split_sessions(bars, (s, e))
    slots = {}
    for S in sessions:
        tot = S["v"] or 1
        for b in S["bars"]:
            x = slots.setdefault(mod(b[0]), {"v": [], "abs": [], "r": []})
            x["v"].append(b[5] / tot)
            x["abs"].append(abs(b[4] / b[1] - 1))
            x["r"].append(b[4] / b[1] - 1)
    print(f"\n== Time of day: {len(sessions)} sessions of {bm}-min bars ({hhmm(s)}-{hhmm(e)}) ==")
    print(f"  {'bar':<7}{'vol share':>10}{'avg |move|':>12}{'avg move':>10}{'% up':>7}   volume")
    mx = max(statistics.mean(x["v"]) for x in slots.values())
    for m_ in sorted(slots):
        x = slots[m_]
        if len(x["r"]) < max(3, len(sessions) // 3):
            continue
        vs = statistics.mean(x["v"])
        print(f"  {hhmm(m_):<7}{vs:>10.1%}{statistics.mean(x['abs']):>12.3%}{statistics.mean(x['r']):>+10.3%}"
              f"{sum(1 for v in x['r'] if v > 0) / len(x['r']):>7.0%}   {'#' * round(20 * vs / mx)}")
    xs, ys = [], []
    for i in range(1, len(sessions)):
        S, pc = sessions[i], sessions[i - 1]["c"]
        first = next((b for b in S["bars"] if mod(b[0]) + bm >= s + 30), None)
        pre = [b for b in S["bars"] if mod(b[0]) + bm <= e - 30]
        if first and pre and mod(first[0]) < mod(pre[-1][0]):
            xs.append(first[4] / pc - 1)
            ys.append(S["c"] / pre[-1][4] - 1)
    if len(xs) >= 20:
        r = statistics.correlation(xs, ys)
        t = r * math.sqrt((len(xs) - 2) / max(1e-12, 1 - r * r))
        hit = sum(1 for x, y in zip(xs, ys) if x * y > 0) / len(xs)
        w = -(-30 // bm) * bm
        print(f"\n  First {w} min (from prior close) vs last {w} min: corr {r:+.3f}, t {t:.2f}, n {len(xs)}, "
              f"same direction {hit:.0%}.\n  Published: positive on SPY 1993-2013 (Gao et al., R^2 ~1-2%); judge t against ~2, "
              "and remember one market over one window is one draw.")
    print("  Volume and volatility usually form a U: heavy at the open and close, quiet at midday.")


# --------------------------------------------------------------------------- plan
def cmd_plan(a):
    d = 1 if a.entry > a.stop else -1
    risk_ps = abs(a.entry - a.stop)
    if risk_ps <= 0:
        sys.exit("entry and stop must differ")
    target = a.target if a.target is not None else a.entry + d * a.target_r * risk_ps
    if (target - a.entry) * d <= 0:
        sys.exit("target is on the wrong side of the entry")
    tr = abs(target - a.entry) / risk_ps
    risk_cash = a.equity * a.risk / 100
    qty = math.floor(risk_cash / risk_ps)
    cap = math.floor(a.equity * a.bp / a.entry)
    capped = qty > cap
    qty = min(qty, cap)
    if qty <= 0:
        sys.exit("size rounds to zero: the stop is too wide for this risk budget")
    cost_rt = qty * a.entry * 2 * a.cost_bps / 1e4 + 2 * qty * a.fee_share
    cost_r = cost_rt / (qty * risk_ps)
    be = (1 + cost_r) / (tr + 1)
    daily_cash = a.equity * a.daily_loss / 100
    sym = a.symbol or "SYMBOL"
    rows = [("Direction", "long" if d > 0 else "short"),
            ("Quantity", f"{qty:,}{'  (capped by buying power %gx)' % a.bp if capped else ''}"),
            ("Risk to stop", f"{qty * risk_ps:,.2f} = {qty * risk_ps / a.equity:.2%} of equity ({risk_ps:,.4g}/share)"),
            ("Notional", f"{qty * a.entry:,.0f} = {qty * a.entry / a.equity:.2f}x equity"),
            ("Target", f"{target:,.4g} = {tr:.2f}R  (+{qty * abs(target - a.entry):,.0f})"),
            ("Round-trip costs", f"{cost_rt:,.2f} = {cost_r:.2f}R  ({a.cost_bps:g} bps/side + {a.fee_share:g}/share/side)"),
            ("Net at target / at stop", f"{tr - cost_r:+.2f}R / {-1 - cost_r:+.2f}R"),
            ("Breakeven win rate", f"{be:.0%} at this target, after costs"),
            ("Daily loss limit", f"{daily_cash:,.0f} ({a.daily_loss:g}%) = {daily_cash / (qty * risk_ps):.1f} full losses; "
                                 f"max {a.max_trades} trades -> stop for the day at whichever comes first")]
    out(rows, f"Day-trade plan: {sym}")
    if cost_r > 0.15:
        print(f"  WARNING: costs are {cost_r:.0%} of the risk. A tighter stop raises size, not edge; widen the stop or skip.")
    if a.equity < 25000 and a.bp > 1:
        print("  US margin accounts: FINRA replaced the pattern-day-trader rule ($25,000 minimum, 3 day trades per 5 days) "
              "with intraday margin checks from 4 Jun 2026, but brokers may keep the old rule until 20 Oct 2027 -- "
              "ask yours which applies. Intraday buying power then follows normal margin, not a flat 4x.")
    side = "BUY" if d > 0 else "SELL SHORT"
    print(f"\n  Bracket ticket (one cancels the other):\n    {side} {qty:,} {sym} {a.entry_type.upper()} {a.entry:,.4g}"
          f"\n      + STOP-LOSS {a.stop:,.4g}   + TAKE-PROFIT {target:,.4g}   TIF DAY, flatten {a.flatten} if neither fills")
    print(f"  Paper-trade it:  python paperkit.py order {sym} --side {'long' if d > 0 else 'short'} --qty {qty} "
          f"--entry {a.entry_type}:{a.entry:g} --stop {a.stop:g} --target {target:.4g} --flatten {a.flatten}")


# --------------------------------------------------------------------------- journal
def load_journal(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        sys.exit(f"{path}: empty")
    cols = {k.strip().lower(): k for k in rows[0]}

    def get(row, *names):
        for n_ in names:
            if n_ in cols and str(row[cols[n_]]).strip() != "":
                return row[cols[n_]]
        return None
    trades = []
    for row in rows:
        t = get(row, "entry_time", "open_time", "time", "date", "datetime")
        try:
            when = parse_dt(t) if t and len(t.strip()) > 10 else dt.datetime.strptime(t.strip()[:10], "%Y-%m-%d")
        except (ValueError, AttributeError):
            continue
        side = (get(row, "side", "direction") or "long").strip().lower()
        d = -1 if side in ("short", "sell", "s", "-1", "sell_short") else 1
        num = lambda *n_: float(get(row, *n_)) if get(row, *n_) is not None else None  # noqa: E731
        pnl, entry, exit_, qty, fees = num("pnl", "net_pnl", "profit"), num("entry", "entry_price"), \
            num("exit", "exit_price"), num("qty", "quantity", "shares", "size"), num("fees", "commission") or 0.0
        if pnl is None and None not in (entry, exit_, qty):
            pnl = d * (exit_ - entry) * qty - fees
        if pnl is None:
            continue
        r = num("r", "r_multiple")
        risk = num("risk", "risk_cash", "risk$")
        stop = num("stop", "stop_price")
        if r is None and risk:
            r = pnl / risk
        if r is None and stop is not None and None not in (entry, qty) and abs(entry - stop) > 0:
            r = pnl / (abs(entry - stop) * qty)
        et = get(row, "exit_time", "close_time")
        hold = None
        if et and len(et.strip()) > 10:
            try:
                hold = (parse_dt(et) - when).total_seconds() / 60
            except ValueError:
                pass
        trades.append({"when": when, "sym": get(row, "symbol", "ticker") or "", "side": d, "pnl": pnl, "R": r,
                       "setup": (get(row, "setup", "strategy", "tag") or "untagged").strip(), "hold": hold})
    if not trades:
        sys.exit(f"{path}: no usable rows (need a time/date and pnl, or entry/exit/qty)")
    trades.sort(key=lambda x: x["when"])
    return trades


def cmd_journal(a):
    tr = load_journal(a.file)
    use_r = all(t["R"] is not None for t in tr)
    key = "R" if use_r else "pnl"
    f = (lambda x: f"{x:+.2f}R") if use_r else (lambda x: f"{x:+,.0f}")
    vals = [t[key] for t in tr]
    m, sd = statistics.mean(vals), statistics.stdev(vals) if len(vals) > 1 else 0.0
    wins = [v for v in vals if v > 0]
    days = {}
    for t in tr:
        days.setdefault(t["when"].date(), []).append(t)
    day_pnl = {d: sum(x["pnl"] for x in ts) for d, ts in days.items()}
    streak = worst_streak = 0
    for v in vals:
        streak = streak + 1 if v <= 0 else 0
        worst_streak = max(worst_streak, streak)
    need = math.ceil((Z95 * sd / m) ** 2) if m > 0 and sd > 0 else None
    rows = [("Trades / days", f"{len(tr)} over {len(days)} days ({len(tr) / len(days):.1f} per day)"),
            ("Expectancy", f"{f(m)} per trade; win rate {len(wins) / len(vals):.0%}; "
                           f"avg win {f(statistics.mean(wins)) if wins else 'n/a'}, avg loss {f(statistics.mean([v for v in vals if v <= 0])) if len(wins) < len(vals) else 'n/a'}"),
            ("Net P&L", f"{sum(t['pnl'] for t in tr):+,.2f}"),
            ("Green days", f"{sum(1 for v in day_pnl.values() if v > 0) / len(day_pnl):.0%}; best {max(day_pnl.values()):+,.0f}, "
                           f"worst {min(day_pnl.values()):+,.0f}"),
            ("Longest losing streak", f"{worst_streak} trades"),
            ("Sample", f"about {need:,} trades to show this edge > 0 (95%); you have {len(tr)}" if need else
             "expectancy <= 0: no edge yet in this sample")]
    if a.daily_loss:
        br = [d for d, v in day_pnl.items() if v < -a.daily_loss]
        rows.append(("Daily-limit breaches", f"{len(br)} days lost more than {a.daily_loss:,.0f}" + (f" (e.g. {br[0]})" if br else "")))
    out(rows, f"Journal review: {os.path.basename(a.file)}")

    def group(name, keyf, order=None):
        g = {}
        for i, t in enumerate(tr):
            g.setdefault(keyf(i, t), []).append(t[key])
        ks = order or sorted(g, key=lambda k: (str(type(k)), k))
        print(f"\n  By {name}:")
        for k in ks:
            if k in g:
                xs = g[k]
                print(f"    {str(k):<16}{len(xs):>5} trades  {f(statistics.mean(xs)):>9}/trade  win {sum(1 for x in xs if x > 0) / len(xs):>4.0%}"
                      f"  total {f(sum(xs)):>10}")
        return g
    group("entry hour", lambda i, t: f"{t['when'].hour:02d}:00")
    g_setup = group("setup", lambda i, t: t["setup"])
    group("weekday", lambda i, t: t["when"].strftime("%a"), ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    nth = {}
    for t in tr:
        nth[id(t)] = sum(1 for x in days[t["when"].date()] if x["when"] <= t["when"])
    group("trade number of the day", lambda i, t: f"#{min(nth[id(t)], 4)}{'+' if nth[id(t)] >= 4 else ''}")
    group("previous trade", lambda i, t: "first trade" if i == 0 or tr[i - 1]["when"].date() != t["when"].date()
          else ("after a win" if tr[i - 1]["pnl"] > 0 else "after a loss"))
    if all(t["hold"] is not None for t in tr):
        group("holding time", lambda i, t: "<5 min" if t["hold"] < 5 else "5-30 min" if t["hold"] < 30 else
              "30-120 min" if t["hold"] < 120 else ">2 h", ["<5 min", "5-30 min", "30-120 min", ">2 h"])
    leaks = sorted(((k, xs) for k, xs in g_setup.items() if len(xs) >= 5 and statistics.mean(xs) < 0), key=lambda kv: sum(kv[1]))
    if leaks:
        print("\n  Biggest leaks (setups with >= 5 trades and negative expectancy): "
              + "; ".join(f"{k} {f(sum(xs))} over {len(xs)}" for k, xs in leaks[:3]))
    print("\n  Small groups are noise: act on a pattern only when it has dozens of trades and a reason behind it.")


# --------------------------------------------------------------------------- in play
def inplay_row(sym, bars, sess=(570, 960), primary=5):
    s, e = sess
    sessions, pending = split_sessions(bars, sess)
    if len(sessions) < 3:
        return None
    pre_open = pending and pending[-1][0].date() > sessions[-1]["date"]
    i = len(sessions) if pre_open else len(sessions) - 1
    hist = sessions[:i]
    prev = hist[-1]
    atr_v, _ = daily_atr(sessions, i) if i < len(sessions) else daily_atr(sessions + [prev], i)
    adv = statistics.mean(S["v"] for S in hist[-14:])
    if pre_open:
        px, t = pending[-1][4], pending[-1][0]
        lm = mod(t)
        pv = sum(b[5] for b in pending if b[0].date() == t.date())
        hist_pv = [sum(b[5] for b in S["pre"] if b[0].date() == S["date"] and mod(b[0]) <= lm) for S in hist[-14:]]
        hist_pv = [x for x in hist_pv if x > 0]
        rvol = pv / statistics.mean(hist_pv) if hist_pv and pv else None
        r = {"sym": sym, "time": t.strftime("%m-%d %H:%M"), "phase": "pre-market", "price": px, "gap": px / prev["c"] - 1,
             "rvol": rvol, "or": None, "vwap_side": None}
    else:
        S = sessions[-1]
        lm = mod(S["bars"][-1][0])
        rvol, _ = rel_volume(sessions, i, S["bars"], lm)
        px = S["bars"][-1][4]
        orb = opening_range(S["bars"], s, primary)
        vw, _ = vwap_series(S["bars"])
        pos = None
        if orb and orb["complete"]:
            pos = "above" if px > orb["hi"] else "below" if px < orb["lo"] else "inside"
        r = {"sym": sym, "time": S["bars"][-1][0].strftime("%m-%d %H:%M"), "phase": "session", "price": px,
             "gap": S["o"] / prev["c"] - 1, "rvol": rvol, "or": pos, "vwap_side": "above" if px > vw[-1][0] else "below",
             "or_hi": orb["hi"] if orb else None, "or_lo": orb["lo"] if orb else None, "vwap": vw[-1][0]}
    r.update(atr=atr_v, adv=adv, gap_atr=(r["gap"] * prev["c"] / atr_v) if atr_v else None, prev_close=prev["c"])
    r["liquid"] = px > 5 and adv >= 1e6 and (atr_v or 0) >= 0.5
    r["in_play"] = r["liquid"] and (r["rvol"] or 0) >= 1.0
    return r


def cmd_inplay(a):
    import fetch  # noqa: PLC0415
    syms = list(a.symbols or [])
    if a.universe:
        from scanner import UNIVERSES  # noqa: PLC0415
        for u in a.universe:
            syms += UNIVERSES.get(u, [])
    if not syms:
        sys.exit("pass --symbols or --universe")
    rows = []
    for sym in dict.fromkeys(syms):
        try:
            raw, _, _ = fetch.yahoo_bars(sym, "5m", days=a.days, prepost=True)
            r = inplay_row(sym, bars_from_rows(raw), parse_session(a.session), a.primary)
            if r:
                rows.append(r)
        except Exception as e:  # noqa: BLE001
            print(f"  skip {sym}: {e}", file=sys.stderr)
    rows.sort(key=lambda r: -(r["rvol"] or 0))
    print(f"\n== Stocks in play: {sum(r['in_play'] for r in rows)} of {len(rows)} pass (price > 5, avg volume >= 1M, "
          f"ATR >= 0.50, relative volume >= 1) ==")
    print(f"  {'symbol':<9}{'time':<13}{'price':>10}{'gap':>8}{'gap/ATR':>9}{'RVOL':>7}{'ATR':>8}{'avg vol':>9}  {'range':<8}{'VWAP':<7}flag")
    for r in rows:
        print(f"  {r['sym']:<9}{r['time']:<13}{r['price']:>10,.2f}{r['gap']:>+8.1%}{(r['gap_atr'] or 0):>+9.2f}"
              f"{(r['rvol'] or 0):>7.2f}{(r['atr'] or 0):>8.2f}{r['adv'] / 1e6:>8.1f}m  {(r['or'] or '-'):<8}{(r['vwap_side'] or '-'):<7}"
              f"{'IN PLAY' if r['in_play'] else '' if r['liquid'] else 'illiquid'}")
    print("  Filters follow Zarattini-Barbon-Aziz's 'stocks in play' screen [Weak, vendor study]. A screen, not a signal:"
          "\n  confirm the catalyst (news, earnings), then run `levels` on the name. Yahoo data is delayed.")


# --------------------------------------------------------------------------- CLI
def build():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)

    def sess(x):
        x.add_argument("--session", default="09:30-16:00", help="session hours HH:MM-HH:MM, exchange-local (24h: 00:00-24:00)")

    x = s.add_parser("levels", help="the day-trading map + bottom line + bracket ticket")
    x.add_argument("file")
    sess(x)
    x.add_argument("--date", help="YYYY-MM-DD (default: the latest session)")
    x.add_argument("--symbol")
    x.add_argument("--ors", type=int, nargs="+", default=[5, 15, 30], help="opening-range lengths in minutes")
    x.add_argument("--primary", type=int, default=5, help="opening range used for the read (minutes)")
    x.add_argument("--price", type=float, help="override the last price (e.g. a live quote)")
    x.add_argument("--equity", type=float)
    x.add_argument("--risk", type=float, default=0.5, help="%% of equity risked per trade")
    x.add_argument("--bp", type=float, default=4.0, help="buying power multiple (4 = US margin intraday, 1 = cash)")
    x.add_argument("--target-r", type=float, default=2.0)
    x.set_defaults(fn=cmd_levels)

    x = s.add_parser("backtest", help="intraday rule backtest: orb, vwap, imom, noise, gap")
    x.add_argument("file")
    x.add_argument("--rule", choices=["orb", "vwap", "imom", "noise", "gap"], required=True)
    sess(x)
    x.add_argument("--or", dest="or_min", type=int, default=5, help="orb: opening range in minutes")
    x.add_argument("--mode", choices=["break", "candle"], default="break", help="orb: stop orders at the range, or the range's direction")
    x.add_argument("--target-r", type=float, default=10.0, help="orb: take profit at this many R (10 ~ hold to the close)")
    x.add_argument("--stop-atr", type=float, default=0.0, help="orb: stop at this fraction of daily ATR instead of the range (e.g. 0.1)")
    x.add_argument("--signal-min", type=int, default=30, help="imom: signal window after the open (minutes)")
    x.add_argument("--trade-min", type=int, default=30, help="imom: trade window before the close (minutes)")
    x.add_argument("--check", type=int, default=30, help="noise: check interval (minutes)")
    x.add_argument("--flatten", help="HH:MM: no bars at or after this time (default: the session close)")
    x.add_argument("--cost-bps", type=float, default=1.0, help="per side: spread + slippage + fees (liquid ETFs ~1; small caps 5-20)")
    x.add_argument("--risk", type=float, default=1.0, help="orb: %% of equity risked per trade")
    x.add_argument("--max-lev", type=float, default=4.0, help="orb: leverage cap (US intraday margin = 4)")
    x.add_argument("--lev", type=float, default=1.0, help="vwap/imom/noise: leverage")
    x.add_argument("--long-only", action="store_true")
    x.add_argument("--grid", action="store_true", help="orb: also run 5/15/30/60-min x break/candle x 2R/10R and deflate the best")
    x.add_argument("--extra-trials", type=int, default=1, help="multiply the trial count by this (other things you tried)")
    x.set_defaults(fn=cmd_backtest)

    x = s.add_parser("timeofday", help="volume / volatility / return by time of day")
    x.add_argument("file")
    sess(x)
    x.set_defaults(fn=cmd_timeofday)

    x = s.add_parser("plan", help="day-trade plan + bracket ticket from entry and stop")
    x.add_argument("--equity", type=float, required=True)
    x.add_argument("--entry", type=float, required=True)
    x.add_argument("--stop", type=float, required=True)
    x.add_argument("--target", type=float)
    x.add_argument("--target-r", type=float, default=2.0)
    x.add_argument("--risk", type=float, default=0.5, help="%% of equity at risk")
    x.add_argument("--bp", type=float, default=4.0)
    x.add_argument("--cost-bps", type=float, default=1.0)
    x.add_argument("--fee-share", type=float, default=0.0, help="commission per share per side")
    x.add_argument("--daily-loss", type=float, default=1.5, help="daily loss limit, %% of equity")
    x.add_argument("--max-trades", type=int, default=4)
    x.add_argument("--entry-type", choices=["market", "limit", "stop"], default="stop")
    x.add_argument("--flatten", default="15:55")
    x.add_argument("--symbol")
    x.set_defaults(fn=cmd_plan)

    x = s.add_parser("journal", help="day-trading journal review")
    x.add_argument("file", help="CSV: entry_time,symbol,side,entry,exit,qty[,stop|risk|r][,pnl][,setup][,exit_time][,fees]")
    x.add_argument("--daily-loss", type=float, help="flag days that lost more than this (currency)")
    x.set_defaults(fn=cmd_journal)

    x = s.add_parser("inplay", help="stocks-in-play screen (fetches 5-min bars from Yahoo)")
    x.add_argument("--symbols", nargs="+")
    x.add_argument("--universe", nargs="+", help="etf-core sectors megacap ... (from scanner.py)")
    x.add_argument("--days", type=float, default=25, help="lookback for ATR and relative volume")
    x.add_argument("--primary", type=int, default=5)
    sess(x)
    x.set_defaults(fn=cmd_inplay)
    return p


def main(argv=None):
    a = build().parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
