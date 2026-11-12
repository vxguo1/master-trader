#!/usr/bin/env python3
"""eventkit -- event studies and scenario trees for geopolitical / macro shocks.

Companion to tradekit.py / techkit.py / flowkit.py / fetch.py. Standard library only.

Commands
  study       multi-asset event study: returns (or level changes) at several horizons after each
              event, pre-event drift, max drawdown and days-to-trough, days to recover the
              pre-event close, realized-vol change, abnormal returns vs a benchmark, and a
              cross-event summary (mean / median / % positive / worst / best).
  scenarios   probability-weighted scenario tree -> P&L per scenario for a portfolio, expected
              P&L, dispersion, worst case, P(loss), and the scale factor that caps the worst case.

Asset spec for `study`:  NAME=PATH[@COLUMN][,level]
  PATH    a CSV with a date column (date/time/timestamp) and a value column; fetch.py prices
          output (uses close) and fetch.py fred output (uses the series column) both work.
  @COLUMN pick the value column explicitly.
  ,level  treat as a level series (yields, spreads, VIX, uncertainty indices): report changes in
          points instead of % returns, and max rise / max fall instead of drawdown/recovery.
Examples
  eventkit.py study --assets SPX=spx.csv OIL=wti.csv UST10=dgs10.csv,level VIX=vix.csv,level
      --events-file events.csv --bench SPX
  eventkit.py scenarios --file tree.csv --pos SPX=200000 OIL=-50000 UST10=8000,dv01 --max-loss 15000

Anchoring: the base is the last close strictly BEFORE the event date, so weekend and intraday
events are measured from the prior close (h=1 is the first close after the news). Use --same-day
for events announced after that day's close.
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tradekit import out, pct  # noqa: E402

DATE_COLS = ("date", "time", "timestamp", "observation_date", "datetime", "day")
VALUE_PREF = ("adj close", "adj_close", "adjclose", "close", "value", "price", "level")


# --------------------------------------------------------------------------- loading
def _num(s):
    try:
        x = float(s)
        return x if math.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def parse_asset(spec: str):
    if "=" not in spec:
        sys.exit(f"asset spec '{spec}' must be NAME=PATH[@COLUMN][,level]")
    name, rest = spec.split("=", 1)
    level = False
    if rest.lower().endswith(",level"):
        rest, level = rest[:-6], True
    col = None
    if "@" in rest:
        rest, col = rest.rsplit("@", 1)
    return name.strip(), rest.strip(), col, level


def load_series(path: str, col: str | None):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        r = csv.DictReader(fh)
        fields = r.fieldnames or []
        low = {f.strip().lower(): f for f in fields}
        dcol = next((low[d] for d in DATE_COLS if d in low), fields[0] if fields else None)
        rows = list(r)
    if col:
        vcol = low.get(col.strip().lower())
        if not vcol:
            sys.exit(f"{path}: no column '{col}'; columns: {fields}")
    else:
        vcol = next((low[p] for p in VALUE_PREF if p in low), None)
        if not vcol:
            numeric = [f for f in fields if f != dcol and rows and _num(rows[0].get(f)) is not None]
            if len(numeric) != 1:
                sys.exit(f"{path}: can't tell which column to use ({numeric}); write NAME=PATH@COLUMN")
            vcol = numeric[0]
    dates, vals = [], []
    for row in rows:
        v = _num(row.get(vcol))
        d = (row.get(dcol) or "").strip()[:10]
        if v is not None and d:
            dates.append(d)
            vals.append(v)
    order = sorted(range(len(dates)), key=lambda i: dates[i])
    return [dates[i] for i in order], [vals[i] for i in order]


def load_events(a):
    ev = []
    for e in a.events or []:
        d, _, label = e.partition("=")
        ev.append((d.strip(), label.strip() or d.strip(), ""))
    if a.events_file:
        with open(a.events_file, newline="", encoding="utf-8-sig") as fh:
            for row in csv.DictReader(fh):
                low = {k.strip().lower(): v for k, v in row.items() if k}
                d = (low.get("date") or "").strip()
                if not d:
                    continue
                typ = (low.get("type") or "").strip()
                if a.type and typ.lower() not in [t.lower() for t in a.type]:
                    continue
                ev.append((d[:10], (low.get("label") or low.get("event") or d).strip(), typ))
    if not ev:
        sys.exit("no events: pass --events DATE[=LABEL] ... and/or --events-file CSV (date,label[,type])")
    return sorted(ev)


# --------------------------------------------------------------------------- study
def anchor_index(dates, d, same_day):
    lo, hi = 0, len(dates)
    while lo < hi:  # first index with date >= d
        mid = (lo + hi) // 2
        if dates[mid] < d:
            lo = mid + 1
        else:
            hi = mid
    if same_day and lo < len(dates) and dates[lo] == d:
        return lo
    return lo - 1  # last close strictly before the event


def event_metrics(dates, vals, i0, horizons, pre, ddw, recmax, level):
    n = len(vals)
    base = vals[i0]
    m = {"anchor": dates[i0]}
    f = (lambda j: vals[j] - base) if level else (lambda j: vals[j] / base - 1)
    m["pre"] = (base - vals[i0 - pre] if level else base / vals[i0 - pre] - 1) if i0 - pre >= 0 else None
    for h in horizons:
        m[h] = f(i0 + h) if i0 + h < n else None
    end = min(n - 1, i0 + ddw)
    window = vals[i0 + 1:end + 1]
    if not window:
        return m
    if level:
        m["max_rise"] = max(window) - base
        m["max_fall"] = min(window) - base
    else:
        jt = min(range(i0 + 1, end + 1), key=lambda j: vals[j])
        m["max_dd"] = min(0.0, vals[jt] / base - 1)
        m["days_to_trough"] = jt - i0 if vals[jt] < base else 0
        rec = None
        if vals[jt] < base:
            for j in range(jt, min(n, i0 + recmax + 1)):
                if vals[j] >= base:
                    rec = j - i0
                    break
            m["recover"] = rec if rec is not None else (f">{recmax}" if i0 + recmax < n else "not yet")
        else:
            m["recover"] = 0
        lr = lambda a_, b_: [math.log(vals[k] / vals[k - 1]) for k in range(a_, b_) if vals[k - 1] > 0 and vals[k] > 0]
        before, after = lr(max(1, i0 - 20), i0 + 1), lr(i0 + 1, min(n, i0 + 22))
        if len(before) > 5 and len(after) > 5:
            m["vol_pre"] = statistics.stdev(before) * math.sqrt(252)
            m["vol_post"] = statistics.stdev(after) * math.sqrt(252)
    return m


def fmt(v, level, kind="ret"):
    if v is None:
        return "n/a"
    if isinstance(v, str):
        return v
    if kind == "days":
        return f"{v:d}" if isinstance(v, int) else str(v)
    return f"{v:+.2f}" if level else f"{v * 100:+.1f}%"


def cmd_study(a):
    events = load_events(a)
    assets = []
    for spec in a.assets:
        name, path, col, level = parse_asset(spec)
        dates, vals = load_series(path, col)
        if len(vals) < 30:
            sys.exit(f"{name}: only {len(vals)} rows in {path}")
        assets.append((name, dates, vals, level))
    if a.align:  # put every series on one trading calendar (forward-fill) so "5d" means 5 bars of the reference
        ref = next((x for x in assets if x[0] == a.align), None)
        if not ref:
            sys.exit(f"--align {a.align} is not one of the asset names")
        rdates = ref[1]
        aligned = []
        for name, dates, vals, level in assets:
            if name == a.align:
                aligned.append((name, dates, vals, level))
                continue
            nd, nv, j, last_v = [], [], 0, None
            for d in rdates:
                while j < len(dates) and dates[j] <= d:
                    last_v = vals[j]
                    j += 1
                if last_v is not None:
                    nd.append(d)
                    nv.append(last_v)
            aligned.append((name, nd, nv, level))
        assets = aligned
    H = sorted(set(a.horizons))
    results = {}  # (asset, event_date) -> metrics
    for name, dates, vals, level in assets:
        for d, label, typ in events:
            i0 = anchor_index(dates, d, a.same_day)
            if i0 < 0 or i0 >= len(vals) - 1:
                continue
            results[(name, d)] = event_metrics(dates, vals, i0, H, a.pre, a.dd_window, a.recover_max, level)
    bench = next((x for x in assets if x[0] == a.bench), None) if a.bench else None
    if a.bench and not bench:
        sys.exit(f"--bench {a.bench} is not one of the asset names")
    if bench and bench[3]:
        sys.exit("--bench must be a price asset, not a level series")

    for name, dates, vals, level in assets:
        print(f"\n== {name}  ({'level change, points' if level else 'return'}; base = prior close"
              f"{' or same-day close' if a.same_day else ''}) ==")
        hdr = f"  {'event':<34}{'date':<12}{'pre' + str(a.pre):>8}" + "".join(f"{str(h) + 'd':>8}" for h in H)
        hdr += f"{'maxRise':>9}{'maxFall':>9}" if level else f"{'maxDD':>8}{'trough':>7}{'recover':>8}{'vol pre>post':>15}"
        print(hdr)
        for d, label, typ in events:
            m = results.get((name, d))
            if not m:
                print(f"  {label[:33]:<34}{d:<12}  (no data)")
                continue
            line = f"  {label[:33]:<34}{d:<12}{fmt(m.get('pre'), level):>8}" + "".join(f"{fmt(m.get(h), level):>8}" for h in H)
            if level:
                line += f"{fmt(m.get('max_rise'), level):>9}{fmt(m.get('max_fall'), level):>9}"
            else:
                vp = (f"{m['vol_pre'] * 100:.0f}%>{m['vol_post'] * 100:.0f}%" if "vol_pre" in m else "n/a")
                line += f"{fmt(m.get('max_dd'), level):>8}{fmt(m.get('days_to_trough'), level, 'days'):>7}" \
                        f"{fmt(m.get('recover'), level, 'days'):>8}{vp:>15}"
            print(line)
        # summary
        print(f"  {'-' * 30}")
        for stat in ("mean", "median", "% > 0", "worst", "best", "n"):
            line = f"  {stat:<46}"
            for key in ["pre"] + H:
                xs = [results[(name, d)][key] for d, _, _ in events
                      if (name, d) in results and isinstance(results[(name, d)].get(key), (int, float))]
                if not xs:
                    line += f"{'n/a':>8}"
                    continue
                v = {"mean": statistics.mean(xs), "median": statistics.median(xs),
                     "% > 0": sum(x > 0 for x in xs) / len(xs), "worst": min(xs), "best": max(xs), "n": len(xs)}[stat]
                if stat == "% > 0":
                    line += f"{v:>8.0%}"
                elif stat == "n":
                    line += f"{v:>8d}"
                else:
                    line += f"{fmt(v, level):>8}"
            if not level and stat == "median":
                dds = [results[(name, d)]["max_dd"] for d, _, _ in events if "max_dd" in results.get((name, d), {})]
                recs = [results[(name, d)]["recover"] for d, _, _ in events
                        if isinstance(results.get((name, d), {}).get("recover"), int)]
                if dds:
                    line += f"{fmt(statistics.median(dds), level):>8}"
                if recs:
                    line += f"{'':>7}{int(statistics.median(recs)):>8}"
            print(line)
        if bench and name != bench[0] and not level:
            line = f"  {'median excess vs ' + bench[0]:<46}{'':>8}"
            for h in H:
                xs = [results[(name, d)][h] - results[(bench[0], d)][h] for d, _, _ in events
                      if (name, d) in results and (bench[0], d) in results
                      and results[(name, d)].get(h) is not None and results[(bench[0], d)].get(h) is not None]
                line += f"{fmt(statistics.median(xs), False) if xs else 'n/a':>8}"
            print(line)
    print("\n  Read: small samples (each event is one draw); medians beat means here. Check whether the shock")
    print("  changed the regime (inflation, policy, supply) -- dip-buying base rates fail when it does.")
    if a.out:
        with open(a.out, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["asset", "event_date", "label", "type", "anchor", "metric", "value"])
            for name, *_ in assets:
                for d, label, typ in events:
                    m = results.get((name, d))
                    if not m:
                        continue
                    for k, v in m.items():
                        if k != "anchor":
                            w.writerow([name, d, label, typ, m["anchor"], k if isinstance(k, str) else f"{k}d", v])
        print(f"  wrote {a.out}")


# --------------------------------------------------------------------------- scenarios
def cmd_scenarios(a):
    with open(a.file, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        sys.exit("empty scenario file")
    cols = list(rows[0].keys())
    low = {c.strip().lower(): c for c in cols}
    sc_col = low.get("scenario") or low.get("name") or cols[0]
    p_col = low.get("prob") or low.get("probability") or low.get("p")
    if not p_col:
        sys.exit("scenario file needs a prob column (0-1 or %)")
    pos = {}
    for spec in a.pos:
        name, _, rest = spec.partition("=")
        dv01 = rest.lower().endswith(",dv01")
        amt = float(rest[:-5] if dv01 else rest)
        pos[name.strip()] = (amt, dv01)
    missing = [n for n in pos if n not in cols]
    if missing:
        sys.exit(f"positions {missing} have no column in {a.file}; columns: {cols}")
    probs = [float(r[p_col]) for r in rows]
    if max(probs) > 1:
        probs = [p / 100 for p in probs]
    tot = sum(probs)
    if abs(tot - 1) > 0.01:
        print(f"  note: probabilities sum to {tot:.3f}; normalising to 1")
        probs = [p / tot for p in probs]
    names = list(pos)
    print(f"\n== Scenario P&L  (price assets: amount x move%; ,dv01 assets: -DV01 x move in bp) ==")
    print(f"  {'scenario':<28}{'prob':>6}" + "".join(f"{n:>12}" for n in names) + f"{'total':>13}")
    pnl = []
    for r, p in zip(rows, probs):
        parts = []
        for n in names:
            amt, dv01 = pos[n]
            mv = float(r[n] or 0)
            parts.append(-amt * mv if dv01 else amt * mv / 100)
        t = sum(parts)
        pnl.append(t)
        print(f"  {str(r[sc_col])[:27]:<28}{p:>6.0%}" + "".join(f"{x:>12,.0f}" for x in parts) + f"{t:>13,.0f}")
    ev = sum(p * x for p, x in zip(probs, pnl))
    sd = math.sqrt(sum(p * (x - ev) ** 2 for p, x in zip(probs, pnl)))
    worst = min(pnl)
    rows_out = [
        ("Expected P&L", f"{ev:,.0f}"),
        ("Prob-weighted std dev", f"{sd:,.0f}"),
        ("Worst scenario", f"{worst:,.0f}  ({rows[pnl.index(worst)][sc_col]})"),
        ("Best scenario", f"{max(pnl):,.0f}"),
        ("P(loss)", pct(sum(p for p, x in zip(probs, pnl) if x < 0), 0)),
        ("Expected loss given loss", f"{(sum(p * x for p, x in zip(probs, pnl) if x < 0) / max(1e-12, sum(p for p, x in zip(probs, pnl) if x < 0))):,.0f}"
                                     if any(x < 0 for x in pnl) else "n/a"),
    ]
    if a.max_loss and worst < 0:
        k = min(1.0, a.max_loss / -worst)
        rows_out.append(("Scale to cap worst case", f"x{k:.2f} of current sizes keeps the worst scenario at -{a.max_loss:,.0f}"))
    rows_out.append(("Read", "probabilities are judgments -- vary them +/-10pts and check the decision survives"))
    out(rows_out, "Summary")


# --------------------------------------------------------------------------- CLI
def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("study", help="multi-asset event study")
    x.add_argument("--assets", nargs="+", required=True, help="NAME=PATH[@COLUMN][,level] ...")
    x.add_argument("--events", nargs="*", help="DATE[=LABEL] ...")
    x.add_argument("--events-file", help="CSV with date,label[,type]")
    x.add_argument("--type", nargs="*", help="only events of these types (events-file type column)")
    x.add_argument("--horizons", type=int, nargs="+", default=[1, 5, 21, 63], help="trading days after the event")
    x.add_argument("--pre", type=int, default=5, help="pre-event drift window (trading days)")
    x.add_argument("--dd-window", type=int, default=63, help="window for max drawdown / max rise-fall")
    x.add_argument("--recover-max", type=int, default=504, help="max trading days to look for recovery")
    x.add_argument("--bench", help="asset NAME to compute excess returns against")
    x.add_argument("--same-day", action="store_true", help="anchor at the event date's close (after-close news)")
    x.add_argument("--align", help="asset NAME whose trading calendar all series are forward-filled onto "
                                   "(use for sparse series, e.g. FRED oil spot before 2006)")
    x.add_argument("--out", help="write long-format results CSV")
    x.set_defaults(fn=cmd_study)
    x = s.add_parser("scenarios", help="scenario-tree P&L")
    x.add_argument("--file", required=True, help="CSV: scenario,prob,<ASSET moves...> (%% for prices, bp for ,dv01)")
    x.add_argument("--pos", nargs="+", required=True, help="NAME=AMOUNT (notional) or NAME=DV01,dv01")
    x.add_argument("--max-loss", type=float, help="cap for the worst-scenario loss -> suggested scale factor")
    x.set_defaults(fn=cmd_scenarios)
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
