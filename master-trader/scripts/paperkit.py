#!/usr/bin/env python3
"""paperkit -- a paper portfolio with bracket orders, for testing trade plans before real money.

Standard library only. The book is one JSON file (--book, default ./paper_book.json or $PAPER_BOOK) holding cash,
working orders, open positions, every closed trade and an equity curve. Fills come from real intraday bars
(Yahoo 1-minute bars for the last week, 5-minute bars back to ~2 months), or from your own bar files in replay.

Commands
  init      start a book: --equity, commissions, slippage, buying power, risk caps
  order     a bracket order: entry (market / limit:PRICE / stop:PRICE) with an attached stop-loss and take-profit
            that cancel each other, an optional flatten time for day trades, sized by --qty or --risk-pct.
            Stocks/ETFs long or short; listed puts and calls (buy to open, --put/--call --strike --expiry), with
            the bracket on the underlying's price by default
  update    walk the bars since the last update: fill entries, trigger stops/targets/flatten, settle expiries,
            mark to market, record equity
  status    account, open positions with live P&L in R, working orders, recent trades, plain-English summary
  close     close a position now at the market;   cancel   cancel a working order
  trades    closed-trade log (--csv FILE writes a file daykit.py journal reads)

Fill rules (conservative): an order only sees bars that start after it was placed; market and stop fills pay
slippage; a stop fills at its price or a worse open (gaps); when a bar touches both stop and target, the stop
wins; on the entry bar only the stop can trigger. Options without a live quote are priced with Black-Scholes at
the implied vol recorded at entry. Paper fills are kinder than real ones (no queue, no partial fills, no halts).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tradekit import bs, out  # noqa: E402

DEFAULT_BOOK = os.environ.get("PAPER_BOOK", "paper_book.json")
R_FREE = 0.04
SEC_FEE = 20.60e-6  # SEC Section 31 fee on sale proceeds (from 4 Apr 2026); FINRA TAF is $0 for Q4 2026
YEAR = 365.25 * 86400


# --------------------------------------------------------------------------- book file
def new_book(equity, commission_share=0.0, commission_contract=0.65, slippage_bps=2.0, bp=4.0, max_risk_pct=1.0,
             max_heat_pct=6.0, currency="USD"):
    t = dt.datetime.now(dt.timezone.utc).timestamp()
    return {"version": 1, "created": t, "currency": currency, "start_equity": equity, "cash": equity,
            "settings": {"commission_share": commission_share, "commission_contract": commission_contract,
                         "slippage_bps": slippage_bps, "bp": bp, "max_risk_pct": max_risk_pct, "max_heat_pct": max_heat_pct},
            "next_id": 1, "orders": [], "positions": [], "trades": [], "equity": [[t, equity]], "cursor": {}, "log": []}


def load_book(path=DEFAULT_BOOK):
    if not os.path.exists(path):
        raise FileNotFoundError(f"no paper book at {path}: start one with `paperkit.py init --equity 100000`")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save_book(book, path=DEFAULT_BOOK):
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(book, fh, indent=1)
    os.replace(tmp, path)  # atomic: a crash never leaves half a book


def _tz(name):
    try:
        from zoneinfo import ZoneInfo  # noqa: PLC0415
        return ZoneInfo(name or "America/New_York")
    except Exception:  # noqa: BLE001
        return dt.timezone(dt.timedelta(hours=-5))


def label(ts, tzname=None):
    return dt.datetime.fromtimestamp(ts, _tz(tzname)).strftime("%Y-%m-%d %H:%M")


def parse_local(s, tzname=None):
    return dt.datetime.strptime(s.strip()[:16], "%Y-%m-%d %H:%M").replace(tzinfo=_tz(tzname)).timestamp()


def _log(book, msg, ts=None):
    book["log"].append([ts or dt.datetime.now(dt.timezone.utc).timestamp(), msg])
    book["log"] = book["log"][-500:]


# --------------------------------------------------------------------------- prices
def live_quote(symbol):
    import fetch  # noqa: PLC0415
    return fetch.quote(symbol)


def option_quote(symbol, expiry, strike, right):
    """(bid, ask, mid, iv) from the listed chain, or None when Yahoo has no two-sided quote."""
    import fetch  # noqa: PLC0415
    try:
        ch = fetch.option_chain(symbol, expiry)
    except Exception:  # noqa: BLE001
        return None
    if ch["expiry"] != expiry:
        return None
    leg = next((x for x in ch["puts" if right == "put" else "calls"] if abs(x["strike"] - strike) < 1e-6), None)
    if not leg or not leg["ask"]:
        return None
    return leg["bid"], leg["ask"], leg["mid"], leg["iv"]


def expiry_ts(expiry, tzname):
    return parse_local(expiry + " 16:00", tzname)


def model_option(p, s, ts):
    """Black-Scholes value of an option position at underlying price s and time ts, at its entry IV."""
    t = max(0.0, (expiry_ts(p["expiry"], p.get("tz")) - ts) / YEAR)
    return bs(s, p["strike"], t, R_FREE, 0.0, p.get("iv") or 0.3, p["right"])["price"]


def live_bars(symbol, since):
    """Completed and forming bars since `since` (epoch): 1-minute for the last week, else 5-minute (~2 months)."""
    import fetch  # noqa: PLC0415
    age_d = (dt.datetime.now(dt.timezone.utc).timestamp() - since) / 86400
    iv = "1m" if age_d < 6.5 else "5m"
    rows, _, meta = fetch.yahoo_bars(symbol, iv, days=min(age_d + 1, 7 if iv == "1m" else 59), prepost=False)
    return rows, fetch.INTERVAL_SECS[iv], meta.get("exchangeTimezoneName")


# --------------------------------------------------------------------------- orders
def parse_entry(s):
    s = (s or "market").strip().lower()
    if s == "market":
        return {"type": "market", "price": None}
    kind, _, px = s.partition(":")
    if kind not in ("limit", "stop") or not px:
        raise ValueError("--entry must be market, limit:PRICE or stop:PRICE")
    return {"type": kind, "price": float(px)}


def _fees(book, kind, qty, price, selling, mult=1):
    st = book["settings"]
    f = qty * (st["commission_contract"] if kind == "option" else st["commission_share"])
    if selling:
        f += SEC_FEE * qty * price * mult
    return f


def _value(p, mark):
    m = p.get("mult", 1)
    return p["qty"] * mark * m * (-1 if p["side"] == "short" else 1)


def equity_of(book):
    return book["cash"] + sum(_value(p, p.get("mark", p["entry_price"])) for p in book["positions"])


def open_risk(book):
    """Cash at risk to each position's stop (long options: premium at risk) plus working orders' planned risk."""
    r = 0.0
    for p in book["positions"]:
        if p["kind"] == "option":
            r += p["qty"] * p.get("mark", p["entry_price"]) * p.get("mult", 100)
        elif p.get("stop") is not None:
            d = 1 if p["side"] == "long" else -1
            r += max(0.0, d * (p.get("mark", p["entry_price"]) - p["stop"])) * p["qty"]
    return r + sum(o.get("risk_cash", 0.0) for o in book["orders"] if o["status"] == "working")


def place_order(book, symbol, side="long", qty=None, risk_pct=None, entry="market", stop=None, target=None,
                target_r=None, flatten=None, tif="day", setup="", note="", right=None, strike=None, expiry=None,
                trigger="underlying", iv=None, now=None, price=None, tzname=None, force=False, quote=None,
                slippage_bps=None):
    """Validate, size and record a bracket order (filling a market order at once when a price is known).
    slippage_bps overrides the book's slippage for this order and the position it opens (one book trading both
    liquid ETFs and thin small caps). Returns (order, notes). Raises ValueError when the order breaks a rule."""
    symbol = symbol.upper()
    notes = []
    st = book["settings"]
    en = parse_entry(entry)
    kind = "option" if right else "stock"
    if kind == "option":
        if right not in ("put", "call") or strike is None or not expiry:
            raise ValueError("options need --put or --call with --strike and --expiry YYYY-MM-DD")
        if side != "long":
            raise ValueError("paper options are buy-to-open only (long puts and calls)")
        if en["type"] != "market":
            raise ValueError("option orders are market orders here; put the bracket on the underlying")
    if side not in ("long", "short"):
        raise ValueError("--side must be long or short")
    t_now = now or dt.datetime.now(dt.timezone.utc).timestamp()
    q = quote
    if price is None and q is None:
        q = live_quote(symbol)
    und = price if price is not None else q["price"]
    tzname = tzname or (q or {}).get("tzname") or "America/New_York"
    market_open = price is not None or (q and q["state"] == "open" and (q.get("age_s") or 0) < 1200)
    ref = en["price"] if en["price"] is not None else und
    d = 1 if side == "long" else -1
    d_und = -1 if right == "put" else d  # direction on the underlying: a long put profits when it falls
    if stop is not None and d_und * (ref - stop) <= 0:
        raise ValueError(f"stop {stop:g} must be {'below' if d_und > 0 else 'above'} the entry {ref:g}"
                         + (" (option brackets sit on the underlying: a put's stop is above the price)" if right == "put" else ""))
    if target is None and target_r and stop is not None:
        target = ref + d_und * target_r * abs(ref - stop)
    if target is not None and d_und * (target - ref) <= 0:
        raise ValueError(f"target {target:g} is on the wrong side of the entry {ref:g}")
    prem, opt_iv, mult = None, iv, 1
    if kind == "option":
        mult = 100
        oq = None if price is not None else option_quote(symbol, expiry, strike, right)
        if oq:
            bid, ask, mid, chain_iv = oq
            prem, opt_iv = ask, opt_iv or chain_iv
        else:
            if not opt_iv:
                raise ValueError("no two-sided quote for that contract: pass --iv to price it with the model")
            t = max(0.0, (expiry_ts(expiry, tzname) - t_now) / YEAR)
            prem = bs(und, strike, t, R_FREE, 0.0, opt_iv, right)["price"] * 1.02
            notes.append(f"no live option quote: priced with the model at IV {opt_iv:.0%} plus 2% for the spread")
    eq = equity_of(book)
    per_unit = prem * mult if kind == "option" else (abs(ref - stop) if stop is not None else None)
    if qty is None:
        if not risk_pct:
            raise ValueError("give --qty or --risk-pct")
        if not per_unit:
            raise ValueError("--risk-pct needs a stop (stocks) to size from")
        qty = math.floor(eq * risk_pct / 100 / per_unit)
        if qty <= 0:
            raise ValueError(f"size rounds to zero: one unit risks {per_unit:,.2f}, the budget is {eq * risk_pct / 100:,.2f}")
    if stop is None and kind == "stock":
        notes.append("no stop-loss: this is not a bracket, and the risk is open-ended")
    risk_cash = qty * per_unit if per_unit else 0.0
    if risk_cash > eq * st["max_risk_pct"] / 100 and not force:
        raise ValueError(f"risk {risk_cash:,.0f} = {risk_cash / eq:.2%} of equity breaks the {st['max_risk_pct']:g}% cap "
                         "(lower the size or pass --force)")
    heat = open_risk(book) + risk_cash
    if heat > eq * st["max_heat_pct"] / 100 and not force:
        raise ValueError(f"total open risk would be {heat / eq:.1%} of equity, above the {st['max_heat_pct']:g}% cap")
    if kind == "stock":
        gross = sum(p["qty"] * p.get("mark", p["entry_price"]) for p in book["positions"] if p["kind"] == "stock")
        if gross + qty * ref > eq * st["bp"] and not force:
            raise ValueError(f"buying power: {gross + qty * ref:,.0f} of positions vs {eq * st['bp']:,.0f} allowed ({st['bp']:g}x)")
    elif qty * prem * mult > book["cash"]:
        raise ValueError(f"not enough cash for {qty} contracts at {prem:.2f}")
    oid = book["next_id"]
    book["next_id"] += 1
    o = {"id": oid, "symbol": symbol, "kind": kind, "side": side, "qty": qty, "entry": en, "stop": stop,
         "target": target, "flatten": flatten, "tif": tif, "setup": setup, "note": note, "created": t_now,
         "status": "working", "risk_cash": risk_cash, "tz": tzname, "trigger": trigger}
    if slippage_bps is not None:
        o["slippage_bps"] = float(slippage_bps)
    if kind == "option":
        o.update(right=right, strike=strike, expiry=expiry, mult=mult, iv=opt_iv, premium=prem)
    book["orders"].append(o)
    _log(book, f"order #{oid}: {side} {qty} {_desc(o)} {en['type']}{' ' + str(en['price']) if en['price'] else ''}"
               f" stop {stop} target {target}", t_now)
    if en["type"] == "market" and market_open:
        fill = prem if kind == "option" else und * (1 + d * _slip(book, o))
        _open_position(book, o, fill, t_now, und)
        notes.append(f"filled at {fill:,.4g} ({'ask' if kind == 'option' else 'quote + slippage'})")
    elif en["type"] == "market":
        notes.append("market closed or quote stale: fills at the next bar's open on `update`")
    return o, notes


def _desc(o):
    if o["kind"] == "option":
        return f"{o['symbol']} {o['expiry']} {o['strike']:g} {o['right']}"
    return o["symbol"]


def _open_position(book, o, fill, ts, und):
    mult = o.get("mult", 1)
    fees = _fees(book, o["kind"], o["qty"], fill, o["side"] == "short", mult)
    if o["side"] == "long":
        book["cash"] -= o["qty"] * fill * mult + fees
    else:
        book["cash"] += o["qty"] * fill - fees
    o["status"] = "filled"
    p = {k: o[k] for k in ("id", "symbol", "kind", "side", "qty", "stop", "target", "flatten", "setup", "note", "tz",
                           "trigger", "risk_cash", "slippage_bps") if k in o}
    p.update(entry_price=fill, entry_ts=ts, fees=fees, mark=fill, mark_ts=ts, und_entry=und, mfe=0.0, mae=0.0, mult=mult)
    if o["kind"] == "option":
        p.update(right=o["right"], strike=o["strike"], expiry=o["expiry"], iv=o["iv"])
    if o["kind"] == "stock" and o.get("stop") is not None:
        p["risk_cash"] = abs(fill - o["stop"]) * o["qty"]  # risk from the actual fill
    book["positions"].append(p)
    _log(book, f"filled #{o['id']} {o['side']} {o['qty']} {_desc(o)} at {fill:,.4g}", ts)
    return p


def _close(book, p, price, ts, reason):
    mult = p.get("mult", 1)
    fees = _fees(book, p["kind"], p["qty"], price, p["side"] == "long", mult)
    if p["side"] == "long":
        book["cash"] += p["qty"] * price * mult - fees
        gross = (price - p["entry_price"]) * p["qty"] * mult
    else:
        book["cash"] -= p["qty"] * price + fees
        gross = (p["entry_price"] - price) * p["qty"]
    pnl = gross - p["fees"] - fees
    risk = p.get("risk_cash") or 0.0
    tzn = p.get("tz")
    tr = {"id": p["id"], "symbol": p["symbol"], "contract": _desc(p), "kind": p["kind"], "side": p["side"], "qty": p["qty"],
          "entry_price": p["entry_price"], "exit_price": price, "entry_ts": p["entry_ts"], "exit_ts": ts,
          "entry_time": label(p["entry_ts"], tzn), "exit_time": label(ts, tzn), "pnl": pnl, "fees": p["fees"] + fees,
          "R": pnl / risk if risk else None, "risk_cash": risk, "reason": reason, "setup": p.get("setup", ""),
          "note": p.get("note", ""), "stop": p.get("stop"), "target": p.get("target"),
          "hold_min": (ts - p["entry_ts"]) / 60, "mfe_R": p["mfe"] / risk if risk else None,
          "mae_R": p["mae"] / risk if risk else None}
    book["trades"].append(tr)
    book["positions"].remove(p)
    _log(book, f"closed #{p['id']} {_desc(p)} at {price:,.4g} ({reason}): {pnl:+,.2f}", ts)
    return tr


def _slip(book, x):
    """An order's or position's own slippage (fraction), else the book's."""
    return x.get("slippage_bps", book["settings"]["slippage_bps"]) / 1e4


def cancel_order(book, oid):
    o = next((x for x in book["orders"] if x["id"] == oid and x["status"] == "working"), None)
    if not o:
        raise ValueError(f"no working order #{oid}")
    o["status"] = "cancelled"
    _log(book, f"cancelled #{oid}")
    return o


def close_position(book, ref, price=None, now=None):
    """Close by position id or symbol at the market (quote, or option bid / model)."""
    ps = [p for p in book["positions"] if str(p["id"]) == str(ref) or p["symbol"] == str(ref).upper()]
    if not ps:
        raise ValueError(f"no open position '{ref}'")
    t = now or dt.datetime.now(dt.timezone.utc).timestamp()
    done = []
    for p in ps:
        px = price
        if px is None:
            if p["kind"] == "option":
                oq = option_quote(p["symbol"], p["expiry"], p["strike"], p["right"])
                px = oq[0] if oq and oq[0] else model_option(p, live_quote(p["symbol"])["price"], t) * 0.98
            else:
                d = 1 if p["side"] == "long" else -1
                px = live_quote(p["symbol"])["price"] * (1 - d * _slip(book, p))
        done.append(_close(book, p, px, t, "manual close"))
    return done


# --------------------------------------------------------------------------- the simulator
def _hhmm(ts, tzname):
    t = dt.datetime.fromtimestamp(ts, _tz(tzname))
    return t.strftime("%Y-%m-%d"), t.strftime("%H:%M")


def _step(book, sym, bar, secs, tzname, events):
    """Process one bar [ts, label, o, h, l, c, v] of the underlying for every order and position on sym."""
    ts, _, o_, h, l, c = bar[:6]
    day, hm = _hhmm(ts, tzname)
    # entries
    for o in [x for x in book["orders"] if x["symbol"] == sym and x["status"] == "working"]:
        if ts < o["created"]:
            continue
        cday, _ = _hhmm(o["created"], tzname)
        if o["tif"] == "day" and (day > cday or (o.get("flatten") and hm >= o["flatten"])):
            o["status"] = "expired"
            events.append(f"#{o['id']} expired unfilled")
            continue
        d = 1 if o["side"] == "long" else -1
        e, fill, slip = o["entry"], None, _slip(book, o)
        if e["type"] == "market":
            fill = o_ * (1 + d * slip)
        elif e["type"] == "limit" and ((d > 0 and l <= e["price"]) or (d < 0 and h >= e["price"])):
            fill = min(o_, e["price"]) if d > 0 else max(o_, e["price"])
        elif e["type"] == "stop" and ((d > 0 and h >= e["price"]) or (d < 0 and l <= e["price"])):
            fill = (max(o_, e["price"]) if d > 0 else min(o_, e["price"])) * (1 + d * slip)
        if fill is None:
            continue
        if o["kind"] == "option":
            p = _open_position(book, o, model_option(dict(o, tz=tzname), fill, ts) * 1.02, ts, fill)
        else:
            p = _open_position(book, o, fill, ts, fill)
        p["fresh"] = True
        events.append(f"#{o['id']} entry filled at {p['entry_price']:,.4g}")
    # exits
    for p in [x for x in book["positions"] if x["symbol"] == sym]:
        if ts < p["entry_ts"] and not p.get("fresh"):
            continue
        first = p.pop("fresh", False)
        opt = p["kind"] == "option"
        d = (-1 if p.get("right") == "put" else 1) if opt else (1 if p["side"] == "long" else -1)  # direction on the underlying
        stop, tgt = p.get("stop"), p.get("target")
        exit_und, reason = None, None
        if opt and ts >= expiry_ts(p["expiry"], p.get("tz") or tzname):
            s_exp = p.get("und_last", o_)  # the expiry day's last close, not the next session's open
            intrinsic = max(0.0, (p["strike"] - s_exp) if p["right"] == "put" else (s_exp - p["strike"]))
            events.append(f"#{p['id']} expired, settled at intrinsic {intrinsic:.2f}")
            _close(book, p, intrinsic, ts, "expiry")
            continue
        if not first:
            if stop is not None and d * (o_ - stop) <= 0:
                exit_und, reason = o_, "stop (gapped through)"
            elif tgt is not None and d * (o_ - tgt) >= 0:
                exit_und, reason = o_, "target (gap)"
        if exit_und is None and stop is not None and ((d > 0 and l <= stop) or (d < 0 and h >= stop)):
            exit_und, reason = stop, "stop"
        elif exit_und is None and not first and tgt is not None and ((d > 0 and h >= tgt) or (d < 0 and l <= tgt)):
            exit_und, reason = tgt, "target"
        elif exit_und is None and p.get("flatten") and hm >= p["flatten"] and ts > p["entry_ts"]:
            exit_und, reason = o_, f"flatten {p['flatten']}"
        if exit_und is None:
            # excursions in cash terms, from the bar's extremes
            best, worst = (h, l) if d > 0 else (l, h)
            if opt:
                fav, adv = model_option(p, best, ts), model_option(p, worst, ts)
                p["mfe"] = max(p["mfe"], (fav - p["entry_price"]) * p["qty"] * p["mult"])
                p["mae"] = min(p["mae"], (adv - p["entry_price"]) * p["qty"] * p["mult"])
            else:
                sgn = 1 if p["side"] == "long" else -1
                p["mfe"] = max(p["mfe"], sgn * (best - p["entry_price"]) * p["qty"])
                p["mae"] = min(p["mae"], sgn * (worst - p["entry_price"]) * p["qty"])
            p["mark"] = model_option(p, c, ts) if opt else c
            p["mark_ts"] = ts + secs
            p["und_last"] = c
            continue
        if opt:
            px = model_option(p, exit_und, ts) * 0.98  # sell near the bid
        else:
            sgn = 1 if p["side"] == "long" else -1
            px = exit_und * (1 - sgn * _slip(book, p)) if reason != "target" else exit_und  # targets are limit orders
        tr = _close(book, p, px, ts, reason)
        events.append(f"#{p['id']} {reason}: out at {px:,.4g}, {tr['pnl']:+,.2f}" + (f" ({tr['R']:+.2f}R)" if tr["R"] is not None else ""))


def update_book(book, bars_for=None, now=None):
    """Advance the book to `now`: process every completed bar since the last update, then mark to market."""
    t_now = now or dt.datetime.now(dt.timezone.utc).timestamp()
    events = []
    syms = sorted({o["symbol"] for o in book["orders"] if o["status"] == "working"} | {p["symbol"] for p in book["positions"]})
    for sym in syms:
        items = [o["created"] for o in book["orders"] if o["symbol"] == sym and o["status"] == "working"] + \
                [p["entry_ts"] for p in book["positions"] if p["symbol"] == sym]
        since = max(min(items), book["cursor"].get(sym, 0))
        try:
            rows, secs, tzname = (bars_for or live_bars)(sym, since)
        except Exception as e:  # noqa: BLE001
            events.append(f"{sym}: no bars ({e})")
            continue
        last = book["cursor"].get(sym, 0)
        for bar in rows:
            if bar[0] <= last or bar[0] + secs > t_now:
                continue  # already processed, or still forming
            _step(book, sym, bar, secs, tzname, events)
            book["cursor"][sym] = bar[0]
    if bars_for is None:
        _mark_live(book)
    book["equity"].append([t_now, equity_of(book)])
    book["last_update"] = t_now
    for e in events:
        _log(book, e, t_now)
    return events


def _mark_live(book):
    for p in book["positions"]:
        try:
            if p["kind"] == "option":
                oq = option_quote(p["symbol"], p["expiry"], p["strike"], p["right"])
                if oq and oq[2]:
                    p["mark"], p["mark_src"] = oq[2], "chain mid"
                else:
                    s = live_quote(p["symbol"])["price"]
                    p["mark"], p["mark_src"], p["und_last"] = model_option(p, s, dt.datetime.now(dt.timezone.utc).timestamp()), "model", s
            else:
                q = live_quote(p["symbol"])
                p["mark"], p["mark_src"], p["und_last"] = q["price"], "quote", q["price"]
        except Exception:  # noqa: BLE001 -- keep the last bar's mark
            p["mark_src"] = "last bar"


# --------------------------------------------------------------------------- reporting
def day_trades_5d(book):
    """Round trips opened and closed on the same day within the last five business days."""
    d, recent = dt.date.today(), set()
    while len(recent) < 5:
        if d.weekday() < 5:
            recent.add(d.isoformat())
        d -= dt.timedelta(days=1)
    return sum(1 for t in book["trades"] if t["entry_time"][:10] == t["exit_time"][:10] and t["exit_time"][:10] in recent)


def status(book):
    eq = equity_of(book)
    start = book["start_equity"]
    pos = []
    for p in book["positions"]:
        mark = p.get("mark", p["entry_price"])
        sgn = 1 if p["side"] == "long" else -1
        upnl = sgn * (mark - p["entry_price"]) * p["qty"] * p.get("mult", 1) - p["fees"]
        pos.append({"id": p["id"], "contract": _desc(p), "symbol": p["symbol"], "kind": p["kind"], "side": p["side"],
                    "qty": p["qty"], "entry": p["entry_price"], "mark": mark, "mark_src": p.get("mark_src", "last bar"),
                    "upnl": upnl, "R": upnl / p["risk_cash"] if p.get("risk_cash") else None, "stop": p.get("stop"),
                    "target": p.get("target"), "flatten": p.get("flatten"), "entry_time": label(p["entry_ts"], p.get("tz")),
                    "und": p.get("und_last"), "setup": p.get("setup", "")})
    orders = [{"id": o["id"], "contract": _desc(o), "side": o["side"], "qty": o["qty"], "entry": o["entry"],
               "stop": o["stop"], "target": o["target"], "flatten": o.get("flatten"), "tif": o["tif"],
               "created": label(o["created"], o.get("tz")), "risk_cash": o.get("risk_cash")}
              for o in book["orders"] if o["status"] == "working"]
    tr = book["trades"]
    rs = [t["R"] for t in tr if t["R"] is not None]
    realized = sum(t["pnl"] for t in tr)
    unreal = sum(x["upnl"] for x in pos)
    heat = open_risk(book)
    stats = {"n": len(tr), "win": sum(1 for t in tr if t["pnl"] > 0) / len(tr) if tr else None,
             "exp_R": sum(rs) / len(rs) if rs else None, "pnl": realized}
    started = label(book["created"])[:10]
    bl = f"The paper account is at {eq:,.0f} ({eq / start - 1:+.2%} since {started})."
    bl += f" {len(pos)} open position{'s' if len(pos) != 1 else ''}" + (f" risking {heat / eq:.1%} of equity" if pos or orders else "")
    bl += f", {len(orders)} working order{'s' if len(orders) != 1 else ''}."
    if tr:
        bl += (f" {len(tr)} closed trade{'s' if len(tr) != 1 else ''}: {stats['win']:.0%} winners"
               + (f", {stats['exp_R']:+.2f}R per trade" if stats["exp_R"] is not None else "")
               + (" -- far too few to judge an edge (think 100-300+)." if len(tr) < 100 else "."))
    return {"equity": eq, "cash": book["cash"], "start_equity": start, "total_pnl": eq - start, "total_ret": eq / start - 1,
            "realized": realized, "unrealized": unreal, "open_risk": heat, "heat_pct": heat / eq if eq else None,
            "positions": pos, "orders": orders, "trades": tr[-100:][::-1], "equity_curve": book["equity"][-2000:],
            "day_trades_5d": day_trades_5d(book), "stats": stats, "bottom_line": bl, "settings": book["settings"],
            "last_update": label(book["last_update"]) if book.get("last_update") else None,
            "log": [[label(t), m] for t, m in book["log"][-30:]][::-1]}


def write_trades_csv(book, path):
    cols = ["entry_time", "exit_time", "symbol", "contract", "side", "qty", "entry", "exit", "stop", "pnl", "r", "risk",
            "fees", "setup", "reason", "note"]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for t in book["trades"]:
            w.writerow([t["entry_time"], t["exit_time"], t["symbol"], t["contract"], t["side"], t["qty"],
                        round(t["entry_price"], 6), round(t["exit_price"], 6), t.get("stop"), round(t["pnl"], 2),
                        round(t["R"], 4) if t["R"] is not None else "", round(t["risk_cash"], 2), round(t["fees"], 2),
                        t["setup"], t["reason"], t["note"]])


# --------------------------------------------------------------------------- CLI
def _book(a):
    try:
        return load_book(a.book)
    except FileNotFoundError as e:
        sys.exit(str(e))


def _replay(a):
    """--bars SYM=FILE (bar-start times in --tz) -> a bars_for() that serves those files."""
    if not a.bars:
        return None
    import daykit  # noqa: PLC0415
    files = dict(x.split("=", 1) for x in a.bars)

    def bars_for(sym, since):
        if sym not in files:
            raise ValueError("no --bars file for this symbol")
        bars = daykit.load_bars(files[sym])
        secs = daykit.bar_minutes(bars) * 60
        tz = _tz(a.tz)
        return [[b[0].replace(tzinfo=tz).timestamp(), b[0].strftime("%Y-%m-%d %H:%M")] + b[1:] for b in bars], secs, a.tz
    return bars_for


def cmd_init(a):
    if os.path.exists(a.book) and not a.force:
        sys.exit(f"{a.book} exists; pass --force to start over (the old book is overwritten)")
    b = new_book(a.equity, a.commission_share, a.commission_contract, a.slippage_bps, a.bp, a.max_risk, a.max_heat)
    save_book(b, a.book)
    print(f"  paper book {a.book}: {a.equity:,.0f} cash; risk cap {a.max_risk:g}%/trade, heat cap {a.max_heat:g}%, "
          f"buying power {a.bp:g}x, slippage {a.slippage_bps:g} bps, commissions {a.commission_share:g}/share, "
          f"{a.commission_contract:g}/contract")


def cmd_order(a):
    b = _book(a)
    now = parse_local(a.now, a.tz) if a.now else None
    right = "put" if a.put else "call" if a.call else None
    try:
        o, notes = place_order(b, a.symbol, a.side, a.qty, a.risk_pct, a.entry, a.stop, a.target, a.target_r, a.flatten,
                               a.tif, a.setup or "", a.note or "", right, a.strike, a.expiry, "underlying", a.iv, now,
                               a.price, a.tz if a.price is not None else None, a.force)
    except ValueError as e:
        sys.exit(f"  order rejected: {e}")
    save_book(b, a.book)
    en = o["entry"]
    print(f"  #{o['id']} {o['side']} {o['qty']} {_desc(o)}: entry {en['type']}{' ' + format(en['price'], 'g') if en['price'] else ''}"
          f", stop-loss {o['stop']}, take-profit {o['target'] if o['target'] is None else round(o['target'], 4)}"
          f"{', flatten ' + o['flatten'] if o['flatten'] else ''} ({o['tif']}); risk {o['risk_cash']:,.2f}"
          f" = {o['risk_cash'] / equity_of(b):.2%} of equity -> {o['status']}")
    for n in notes:
        print(f"    {n}")


def cmd_update(a):
    b = _book(a)
    ev = update_book(b, _replay(a), parse_local(a.now, a.tz) if a.now else None)
    save_book(b, a.book)
    for e in ev:
        print(f"  {e}")
    print(f"  updated: equity {equity_of(b):,.2f}" + ("" if ev else " (nothing happened)"))


def cmd_status(a):
    s = status(_book(a))
    print(f"\n  Bottom line: {s['bottom_line']}")
    out([("Equity / cash", f"{s['equity']:,.2f} / {s['cash']:,.2f}"),
         ("P&L total / realized / open", f"{s['total_pnl']:+,.2f} ({s['total_ret']:+.2%}) / {s['realized']:+,.2f} / {s['unrealized']:+,.2f}"),
         ("Open risk (heat)", f"{s['open_risk']:,.2f} = {(s['heat_pct'] or 0):.2%} of equity (cap {s['settings']['max_heat_pct']:g}%)"),
         ("Day trades, last 5 days", s["day_trades_5d"]), ("Last update", s["last_update"] or "never")], "Paper account")
    if s["positions"]:
        print(f"\n  {'id':>3} {'position':<28}{'side':<6}{'qty':>6}{'entry':>10}{'mark':>10}{'P&L':>10}{'R':>7}{'stop':>9}{'target':>9}")
        for p in s["positions"]:
            print(f"  {p['id']:>3} {p['contract']:<28}{p['side']:<6}{p['qty']:>6}{p['entry']:>10,.4g}{p['mark']:>10,.4g}"
                  f"{p['upnl']:>+10,.0f}{(p['R'] if p['R'] is not None else 0):>+7.2f}{str(p['stop']):>9}{(round(p['target'], 2) if p['target'] else '-'):>9}")
    if s["orders"]:
        print("\n  Working orders:")
        for o in s["orders"]:
            print(f"    #{o['id']} {o['side']} {o['qty']} {o['contract']} {o['entry']['type']} {o['entry']['price'] or ''} "
                  f"stop {o['stop']} target {o['target']} ({o['tif']}, placed {o['created']})")
    if s["trades"]:
        print("\n  Recent trades:")
        for t in s["trades"][:10]:
            print(f"    #{t['id']} {t['contract']:<26} {t['side']:<5} {t['entry_time']} -> {t['exit_time'][11:]}  "
                  f"{t['pnl']:+10,.2f}" + (f"  {t['R']:+.2f}R" if t["R"] is not None else "") + f"  {t['reason']}")


def cmd_close(a):
    b = _book(a)
    try:
        done = close_position(b, a.ref, a.price, parse_local(a.now, a.tz) if a.now else None)
    except ValueError as e:
        sys.exit(str(e))
    save_book(b, a.book)
    for t in done:
        print(f"  closed #{t['id']} {t['contract']} at {t['exit_price']:,.4g}: {t['pnl']:+,.2f}")


def cmd_cancel(a):
    b = _book(a)
    try:
        cancel_order(b, a.id)
    except ValueError as e:
        sys.exit(str(e))
    save_book(b, a.book)
    print(f"  cancelled #{a.id}")


def cmd_trades(a):
    b = _book(a)
    if a.csv:
        write_trades_csv(b, a.csv)
        print(f"  wrote {len(b['trades'])} trades to {a.csv}  (review with: daykit.py journal {a.csv})")
        return
    for t in b["trades"]:
        print(f"  #{t['id']:<3} {t['contract']:<26} {t['side']:<5} {t['qty']:>6} {t['entry_time']} {t['entry_price']:>10,.4g} -> "
              f"{t['exit_time']} {t['exit_price']:>10,.4g} {t['pnl']:>+10,.2f}" + (f" {t['R']:+.2f}R" if t["R"] is not None else "")
              + f"  {t['reason']}")


def build():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--book", default=DEFAULT_BOOK, help="paper book JSON file")
    p.add_argument("--tz", default="America/New_York", help="time zone for --now and replay bar files")
    s = p.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("init")
    x.add_argument("--equity", type=float, required=True)
    x.add_argument("--commission-share", type=float, default=0.0)
    x.add_argument("--commission-contract", type=float, default=0.65)
    x.add_argument("--slippage-bps", type=float, default=2.0, help="on market and stop fills")
    x.add_argument("--bp", type=float, default=4.0, help="buying power multiple for stock positions")
    x.add_argument("--max-risk", type=float, default=1.0, help="%% of equity one trade may risk")
    x.add_argument("--max-heat", type=float, default=6.0, help="%% of equity all open trades may risk")
    x.add_argument("--force", action="store_true")
    x.set_defaults(fn=cmd_init)
    x = s.add_parser("order", help="bracket order")
    x.add_argument("symbol")
    x.add_argument("--side", choices=["long", "short"], default="long")
    x.add_argument("--qty", type=int)
    x.add_argument("--risk-pct", type=float, help="size so the stop (or a long option's premium) risks this %% of equity")
    x.add_argument("--entry", default="market", help="market | limit:PRICE | stop:PRICE")
    x.add_argument("--stop", type=float, help="stop-loss price (underlying price for options)")
    x.add_argument("--target", type=float, help="take-profit price")
    x.add_argument("--target-r", type=float, help="take-profit at this many R from the entry")
    x.add_argument("--flatten", help="HH:MM exchange time: exit a day trade then if still open")
    x.add_argument("--tif", choices=["day", "gtc"], default="day", help="entry time in force")
    x.add_argument("--put", action="store_true")
    x.add_argument("--call", action="store_true")
    x.add_argument("--strike", type=float)
    x.add_argument("--expiry", help="YYYY-MM-DD (a listed expiry)")
    x.add_argument("--iv", type=float, help="implied vol for model pricing when no quote (0.30 = 30%%)")
    x.add_argument("--setup")
    x.add_argument("--note")
    x.add_argument("--price", type=float, help="replay: the underlying price at --now (skips the live quote)")
    x.add_argument("--now", help="replay: 'YYYY-MM-DD HH:MM' in --tz")
    x.add_argument("--force", action="store_true", help="override the risk, heat and buying-power caps")
    x.set_defaults(fn=cmd_order)
    x = s.add_parser("update")
    x.add_argument("--bars", nargs="*", help="replay: SYMBOL=FILE intraday bar files instead of Yahoo")
    x.add_argument("--now", help="replay: process bars up to 'YYYY-MM-DD HH:MM' in --tz")
    x.set_defaults(fn=cmd_update)
    x = s.add_parser("status")
    x.set_defaults(fn=cmd_status)
    x = s.add_parser("close")
    x.add_argument("ref", help="position id or symbol")
    x.add_argument("--price", type=float)
    x.add_argument("--now")
    x.set_defaults(fn=cmd_close)
    x = s.add_parser("cancel")
    x.add_argument("id", type=int)
    x.set_defaults(fn=cmd_cancel)
    x = s.add_parser("trades")
    x.add_argument("--csv")
    x.set_defaults(fn=cmd_trades)
    return p


def main(argv=None):
    a = build().parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
