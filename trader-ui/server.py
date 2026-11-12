#!/usr/bin/env python3
"""Trader UI -- a local web app over the master-trader toolkit.

    python server.py            ->  http://127.0.0.1:8765

Binds to localhost only. Data comes from the toolkit (Yahoo daily bars, FRED, SEC EDGAR, Kraken/Coinbase
public trades) and is cached in ./cache. Calculator panels run whitelisted toolkit commands without a shell.
"""
from __future__ import annotations

import csv
import json
import math
import os
import re
import statistics
import subprocess
import sys
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "master-trader" / "scripts"
CACHE = HERE / "cache"
CACHE.mkdir(exist_ok=True)
sys.path.insert(0, str(SCRIPTS))

import daykit  # noqa: E402
import equitykit  # noqa: E402
import eventkit  # noqa: E402
import fetch  # noqa: E402
import flowkit  # noqa: E402
import paperkit  # noqa: E402
import scanner  # noqa: E402
import techkit  # noqa: E402
import tradekit  # noqa: E402

PORT = int(os.environ.get("TRADER_UI_PORT", "8765"))
_mem, _lock = {}, threading.Lock()
DATA = HERE / "data"
DATA.mkdir(exist_ok=True)
PAPER = DATA / "paper_book.json"
_paper_lock = threading.Lock()


def cached(key, ttl, fn):
    with _lock:
        hit = _mem.get(key)
        if hit and time.time() - hit[0] < ttl:
            return hit[1]
    val = fn()
    with _lock:
        _mem[key] = (time.time(), val)
    return val


def clean(x):
    """JSON-safe: NaN/inf -> None, tuples -> lists."""
    if isinstance(x, float):
        return x if math.isfinite(x) else None
    if isinstance(x, dict):
        return {k: clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    return x


def run_script(script, args, timeout=180):
    r = subprocess.run([sys.executable, str(SCRIPTS / script), *args], capture_output=True, text=True,
                       timeout=timeout, cwd=str(CACHE), encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    return (r.stdout + ("\n" + r.stderr if r.returncode else "")).strip()


# --------------------------------------------------------------------------- data
def safe_name(sym):
    return re.sub(r"[^A-Za-z0-9_.-]", "_", sym)


def bars(symbol, years=3):
    """Adjusted daily OHLCV (today's in-progress bar dropped), cached 15 min and written to cache/<sym>.csv."""
    def load():
        try:
            rows = fetch.yahoo_history(symbol, years)
        except HTTPError as e:
            if e.code == 404:
                raise ValueError(f"No Yahoo data for '{symbol}'. Check the symbol (Yahoo style: BTC-USD, ES=F, "
                                 "EURUSD=X, BRK-B).") from e
            raise
        if not rows:
            raise ValueError(f"Yahoo returned no bars for '{symbol}'.")
        if len(rows[-1]) > 7:
            rows.pop()
        out = {"date": [], "open": [], "high": [], "low": [], "close": [], "volume": []}
        for r in rows:
            f = r[6] / r[4] if r[4] else 1.0
            for k, v in zip(("date", "open", "high", "low", "close", "volume"),
                            (r[0], r[1] * f, r[2] * f, r[3] * f, r[6], int(r[5]))):
                out[k].append(v)
        path = CACHE / f"{safe_name(symbol)}_{years}y.csv"
        with open(path, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(list(out))
            w.writerows(zip(*out.values()))
        out["path"] = str(path)
        return out
    return cached(("bars", symbol, years), 900, load)


def chart_bars(sym, interval, rng, years):
    """Bars for the Charts tab with the in-progress bar kept (fetch.yahoo_bars): hourly cached 60 s, daily 5 min."""
    key, ttl = (("chart", sym, "1h", rng), 60) if interval == "1h" else (("chart", sym, "1d", years), 300)
    return cached(key, ttl, lambda: fetch.yahoo_bars(sym, interval, years=years, rng=rng))


def api_prices(q):
    sym = q.get("symbol", "SPY").strip().upper()
    interval = "1h" if q.get("interval") == "1h" else "1d"
    rng = q.get("range") if q.get("range") in fetch.INTRADAY_RANGES else "1mo"
    years = max(0.25, min(30.0, float(q.get("years", 2))))
    rows, partial, meta = chart_bars(sym, interval, rng, years)
    cols = list(zip(*rows))
    c, h, l = list(cols[5]), list(cols[3]), list(cols[4])
    mid, sd = techkit.sma(c, 20), techkit.rolling_std(c, 20)
    done = rows[:-1] if partial else rows  # indicator text uses completed bars only
    text = "need 60+ completed bars for the indicator summary"
    if len(done) >= 60:
        path = CACHE / f"chart_{safe_name(sym)}_{interval}.csv"
        with open(path, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["date", "open", "high", "low", "close", "volume"])
            w.writerows(r[1:] for r in done)
        span_years = max((done[-1][0] - done[0][0]) / (365.25 * 86400), 1 / 365)
        text = run_script("techkit.py", ["indicators", str(path), "--ppy", str(round(len(done) / span_years))])
    return {"symbol": sym, "interval": interval, "range": rng if interval == "1h" else f"{years:g}y",
            "date": list(cols[1]), "open": list(cols[2]), "high": h, "low": l, "close": c, "volume": list(cols[6]),
            "partial": partial, "tz": meta.get("exchangeTimezoneShortName") or meta.get("timezone"),
            "sma20": mid, "sma50": techkit.sma(c, 50), "sma200": techkit.sma(c, 200),
            "bb_up": [m + 2 * s if m is not None else None for m, s in zip(mid, sd)],
            "bb_lo": [m - 2 * s if m is not None else None for m, s in zip(mid, sd)],
            "rsi14": techkit.rsi(c, 14), "atr14": techkit.atr(h, l, c, 14), "text": text}


def api_quote(q):
    sym = q.get("symbol", "SPY").strip().upper()
    qt = cached(("quote", sym), 15, lambda: fetch.quote(sym))
    return {**qt, "age_s": time.time() - qt["ts"] if qt.get("ts") else None}  # age as of now, not as of the cache


def api_summary(q):
    """Plain-English bottom line + rule-based next best action (techkit.summarize) from 3y of daily bars + live price."""
    sym = q.get("symbol", "SPY").strip().upper()
    rows, _, _ = chart_bars(sym, "1d", None, 3.0)
    try:
        qt = api_quote({"symbol": sym})
    except Exception:  # noqa: BLE001 -- the summary still works from daily closes
        qt = None
    return techkit.summarize(sym, [r[1] for r in rows], [r[3] for r in rows], [r[4] for r in rows],
                             [r[5] for r in rows], qt)


def api_macro(q):
    def load():
        m = fetch.macro_data(fetch.fred_key())
        sections = []
        for name, rows in fetch.DASH:
            out = []
            for sid, label, kind in rows:
                obs = m["data"].get(sid)
                if not obs:
                    out.append({"id": sid, "label": label, "error": m["errors"].get(sid, "no data")})
                    continue
                tail = obs[-260:]
                out.append({"id": sid, "label": label, "last": obs[-1][1], "date": obs[-1][0],
                            "chg1m": fetch.change(obs, 30), "chg3m": fetch.change(obs, 91), "chg1y": fetch.change(obs, 365),
                            "spark_d": [d for d, _ in tail], "spark_v": [v for _, v in tail]})
            sections.append({"name": name, "rows": out})
        return {"sections": sections, "flags": m["flags"], "plain": m.get("plain")}
    return cached("macro", 1800, load)


def api_regime(q):
    uni = [u for u in q.get("universe", "etf-core,sectors").split(",") if u]
    ns = scan_ns(uni)
    data = cached(("universe", tuple(uni)), 3600, lambda: scanner.load_universe(ns))
    r = scanner.regime_read(data, "SPY" if "SPY" in data else None)
    return {k: v for k, v in r.items() if k != "feats"} | {"n": len(r["feats"])}


def scan_ns(universe, **kw):
    from types import SimpleNamespace
    base = dict(files=[], universe=universe, symbols=None, symbols_file=None, fetch=True, years=3,
                data_dir=str(CACHE / "scan"), bench="SPY", equity=100000.0, risk=0.5, max_weight=0.25,
                min_price=5.0, min_adv=20e6, top=25, cluster_corr=0.7)
    base.update(kw)
    return SimpleNamespace(**base)


def api_scan(q):
    uni = [u for u in q.get("universe", "etf-core,sectors").split(",") if u]
    syms = [s.strip().upper() for s in q.get("symbols", "").split(",") if s.strip()]
    ns = scan_ns(uni if not syms else None, symbols=syms or None,
                 equity=float(q.get("equity", 100000)), risk=float(q.get("risk", 0.5)), top=int(q.get("top", 25)))
    data = cached(("universe", tuple(uni), tuple(syms)), 3600, lambda: scanner.load_universe(ns))
    r = scanner.scan(data, ns)
    reg = {k: v for k, v in r["reg"].items() if k != "feats"}
    ranked = [{k: v for k, v in x.items() if k != "rets"} | {"cluster": r["clusters"][x["sym"]]} for x in r["ranked"]]
    puts = []
    if q.get("puts") == "1":
        budget = ns.equity * ns.risk / 100 * reg["tilt"]["short"]
        for x in r["shorts"][:int(q.get("put_top", 5))]:
            try:
                pp = cached(("puts", x["sym"], round(x["entry"], 2)), 600,
                            lambda x=x: scanner.put_plan(x["sym"], x["entry"], x["stop"], x["target"], budget, 35))
            except Exception as e:  # noqa: BLE001 -- futures, FX and crypto have no listed chain on Yahoo
                pp = {"error": str(e)}
            puts.append({k: v for k, v in x.items() if k != "rets"} | {"puts": pp, "budget": budget})
    return {"regime": reg, "ranked": ranked, "skipped": r["skipped"], "n": len(r["feats"]), "puts": puts}


# --------------------------------------------------------------------------- day trading
def day_rows(sym, interval, days):
    return cached(("day", sym, interval, days), 30, lambda: fetch.yahoo_bars(sym, interval, days=days, prepost=True))


def api_day(q):
    """Intraday map for one symbol: daykit.levels + the last two sessions (with extended hours) for the chart."""
    sym = q.get("symbol", "SPY").strip().upper()
    interval = q.get("interval", "5m") if q.get("interval") in ("1m", "2m", "5m", "15m") else "5m"
    sess = daykit.parse_session(q.get("session", "09:30-16:00"))
    rows, partial, meta = day_rows(sym, interval, 7 if interval == "1m" else 30)
    done = rows[:-1] if partial and len(rows) > 1 else rows
    bars = daykit.bars_from_rows(done)
    eq = float(q["equity"]) if q.get("equity") else None
    lv = daykit.levels(bars, sess, None, (5, 15, 30), int(q.get("primary", 5)), eq, float(q.get("risk", 0.5)),
                       float(q.get("bp", 4)), float(q.get("target_r", 2)), None, sym)
    sessions, _ = daykit.split_sessions(bars, sess)
    start = sessions[-2]["bars"][0][0] if len(sessions) >= 2 else bars[0][0]
    if lv["phase"] == "pre-open" and sessions:
        start = sessions[-1]["bars"][0][0]
    show = [r for r in rows if r[1] >= start.strftime("%Y-%m-%d %H:%M")]

    def is_ext(r):
        m = int(r[1][11:13]) * 60 + int(r[1][14:16])
        return not sess[0] <= m < sess[1]
    ext = [r for r in show if is_ext(r)]
    if ext and lv.get("atr"):  # thin off-hours bad prints (same rule the levels use) would squash the price axis
        med, tol = statistics.median(r[5] for r in ext), 1.5 * lv["atr"]
        show = [r for r in show if not (is_ext(r) and (r[3] > med + tol or r[4] < med - tol))]
    today = [b for b in bars if b[0].date().isoformat() == lv["date"] and sess[0] <= daykit.mod(b[0]) < sess[1]]
    vw, _ = daykit.vwap_series(today)
    vmap = {b[0].strftime("%Y-%m-%d %H:%M"): v for b, v in zip(today, vw)}
    cols = list(zip(*show))
    x = list(cols[1])
    return {"symbol": sym, "interval": interval, "partial": partial, "tz": meta.get("exchangeTimezoneShortName"),
            "volume_fixed": meta.get("volume_fixed", 0), "levels": lv,
            "chart": {"date": x, "open": cols[2], "high": cols[3], "low": cols[4], "close": cols[5], "volume": cols[6],
                      "vwap": [vmap[d][0] if d in vmap else None for d in x],
                      "sd": [vmap[d][1] if d in vmap else None for d in x],
                      "ext": [not (sess[0] <= int(d[11:13]) * 60 + int(d[14:16]) < sess[1]) for d in x]}}


def api_inplay(q):
    from concurrent.futures import ThreadPoolExecutor
    syms = [s.strip().upper() for s in q.get("symbols", "").split(",") if s.strip()]
    for u in [u for u in q.get("universe", "").split(",") if u]:
        syms += scanner.UNIVERSES.get(u, [])
    syms = list(dict.fromkeys(syms))[:60]
    if not syms:
        raise ValueError("Enter symbols or pick a universe.")

    def one(sym):
        try:
            rows, _, _ = day_rows(sym, "5m", 25)
            return daykit.inplay_row(sym, daykit.bars_from_rows(rows))
        except Exception as e:  # noqa: BLE001
            return {"sym": sym, "error": str(e)}
    with ThreadPoolExecutor(8) as ex:
        res = [r for r in ex.map(one, syms) if r]
    ok = sorted((r for r in res if "error" not in r), key=lambda r: -(r["rvol"] or 0))
    return {"rows": ok, "errors": [r for r in res if "error" in r]}


def api_day_backtest(q):
    import contextlib
    import io
    sym = q.get("symbol", "SPY").strip().upper()
    interval = "1h" if q.get("interval") == "1h" else "5m"
    rule = q.get("rule", "orb")
    if rule not in ("orb", "vwap", "imom", "noise"):
        raise ValueError("rule must be orb, vwap, imom or noise")
    rows = cached(("bt", sym, interval), 600, lambda: fetch.yahoo_bars(sym, interval, days=59, rng="2y")[0])
    bars = daykit.bars_from_rows(rows[:-1])
    p = {"or": int(q.get("or", 5 if interval == "5m" else 60)), "mode": q.get("mode", "break"),
         "target_r": float(q.get("target_r", 10)), "stop_atr": float(q.get("stop_atr", 0) or 0),
         "cost": float(q.get("cost", 1)), "short": q.get("long_only") != "1", "flat": None, "risk": float(q.get("risk", 1)),
         "max_lev": 4.0, "lev": 1.0, "signal_min": 30, "trade_min": 30, "check": 30}
    bm = daykit.bar_minutes(bars)
    if rule == "orb" and (p["or"] < bm or p["or"] % bm):
        p["or"] = bm
    res = daykit.run_backtest(bars, (570, 960), rule, p)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        st = daykit.print_bt(res, rule, p)
    eq, curve = 1.0, []
    for d, r in res["daily"]:
        eq *= 1 + r
        curve.append([d.isoformat(), eq - 1])
    return {"text": buf.getvalue(), "curve": curve, "stats": {k: v for k, v in st.items() if k not in ("unit", "daily")},
            "sessions": res["sessions"], "bar_minutes": res["bar_minutes"]}


def api_smallcap(q):
    from types import SimpleNamespace
    ns = SimpleNamespace(min_change=float(q.get("min_change", 10)), min_rvol=float(q.get("min_rvol", 5)),
                         price=[float(q.get("price_lo", 2)), float(q.get("price_hi", 20))],
                         max_float=float(q.get("max_float", 20)) * 1e6, news_hours=float(q.get("news_hours", 24)),
                         near=q.get("near") == "1", deep=int(q.get("deep", 25)))
    res = cached(("smallcap", repr(sorted(vars(ns).items()))), 120, lambda: scanner.smallcap_screen(ns))
    lead = [r for r in res["rows"] if r["met"] >= 4][:3]
    plans = {}
    eq = float(q.get("equity", 100000))
    for r in lead:
        try:
            rows, partial, _ = day_rows(r["symbol"], "5m", 20)
            lv = daykit.levels(daykit.bars_from_rows(rows[:-1] if partial else rows), (570, 960), equity=eq,
                               risk=float(q.get("risk", 0.25)), symbol=r["symbol"])
            plans[r["symbol"]] = {k: lv.get(k) for k in ("bottom_line", "action", "ticket", "vwap", "hod", "lod", "pdc", "phase", "cautions")}
        except Exception as e:  # noqa: BLE001
            plans[r["symbol"]] = {"error": str(e)}
    return {**res, "plans": plans, "criteria": vars(ns)}


# --------------------------------------------------------------------------- paper portfolio
def _paper(fn):
    with _paper_lock:
        book = paperkit.load_book(str(PAPER)) if PAPER.exists() else None
        out = fn(book)
        if out is not None and "book" in out:
            paperkit.save_book(out["book"], str(PAPER))
            book = out["book"]
        res = {"exists": book is not None}
        if book is not None:
            res |= paperkit.status(book)
        if out:
            res |= {k: v for k, v in out.items() if k != "book"}
        return res


def api_paper(q):
    return _paper(lambda b: None)


def api_paper_init(body):
    eq = float(body.get("equity", 100000))
    if not 1000 <= eq <= 1e9:
        raise ValueError("equity must be between 1,000 and 1,000,000,000")
    return _paper(lambda b: {"book": paperkit.new_book(eq, float(body.get("commission_share", 0)),
                                                       float(body.get("commission_contract", 0.65)),
                                                       float(body.get("slippage_bps", 2)), float(body.get("bp", 4)),
                                                       float(body.get("max_risk", 1)), float(body.get("max_heat", 6)))})


def _need(b):
    if b is None:
        raise ValueError("Start a paper account first.")
    return b


def api_paper_order(body):
    def go(b):
        b = _need(b)
        f = lambda k: float(body[k]) if body.get(k) not in (None, "") else None  # noqa: E731
        right = body.get("right") if body.get("right") in ("put", "call") else None
        o, notes = paperkit.place_order(
            b, str(body["symbol"]).strip().upper(), body.get("side", "long"),
            int(body["qty"]) if body.get("qty") not in (None, "") else None, f("risk_pct"), body.get("entry") or "market",
            f("stop"), f("target"), f("target_r"), body.get("flatten") or None, body.get("tif", "day"),
            str(body.get("setup", ""))[:40], str(body.get("note", ""))[:200], right, f("strike"),
            body.get("expiry") or None, "underlying", f("iv"), force=bool(body.get("force")))
        return {"book": b, "placed": o["id"], "notes": notes}
    return _paper(go)


def api_paper_update(body):
    def go(b):
        b = _need(b)
        return {"book": b, "events": paperkit.update_book(b)}
    return _paper(go)


def api_paper_close(body):
    def go(b):
        b = _need(b)
        return {"book": b, "closed": [t["id"] for t in paperkit.close_position(b, body["ref"])]}
    return _paper(go)


def api_paper_cancel(body):
    def go(b):
        b = _need(b)
        paperkit.cancel_order(b, int(body["id"]))
        return {"book": b}
    return _paper(go)


def api_select(q):
    syms = [s.strip().upper() for s in q.get("symbols", "SPY,QQQ,GLD,TLT").split(",") if s.strip()][:12]
    args = ["select", "--symbols", *syms, "--fetch", "--years", "20", "--data-dir", str(CACHE / "select")]
    if q.get("short") == "1":
        args.append("--short")
    return {"text": cached(("select", tuple(syms), q.get("short")), 21600, lambda: run_script("scanner.py", args, 600))}


def api_stock(q):
    t = q.get("ticker", "NVDA").upper()
    wacc, tg = float(q.get("wacc", 0.10)), float(q.get("tg", 0.03))
    f = cached(("fund", t), 21600, lambda: fetch.fundamentals(t))
    _, _, ed = cached(("edates", t), 21600, lambda: fetch.earnings_dates(t))
    b = bars(t, 7)
    px = list(zip(b["date"], b["open"], b["close"]))
    react = equitykit.earnings_reactions(px, [(d, tm) for d, _, tm, _ in ed])
    rows, last = f["rows"], f["rows"][-1]
    price, shares = b["close"][-1], last.get("shares_diluted")
    fcf = (last.get("fcf_ttm") or 0) - (last.get("sbc_ttm") or 0 if q.get("sbc", "1") == "1" else 0)
    dcf = None
    if shares and fcf > 0:
        target_ev = price * shares - f["net_cash"]
        g = equitykit.implied_growth(fcf, target_ev, tg, wacc, 10)
        grid = {f"{w:.3f}": {f"{gg:.2f}": (equitykit.dcf_value(fcf, gg, tg, w, 10) + f["net_cash"]) / shares
                             for gg in (0.10, 0.15, 0.20, 0.25, 0.30, 0.35)} for w in (wacc - 0.01, wacc, wacc + 0.01)}
        dcf = {"price": price, "shares": shares, "fcf": fcf, "net_cash": f["net_cash"], "wacc": wacc, "tg": tg,
               "implied_growth": g, "mcap": price * shares, "fcf_yield": fcf / (price * shares), "grid": grid}
    moves = [r[3] for r in react]
    stats = {"n": len(moves), "mean_abs": statistics.mean(abs(m) for m in moves) if moves else None,
             "median_abs": statistics.median(abs(m) for m in moves) if moves else None,
             "sd": statistics.pstdev(moves) if len(moves) > 1 else None}
    lv = [x for x in b["close"][-252:]]
    lr = [math.log(lv[i] / lv[i - 1]) for i in range(1, len(lv))]
    return {"ticker": t, "entity": f["entity"], "cik": f["cik"], "rows": rows[-16:], "net_cash": f["net_cash"],
            "price": price, "price_date": b["date"][-1], "realized_vol_1y": statistics.stdev(lr) * math.sqrt(252),
            "reactions": react, "reaction_stats": stats, "dcf": dcf, "next_release_note":
            "Upcoming release dates are not in SEC filings -- confirm on the company's IR calendar."}


def api_projection(body):
    spot, days = float(body["spot"]), float(body.get("days", 90))
    T = days / 365
    iv = float(body["iv"])
    ev = body.get("event_move")
    ev_sd = math.log(1 + float(ev)) if ev else None
    sc = [(s["name"], float(s["prob"]), float(s["price"])) for s in body.get("scenarios", []) if s.get("price")]
    mkt, mine = equitykit.simulate(spot, T, float(body.get("base_iv") or iv), body.get("iv_down") or None,
                                   body.get("iv_up") or None, ev_sd, sc or None, None, 40000, 7)
    lo = min(mkt + (mine or [])) * 0.98
    hi = max(min(max(mkt + (mine or [])), spot * 3), spot * 1.05)
    nb = 60
    w = (hi - lo) / nb

    def hist(xs):
        h = [0] * nb
        for x in xs:
            if lo <= x < hi:
                h[int((x - lo) / w)] += 1
        return [c / len(xs) for c in h]

    qs = [0.05, 0.10, 0.25, 0.5, 0.75, 0.90, 0.95]
    out = {"bins": [lo + (i + 0.5) * w for i in range(nb)], "market": {"hist": hist(mkt), "pct": equitykit.pctiles(mkt, qs),
                                                                     "mean": statistics.mean(mkt)}}
    levels = [float(x) for x in body.get("levels", [])]
    out["market"]["p_above"] = [sum(1 for x in mkt if x > L) / len(mkt) for L in levels]
    if mine:
        out["mine"] = {"hist": hist(mine), "pct": equitykit.pctiles(mine, qs), "mean": statistics.mean(mine),
                       "p_above": [sum(1 for x in mine if x > L) / len(mine) for L in levels]}
    out["levels"] = levels
    return out


def api_payoff(body):
    S, days, vol, r = float(body["spot"]), float(body.get("days", 30)), float(body["vol"]), float(body.get("r", 0.04))
    T = days / 365
    legs = []
    for lg in body["legs"]:
        kind, qty = lg["type"], float(lg["qty"])
        if kind == "stock":
            legs.append({"type": "stock", "qty": qty, "strike": None, "premium": S})
            continue
        K = float(lg["strike"])
        g = tradekit.bs(S, K, T, r, 0.0, vol, kind)
        prem = float(lg["premium"]) if lg.get("premium") not in (None, "") else g["price"]
        legs.append({"type": kind, "qty": qty, "strike": K, "premium": prem,
                     **{k: g[k] for k in ("delta", "gamma", "vega_1pt", "theta_day")}})
    grid = [S * (0.6 + 0.8 * i / 160) for i in range(161)]

    def value(x, t_left):
        tot = 0.0
        for lg in legs:
            if lg["type"] == "stock":
                tot += lg["qty"] * (x - lg["premium"])
            else:
                v = tradekit.bs(x, lg["strike"], t_left, r, 0.0, vol, lg["type"])["price"] if t_left > 0 else \
                    max(0.0, (x - lg["strike"]) if lg["type"] == "call" else (lg["strike"] - x))
                tot += lg["qty"] * 100 * (v - lg["premium"])
        return tot

    greeks = {k: sum(lg.get(k, 0) * lg["qty"] * 100 for lg in legs if lg["type"] != "stock")
              + (sum(lg["qty"] for lg in legs if lg["type"] == "stock") if k == "delta" else 0)
              for k in ("delta", "gamma", "vega_1pt", "theta_day")}
    return {"grid": grid, "expiry": [value(x, 0) for x in grid], "today": [value(x, T) for x in grid],
            "legs": legs, "greeks": greeks, "net_premium": sum(lg["qty"] * 100 * lg["premium"] for lg in legs if lg["type"] != "stock")}


EVENT_ASSETS = {"SPX": ("^GSPC", False), "GOLD": ("GC=F", False), "VIX": ("^VIX", True)}


def api_events(q):
    types = [t for t in q.get("types", "").split(",") if t]

    def files():
        out = {}
        for name, (sym, level) in EVENT_ASSETS.items():
            out[name] = (bars(sym, 37)["path"], level)
        key = fetch.fred_key()
        for name, sid, level in (("WTI", "DCOILWTICO", False), ("UST10", "DGS10", True)):
            path = CACHE / f"fred_{sid}.csv"
            obs = fetch.fred_series(sid, key, "1989-01-01")
            with open(path, "w", newline="") as fh:
                w = csv.writer(fh)
                w.writerow(["date", sid])
                w.writerows(obs)
            out[name] = (str(path), level)
        return out
    fs = cached("event_files", 21600, files)
    lib = str(SCRIPTS.parent / "assets" / "geopolitical_events.csv")
    args = ["study", "--assets"] + [f"{n}={p}{',level' if lv else ''}" for n, (p, lv) in fs.items()] + \
           ["--events-file", lib, "--bench", "SPX", "--align", "SPX"] + (["--type", *types] if types else [])
    text = run_script("eventkit.py", args)
    # per-event SPX/oil/gold rows for charts
    from types import SimpleNamespace
    evs = eventkit.load_events(SimpleNamespace(events=None, events_file=lib, type=types or None))
    series = {n: eventkit.load_series(p, None) for n, (p, _) in fs.items()}
    rows = []
    for d, label, typ in evs:
        row = {"date": d, "label": label, "type": typ}
        for n, (dates, vals) in series.items():
            i0 = eventkit.anchor_index(dates, d, False)
            if 0 <= i0 < len(vals) - 1:
                m = eventkit.event_metrics(dates, vals, i0, [1, 5, 21, 63], 5, 63, 504, fs[n][1])
                row[n] = {k if isinstance(k, str) else f"d{k}": v for k, v in m.items() if k != "anchor"}
        rows.append(row)
    with open(lib, newline="", encoding="utf-8-sig") as fh:
        meta = {r["date"]: r for r in csv.DictReader(fh)}
    for r in rows:
        m = meta.get(r["date"], {})
        r["regime_change"], r["channel"] = m.get("regime_change"), m.get("primary_channel")
    alltypes = sorted({r["type"] for r in meta.values() if r.get("type")})
    return {"text": text, "rows": rows, "types": alltypes}


def api_geo(q):
    def load():
        key = fetch.fred_key()
        out = {}
        for sid in ("USEPUINDXD", "OVXCLS", "VIXCLS", "GVZCLS", "DCOILBRENTEU"):
            obs = fetch.fred_series(sid, key, fetch.days_ago(3 * 365))
            out[sid] = {"d": [d for d, _ in obs], "v": [v for _, v in obs]}
        gpr = CACHE / "gpr_daily.csv"
        if not gpr.exists() or time.time() - gpr.stat().st_mtime > 86400:
            run_script("fetch.py", ["gpr", "--freq", "daily", "--out", str(gpr), "--out-xls", str(CACHE / "gpr_daily.xls")], 300)
        if gpr.exists():
            with open(gpr, newline="") as fh:
                rows = [r for r in csv.DictReader(fh)][-3 * 365:]
            vals = [float(r["GPRD"]) for r in rows]
            ma7 = [statistics.mean(vals[max(0, i - 6):i + 1]) for i in range(len(vals))]
            out["GPR"] = {"d": [r["date"] for r in rows], "v": vals, "ma7": ma7}
        return out
    return cached("geo", 3600, load)


def api_flow(q):
    sym = re.sub(r"[^A-Za-z-]", "", q.get("symbol", "BTC")).upper() or "BTC"
    ex = "kraken" if q.get("exchange") == "kraken" else "coinbase"
    minutes = max(1, min(60, float(q.get("minutes", 10))))
    bar = q.get("bar", "30s") if re.fullmatch(r"\d+[smh]|\d+[tv]", q.get("bar", "30s")) else "30s"
    path = CACHE / f"trades_{sym}_{ex}.csv"
    run_script("fetch.py", ["trades", sym, "--exchange", ex, "--minutes", str(minutes), "--out", str(path)], 240)
    trades, inferred = flowkit.load_trades(str(path))
    bs_ = flowkit.build_bars(trades, bar)
    cvd = 0.0
    out = {"t": [], "o": [], "h": [], "l": [], "c": [], "buy": [], "sell": [], "delta": [], "cvd": []}
    for b in bs_:
        d = b["buy"] - b["sell"]
        cvd += d
        for k, v in (("t", b["t"]), ("o", b["o"]), ("h", b["h"]), ("l", b["l"]), ("c", b["c"]), ("buy", b["buy"]),
                     ("sell", b["sell"]), ("delta", d), ("cvd", cvd)):
            out[k].append(v)
    lo_p, hi_p = min(p for _, p, _, _ in trades), max(p for _, p, _, _ in trades)
    tick = flowkit.nice_tick((hi_p - lo_p) / 40)
    base = math.floor(lo_p / tick) * tick
    nlev = int((hi_p - base) / tick) + 1
    vols = [0.0] * nlev
    for _, p, v, _ in trades:
        vols[min(nlev - 1, int((p - base) / tick))] += v
    poc, va_lo, va_hi = flowkit.value_area(list(range(nlev)), vols)
    vw = sum(p * v for _, p, v, _ in trades) / sum(v for _, _, v, _ in trades)
    out["profile"] = {"price": [base + (i + 0.5) * tick for i in range(nlev)], "vol": vols, "poc": base + (poc + 0.5) * tick,
                      "va_lo": base + va_lo * tick, "va_hi": base + (va_hi + 1) * tick, "vwap": vw}
    out["text"] = run_script("flowkit.py", ["delta", str(path), "--bar", bar, "--show", "6", "--events", "12"])
    out["meta"] = {"symbol": sym, "exchange": ex, "trades": len(trades), "inferred_side": inferred}
    return out


RUN_WHITELIST = {
    "tradekit.py": {"size", "kelly", "expectancy", "ruin", "drawdown", "sharpe", "bs", "iv", "move", "impact"},
    "equitykit.py": {"dcf"},
    "eventkit.py": {"scenarios"},
}
TOKEN = re.compile(r"^[A-Za-z0-9_.,:=+-]{1,40}$")


def api_run(body):
    kit, cmd = body.get("kit"), body.get("cmd")
    if cmd not in RUN_WHITELIST.get(kit, set()):
        raise ValueError(f"not allowed: {kit} {cmd}")
    args = [cmd]
    if kit == "eventkit.py":  # scenario tree arrives as rows -> temp CSV
        tree = CACHE / "ui_tree.csv"
        rows = body["tree"]
        cols = list(rows[0].keys())
        with open(tree, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(cols)
            w.writerows([[r[c] for c in cols] for r in rows])
        args += ["--file", str(tree)]
    for flag, val in (body.get("args") or {}).items():
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9-]{0,30}", flag):  # tradekit bs/iv/move use --S/--K
            raise ValueError(f"bad flag {flag}")
        if val is True:
            args.append(f"--{flag}")
            continue
        if val in (None, "", False):
            continue
        vals = val if isinstance(val, list) else str(val).split()
        if not all(TOKEN.match(str(v)) for v in vals):
            raise ValueError(f"bad value for {flag}")
        args += [f"--{flag}", *map(str, vals)]
    return {"text": run_script(kit, args, 120)}


GET = {"/api/prices": api_prices, "/api/quote": api_quote, "/api/summary": api_summary, "/api/macro": api_macro, "/api/regime": api_regime, "/api/scan": api_scan,
       "/api/select": api_select, "/api/stock": api_stock, "/api/events": api_events, "/api/geo": api_geo,
       "/api/flow": api_flow, "/api/day": api_day, "/api/inplay": api_inplay, "/api/day/backtest": api_day_backtest,
       "/api/smallcap": api_smallcap, "/api/paper": api_paper}
POST = {"/api/projection": api_projection, "/api/payoff": api_payoff, "/api/run": api_run,
        "/api/paper/init": api_paper_init, "/api/paper/order": api_paper_order, "/api/paper/update": api_paper_update,
        "/api/paper/close": api_paper_close, "/api/paper/cancel": api_paper_cancel}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(clean(body)).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _handle(self, table, arg):
        path = urlparse(self.path).path
        if path not in table:
            return self._send(404, {"error": "not found"})
        try:
            self._send(200, table[path](arg))
        except (SystemExit, ValueError) as e:  # bad input: toolkit sys.exit messages, bad symbols, whitelist rejects
            self._send(400, {"error": str(e)})
        except Exception as e:  # noqa: BLE001 -- surface the reason in the UI
            traceback.print_exc()
            self._send(500, {"error": f"{type(e).__name__}: {e}"})

    def do_GET(self):
        u = urlparse(self.path)
        if u.path in ("/", "/index.html"):
            return self._send(200, (HERE / "index.html").read_bytes(), "text/html; charset=utf-8")
        self._handle(GET, {k: v[0] for k, v in parse_qs(u.query).items()})

    def do_POST(self):
        # JSON only: a cross-site form can't send application/json without a CORS preflight, which this server
        # never answers -- so other web pages can't place paper orders through the browser.
        if not (self.headers.get("Content-Type") or "").startswith("application/json"):
            return self._send(415, {"error": "POST bodies must be application/json"})
        n = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
        except json.JSONDecodeError:
            return self._send(400, {"error": "bad JSON"})
        self._handle(POST, body)

    def log_message(self, fmt, *args):
        sys.stderr.write(f"{self.log_date_time_string()} {fmt % args}\n")


if __name__ == "__main__":
    print(f"Trader UI on http://127.0.0.1:{PORT}  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
