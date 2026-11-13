#!/usr/bin/env python3
"""fetch -- pull macro and price data for the master-trader toolkit.

Standard library only. Output CSVs feed straight into tradekit.py / techkit.py.

Commands
  macro                    one-screen macro/regime dashboard from FRED (needs FRED key)
  fred SERIES... [--out]   download FRED series (merged on date) to CSV / print latest
  search "text"            find FRED series IDs
  gpr [--freq daily]       Caldara-Iacoviello Geopolitical Risk index (needs xlrd to parse .xls)
  fundamentals TICKER      quarterly financials from SEC XBRL: revenue, growth, margins, EPS, FCF, SBC, inventory days
  earnings-dates TICKER    past earnings release dates and AMC/BMO timing from SEC 8-K item 2.02 filings
  prices SYMBOL [--out]    daily OHLCV history (Yahoo chart API; no key); --interval 1h|30m|15m|5m|2m|1m for
                           intraday bars (--range/--days, --prepost for extended hours)
  options SYMBOL           listed option chain near the money: bid/ask/mid, IV, open interest (Yahoo; no key)
  quote SYMBOL...          latest price, change vs previous close, session state and quote age (Yahoo; no key)
  trades SYMBOL            recent crypto trades with aggressor side (Kraken/Coinbase public; no key)
  book SYMBOL              crypto L2 order-book snapshot (Coinbase/Kraken public; no key)

FRED key lookup (first hit wins): $FRED_API_KEY, --key-file, then any *fred*.txt file in
$TRADER_KEYS_DIR, F:/dev/Keys, ~/OneDrive/keys, ~/.keys. The key is never printed.

Data caveats: FRED is end-of-day or slower (macro releases lag by weeks). Yahoo's endpoint is
unofficial and can be delayed or change without notice -- fine for research and backtests,
not for live order decisions. Verify anything important against a second source.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import glob
import json
import math
import os
import re
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tradekit import out  # noqa: E402

FRED = "https://api.stlouisfed.org/fred"
UA = {"User-Agent": "Mozilla/5.0 (research script)"}
KEY_DIRS = [os.environ.get("TRADER_KEYS_DIR", ""), "F:/dev/Keys",
            os.path.expanduser("~/OneDrive/keys"), os.path.expanduser("~/.keys")]


# --------------------------------------------------------------------------- plumbing
def http_json(url: str, timeout: int = 30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def http_text(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def fred_key(key_file: str | None = None) -> str:
    if os.environ.get("FRED_API_KEY"):
        return os.environ["FRED_API_KEY"].strip()
    candidates = [key_file] if key_file else []
    for d in KEY_DIRS:
        if d and os.path.isdir(d):
            candidates += sorted(p for p in glob.glob(os.path.join(d, "*.txt")) if "fred" in os.path.basename(p).lower())
    for p in candidates:
        if p and os.path.isfile(p):
            with open(p, encoding="utf-8-sig") as fh:
                k = fh.readline().strip()
            if len(k) == 32 and k.isalnum():
                return k
    sys.exit("No FRED key found. Get one free at https://fredaccount.stlouisfed.org/apikeys and save it as a "
             "*fred*.txt file in one of: " + ", ".join(d for d in KEY_DIRS if d) + " (or set FRED_API_KEY).")


def fred_get(path: str, key: str, **params):
    params.update(api_key=key, file_type="json")
    url = f"{FRED}/{path}?{urllib.parse.urlencode(params)}"
    try:
        return http_json(url)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        msg = body.replace(key, "***")[:300]
        raise SystemExit(f"FRED error {e.code} for {params.get('series_id', path)}: {msg}")


def fred_series(sid: str, key: str, start: str | None = None) -> list[tuple[str, float]]:
    p = {"series_id": sid}
    if start:
        p["observation_start"] = start
    js = fred_get("series/observations", key, **p)
    obs = []
    for o in js.get("observations", []):
        if o["value"] not in (".", ""):
            obs.append((o["date"], float(o["value"])))
    return obs


def value_at_or_before(obs, date: str):
    v = None
    for d, x in obs:
        if d <= date:
            v = x
        else:
            break
    return v


def days_ago(n: int) -> str:
    return (dt.date.today() - dt.timedelta(days=n)).isoformat()


# --------------------------------------------------------------------------- macro dashboard
# (series, label, kind) kind: level (show level + bp/pt changes), yoy (monthly index -> YoY %), bn (millions -> $bn)
DASH = [
    ("Policy & rates", [
        ("DFF", "Fed funds effective %", "level"),
        ("SOFR", "SOFR %", "level"),
        ("DGS2", "2y Treasury %", "level"),
        ("DGS10", "10y Treasury %", "level"),
        ("DFII10", "10y real yield (TIPS) %", "level"),
        ("T10YIE", "10y breakeven inflation %", "level"),
        ("T10Y2Y", "10y-2y curve %", "level"),
        ("T10Y3M", "10y-3m curve %", "level"),
    ]),
    ("Inflation & labor", [
        ("CPIAUCSL", "CPI YoY %", "yoy"),
        ("CPILFESL", "Core CPI YoY %", "yoy"),
        ("PCEPILFE", "Core PCE YoY %", "yoy"),
        ("UNRATE", "Unemployment %", "level"),
        ("ICSA", "Initial claims", "level"),
    ]),
    ("Risk & conditions", [
        ("VIXCLS", "VIX", "level"),
        ("BAMLH0A0HYM2", "HY OAS %", "level"),
        ("BAMLC0A0CM", "IG OAS %", "level"),
        ("NFCI", "Chicago Fed NFCI (>0 = tight)", "level"),
        ("DTWEXBGS", "Broad trade-weighted USD", "level"),
    ]),
    ("Geopolitics, uncertainty & safe havens", [
        ("USEPUINDXD", "US policy uncertainty (EPU, daily)", "level"),
        ("EPUTRADE", "Trade-policy uncertainty (EPU, monthly)", "level"),
        ("EPUNATSEC", "Natl-security uncertainty (EPU, monthly)", "level"),
        ("GEPUCURRENT", "Global policy uncertainty (monthly)", "level"),
        ("OVXCLS", "Oil implied vol (OVX)", "level"),
        ("GVZCLS", "Gold implied vol (GVZ)", "level"),
        ("DEXJPUS", "JPY per USD (yen strengthens = lower)", "level"),
        ("DEXSZUS", "CHF per USD (franc strengthens = lower)", "level"),
    ]),
    ("Liquidity & commodities", [
        ("WALCL", "Fed total assets $bn", "bn"),
        ("WTREGEN", "Treasury General Account $bn", "bn"),
        ("RRPONTSYD", "Overnight reverse repo $bn", "level"),
        ("DCOILBRENTEU", "Brent spot $/bbl (EIA, lagged)", "level"),
        ("DCOILWTICO", "WTI spot $/bbl (EIA, lagged)", "level"),
        ("SP500", "S&P 500 (FRED, lagged)", "level"),
    ]),
]


def yoy_series(obs):
    idx = {d: v for d, v in obs}
    out = []
    for d, v in obs:
        y = f"{int(d[:4]) - 1}{d[4:]}"
        if y in idx and idx[y]:
            out.append((d, (v / idx[y] - 1) * 100))
    return out


def change(obs, days):
    """Last value minus the value `days` calendar days before the last observation (None if no history)."""
    ld, lv = obs[-1]
    pv = value_at_or_before(obs, (dt.date.fromisoformat(ld) - dt.timedelta(days=days)).isoformat())
    return None if pv is None else lv - pv


def macro_data(key, days=800):
    """Every DASH series (transformed: yoy / bn) plus mechanical regime flags."""
    start = days_ago(days)
    data, errors = {}, {}
    for _, rows in DASH:
        for sid, label, kind in rows:
            try:
                obs = fred_series(sid, key, start)
            except SystemExit as e:
                errors[sid] = str(e)[:60]
                continue
            if kind == "yoy":
                obs = yoy_series(obs)
            if kind == "bn":
                obs = [(d, v / 1000) for d, v in obs]
            if obs:
                data[sid] = obs
    return {"data": data, "errors": errors, "flags": regime_flags(data), "plain": macro_plain(data)}


def cmd_macro(a):
    m = macro_data(fred_key(a.key_file))
    data = m["data"]
    print(f"\nMacro dashboard  (FRED, fetched {dt.date.today().isoformat()}; each row shows its own last date)")
    for section, rows in DASH:
        print(f"\n== {section} ==")
        print(f"  {'series':<40}{'last':>10}  {'date':<11}{'1m chg':>9}{'3m chg':>9}{'1y chg':>9}")
        for sid, label, kind in rows:
            if sid in m["errors"]:
                print(f"  {label:<40}  unavailable ({m['errors'][sid]})")
                continue
            obs = data.get(sid)
            if not obs:
                print(f"  {label:<40}  no data")
                continue
            ld, lv = obs[-1]

            def chg(days):
                c = change(obs, days)
                return "" if c is None else f"{c:+.2f}" if abs(lv) < 1000 else f"{c:+,.0f}"

            fmt = f"{lv:,.2f}" if abs(lv) < 10000 else f"{lv:,.0f}"
            print(f"  {label:<40}{fmt:>10}  {ld:<11}{chg(30):>9}{chg(91):>9}{chg(365):>9}")
    pl = m["plain"]
    print(f"\n== In plain English ({pl['stance']}) ==\n  Bottom line: {pl['bottom_line']}\n"
          f"  Next best action: {pl['action']['label']} -- {pl['action']['text']}")
    for p_ in pl["points"]:
        print(f"  - {p_['gauge']}: {p_['plain']}")
    if pl["watch"]:
        print("  Watch: " + "; ".join(pl["watch"]) + ".")
    print("\n== Regime read (mechanical flags -- interpret with references/macro-regimes.md) ==")
    for f in m["flags"]:
        print("  - " + f)
    print("\n  Rows lag by series (daily markets ~1 day, weekly ~1 week, monthly data ~2-6 weeks).")


def regime_flags(data):
    def last(sid):
        return data[sid][-1][1] if sid in data else None

    flags = []
    c210, c103m = last("T10Y2Y"), last("T10Y3M")
    if c210 is not None:
        flags.append(f"Curve 10y-2y {c210:+.2f}: " + ("inverted" if c210 < 0 else "positive")
                     + ("" if c103m is None else f"; 10y-3m {c103m:+.2f} " + ("inverted" if c103m < 0 else "positive")))
    ff, core = last("DFF"), last("PCEPILFE") or last("CPILFESL")
    if ff is not None and core is not None:
        rr = ff - core
        flags.append(f"Real policy rate ~ {rr:+.2f}% (fed funds - core inflation): "
                     + ("restrictive" if rr > 1 else "roughly neutral" if rr > -0.5 else "accommodative"))
    hy = last("BAMLH0A0HYM2")
    if hy is not None:
        flags.append(f"HY OAS {hy:.2f}%: " + ("very tight (complacent)" if hy < 3 else "tight" if hy < 3.5 else "normal" if hy < 5
                                                 else "stressed" if hy < 8 else "crisis"))
    vix = last("VIXCLS")
    if vix is not None:
        flags.append(f"VIX {vix:.1f}: " + ("calm" if vix < 15 else "normal" if vix < 22 else "elevated" if vix < 30
                                             else "stressed/panic"))
    nfci = last("NFCI")
    if nfci is not None:
        flags.append(f"NFCI {nfci:+.2f}: financial conditions " + ("tighter" if nfci > 0 else "looser") + " than average")
    if all(s in data for s in ("WALCL", "WTREGEN", "RRPONTSYD")):
        nl = last("WALCL") - last("WTREGEN") - last("RRPONTSYD")
        flags.append(f"'Net liquidity' proxy (Fed assets - TGA - RRP) ~ ${nl:,.0f}bn  [Contested: weak evidence as an equity predictor]")
    return flags


def macro_plain(data):
    """Plain-English read of the macro flags: stance, bottom line, next best action, one line per gauge, and what
    to watch. Mechanical thresholds (references/macro-regimes.md); a backdrop, not a timing signal."""
    def last(sid):
        return data[sid][-1][1] if data.get(sid) else None

    def chg30(sid):
        return change(data[sid], 30) if data.get(sid) else None
    pts, flash, support, severe = [], [], 0, False
    c210, c103m = last("T10Y2Y"), last("T10Y3M")
    if c210 is not None:
        inv = c210 < 0 or (c103m is not None and c103m < 0)
        flash += ["the yield curve"] * inv
        support += not inv
        pts.append(("Yield curve", "Short-term rates are above long-term ones (an 'inverted' curve), the classic recession "
                    "warning -- though the 2022-24 inversion turned out to be a false alarm." if inv else
                    "Long-term rates are a little above short-term ones, the normal shape: the bond market is not "
                    "signalling a recession."))
    ff, core = last("DFF"), last("PCEPILFE") or last("CPILFESL")
    if ff is not None and core is not None:
        rr = ff - core
        if rr > 1:
            flash.append("Fed policy")
            txt = f"The Fed's rate is {rr:.1f} points above inflation: it is leaning on the brakes, which slows growth over time."
        elif rr > -0.5:
            txt = f"The Fed's rate is about {rr:+.1f} points versus inflation: neither braking nor pushing the economy."
        else:
            support += 1
            txt = f"The Fed's rate is below inflation ({rr:+.1f} points): money is cheap, which helps prices but risks inflation."
        pts.append(("Fed policy", txt))
    hy, dhy = last("BAMLH0A0HYM2"), chg30("BAMLH0A0HYM2")
    if hy is not None:
        if hy < 3.5:
            support += 1
            txt = (f"Riskier companies pay only {hy:.1f} points more than the government to borrow: lenders aren't worried "
                   "about defaults. Good for stocks now, but there is little cushion if bad news arrives.")
        elif hy < 5:
            txt = f"Riskier companies pay {hy:.1f} points over government rates, an ordinary level of credit worry."
        else:
            flash.append("credit spreads")
            severe = severe or hy >= 8
            txt = f"Riskier companies pay {hy:.1f} points over government rates: lenders are nervous, which usually hurts stocks."
        if dhy is not None and dhy >= 0.5:
            flash.append("credit spreads widening")
            txt += f" The spread has widened {dhy:.1f} points in a month -- an early warning worth respecting."
        pts.append(("Credit", txt))
    vix = last("VIXCLS")
    if vix is not None:
        day = vix / 15.87
        if vix < 15:
            txt = f"Options price the S&P 500 to move about {day:.1f}% a day: calm. Calm can last, but it often ends abruptly."
        elif vix < 22:
            txt = f"Options price the S&P 500 to move about {day:.1f}% a day: average -- not calm, not fearful."
        else:
            flash.append("the VIX")
            severe = severe or vix >= 30
            txt = f"Options price the S&P 500 to move about {day:.1f}% a day: {'fearful' if vix >= 30 else 'nervous'}; expect bigger swings and smaller safe position sizes."
        spx = [v for _, v in (data.get("SP500") or [])][-22:]
        if len(spx) >= 15:
            lr =[math.log(b / a) for a, b in zip(spx, spx[1:]) if a > 0 and b > 0]
            rv = statistics.stdev(lr) * math.sqrt(252) * 100 if len(lr) > 2 else None
            if rv and rv > vix * 1.15:
                txt += (f" But the index has actually been swinging more ({rv:.0f}% annualized over the last month vs the VIX's "
                        f"{vix:.0f}): options look cheap next to recent moves, and position sizes should follow the bigger, realized swings.")
            elif rv and rv < vix * 0.6:
                txt += f" Recent swings have been smaller ({rv:.0f}% annualized): options carry a fear premium."
        pts.append(("Volatility (VIX)", txt))
    nfci = last("NFCI")
    if nfci is not None:
        flash += ["financial conditions"] * (nfci > 0)
        support += nfci <= 0
        pts.append(("Financial conditions", "Borrowing and funding are easier than average: money is flowing." if nfci <= 0 else
                    "Borrowing and funding are tighter than average: money is harder to get, a headwind for risk assets."))
    oil, ovx = last("DCOILBRENTEU"), last("OVXCLS")
    d1y = change(data["DCOILBRENTEU"], 365) if data.get("DCOILBRENTEU") else None
    if oil is not None and d1y is not None and oil - d1y > 0:
        up = d1y / (oil - d1y)
        shock = up >= 0.3 or (ovx is not None and ovx >= 40)
        flash += ["oil"] * shock
        txt = f"Brent oil is ${oil:,.0f}, {'up' if up >= 0 else 'down'} {abs(up):.0%} in a year"
        txt += (f", and oil options price big swings (OVX {ovx:.0f})" if ovx is not None and ovx >= 40 else "")
        txt += (": an oil shock feeds inflation and squeezes growth, the mix that hurts stocks and bonds together."
                if shock else ": not a macro problem at this level.")
        pts.append(("Oil", txt))
    if all(data.get(s_) for s_ in ("WALCL", "WTREGEN", "RRPONTSYD")):
        pts.append(("'Net liquidity'", "A popular gauge of cash the Fed adds to the system; the evidence that it predicts "
                    "stocks is weak, so don't trade off it."))
    caution = len(flash)
    if severe or caution >= 3:
        stance, label = "risk-off", "Reduce risk"
        act = "Cut position sizes, favour defined-risk trades and cash, and wait for credit and volatility to calm."
    elif caution == 2:
        stance, label = "mixed", "Trade smaller"
        act = f"Keep trading your rules at reduced size and favour quality; {flash[0]} and {flash[1]} are flashing."
    elif caution == 1:
        stance, label = "mostly supportive", "Stay invested, stay alert"
        act = f"No macro reason to cut exposure, but keep an eye on {flash[0]}, the one gauge flashing."
    else:
        stance, label = "supportive", "Stay invested, follow your trend rules"
        act = "Macro gives no reason to cut stock exposure; let your trend and stop rules do the work."
    calm = {"supportive": "calm and supportive", "mostly supportive": f"mostly supportive, with one warning light: {flash[0] if flash else ''}",
            "mixed": f"mixed: {' and '.join(flash[:2])} are flashing", "risk-off": "stressed: " + ", ".join(flash)}[stance]
    bottom = f"The economy-and-markets backdrop looks {calm}."
    if stance in ("supportive", "mostly supportive") and hy is not None and hy < 3.5:
        bottom += " The other risk is complacency: lenders are charging very little for risk." if flash else \
            " The main risk is complacency: lenders are charging very little for risk."
    watch = []
    if hy is not None:
        watch.append(f"junk-bond spreads rising toward {max(4.0, hy + 1):.1f}% or widening 0.5 points in a month")
    if vix is not None:
        watch.append("the VIX staying above 25" if vix < 25 else "the VIX falling back below 20")
    if c210 is not None and c210 >= 0:
        watch.append("the yield curve turning negative again")
    if nfci is not None and nfci <= 0:
        watch.append("NFCI rising above zero")
    if oil is not None and any(p_[0] == "Oil" and "shock" in p_[1] for p_ in pts):
        watch.append(f"Brent holding above ${oil:,.0f} or core inflation turning up")
    return {"stance": stance, "flashing": flash, "bottom_line": bottom, "action": {"label": label, "text": act},
            "points": [{"gauge": g, "plain": t} for g, t in pts], "watch": watch}


def cmd_fred(a):
    key = fred_key(a.key_file)
    merged: dict[str, dict[str, float]] = {}
    for sid in a.series:
        obs = fred_series(sid.upper(), key, a.start)
        if a.yoy:
            obs = yoy_series(obs)
        for d, v in obs:
            merged.setdefault(d, {})[sid.upper()] = v
        if obs:
            print(f"  {sid.upper():<16} {len(obs):>6} obs  {obs[0][0]} .. {obs[-1][0]}  last {obs[-1][1]:,.4g}")
        else:
            print(f"  {sid.upper():<16} no observations")
    if a.out:
        cols = [s.upper() for s in a.series]
        with open(a.out, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["date"] + cols)
            for d in sorted(merged):
                w.writerow([d] + [merged[d].get(c, "") for c in cols])
        print(f"  wrote {a.out}")


def cmd_search(a):
    key = fred_key(a.key_file)
    js = fred_get("series/search", key, search_text=a.text, limit=a.limit, order_by="popularity", sort_order="desc")
    for s in js.get("seriess", []):
        print(f"  {s['id']:<20} {s['frequency_short']:<3} {s['observation_end']}  {s['title'][:80]}  [{s['units_short']}]")


# --------------------------------------------------------------------------- prices
def yahoo_history(symbol: str, years: float):
    # explicit period1/period2: Yahoo silently returns monthly/quarterly bars for range=max
    p2 = int(dt.datetime.now(dt.timezone.utc).timestamp())
    p1 = max(0, int(p2 - years * 365.25 * 86400))
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}"
           f"?period1={p1}&period2={p2}&interval=1d&events=div%2Csplits&includeAdjustedClose=true")
    js = http_json(url)
    res = js["chart"]["result"][0]
    ts = res["timestamp"]
    reg = res.get("meta", {}).get("currentTradingPeriod", {}).get("regular", {})
    session_open = bool(reg) and reg.get("start", 0) <= dt.datetime.now(dt.timezone.utc).timestamp() < reg.get("end", 0)
    q = res["indicators"]["quote"][0]
    adj = res["indicators"].get("adjclose", [{}])[0].get("adjclose")
    rows = []
    for i, t in enumerate(ts):
        o, h, l, c, v = q["open"][i], q["high"][i], q["low"][i], q["close"][i], q["volume"][i]
        if None in (o, h, l, c):
            continue
        d = dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat()
        rows.append([d, o, h, l, c, v or 0, adj[i] if adj and adj[i] is not None else c])
    if rows and session_open and ts[-1] >= reg.get("start", 0):
        rows[-1].append("partial")  # today's session is still trading
    return rows


YAHOO_CHART = "https://query1.finance.yahoo.com/v8/finance/chart/"
INTRADAY_RANGES = ("5d", "1mo", "3mo", "6mo", "1y", "2y")  # Yahoo serves 1h bars for the last 730 days


def yahoo_chart(symbol: str, **params):
    """Raw Yahoo chart result (meta, timestamp, indicators). A bad symbol raises ValueError with a readable hint."""
    try:
        js = http_json(f"{YAHOO_CHART}{urllib.parse.quote(symbol)}?{urllib.parse.urlencode(params)}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError(f"No Yahoo data for '{symbol}'. Check the symbol (Yahoo style: BTC-USD, ES=F, "
                             "EURUSD=X, BRK-B).") from e
        raise
    res = (js.get("chart") or {}).get("result") or []
    if not res:
        raise ValueError(f"Yahoo returned nothing for '{symbol}': {(js.get('chart') or {}).get('error')}")
    return res[0]


def exchange_tz(meta: dict):
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(meta["exchangeTimezoneName"])
    except Exception:  # noqa: BLE001 -- no tzdata: fall back to the current offset
        return dt.timezone(dt.timedelta(seconds=meta.get("gmtoffset") or 0))


INTERVAL_SECS = {"1m": 60, "2m": 120, "5m": 300, "15m": 900, "30m": 1800, "1h": 3600}
INTRADAY_DAYS = {"1m": 7, "2m": 59, "5m": 59, "15m": 59, "30m": 59}  # Yahoo's lookback limits for minute bars
RANGE_DAYS = {"5d": 5, "1mo": 31, "3mo": 92, "6mo": 183, "1y": 366, "2y": 729}


def yahoo_bars(symbol: str, interval: str = "1d", years: float = 3.0, rng: str = "1mo", prepost: bool = False,
               days: float | None = None):
    """Bars that keep the in-progress bar: (rows, partial, meta), rows = [ts, label, o, h, l, c, v].
    Daily bars are dividend/split adjusted and labelled YYYY-MM-DD; intraday bars (1m 2m 5m 15m 30m 1h) are raw
    (Yahoo has no intraday adjusted close), labelled 'YYYY-MM-DD HH:MM' (bar start) in exchange-local time.
    Minute bars reach back 7 days (1m) or 59 days (2m-30m); `days` sets the lookback, else `rng`.
    prepost=True adds pre-market and after-hours bars (minute intervals only)."""
    secs = INTERVAL_SECS.get(interval)
    p2 = int(dt.datetime.now(dt.timezone.utc).timestamp())
    if interval == "1h":
        res = yahoo_chart(symbol, interval="1h", range=rng if rng in INTRADAY_RANGES else "1mo")
    elif secs:
        lim = INTRADAY_DAYS[interval]
        want = min(lim, days if days else RANGE_DAYS.get(rng, 31))
        res = yahoo_chart(symbol, interval=interval, period1=int(p2 - want * 86400), period2=p2,
                          includePrePost="true" if prepost else "false")
    else:
        res = yahoo_chart(symbol, interval="1d", period1=max(0, int(p2 - years * 365.25 * 86400)), period2=p2,
                          events="div,splits", includeAdjustedClose="true")
    meta, ts = res["meta"], res.get("timestamp") or []
    tz, qt = exchange_tz(meta), res["indicators"]["quote"][0]
    adj = (res["indicators"].get("adjclose") or [{}])[0].get("adjclose")
    rows = []
    for i, t in enumerate(ts):
        o, h, l, c, v = (qt[k][i] for k in ("open", "high", "low", "close", "volume"))
        if None in (o, h, l, c):
            continue
        if secs:
            # Yahoo stamps the live bar with the last trade time; snap it to its slot. Hourly slots start at the
            # session open (09:30, 10:30 ...), minute slots on the clock.
            t -= (t - ts[0]) % secs if interval == "1h" else t % secs
            label = dt.datetime.fromtimestamp(t, tz).strftime("%Y-%m-%d %H:%M")
            if rows and rows[-1][1] == label:  # merge a duplicate slot
                r = rows[-1]
                r[3], r[4], r[5], r[6] = max(r[3], h), min(r[4], l), c, r[6] + int(v or 0)
                continue
            f = 1.0
        else:
            label = dt.datetime.fromtimestamp(t, tz).strftime("%Y-%m-%d")
            f = adj[i] / c if adj and adj[i] is not None and c else 1.0
        rows.append([t, label, o * f, h * f, l * f, c * f, int(v or 0)])
    if not rows:
        raise ValueError(f"Yahoo returned no bars for '{symbol}'.")
    if secs:
        meta["volume_fixed"] = _repair_volume(symbol, rows, meta, interval)
    ctp = meta.get("currentTradingPeriod") or {}
    reg = ctp.get("regular") or {}
    now, last = dt.datetime.now(dt.timezone.utc).timestamp(), rows[-1][0]
    if secs:
        end = last + secs
        sess_end = (ctp.get("post") or reg).get("end", 0) if prepost else reg.get("end", 0)
        if reg.get("start", 0) <= last < sess_end:
            end = min(end, sess_end)
    else:
        end = reg.get("end", 0) if last >= reg.get("start", float("inf")) else 0
    return rows, now < end, meta


def _repair_volume(symbol, rows, meta, interval):
    """Yahoo sometimes stores the running day total as a bar's volume during the live session (e.g. 301M, 318M,
    341M ... on 5-minute bars that trade ~10M). It inflates relative volume and drags VWAP. When today's bar volumes
    sum to well over the quote's session volume, replace bars that look like a running total with the median of
    the recent clean bars (minute bars), or rebuild today's hourly volumes from repaired 5-minute bars (1h).
    Returns the number of bars repaired."""
    reg = (meta.get("currentTradingPeriod") or {}).get("regular") or {}
    vq = meta.get("regularMarketVolume")
    today = [r for r in rows if reg.get("start", 0) <= r[0] < reg.get("end", 0)]
    if not vq or not today or sum(r[6] for r in today) <= 1.3 * vq:
        return 0
    if interval == "1h":
        try:
            fine, _, _ = yahoo_bars(symbol, "5m", days=1)
        except ValueError:
            return 0
        starts = [r[0] for r in today]
        vol = {t: 0 for t in starts}
        for f in fine:
            if reg["start"] <= f[0] < reg["end"]:
                slot = max([t for t in starts if t <= f[0]], default=None)
                if slot is not None:
                    vol[slot] += f[6]
        for r in today:
            r[6] = vol[r[0]]
        return len(today)
    clean, cum, fixed = [], 0, 0
    for r in today:
        v = r[6]
        if clean and cum > 0:
            med = statistics.median(clean[-12:])
            if v > 5 * max(med, 1) and 0.4 * cum <= v <= 1.6 * cum:
                v = r[6] = int(med)
                fixed += 1
        clean.append(v)
        cum += v
    if cum > 1.15 * vq:  # still too high (filled bars run above the true ones): keep the shape, match the quote's total
        for r in today:
            r[6] = int(r[6] * vq / cum)
        fixed = fixed or len(today)
    return fixed


_YAHOO_SESSION = {}


def _yahoo_crumb():
    """Cookie + crumb that Yahoo's options endpoint requires (no account, no key)."""
    if "op" not in _YAHOO_SESSION:
        import http.cookiejar  # noqa: PLC0415
        op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        try:
            op.open(urllib.request.Request("https://fc.yahoo.com", headers=UA), timeout=20)
        except urllib.error.HTTPError:
            pass  # a 404 still sets the cookie
        crumb = op.open(urllib.request.Request("https://query2.finance.yahoo.com/v1/test/getcrumb", headers=UA),
                        timeout=20).read().decode()
        _YAHOO_SESSION.update(op=op, crumb=crumb)
    return _YAHOO_SESSION["op"], _YAHOO_SESSION["crumb"]


def option_chain(symbol: str, expiry: str | None = None) -> dict:
    """Listed options from Yahoo (unofficial, delayed ~15 min): {spot, expiries[YYYY-MM-DD], expiry, calls, puts}.
    Each contract: strike, bid, ask, mid, last, iv, oi, volume, itm. expiry=None -> the nearest expiry; a date with
    no listing -> the first expiry on or after it."""
    url = f"https://query2.finance.yahoo.com/v7/finance/options/{urllib.parse.quote(symbol)}?"

    def get(params):
        for attempt in (0, 1):
            op, crumb = _yahoo_crumb()
            try:
                req = urllib.request.Request(url + urllib.parse.urlencode({**params, "crumb": crumb}), headers=UA)
                js = json.loads(op.open(req, timeout=30).read().decode())
                return ((js.get("optionChain") or {}).get("result") or [None])[0]
            except urllib.error.HTTPError as e:
                if e.code != 401 or attempt:
                    raise
                _YAHOO_SESSION.clear()  # stale crumb: get a new one once

    res = get({})
    if not res or not res.get("expirationDates"):
        raise ValueError(f"No listed options for '{symbol}' on Yahoo.")
    exps = res["expirationDates"]
    iso = [dt.datetime.fromtimestamp(e, dt.timezone.utc).date().isoformat() for e in exps]
    pick = exps[0]
    if expiry:
        later = [e for e, d in zip(exps, iso) if d >= expiry]
        pick = later[0] if later else exps[-1]
    if pick != ((res.get("options") or [{}])[0]).get("expirationDate"):
        res = get({"date": pick})

    def legs(xs):
        rows = []
        for o in xs:
            b, k = o.get("bid") or 0.0, o.get("ask") or 0.0
            rows.append({"strike": o["strike"], "bid": b, "ask": k, "mid": (b + k) / 2 if k else o.get("lastPrice"),
                         "last": o.get("lastPrice"), "iv": o.get("impliedVolatility"), "oi": o.get("openInterest") or 0,
                         "volume": o.get("volume") or 0, "itm": bool(o.get("inTheMoney"))})
        return rows
    opt = (res.get("options") or [{}])[0]
    return {"symbol": symbol, "spot": (res.get("quote") or {}).get("regularMarketPrice"), "expiries": iso,
            "expiry": dt.datetime.fromtimestamp(pick, dt.timezone.utc).date().isoformat(),
            "calls": legs(opt.get("calls") or []), "puts": legs(opt.get("puts") or [])}


def _yjson(url, body=None):
    """GET/POST a Yahoo JSON endpoint with the cookie + crumb session (retries once on a stale crumb)."""
    for attempt in (0, 1):
        op, crumb = _yahoo_crumb()
        u = url + ("&" if "?" in url else "?") + "crumb=" + urllib.parse.quote(crumb)
        hdr = dict(UA, **({"Content-Type": "application/json"} if body is not None else {}))
        try:
            req = urllib.request.Request(u, data=json.dumps(body).encode() if body is not None else None, headers=hdr)
            return json.loads(op.open(req, timeout=30).read().decode())
        except urllib.error.HTTPError as e:
            if e.code != 401 or attempt:
                raise
            _YAHOO_SESSION.clear()


MAJOR_EXCHANGES = ("NMS", "NGM", "NCM", "NYQ", "ASE", "PCX", "BTS")  # Nasdaq tiers, NYSE, NYSE American, Arca, Cboe BZX


def yahoo_screen(min_change=10.0, price_lo=2.0, price_hi=20.0, min_volume=0, size=250):
    """US-listed stocks up at least min_change% today within a price band (Yahoo's screener; regular session,
    delayed). Returns quote dicts with price, change %, volume, average volumes, shares outstanding, market cap."""
    ops = [{"operator": "GT", "operands": ["percentchange", min_change]},
           {"operator": "BTWN", "operands": ["intradayprice", price_lo, price_hi]},
           {"operator": "EQ", "operands": ["region", "us"]},
           {"operator": "OR", "operands": [{"operator": "EQ", "operands": ["exchange", x]} for x in MAJOR_EXCHANGES]}]
    if min_volume:
        ops.append({"operator": "GT", "operands": ["dayvolume", min_volume]})
    body = {"offset": 0, "size": size, "sortField": "percentchange", "sortType": "DESC", "quoteType": "EQUITY",
            "query": {"operator": "AND", "operands": ops}, "userId": "", "userIdType": "guid"}
    res = ((_yjson("https://query2.finance.yahoo.com/v1/finance/screener", body).get("finance") or {}).get("result") or [{}])[0]
    rows = []
    for q in res.get("quotes") or []:
        rows.append({"symbol": q["symbol"], "name": q.get("shortName") or q.get("longName") or q["symbol"],
                     "exchange": q.get("exchange"), "price": q.get("regularMarketPrice"),
                     "change_pct": (q.get("regularMarketChangePercent") or 0) / 100, "volume": q.get("regularMarketVolume") or 0,
                     "avg_vol_3m": q.get("averageDailyVolume3Month") or 0, "avg_vol_10d": q.get("averageDailyVolume10Day") or 0,
                     "shares_out": q.get("sharesOutstanding"), "mcap": q.get("marketCap"), "open": q.get("regularMarketOpen"),
                     "prev_close": q.get("regularMarketPreviousClose"), "high": q.get("regularMarketDayHigh"),
                     "low": q.get("regularMarketDayLow"), "state": q.get("marketState"), "time": q.get("regularMarketTime"),
                     "delay_min": q.get("exchangeDataDelayedBy")})
    return rows


def yahoo_universe(mcap_lo=50e6, mcap_hi=2e9, price_lo=1.0, min_dollar_volume=250e3, limit=6000):
    """US-listed stocks in a market-cap band (Yahoo's screener, paged 250 at a time), for building a small- or
    micro-cap universe. Keeps names whose 3-month average dollar volume clears min_dollar_volume. Returns dicts
    with symbol, name, exchange, price, mcap, avg_vol_3m and dollar_volume, largest first."""
    ops = [{"operator": "BTWN", "operands": ["intradaymarketcap", mcap_lo, mcap_hi]},
           {"operator": "GT", "operands": ["intradayprice", price_lo]},
           {"operator": "EQ", "operands": ["region", "us"]},
           {"operator": "OR", "operands": [{"operator": "EQ", "operands": ["exchange", x]} for x in MAJOR_EXCHANGES]}]
    rows, offset = [], 0
    while offset < limit:
        body = {"offset": offset, "size": 250, "sortField": "intradaymarketcap", "sortType": "DESC", "quoteType": "EQUITY",
                "query": {"operator": "AND", "operands": ops}, "userId": "", "userIdType": "guid"}
        res = ((_yjson("https://query2.finance.yahoo.com/v1/finance/screener", body).get("finance") or {}).get("result") or [{}])[0]
        page = res.get("quotes") or []
        for q in page:
            px, av = q.get("regularMarketPrice") or 0, q.get("averageDailyVolume3Month") or 0
            if px * av >= min_dollar_volume:
                rows.append({"symbol": q["symbol"], "name": q.get("shortName") or q.get("longName") or q["symbol"],
                             "exchange": q.get("exchange"), "price": px, "mcap": q.get("marketCap"), "avg_vol_3m": av,
                             "dollar_volume": px * av})
        offset += len(page)
        if len(page) < 250 or offset >= (res.get("total") or 0):
            break
    return rows


def key_stats(symbol):
    """Float, shares outstanding and short interest from Yahoo's key statistics (None where Yahoo has nothing)."""
    js = _yjson(f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(symbol)}"
                "?modules=defaultKeyStatistics")
    ks = (((js.get("quoteSummary") or {}).get("result") or [{}])[0] or {}).get("defaultKeyStatistics") or {}

    def raw(k):
        return ks[k].get("raw") if isinstance(ks.get(k), dict) else None
    return {"float": raw("floatShares"), "shares_out": raw("sharesOutstanding"), "short_pct_float": raw("shortPercentOfFloat"),
            "short_ratio": raw("shortRatio")}


LIST_HEADLINE = re.compile(r"\b(top|biggest|notable)\b.*\b(gainers|losers|movers)\b|stocks? (moving|to watch|making)|"
                           r"(pre-?market|mid-?day|after-?hours) (movers|gainers)|\bmovers\b|^\d+ .*\bstocks\b|"
                           r"\bstocks? (with|that|to buy|under)\b", re.I)
COMMENTARY = ("simply wall st", "zacks", "marketbeat", "motley fool", "moby", "stocktwits", "insider monkey", "benzinga")
ASCII_PUNCT = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-",
                             "…": "...", "\xa0": " "})
DILUTION = re.compile(r"offering|registered direct|private placement|warrant|at-the-market|\bATM\b|shelf|"
                      r"reverse (stock )?split|going concern|delist|nasdaq (deficiency|notice)|convertible", re.I)


def news(symbol, n=8):
    """Recent Yahoo Finance headlines for a symbol: title, publisher, age in hours, link. Flags 'list' articles
    (top-gainer roundups, not catalysts) and dilution or listing red flags."""
    js = http_json(f"https://query2.finance.yahoo.com/v1/finance/search?q={urllib.parse.quote(symbol)}"
                   f"&newsCount={n}&quotesCount=0")
    now = dt.datetime.now(dt.timezone.utc).timestamp()
    items = []
    for x in js.get("news") or []:
        rel = x.get("relatedTickers") or []
        if rel and symbol.upper() not in [t.upper() for t in rel]:
            continue
        t = x.get("providerPublishTime") or 0
        title = (x.get("title") or "").translate(ASCII_PUNCT)
        pub = x.get("publisher") or ""
        items.append({"title": title, "publisher": pub, "commentary": pub.lower().startswith(COMMENTARY), "age_h": (now - t) / 3600 if t else None,
                      "link": x.get("link"), "list": bool(LIST_HEADLINE.search(title)), "dilution": bool(DILUTION.search(title))})
    return items


def quote(symbol: str) -> dict:
    """Latest price: regular-session price, change vs previous close, session state, quote age, and the latest
    pre/after-hours print when it is newer than the regular-session price. Yahoo, unofficial; some feeds lag."""
    res = yahoo_chart(symbol, interval="1m", range="1d", includePrePost="true")
    m, now = res["meta"], dt.datetime.now(dt.timezone.utc).timestamp()
    tz = exchange_tz(m)
    price, t = m.get("regularMarketPrice"), m.get("regularMarketTime")
    prev = m.get("previousClose") or m.get("chartPreviousClose")
    ctp = m.get("currentTradingPeriod") or {}

    def inside(k):
        p = ctp.get(k) or {}
        return p.get("start", 0) <= now < p.get("end", 0)
    state = "open" if inside("regular") else "pre-market" if inside("pre") else "after hours" if inside("post") else "closed"
    ext = None
    closes = res["indicators"]["quote"][0].get("close") or []
    for t_, c_ in zip(reversed(res.get("timestamp") or []), reversed(closes)):
        if c_ is not None:
            if t and price and t_ > t + 60:
                ext = {"price": c_, "change_pct": c_ / price - 1,
                       "time": dt.datetime.fromtimestamp(t_, tz).strftime("%Y-%m-%d %H:%M")}
            break
    local = dt.datetime.fromtimestamp(t, tz) if t else None
    return {"symbol": symbol, "name": m.get("longName") or m.get("shortName") or symbol, "currency": m.get("currency"),
            "exchange": m.get("fullExchangeName") or m.get("exchangeName"), "type": m.get("instrumentType"),
            "price": price, "prev_close": prev, "change": price - prev if price and prev else None,
            "change_pct": price / prev - 1 if price and prev else None, "ts": t,
            "time": local.strftime("%Y-%m-%d %H:%M:%S") if local else None, "tz": m.get("timezone"),
            "tzname": m.get("exchangeTimezoneName"),
            "age_s": now - t if t else None, "state": state, "ext": ext,
            "day_high": m.get("regularMarketDayHigh"), "day_low": m.get("regularMarketDayLow"),
            "volume": m.get("regularMarketVolume"), "w52_high": m.get("fiftyTwoWeekHigh"),
            "w52_low": m.get("fiftyTwoWeekLow")}


def cmd_quote(a):
    for sym in a.symbols:
        try:
            q = quote(sym)
        except ValueError as e:
            print(f"  {sym}: {e}")
            continue
        age = q["age_s"] or 0
        stale = "  [no update for %d min: feed likely delayed]" % (age // 60) if q["state"] == "open" and age > 300 else ""
        d = 4 if q["price"] and abs(q["price"]) < 10 else 2  # FX and low-priced symbols need more decimals
        chg = f"{q['change']:+,.{d}f} ({q['change_pct']:+.2%})" if q["change"] is not None else "n/a"
        rows = [("Price", f"{q['price']:,.4f} {q['currency'] or ''}  {chg} vs prev close {q['prev_close']:,.4f}"),
                ("As of", f"{q['time']} {q['tz']} ({age:.0f} s ago), session {q['state']}{stale}"),
                ("Day range", f"{q['day_low']:,.4f} - {q['day_high']:,.4f}") if q["day_low"] else None,
                ("52-week range", f"{q['w52_low']:,.4f} - {q['w52_high']:,.4f}") if q["w52_low"] else None,
                ("Extended hours", f"{q['ext']['price']:,.4f} ({q['ext']['change_pct']:+.2%}) at {q['ext']['time']}")
                if q["ext"] else None]
        out([r for r in rows if r], f"{sym}: {q['name']} ({q['exchange']}, {q['type']})")
    print("\n  Yahoo (unofficial). Futures and some exchanges are delayed ~10-15 min; not for live order decisions.")


def cmd_prices_intraday(a):
    try:
        rows, partial, meta = yahoo_bars(a.symbol, a.interval, rng=a.range, prepost=a.prepost, days=a.days)
    except ValueError as e:
        sys.exit(str(e))
    dropped = rows.pop() if partial and not a.include_partial and len(rows) > 1 else None
    out_path = a.out or f"{a.symbol.replace('^', '').replace('=', '_')}_{a.interval}.csv"
    with open(out_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date", "open", "high", "low", "close", "volume"])
        w.writerows([r[1]] + [round(x, 6) for x in r[2:6]] + [r[6]] for r in rows)
    tzname = meta.get("exchangeTimezoneShortName") or meta.get("timezone") or ""
    days = len({r[1][:10] for r in rows})
    print(f"  {a.symbol}: {len(rows)} {a.interval} bars over {days} days, {rows[0][1]} .. {rows[-1][1]} {tzname} "
          f"(bar start times; raw, unadjusted{'; incl. pre/after-hours' if a.prepost else ''}) from yahoo; "
          f"last close {rows[-1][5]:,.4f} -> {out_path}")
    if dropped:
        print(f"  dropped the still-forming {dropped[1]} bar (close so far {dropped[5]:,.4f}); --include-partial keeps it")
    if a.interval == "1h":
        print("  Indicator periods now count hours: pass --ppy to techkit for annualized figures "
              "(~1,640 for US stocks at 6.5 bars/day; 8,760 for crypto).")
    else:
        print(f"  Yahoo keeps {INTRADAY_DAYS[a.interval]} days of {a.interval} bars: fine for levels and a first look, "
              "too short to prove a day-trading edge (use 1h bars for ~2 years, or the user's broker/vendor history).")


def cmd_prices(a):
    if a.interval != "1d":
        return cmd_prices_intraday(a)
    try:
        rows = yahoo_history(a.symbol, a.years)
    except Exception as e:  # noqa: BLE001
        sys.exit(f"no data for {a.symbol}: {e}. Check the symbol format (SPY, ^GSPC, ES=F, BTC-USD, EURUSD=X) "
                 "or supply your own CSV (date,open,high,low,close,volume).")
    if not rows:
        sys.exit(f"no bars returned for {a.symbol}")
    dropped = None
    if len(rows[-1]) > 7 and not a.include_partial:
        dropped = rows.pop()
    src = "yahoo"
    if a.adjust:  # scale OHLC by adjclose/close so splits/dividends don't create fake gaps
        for r in rows:
            f = r[6] / r[4] if r[4] else 1
            r[1], r[2], r[3], r[4] = r[1] * f, r[2] * f, r[3] * f, r[6]
    out = a.out or f"{a.symbol.replace('^', '').replace('=', '_')}.csv"
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date", "open", "high", "low", "close", "volume"])
        for r in rows:
            w.writerow([r[0]] + [round(x, 6) for x in r[1:5]] + [int(r[5])])
    last = rows[-1]
    print(f"  {a.symbol}: {len(rows)} bars {rows[0][0]} .. {last[0]} from {src}"
          f"{' (adjusted)' if a.adjust else ''}; last close {last[4]:,.4f} -> {out}")
    if len(rows) > 20:
        gaps = sorted((dt.date.fromisoformat(rows[i][0]) - dt.date.fromisoformat(rows[i - 1][0])).days
                      for i in range(1, len(rows)))
        if gaps[len(gaps) // 2] > 3:
            print(f"  WARNING: median gap between bars is {gaps[len(gaps) // 2]} days -- these are not daily bars")
    if dropped:
        print(f"  dropped today's in-progress bar ({dropped[0]}, last {dropped[4]:,.4f}); --include-partial keeps it")
    elif len(rows[-1]) > 7:
        print(f"  WARNING: last bar ({rows[-1][0]}) is an in-progress session")
    print("  note: unofficial endpoint; may be delayed. Daily bars only.")


def cmd_options(a):
    exp = a.expiry
    if a.dte is not None:
        exp = (dt.date.today() + dt.timedelta(days=a.dte)).isoformat()
    try:
        ch = option_chain(a.symbol, exp)
    except (ValueError, urllib.error.URLError) as e:
        sys.exit(f"{a.symbol}: {e}")
    spot = ch["spot"]
    dte = (dt.date.fromisoformat(ch["expiry"]) - dt.date.today()).days
    print(f"\n== {a.symbol} options, expiry {ch['expiry']} ({dte} days), spot {spot:,.2f} ==")
    print(f"  expiries: {', '.join(ch['expiries'][:12])}{' ...' if len(ch['expiries']) > 12 else ''}")
    for side in (("puts", "calls") if a.type == "both" else (a.type + "s",)):
        legs = sorted(ch[side], key=lambda o: o["strike"])
        if not legs:
            continue
        i = min(range(len(legs)), key=lambda j: abs(legs[j]["strike"] - spot))
        print(f"\n  {side.upper():<6}{'strike':>9}{'bid':>9}{'ask':>9}{'mid':>9}{'spread':>8}{'IV':>7}{'OI':>9}{'vol':>8}")
        for o in legs[max(0, i - a.near): i + a.near + 1]:
            spr = (o["ask"] - o["bid"]) / o["mid"] if o["mid"] else float("nan")
            iv = f"{o['iv']:.0%}" if o["iv"] else "n/a"
            mark = "*" if o is legs[i] else " "
            print(f"  {mark:<6}{o['strike']:>9,.2f}{o['bid']:>9.2f}{o['ask']:>9.2f}{(o['mid'] or 0):>9.2f}"
                  f"{spr:>8.0%}{iv:>7}{o['oi']:>9,}{o['volume']:>8,}")
    if a.out:
        with open(a.out, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["type", "expiry", "strike", "bid", "ask", "mid", "last", "iv", "oi", "volume"])
            for side in ("puts", "calls"):
                for o in ch[side]:
                    w.writerow([side[:-1], ch["expiry"], o["strike"], o["bid"], o["ask"], o["mid"], o["last"], o["iv"],
                                o["oi"], o["volume"]])
        print(f"\n  wrote {a.out}")
    print("\n  Yahoo (unofficial, ~15 min delayed). Yahoo's IV is from its own model; zero bids mean no real market. "
          "Check the live chain at your broker before trading.")


# --------------------------------------------------------------------------- geopolitical risk index
GPR_URLS = {"monthly": "https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls",
            "daily": "https://www.matteoiacoviello.com/gpr_files/data_gpr_daily_recent.xls"}


def cmd_gpr(a):
    """Caldara-Iacoviello Geopolitical Risk index (free download, .xls)."""
    url = GPR_URLS[a.freq]
    raw = a.out_xls or os.path.basename(url)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r, open(raw, "wb") as fh:
        fh.write(r.read())
    try:
        import xlrd  # noqa: PLC0415 -- pure Python, no other dependencies
    except ImportError as e:
        sys.exit(f"  saved {raw}, but reading .xls needs xlrd ({e}). Install with `pip install xlrd`, "
                 "or open the file in Excel and save as CSV.")
    book = xlrd.open_workbook(raw)
    sh = book.sheet_by_index(0)
    head = [str(x).strip() for x in sh.row_values(0)]
    low = [h.lower() for h in head]
    di = next((low.index(k) for k in ("day", "month", "date") if k in low), 0)  # DAY (YYYYMMDD) before 'date' serials
    keep = [i for i, h in enumerate(head) if h.upper().startswith("GPR") and "_" not in h][:6]
    keep = keep or [i for i, h in enumerate(head) if h.upper().startswith("GPR")][:6]

    def day(c):
        if c.ctype == xlrd.XL_CELL_DATE:
            return xlrd.xldate_as_datetime(c.value, book.datemode).strftime("%Y-%m-%d")
        s = str(int(c.value)) if c.ctype == xlrd.XL_CELL_NUMBER else str(c.value).strip()
        return f"{s[:4]}-{s[4:6]}-{s[6:8]}" if len(s) == 8 and s.isdigit() else s[:10]
    rows = []
    for r in range(1, sh.nrows):
        cells = sh.row(r)
        if cells[keep[0]].ctype != xlrd.XL_CELL_NUMBER:  # months before the index starts are blank
            continue
        rows.append([day(cells[di])] + [cells[i].value if cells[i].ctype == xlrd.XL_CELL_NUMBER else "" for i in keep])
    names = [head[i] for i in keep]
    out_csv = a.out or f"gpr_{a.freq}.csv"
    with open(out_csv, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date"] + names)
        w.writerows(rows)
    hist = [x[1] for x in rows]
    pctile = sum(1 for x in hist if x <= hist[-1]) / len(hist)
    print(f"  GPR {a.freq}: {len(rows)} rows {rows[0][0]} .. {rows[-1][0]}; columns {names}")
    print(f"  latest {names[0]} = {hist[-1]:.1f} (percentile {pctile:.0%} of history; 100 = 1985-2019 average)")
    print(f"  wrote {out_csv}  (source: Caldara & Iacoviello, matteoiacoviello.com/gpr.htm)")


# --------------------------------------------------------------------------- SEC EDGAR fundamentals & earnings dates
# data.sec.gov works with a generic User-Agent; the ticker->CIK file on www.sec.gov needs a contact address,
# so common names are mapped here and SEC_USER_AGENT (e.g. "Jane Doe jane@example.org") unlocks the full lookup.
CIK_MAP = {"AAPL": 320193, "MSFT": 789019, "NVDA": 1045810, "AMZN": 1018724, "GOOGL": 1652044, "GOOG": 1652044,
           "META": 1326801, "TSLA": 1318605, "AVGO": 1730168, "BRK-B": 1067983, "JPM": 19617, "LLY": 59478,
           "V": 1403161, "UNH": 731766, "XOM": 34088, "MA": 1141391, "COST": 909832, "HD": 354950, "PG": 80424,
           "JNJ": 200406, "NFLX": 1065280, "ORCL": 1341439, "AMD": 2488, "CRM": 1108524, "WMT": 104169,
           "BAC": 70858, "INTC": 50863, "QCOM": 804328, "MU": 723125, "ADBE": 796343, "CSCO": 858877,
           "PEP": 77476, "KO": 21344, "DIS": 1744489, "PLTR": 1321655, "SMCI": 1375365, "MRVL": 1835632,
           "TXN": 97476, "IBM": 51143, "UBER": 1543151, "COIN": 1679788, "MSTR": 1050446, "GS": 886982,
           "MS": 895421, "CVX": 93410}
SEC_UA = {"User-Agent": os.environ.get("SEC_USER_AGENT", "master-trader-skill research script")}

FLOW_TAGS = {  # the tag with the most recent data wins
    "revenue": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"],
    "cogs": ["CostOfRevenue", "CostOfGoodsAndServicesSold"],
    "gross_profit": ["GrossProfit"],
    "rnd": ["ResearchAndDevelopmentExpense"],
    "op_income": ["OperatingIncomeLoss"],
    "net_income": ["NetIncomeLoss"],
    "eps_diluted": ["EarningsPerShareDiluted"],
    "shares_diluted": ["WeightedAverageNumberOfDilutedSharesOutstanding"],
    "cfo": ["NetCashProvidedByUsedInOperatingActivities"],
    "capex": ["PaymentsToAcquireProductiveAssets", "PaymentsToAcquirePropertyPlantAndEquipment"],
    "sbc": ["ShareBasedCompensation", "AllocatedShareBasedCompensationExpense"],
    "buybacks": ["PaymentsForRepurchaseOfCommonStock"],
}
STOCK_TAGS = {
    "cash": ["CashAndCashEquivalentsAtCarryingValue"],
    # total marketable securities (current + non-current) when tagged; tag order breaks ties on the same date
    "investments": ["AvailableForSaleSecuritiesDebtSecurities", "MarketableSecurities", "DebtSecuritiesCurrent",
                    "MarketableSecuritiesCurrent", "ShortTermInvestments", "AvailableForSaleSecuritiesDebtSecuritiesCurrent"],
    "debt": ["LongTermDebt", "LongTermDebtNoncurrent"],
    "inventory": ["InventoryNet"],
    "receivables": ["AccountsReceivableNetCurrent"],
}


def sec_json(url):
    req = urllib.request.Request(url, headers=SEC_UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def resolve_cik(ticker, cik=None):
    if cik:
        return int(cik)
    t = ticker.upper()
    if t in CIK_MAP:
        return CIK_MAP[t]
    try:
        tab = sec_json("https://www.sec.gov/files/company_tickers.json")
        for row in tab.values():
            if row["ticker"].upper() == t:
                return int(row["cik_str"])
    except urllib.error.HTTPError as e:
        sys.exit(f"{t} is not in the built-in CIK map and the SEC ticker file refused the request ({e.code}). "
                 "Pass --cik (find it at sec.gov/edgar/search), or set SEC_USER_AGENT to 'Your Name your@email' "
                 "as the SEC's fair-access policy asks.")
    sys.exit(f"no SEC CIK found for {t} (foreign filers using 20-F/IFRS have no us-gaap facts)")


def _days(a, b):
    return (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days


def _pick(facts, tags, need_start):
    best = None
    for tag in tags:
        for _, entries in facts.get(tag, {}).get("units", {}).items():
            es = [e for e in entries if e.get("form", "").startswith(("10-Q", "10-K")) and (("start" in e) == need_start)]
            if es and (best is None or max(e["end"] for e in es) > best[2]):
                best = (tag, es, max(e["end"] for e in es))
    return best


def quarterly_flows(entries):
    """Quarterly values from 10-Q/10-K duration facts: de-cumulate YTD figures and derive Q4 = FY - 9M."""
    by = {}
    for e in entries:
        k = (e["start"], e["end"])
        if k not in by or e.get("filed", "") > by[k][1]:
            by[k] = (e["val"], e.get("filed", ""))
    q = {}
    for (s, e), (v, _) in by.items():
        if 75 <= _days(s, e) <= 105:
            q[e] = (s, v)
    starts = {}
    for (s, e), (v, _) in by.items():
        starts.setdefault(s, []).append((e, v))
    for s, lst in starts.items():
        lst.sort()
        for (e1, v1), (e2, v2) in zip(lst, lst[1:]):
            if 75 <= _days(e1, e2) <= 105 and e2 not in q:
                q[e2] = (e1, v2 - v1)
    return q


def latest_stock(entries):
    by = {}
    for e in entries:
        if e["end"] not in by or e.get("filed", "") > by[e["end"]][1]:
            by[e["end"]] = (e["val"], e.get("filed", ""))
    return {k: v[0] for k, v in by.items()}


def _bn(v):
    return "n/a" if v is None else f"{v / 1e9:,.2f}"


def _chg(v):
    return "n/a" if v is None else f"{v:+.0%}" if abs(v) >= 1 else f"{v:+.1%}"


def _mg(v):
    return "n/a" if v is None else f"{v:.1%}"


def _num(v, fmt):
    return "n/a" if v is None else format(v, fmt)


def fundamentals(ticker, cik=None):
    """Quarterly rows (oldest first) with growth, margins, FCF and TTM sums, plus net cash and tags used."""
    cik = resolve_cik(ticker, cik)
    js = sec_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json")
    g = js.get("facts", {}).get("us-gaap", {})
    if not g:
        sys.exit("no us-gaap facts (foreign filer or no XBRL)")
    series, used = {}, {}
    for name, tags in FLOW_TAGS.items():
        p = _pick(g, tags, True)
        if p:
            used[name] = p[0]
            series[name] = {e: v for e, (s, v) in quarterly_flows(p[1]).items()}
    for name, tags in STOCK_TAGS.items():
        p = _pick(g, tags, False)
        if p:
            used[name] = p[0]
            series[name] = latest_stock(p[1])
    ends = sorted(series.get("revenue", {}))
    if len(ends) < 5:
        sys.exit("not enough quarterly revenue history")
    rows = []
    for e in ends:
        r = {"quarter_end": e}
        for k in series:
            r[k] = series[k].get(e)
        if r.get("gross_profit") is None and r.get("revenue") and r.get("cogs"):
            r["gross_profit"] = r["revenue"] - r["cogs"]
        if r.get("eps_diluted") is None and r.get("net_income") and r.get("shares_diluted"):
            r["eps_diluted"] = r["net_income"] / r["shares_diluted"]
        if r.get("cfo") is not None and r.get("capex") is not None:
            r["fcf"] = r["cfo"] - r["capex"]
        rows.append(r)

    def ttm(k, j):
        if j < 3 or any(rows[x].get(k) is None for x in range(j - 3, j + 1)):
            return None
        return sum(rows[x][k] for x in range(j - 3, j + 1))

    for j, r in enumerate(rows):
        rev = r.get("revenue")
        r["gm"] = r["gross_profit"] / rev if rev and r.get("gross_profit") is not None else None
        r["op_margin"] = r["op_income"] / rev if rev and r.get("op_income") is not None else None
        r["rev_yoy"] = rev / rows[j - 4]["revenue"] - 1 if j >= 4 and rows[j - 4].get("revenue") else None
        r["rev_qoq"] = rev / rows[j - 1]["revenue"] - 1 if j >= 1 and rows[j - 1].get("revenue") else None
        r["fcf_margin"] = r["fcf"] / rev if rev and r.get("fcf") is not None else None
        cogs = r.get("cogs") or (rev - r["gross_profit"] if rev and r.get("gross_profit") is not None else None)
        r["inv_days"] = r["inventory"] / cogs * 91 if r.get("inventory") and cogs else None
        r["dso"] = r["receivables"] / rev * 91 if r.get("receivables") and rev else None
        for k in ("revenue", "net_income", "fcf", "sbc", "buybacks", "eps_diluted"):
            r[f"{k}_ttm"] = ttm(k, j)
    last = rows[-1]
    net_cash = (last.get("cash") or 0) + (last.get("investments") or 0) - (last.get("debt") or 0)
    return {"entity": js.get("entityName"), "cik": cik, "rows": rows, "used": used, "net_cash": net_cash}


def cmd_fundamentals(a):
    f = fundamentals(a.ticker, a.cik)
    rows, used, cik, net_cash = f["rows"], f["used"], f["cik"], f["net_cash"]
    last = rows[-1]
    print(f"\n== {f['entity']} (CIK {cik}) -- SEC XBRL, quarterly, USD bn ==")
    print(f"  {'qtr end':<11}{'revenue':>9}{'YoY':>8}{'QoQ':>7}{'GM':>7}{'OpM':>7}{'net inc':>9}{'EPS':>7}"
          f"{'FCF':>8}{'FCF%':>7}{'inv d':>7}{'DSO':>6}")
    for r in rows[-a.quarters:]:
        print(f"  {r['quarter_end']:<11}{_bn(r.get('revenue')):>9}{_chg(r.get('rev_yoy')):>8}{_chg(r.get('rev_qoq')):>7}"
              f"{_mg(r.get('gm')):>7}{_mg(r.get('op_margin')):>7}{_bn(r.get('net_income')):>9}"
              f"{_num(r.get('eps_diluted'), '.2f'):>7}{_bn(r.get('fcf')):>8}{_mg(r.get('fcf_margin')):>7}"
              f"{_num(r.get('inv_days'), '.0f'):>7}{_num(r.get('dso'), '.0f'):>6}")
    out([
        ("TTM revenue / net income / FCF", f"{_bn(last.get('revenue_ttm'))} / {_bn(last.get('net_income_ttm'))} / "
                                           f"{_bn(last.get('fcf_ttm'))} bn"),
        ("TTM diluted EPS", _num(last.get("eps_diluted_ttm"), ".2f")),
        ("TTM SBC / buybacks", f"{_bn(last.get('sbc_ttm'))} / {_bn(last.get('buybacks_ttm'))} bn"),
        ("Diluted shares (last qtr)", "n/a" if last.get("shares_diluted") is None else f"{last['shares_diluted'] / 1e9:,.3f} bn"),
        ("Cash + securities - debt", f"{net_cash / 1e9:,.1f} bn (as of {last['quarter_end']})"),
        ("Tags used", ", ".join(f"{k}={v}" for k, v in used.items() if k in ("revenue", "capex", "sbc", "debt", "investments"))),
        ("Caveats", "XBRL as filed (restatements and segment detail not applied); Q4 derived as FY minus 9M; check "
                    "headline numbers against the 10-Q/10-K and the company's release before relying on them"),
    ], "Summary")
    if a.out:
        keys = ["quarter_end"] + sorted({k for r in rows for k in r if k != "quarter_end"})
        with open(a.out, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(keys)
            for r in rows:
                w.writerow(["" if r.get(k) is None else r.get(k) for k in keys])
        print(f"  wrote {a.out}")


def _et(utc_iso):
    from zoneinfo import ZoneInfo  # noqa: PLC0415
    return dt.datetime.fromisoformat(utc_iso.replace("Z", "+00:00")).astimezone(ZoneInfo("America/New_York"))


def earnings_dates(ticker, cik=None):
    """(entity, fiscal_year_end, [(date_et, time_et, AMC|BMO|DMH, accession)]) from 8-K item 2.02 filings."""
    cik = resolve_cik(ticker, cik)
    s = sec_json(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
    r = s["filings"]["recent"]
    rows = []
    for i, form in enumerate(r["form"]):
        if form == "8-K" and "2.02" in (r["items"][i] or ""):
            et = _et(r["acceptanceDateTime"][i])
            hm = et.hour * 60 + et.minute
            timing = "AMC" if hm >= 16 * 60 else "BMO" if hm < 9 * 60 + 30 else "DMH"
            rows.append((et.date().isoformat(), et.strftime("%H:%M"), timing, r["accessionNumber"][i]))
    rows.sort()
    if not rows:
        sys.exit("no 8-K item 2.02 (results of operations) filings in the recent submissions")
    return s.get("name"), s.get("fiscalYearEnd"), rows


def cmd_earnings_dates(a):
    name, fye, rows = earnings_dates(a.ticker, a.cik)
    out_csv = a.out or f"{a.ticker.upper()}_earnings_dates.csv"
    with open(out_csv, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date", "time_et", "timing", "accession"])
        w.writerows(rows)
    print(f"  {name}: {len(rows)} earnings releases (8-K item 2.02) {rows[0][0]} .. {rows[-1][0]}; "
          f"fiscal year end {fye} -> {out_csv}")
    print("  timing: AMC = after 16:00 ET (reaction next session), BMO = before 09:30 ET, DMH = during market hours.")
    print("  Upcoming dates are not in filings -- confirm the next date on the company's IR calendar.")


# --------------------------------------------------------------------------- crypto tape & book (public, no key)
KRAKEN_PAIRS = {"BTC": "XBTUSD", "ETH": "ETHUSD", "SOL": "SOLUSD"}


def _kraken_pair(sym: str) -> str:
    s = sym.upper().replace("-", "").replace("/", "")
    base = s[:-3] if s.endswith("USD") else s
    return KRAKEN_PAIRS.get(base, s if s.endswith("USD") else s + "USD")


def cmd_trades(a):
    """Recent trades with the AGGRESSOR side: buy = taker lifted the offer, sell = taker hit the bid."""
    import time
    rows = []
    if a.exchange == "kraken":
        pair = _kraken_pair(a.symbol)
        since = int((time.time() - a.minutes * 60) * 1e9)
        while len(rows) < a.max:
            js = http_json(f"https://api.kraken.com/0/public/Trades?pair={pair}&since={since}")
            if js.get("error"):
                sys.exit(f"kraken error: {js['error']}")
            res = js["result"]
            key = next(k for k in res if k != "last")
            batch = res[key]
            for p, v, t, side, *rest in batch:  # Kraken REST b/s = taker side (as in Kraken WS v2 docs)
                seq = int(rest[-1]) if rest and str(rest[-1]).isdigit() else len(rows)
                rows.append((float(t), seq, float(p), float(v), "buy" if side == "b" else "sell"))
            if len(batch) < 1000:
                break
            since = int(res["last"])
            time.sleep(1.1)  # public rate limit
    else:  # coinbase: 'side' is the MAKER side -> aggressor is the opposite
        prod = a.symbol.upper() if "-" in a.symbol else f"{a.symbol.upper()}-USD"
        url = f"https://api.exchange.coinbase.com/products/{prod}/trades?limit=1000"
        cutoff = time.time() - a.minutes * 60
        after = None
        while len(rows) < a.max:
            req = urllib.request.Request(url + (f"&after={after}" if after else ""), headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                batch = json.loads(r.read().decode())
                after = r.headers.get("CB-AFTER")
            stop = False
            for t in batch:
                ts = dt.datetime.fromisoformat(t["time"].replace("Z", "+00:00")).timestamp()
                if ts < cutoff:
                    stop = True
                    break
                rows.append((ts, int(t["trade_id"]), float(t["price"]), float(t["size"]),
                             "sell" if t["side"] == "buy" else "buy"))
            if stop or not after or not batch:
                break
            time.sleep(0.35)
    rows.sort(key=lambda r: (r[0], r[1]))  # time, then exchange sequence -- never re-order a sweep by price
    if not rows:
        sys.exit("no trades returned")
    out = a.out or f"{a.symbol.upper().replace('/', '')}_trades.csv"
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["time", "price", "size", "side"])
        for t, _, p, v, s in rows:
            w.writerow([dt.datetime.fromtimestamp(t, dt.timezone.utc).isoformat(timespec="milliseconds"), p, v, s])
    span = (rows[-1][0] - rows[0][0]) / 60
    buys = sum(v for *_, v, s in rows if s == "buy")
    tot = sum(v for *_, v, _ in rows)
    print(f"  {len(rows)} trades over {span:.1f} min from {a.exchange}; buy-aggressor share {buys / tot:.1%} -> {out}")


def cmd_book(a):
    """L2 order-book snapshot as CSV: side,price,size."""
    levels = []
    if a.exchange == "kraken":
        js = http_json(f"https://api.kraken.com/0/public/Depth?pair={_kraken_pair(a.symbol)}&count={a.depth}")
        if js.get("error"):
            sys.exit(f"kraken error: {js['error']}")
        book = next(iter(js["result"].values()))
        levels = [("bid", float(p), float(q)) for p, q, *_ in book["bids"]] + \
                 [("ask", float(p), float(q)) for p, q, *_ in book["asks"]]
    else:
        prod = a.symbol.upper() if "-" in a.symbol else f"{a.symbol.upper()}-USD"
        js = http_json(f"https://api.exchange.coinbase.com/products/{prod}/book?level=2")
        levels = [("bid", float(p), float(q)) for p, q, *_ in js["bids"][:a.depth]] + \
                 [("ask", float(p), float(q)) for p, q, *_ in js["asks"][:a.depth]]
    out = a.out or f"{a.symbol.upper().replace('/', '')}_book.csv"
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["side", "price", "size"])
        w.writerows(levels)
    print(f"  {len(levels)} levels from {a.exchange} at {dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')} -> {out}")
    print("  note: one exchange's book only; crypto liquidity is fragmented across venues.")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--key-file", help="path to a file whose first line is the FRED key")
    s = p.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("macro")
    x.set_defaults(fn=cmd_macro)
    x = s.add_parser("fred")
    x.add_argument("series", nargs="+")
    x.add_argument("--start", help="YYYY-MM-DD")
    x.add_argument("--yoy", action="store_true", help="convert index levels to YoY %%")
    x.add_argument("--out")
    x.set_defaults(fn=cmd_fred)
    x = s.add_parser("search")
    x.add_argument("text")
    x.add_argument("--limit", type=int, default=15)
    x.set_defaults(fn=cmd_search)
    x = s.add_parser("prices")
    x.add_argument("symbol", help="e.g. SPY, ^GSPC, ES=F, BTC-USD, EURUSD=X")
    x.add_argument("--years", type=float, default=10)
    x.add_argument("--no-adjust", dest="adjust", action="store_false", help="keep raw (unadjusted) OHLC")
    x.add_argument("--include-partial", action="store_true", help="keep the still-forming bar as the last bar")
    x.add_argument("--interval", choices=["1d", "1h", "30m", "15m", "5m", "2m", "1m"], default="1d",
                   help="intraday bars are in exchange-local time, labelled by bar start")
    x.add_argument("--range", default="1mo", choices=INTRADAY_RANGES,
                   help="lookback for intraday bars (1h: up to 2y; minute bars: capped at 7d for 1m, 59d otherwise)")
    x.add_argument("--days", type=float, help="lookback in days for minute bars (overrides --range)")
    x.add_argument("--prepost", action="store_true", help="include pre-market and after-hours bars (minute intervals)")
    x.add_argument("--out")
    x.set_defaults(fn=cmd_prices)
    x = s.add_parser("quote", help="latest price, change, session state and quote age (Yahoo)")
    x.add_argument("symbols", nargs="+", help="e.g. SPY NVDA BTC-USD ES=F")
    x.set_defaults(fn=cmd_quote)
    x = s.add_parser("options", help="listed option chain near the money (Yahoo, delayed): bid/ask, IV, open interest")
    x.add_argument("symbol")
    x.add_argument("--expiry", help="YYYY-MM-DD (default: nearest; the first listed on/after this date)")
    x.add_argument("--dte", type=int, help="pick the first expiry at least this many days out")
    x.add_argument("--type", choices=["put", "call", "both"], default="both")
    x.add_argument("--near", type=int, default=6, help="strikes each side of the money")
    x.add_argument("--out", help="write the whole chain (both sides) to CSV")
    x.set_defaults(fn=cmd_options)
    x = s.add_parser("fundamentals", help="quarterly financials from SEC XBRL (revenue, margins, EPS, FCF ...)")
    x.add_argument("ticker")
    x.add_argument("--cik", help="SEC CIK if the ticker is not in the built-in map")
    x.add_argument("--quarters", type=int, default=8, help="quarters to print")
    x.add_argument("--out", help="write every quarter to CSV")
    x.set_defaults(fn=cmd_fundamentals)
    x = s.add_parser("earnings-dates", help="past earnings release dates/times from SEC 8-K item 2.02 filings")
    x.add_argument("ticker")
    x.add_argument("--cik")
    x.add_argument("--out")
    x.set_defaults(fn=cmd_earnings_dates)
    x = s.add_parser("gpr", help="Caldara-Iacoviello Geopolitical Risk index -> CSV")
    x.add_argument("--freq", choices=["monthly", "daily"], default="monthly")
    x.add_argument("--out", help="CSV path (default gpr_<freq>.csv)")
    x.add_argument("--out-xls", help="where to keep the downloaded .xls")
    x.set_defaults(fn=cmd_gpr)
    x = s.add_parser("trades", help="recent crypto trades with aggressor side (public API)")
    x.add_argument("symbol", help="BTC, ETH, SOL or BTC-USD")
    x.add_argument("--exchange", choices=["kraken", "coinbase"], default="kraken")
    x.add_argument("--minutes", type=float, default=60)
    x.add_argument("--max", type=int, default=50000)
    x.add_argument("--out")
    x.set_defaults(fn=cmd_trades)
    x = s.add_parser("book", help="crypto L2 order-book snapshot (public API)")
    x.add_argument("symbol")
    x.add_argument("--exchange", choices=["kraken", "coinbase"], default="coinbase")
    x.add_argument("--depth", type=int, default=100)
    x.add_argument("--out")
    x.set_defaults(fn=cmd_book)
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
