#!/usr/bin/env python3
"""tradekit -- deterministic calculators for the master-trader skill.

LLMs make arithmetic slips; traders lose money on them. Every number that
matters (size, risk, Sharpe significance, option Greeks, cost) should come
from here rather than mental math.

Standard library only (numpy is used for speed in Monte Carlo if present).

Usage:  python tradekit.py <command> [options]      (python tradekit.py -h)

Commands
  size        position size from equity, risk %, entry, stop (or ATR)
  kelly       Kelly fraction: discrete (win rate/payoff) or continuous (mu/sigma)
  expectancy  expectancy in R and trades needed to prove it
  ruin        Monte Carlo probability of hitting a drawdown limit
  drawdown    recovery math + expected max drawdown for a given Sharpe
  sharpe      Sharpe SE, Probabilistic & Deflated Sharpe, min track record
  perf        full performance report from a CSV of returns or prices
  vol         volatility estimators from an OHLC CSV
  meanrev     mean-reversion diagnostics: OU half-life, Hurst, variance ratio
  bs          Black-Scholes-Merton price and Greeks
  iv          implied volatility from an option price
  move        expected move / breakeven daily move from IV or straddle
  impact      square-root market impact + spread cost estimate
"""
from __future__ import annotations

import argparse
import csv
import math
import random
import statistics
import sys
from statistics import NormalDist

N = NormalDist()
EULER_GAMMA = 0.5772156649015329

try:  # optional speed-up
    import numpy as _np  # type: ignore
except Exception:  # pragma: no cover
    _np = None


# --------------------------------------------------------------------------- helpers
def pct(x: float, d: int = 2) -> str:
    return f"{x * 100:.{d}f}%"


def out(rows: list[tuple[str, object]], title: str | None = None) -> None:
    if title:
        print(f"\n== {title} ==")
    w = max(len(k) for k, _ in rows) if rows else 0
    for k, v in rows:
        print(f"  {k:<{w}}  {v}")


def read_csv_column(path: str, col: str | None) -> list[float]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.reader(fh)
        rows = [r for r in reader if r and any(c.strip() for c in r)]
    header = rows[0]
    has_header = any(not _isnum(c) for c in header)
    data = rows[1:] if has_header else rows
    if has_header:
        names = [h.strip().lower() for h in header]
        if col:
            if col.lower() not in names:
                sys.exit(f"no column '{col}' in {path}; columns: {header}")
            idx = names.index(col.lower())
        else:
            # Pick by name -- never fall back to 'last numeric column', which is volume in OHLCV files.
            pref = ("adj close", "adj_close", "adjclose", "close", "equity", "nav", "price", "returns", "return",
                    "ret", "pnl", "spread", "value")
            idx = next((names.index(p) for p in pref if p in names), None)
            if idx is None:
                numeric = [header[i] for i, c in enumerate(data[0]) if _isnum(c)]
                if len(numeric) == 1:
                    idx = names.index(numeric[0].strip().lower())
                else:
                    sys.exit(f"can't tell which column to analyse in {path}; numeric columns: {numeric}. Pass --col NAME.")
    else:
        idx = int(col) if col and col.isdigit() else len(data[0]) - 1
    vals = []
    for r in data:
        if idx < len(r) and _isnum(r[idx]):
            vals.append(float(r[idx]))
    return vals


def read_ohlc(path: str) -> dict[str, list[float]]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        cols = {k.strip().lower(): k for k in reader.fieldnames or []}
        need = {}
        for key, aliases in {
            "open": ("open", "o"),
            "high": ("high", "h"),
            "low": ("low", "l"),
            "close": ("close", "c", "adj close", "adj_close"),
        }.items():
            for a in aliases:
                if a in cols:
                    need[key] = cols[a]
                    break
            else:
                sys.exit(f"OHLC CSV needs a '{key}' column; found {list(cols)}")
        res: dict[str, list[float]] = {k: [] for k in need}
        for r in reader:
            try:
                vals = {k: float(r[v]) for k, v in need.items()}
            except (ValueError, TypeError):
                continue
            for k, v in vals.items():
                res[k].append(v)
    return res


def _isnum(s: str) -> bool:
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


def moments(x: list[float]) -> tuple[float, float, float, float]:
    """mean, stdev (sample), skew, kurtosis (non-excess; normal = 3)."""
    n = len(x)
    m = sum(x) / n
    d = [v - m for v in x]
    m2 = sum(v * v for v in d) / n
    m3 = sum(v ** 3 for v in d) / n
    m4 = sum(v ** 4 for v in d) / n
    sd = math.sqrt(m2 * n / (n - 1)) if n > 1 else 0.0
    skew = m3 / m2 ** 1.5 if m2 > 0 else 0.0
    kurt = m4 / m2 ** 2 if m2 > 0 else 3.0
    return m, sd, skew, kurt


def max_drawdown(equity: list[float]) -> tuple[float, int]:
    """Max drawdown (as positive fraction) and longest underwater stretch (periods)."""
    peak = equity[0]
    mdd = 0.0
    under = longest = 0
    for v in equity:
        if v >= peak:
            peak = v
            under = 0
        else:
            under += 1
            longest = max(longest, under)
            mdd = max(mdd, 1 - v / peak)
    return mdd, longest


def ols(x: list[float], y: list[float]) -> tuple[float, float]:
    """intercept, slope."""
    mx, my = sum(x) / len(x), sum(y) / len(y)
    sxx = sum((a - mx) ** 2 for a in x)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    b = sxy / sxx
    return my - b * mx, b


# --------------------------------------------------------------------------- sizing
def cmd_size(a):
    risk_cash = a.equity * a.risk / 100
    if a.atr is not None:
        stop_dist = a.atr * a.atr_mult
        stop = a.entry - stop_dist if a.side == "long" else a.entry + stop_dist
    elif a.stop is not None:
        stop = a.stop
        stop_dist = abs(a.entry - a.stop)
        if (a.side == "long" and stop >= a.entry) or (a.side == "short" and stop <= a.entry):
            sys.exit(f"stop {stop} is on the wrong side of entry {a.entry} for a {a.side} (use --side short for shorts)")
    else:
        sys.exit("give --stop or --atr")
    if stop_dist <= 0:
        sys.exit("stop distance must be > 0")
    per_unit_risk = stop_dist * a.multiplier
    units_raw = risk_cash / per_unit_risk
    units = math.floor(units_raw / a.lot) * a.lot
    notional = units * a.entry * a.multiplier
    rows = [
        ("Risk budget", f"{risk_cash:,.2f} ({a.risk}% of {a.equity:,.0f})"),
        ("Entry / stop", f"{a.entry} / {stop:.4f}  (distance {stop_dist:.4f}, {pct(stop_dist / a.entry)})"),
        ("Risk per unit", f"{per_unit_risk:,.4f}"),
        ("Units (rounded down)", f"{units:,.0f}  (raw {units_raw:,.2f}, lot {a.lot})"),
        ("Actual cash at risk", f"{units * per_unit_risk:,.2f}"),
        ("Notional", f"{notional:,.2f}  ({pct(notional / a.equity)} of equity, {notional / a.equity:.2f}x)"),
    ]
    if a.target is not None:
        reward = abs(a.target - a.entry)
        rows.append(("Reward:risk", f"{reward / stop_dist:.2f}R  (target {a.target})"))
    if units == 0:
        rows.append(("WARNING", "risk budget smaller than one lot -- use a smaller contract (e.g. micro futures), a tighter "
                                "justified stop, or skip the trade; never round up"))
    if notional / a.equity > a.max_lev:
        rows.append(("WARNING", f"notional exceeds {a.max_lev}x equity -- gap/overnight risk is not covered by the stop"))
    out(rows, f"Position size ({a.side})")


def cmd_kelly(a):
    rows = []
    if a.p is not None and a.b is not None:
        p, b = a.p, a.b
        f = p - (1 - p) / b
        def g(x):
            if x <= 0:
                return 0.0
            if x >= 1:
                return float("-inf")
            return p * math.log(1 + x * b) + (1 - p) * math.log(1 - x)
        rows += [
            ("Win rate / payoff", f"{pct(p)} / {b:.2f}:1"),
            ("Edge per $ risked", f"{p * b - (1 - p):.4f}"),
            ("Full Kelly f*", pct(f)),
        ]
        if f <= 0:
            rows.append(("Verdict", "no edge -- Kelly says bet nothing"))
        else:
            for lbl, k in (("Full", 1), ("Half", 0.5), ("Quarter", 0.25)):
                fx = f * k
                rows.append((f"{lbl} Kelly", f"risk {pct(fx)}/bet, log-growth/bet {g(fx):.5f} ({g(fx) / g(f) * 100:.0f}% of max)"))
            rows.append(("Note", "f* here = fraction of equity LOST if the bet loses (i.e. risk per trade)"))
    elif a.mu is not None and a.sigma is not None:
        ex = a.mu - a.rf
        f = ex / a.sigma ** 2
        def g(x):
            return a.rf + x * ex - 0.5 * x * x * a.sigma ** 2
        sr = ex / a.sigma
        rows += [
            ("Excess return / vol", f"{pct(ex)} / {pct(a.sigma)}  (Sharpe {sr:.2f})"),
            ("Full Kelly leverage", f"{f:.2f}x  -> vol {pct(f * a.sigma)}, growth {pct(g(f))}/yr"),
            ("Half Kelly leverage", f"{f / 2:.2f}x  -> vol {pct(f * a.sigma / 2)}, growth {pct(g(f / 2))}/yr (75% of max growth)"),
            ("Quarter Kelly", f"{f / 4:.2f}x  -> vol {pct(f * a.sigma / 4)}, growth {pct(g(f / 4))}/yr"),
            ("Max growth rate", f"{pct(a.rf + sr * sr / 2)}/yr = rf + SR^2/2 (Kelly-optimal vol = Sharpe)"),
            ("P(ever halving) full/half/quarter", "50% / 12.5% / 0.8%  (Thorp: P(reach x of start) = x^(2/c - 1))"),
            ("Note", "inputs are estimates; overbetting from an inflated mu is far worse than underbetting -- use <= half Kelly"),
        ]
    else:
        sys.exit("give --p and --b (discrete) or --mu and --sigma (continuous)")
    out(rows, "Kelly")


def cmd_expectancy(a):
    p, w, l = a.p, a.win, a.loss
    e = p * w - (1 - p) * l
    var = p * (w - e) ** 2 + (1 - p) * (-l - e) ** 2
    sd = math.sqrt(var)
    rows = [
        ("Win rate", pct(p)),
        ("Avg win / avg loss", f"{w:.2f}R / {l:.2f}R"),
        ("Expectancy", f"{e:+.3f}R per trade"),
        ("Breakeven win rate", pct(l / (w + l))),
        ("Std dev per trade", f"{sd:.3f}R"),
    ]
    if e > 0:
        for z in (2.0, 3.0):
            n = math.ceil((z * sd / e) ** 2)
            rows.append((f"Trades for t={z:.0f}", f"{n}  (sample needed before the edge is distinguishable from luck)"))
        if a.trades:
            se = sd / math.sqrt(a.trades)
            rows.append((f"t-stat at {a.trades} trades", f"{e / se:.2f}"))
    else:
        rows.append(("Verdict", "negative or zero expectancy -- no sizing rule fixes this"))
    out(rows, "Expectancy")


def cmd_ruin(a):
    rng = random.Random(a.seed)
    hits = 0
    finals = []
    mdds = []
    for _ in range(a.sims):
        eq = peak = 1.0
        mdd = 0.0
        hit = False
        for _ in range(a.trades):  # keep running after the limit so drawdown stats are not censored at it
            risk = a.risk / 100 * (eq if a.compound else 1.0)
            eq += risk * a.b if rng.random() < a.p else -risk
            if eq > peak:
                peak = eq
            dd = 1 - eq / peak if peak > 0 else 1
            mdd = max(mdd, dd)
            if dd >= a.limit / 100:
                hit = True
            if eq <= 0:
                eq, mdd, hit = 0.0, 1.0, True
                break
        hits += hit
        finals.append(eq)
        mdds.append(mdd)
    finals.sort()
    mdds.sort()
    q = lambda xs, f: xs[min(len(xs) - 1, int(f * len(xs)))]
    out([
        ("Setup", f"win {pct(a.p)}, payoff {a.b}:1, risk {a.risk}%/trade, {a.trades} trades, {'compounding' if a.compound else 'fixed $'}"),
        (f"P(drawdown >= {a.limit}%)", pct(hits / a.sims, 1)),
        ("Median max drawdown", pct(q(mdds, 0.5), 1)),
        ("95th pct max drawdown", pct(q(mdds, 0.95), 1)),
        ("Median ending equity", f"{q(finals, 0.5):.3f}x"),
        ("5th pct ending equity", f"{q(finals, 0.05):.3f}x"),
        ("Note", "drawdown/equity stats assume the trader keeps going after the limit (uncensored)"),
    ], f"Risk of ruin (Monte Carlo, {a.sims} sims)")


def cmd_drawdown(a):
    rows = []
    for dd in (a.loss or [10, 20, 30, 50, 75, 90]):
        rows.append((f"Lose {dd}%", f"need +{pct(1 / (1 - dd / 100) - 1, 1)} to recover"))
    out(rows, "Recovery math")
    if a.sharpe is not None:
        steps = int(a.years * a.ppy)
        mu = a.sharpe * a.vol / a.ppy
        sd = a.vol / math.sqrt(a.ppy)
        mdds = []
        rng = random.Random(a.seed)
        if _np is not None:
            g = _np.random.default_rng(a.seed)
            r = g.normal(mu, sd, size=(a.sims, steps))
            eq = _np.cumprod(1 + r, axis=1)
            peak = _np.maximum.accumulate(eq, axis=1)
            mdds = sorted((1 - eq / peak).max(axis=1).tolist())
        else:
            for _ in range(a.sims):
                eq = peak = 1.0
                m = 0.0
                for _ in range(steps):
                    eq *= 1 + rng.gauss(mu, sd)
                    peak = max(peak, eq)
                    m = max(m, 1 - eq / peak)
                mdds.append(m)
            mdds.sort()
        q = lambda f: mdds[min(len(mdds) - 1, int(f * len(mdds)))]
        out([
            ("Assumption", f"Sharpe {a.sharpe}, vol {pct(a.vol)}, {a.years}y, normal iid returns (real tails are worse)"),
            ("Median max drawdown", pct(q(0.5), 1)),
            ("75th pct", pct(q(0.75), 1)),
            ("95th pct", pct(q(0.95), 1)),
            ("Rule of thumb", "plan for the 95th pct, then add a margin -- live drawdowns usually exceed backtests"),
        ], f"Expected max drawdown (Monte Carlo, {a.sims} sims)")


# --------------------------------------------------------------------------- statistics
def _psr(sr, sr_star, t, skew, kurt):
    denom = 1 - skew * sr + (kurt - 1) / 4 * sr * sr
    if denom <= 0:
        return float("nan")
    return N.cdf((sr - sr_star) * math.sqrt(t - 1) / math.sqrt(denom))


def _expected_max_sr(n_trials, var_sr):
    if n_trials <= 1:
        return 0.0
    return math.sqrt(var_sr) * ((1 - EULER_GAMMA) * N.inv_cdf(1 - 1 / n_trials)
                                + EULER_GAMMA * N.inv_cdf(1 - 1 / (n_trials * math.e)))


def sharpe_report(sr_ann, t, ppy, skew, kurt, trials, var_sr_ann, bench_ann=0.0):
    sr = sr_ann / math.sqrt(ppy)  # per-period
    var_sr = var_sr_ann / ppy if var_sr_ann is not None else None
    denom = 1 - skew * sr + (kurt - 1) / 4 * sr * sr
    se = math.sqrt(denom / (t - 1)) * math.sqrt(ppy)
    se_iid = math.sqrt((1 + 0.5 * sr * sr) / t) * math.sqrt(ppy)
    rows = [
        ("Annualized Sharpe", f"{sr_ann:.3f}  over {t} obs ({t / ppy:.1f} yrs @ {ppy}/yr)"),
        ("Skew / kurtosis", f"{skew:.2f} / {kurt:.2f}  (normal = 0 / 3)"),
        ("SE of Sharpe (ann.)", f"{se:.3f}  (iid-normal formula: {se_iid:.3f})"),
        ("95% CI", f"[{sr_ann - 1.96 * se:.2f}, {sr_ann + 1.96 * se:.2f}]"),
        ("t-stat vs 0", f"{sr_ann / se:.2f}  (Harvey-Liu-Zhu hurdle for new factors: ~3.0)"),
        (f"PSR(SR>{bench_ann})", pct(_psr(sr, bench_ann / math.sqrt(ppy), t, skew, kurt), 1)),
    ]
    z = N.inv_cdf(0.95)
    if sr > bench_ann / math.sqrt(ppy):
        mtrl = 1 + denom * (z / (sr - bench_ann / math.sqrt(ppy))) ** 2
        yrs = mtrl / ppy
        rows.append(("Min track record (95%)", f"{mtrl:.0f} obs = {yrs:.1f} yrs" if yrs < 100 else "> 100 yrs -- indistinguishable from zero skill"))
    if trials and trials > 1:
        if var_sr is None:
            rows.append(("DSR", "need --var-sr (variance of annualized Sharpes across all trials)"))
        else:
            sr0 = _expected_max_sr(trials, var_sr)
            dsr = _psr(sr, sr0, t, skew, kurt)
            rows += [
                (f"E[max SR] of {trials} null trials", f"{sr0 * math.sqrt(ppy):.3f} (annualized) -- what luck alone produces"),
                ("Deflated Sharpe (DSR)", f"{pct(dsr, 1)}  ({'passes' if dsr > 0.95 else 'FAILS'} 95% threshold)"),
            ]
    return rows


def cmd_sharpe(a):
    out(sharpe_report(a.sr, a.n, a.ppy, a.skew, a.kurt, a.trials, a.var_sr, a.bench), "Sharpe significance")


def cmd_perf(a):
    vals = read_csv_column(a.file, a.col)
    if a.prices:
        rets = [vals[i] / vals[i - 1] - 1 for i in range(1, len(vals))]
    else:
        rets = [v / 100 for v in vals] if a.percent else vals
    n = len(rets)
    if n < 20:
        sys.exit(f"only {n} returns -- too few to say anything")
    m, sd, skew, kurt = moments(rets)
    eq = [1.0]
    for r in rets:
        eq.append(eq[-1] * (1 + r))
    years = n / a.ppy
    cagr = eq[-1] ** (1 / years) - 1 if eq[-1] > 0 else -1
    vol = sd * math.sqrt(a.ppy)
    rf_p = a.rf / a.ppy
    sharpe = (m - rf_p) / sd * math.sqrt(a.ppy) if sd else float("nan")
    downside = [min(0.0, r - rf_p) for r in rets]
    dd_sd = math.sqrt(sum(d * d for d in downside) / n)
    sortino = (m - rf_p) / dd_sd * math.sqrt(a.ppy) if dd_sd else float("nan")
    mdd, under = max_drawdown(eq)
    wins = [r for r in rets if r > 0]
    losses = [r for r in rets if r < 0]
    gp, gl = sum(wins), -sum(losses)
    # lag-1 autocorrelation (Lo 2002: serial correlation biases annualized Sharpe)
    ac1 = sum((rets[i] - m) * (rets[i - 1] - m) for i in range(1, n)) / sum((r - m) ** 2 for r in rets)
    rows = [
        ("Observations", f"{n} ({years:.1f} yrs @ {a.ppy}/yr)"),
        ("Total return", pct(eq[-1] - 1)),
        ("CAGR", pct(cagr)),
        ("Volatility (ann.)", pct(vol)),
        ("Sharpe (ann.)", f"{sharpe:.2f}"),
        ("Sortino (ann.)", f"{sortino:.2f}"),
        ("Max drawdown", pct(mdd)),
        ("Calmar (CAGR/MDD)", f"{cagr / mdd:.2f}" if mdd else "n/a"),
        ("Longest underwater", f"{under} periods ({under / a.ppy:.1f} yrs)"),
        ("Hit rate", pct(len(wins) / n)),
        ("Avg win / avg loss", f"{pct(statistics.mean(wins)) if wins else 'n/a'} / {pct(statistics.mean(losses)) if losses else 'n/a'}"),
        ("Profit factor", f"{gp / gl:.2f}" if gl else "inf"),
        ("Best / worst period", f"{pct(max(rets))} / {pct(min(rets))}"),
        ("Skew / kurtosis", f"{skew:.2f} / {kurt:.2f}"),
        ("Lag-1 autocorrelation", f"{ac1:.3f}" + ("  (material: annualized Sharpe is biased; see Lo 2002)" if abs(ac1) > 0.1 else "")),
    ]
    out(rows, f"Performance: {a.file}")
    out(sharpe_report(sharpe, n, a.ppy, skew, kurt, a.trials, a.var_sr), "Sharpe significance")


def cmd_vol(a):
    d = read_ohlc(a.file)
    o, h, l, c = d["open"], d["high"], d["low"], d["close"]
    w = a.window or len(c) - 1
    o, h, l, c = o[-w - 1:], h[-w - 1:], l[-w - 1:], c[-w - 1:]
    n = len(c) - 1
    if n < 10:
        sys.exit("need at least ~10 bars")
    ln = math.log
    r_cc = [ln(c[i] / c[i - 1]) for i in range(1, len(c))]
    cc = statistics.variance(r_cc)
    park = sum(ln(h[i] / l[i]) ** 2 for i in range(1, len(c))) / (4 * ln(2) * n)
    gk = sum(0.5 * ln(h[i] / l[i]) ** 2 - (2 * ln(2) - 1) * ln(c[i] / o[i]) ** 2 for i in range(1, len(c))) / n
    rs_terms = [ln(h[i] / c[i]) * ln(h[i] / o[i]) + ln(l[i] / c[i]) * ln(l[i] / o[i]) for i in range(1, len(c))]
    rs = sum(rs_terms) / n
    r_on = [ln(o[i] / c[i - 1]) for i in range(1, len(c))]
    r_oc = [ln(c[i] / o[i]) for i in range(1, len(c))]
    k = 0.34 / (1.34 + (n + 1) / (n - 1))
    yz = statistics.variance(r_on) + k * statistics.variance(r_oc) + (1 - k) * rs
    ew = r_cc[0] ** 2
    for r in r_cc[1:]:
        ew = a.lam * ew + (1 - a.lam) * r * r
    ann = lambda v: pct(math.sqrt(max(v, 0) * a.ppy))
    out([
        ("Bars used", n),
        ("Close-to-close", ann(cc)),
        ("Parkinson (high-low)", ann(park) + "  (ignores gaps/drift; biased low with jumps)"),
        ("Garman-Klass", ann(gk) + "  (ignores overnight gaps)"),
        ("Rogers-Satchell", ann(rs) + "  (drift-robust)"),
        ("Yang-Zhang", ann(yz) + "  (handles gaps + drift; best general default)"),
        (f"EWMA lambda={a.lam}", ann(ew) + "  (current conditional vol, RiskMetrics)"),
        ("Overnight share of var", pct(statistics.variance(r_on) / cc if cc else 0)),
        ("Daily 1-sigma (YZ)", pct(math.sqrt(max(yz, 0)))),
    ], f"Volatility: {a.file}")


def cmd_meanrev(a):
    y = read_csv_column(a.file, a.col)
    if a.log:
        y = [math.log(v) for v in y]
    dy = [y[i] - y[i - 1] for i in range(1, len(y))]
    _, b = ols(y[:-1], dy)
    hl = -math.log(2) / math.log(1 + b) if -1 < b < 0 else float("inf")
    # Hurst from scaling of lagged differences
    lags = [t for t in range(2, min(a.max_lag, len(y) // 4))]
    lx, ly = [], []
    for t in lags:
        diffs = [y[i + t] - y[i] for i in range(len(y) - t)]
        s = statistics.pstdev(diffs)
        if s > 0:
            lx.append(math.log(t))
            ly.append(math.log(s))
    hurst = ols(lx, ly)[1] if len(lx) > 2 else float("nan")
    r = dy
    vr_rows = []
    var1 = statistics.pvariance(r)
    for q in (2, 5, 10, 20):
        if len(r) > 4 * q:
            rq = [sum(r[i:i + q]) for i in range(len(r) - q + 1)]
            vr = statistics.pvariance(rq) / (q * var1)
            vr_rows.append((f"Variance ratio q={q}", f"{vr:.3f}  ({'mean-reverting' if vr < 0.9 else 'trending' if vr > 1.1 else '~random walk'})"))
    rows = [
        ("Observations", len(y)),
        ("AR slope (dy on y_lag)", f"{b:.5f}"),
        ("OU half-life", f"{hl:.1f} periods" if math.isfinite(hl) else "none (no mean reversion detected)"),
        ("Hurst exponent", f"{hurst:.3f}  (<0.5 mean-reverting, ~0.5 random walk, >0.5 trending)"),
    ] + vr_rows + [
        ("Caveat", "point estimates are noisy; confirm with ADF/Johansen (statsmodels) and out-of-sample stability"),
    ]
    out(rows, f"Mean reversion: {a.file}")


# --------------------------------------------------------------------------- options
def bs(S, K, T, r, q, sigma, kind):
    if T <= 0 or sigma <= 0:
        intrinsic = max(0.0, S - K) if kind == "call" else max(0.0, K - S)
        return {"price": intrinsic}
    sq = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / sq
    d2 = d1 - sq
    dq, dr = math.exp(-q * T), math.exp(-r * T)
    pdf = N.pdf(d1)
    if kind == "call":
        price = S * dq * N.cdf(d1) - K * dr * N.cdf(d2)
        delta = dq * N.cdf(d1)
        theta = -S * dq * pdf * sigma / (2 * math.sqrt(T)) - r * K * dr * N.cdf(d2) + q * S * dq * N.cdf(d1)
        rho = K * T * dr * N.cdf(d2)
        p_itm = N.cdf(d2)
    else:
        price = K * dr * N.cdf(-d2) - S * dq * N.cdf(-d1)
        delta = -dq * N.cdf(-d1)
        theta = -S * dq * pdf * sigma / (2 * math.sqrt(T)) + r * K * dr * N.cdf(-d2) - q * S * dq * N.cdf(-d1)
        rho = -K * T * dr * N.cdf(-d2)
        p_itm = N.cdf(-d2)
    gamma = dq * pdf / (S * sq)
    vega = S * dq * pdf * math.sqrt(T)
    return {
        "price": price, "delta": delta, "gamma": gamma,
        "vega_1pt": vega / 100, "theta_day": theta / 365, "rho_1pt": rho / 100,
        "vanna": -dq * pdf * d2 / sigma, "volga_1pt": vega * d1 * d2 / sigma / 1e4,
        "d1": d1, "d2": d2, "p_itm": p_itm,
        "dollar_gamma_1pct": 0.5 * gamma * (0.01 * S) ** 2 * 100,
    }


def cmd_bs(a):
    T = a.days / 365
    g = bs(a.S, a.K, T, a.r, a.q, a.vol, a.kind)
    if "delta" not in g:
        out([("Price (intrinsic)", f"{g['price']:.4f}")], "Black-Scholes")
        return
    be_move = a.vol / math.sqrt(252)
    out([
        ("Inputs", f"{a.kind} S={a.S} K={a.K} {a.days}d vol={pct(a.vol)} r={pct(a.r)} q={pct(a.q)}"),
        ("Price", f"{g['price']:.4f}  (x{a.mult} = {g['price'] * a.mult:,.2f} per contract)"),
        ("Delta", f"{g['delta']:.4f}"),
        ("Gamma", f"{g['gamma']:.6f}  (delta change per $1)"),
        ("Vega", f"{g['vega_1pt']:.4f} per 1 vol pt"),
        ("Theta", f"{g['theta_day']:.4f} per calendar day"),
        ("Rho", f"{g['rho_1pt']:.4f} per 1% rate"),
        ("Vanna", f"{g['vanna']:.4f}  (dDelta/dVol per 1.00 vol)"),
        ("Volga", f"{g['volga_1pt']:.6f}  (dVega per 1 vol pt)"),
        ("P(ITM) risk-neutral", pct(g["p_itm"], 1)),
        ("Gamma P&L for 1% move", f"{g['dollar_gamma_1pct']:.4f} per 100 shares"),
        ("Breakeven daily move", f"{pct(be_move)} (= vol/sqrt(252); long gamma wins if realized beats this)"),
    ], "Black-Scholes-Merton")


def implied_vol(price, S, K, T, r, q, kind):
    lo, hi = 1e-4, 5.0
    if price <= bs(S, K, T, r, q, lo, kind)["price"] or price >= bs(S, K, T, r, q, hi, kind)["price"]:
        return float("nan")
    for _ in range(200):
        mid = (lo + hi) / 2
        if bs(S, K, T, r, q, mid, kind)["price"] > price:
            hi = mid
        else:
            lo = mid
        if hi - lo < 1e-7:
            break
    return (lo + hi) / 2


def cmd_iv(a):
    iv = implied_vol(a.price, a.S, a.K, a.days / 365, a.r, a.q, a.kind)
    if math.isnan(iv):
        out([("IV", "no solution (price outside no-arbitrage bounds)")], "Implied vol")
        return
    out([
        ("Implied vol", pct(iv)),
        ("Implied daily move", pct(iv / math.sqrt(252))),
        ("Implied move to expiry (1 SD)", f"{a.S * iv * math.sqrt(a.days / 365):.2f}"),
    ], "Implied vol")


def cmd_move(a):
    rows = []
    T = a.days / 365
    if a.vol is not None:
        sd = a.S * a.vol * math.sqrt(T)
        rows += [
            ("1 SD move to expiry", f"+/-{sd:.2f} ({pct(sd / a.S)})  -> {a.S - sd:.2f} .. {a.S + sd:.2f}"),
            ("2 SD move", f"+/-{2 * sd:.2f}"),
            ("Expected |move| (mean abs)", f"{sd * math.sqrt(2 / math.pi):.2f}  (~ ATM straddle value)"),
            ("Breakeven daily move", f"{pct(a.vol / math.sqrt(252))}  (rule of 16: vol/16)"),
        ]
    if a.straddle is not None:
        sd = a.straddle / math.sqrt(2 / math.pi)
        rows += [
            ("Straddle price", f"{a.straddle:.2f} ({pct(a.straddle / a.S)}) = market's expected |move|"),
            ("Implied 1 SD move", f"+/-{sd:.2f} ({pct(sd / a.S)})  = straddle x 1.25"),
            ("Implied vol (approx)", pct(sd / a.S / math.sqrt(T)) if T > 0 else "n/a"),
        ]
    if a.event_vol is not None and a.base_vol is not None:
        # total variance = base variance over T + event day variance
        ev = math.sqrt(max(0.0, a.event_vol ** 2 * T - a.base_vol ** 2 * (T - 1 / 365)))
        rows.append(("Implied event-day move", f"{pct(ev)} of spot (1 SD) extracted from term structure"))
    if not rows:
        sys.exit("give --vol and/or --straddle (or --event-vol with --base-vol)")
    out(rows, f"Expected move ({a.days}d)")


def cmd_impact(a):
    part = a.qty / a.adv
    impact = a.y * a.daily_vol * math.sqrt(part)
    spread = a.spread_bps / 2 / 1e4
    total = impact + spread
    notional = a.qty * a.price
    rows = [
        ("Order / ADV", f"{pct(part)}"),
        ("Impact (sqrt law)", f"{impact * 1e4:.1f} bps  (Y={a.y} x daily vol {pct(a.daily_vol)} x sqrt({part:.4f}))"),
        ("Half-spread", f"{spread * 1e4:.1f} bps"),
        ("Total one-way cost", f"{total * 1e4:.1f} bps  = {total * notional:,.0f} on {notional:,.0f}"),
        ("Round trip", f"{2 * total * 1e4:.1f} bps"),
    ]
    if part > 0.1:
        rows.append(("WARNING", ">10% of ADV: expect multi-day execution, information leakage, and worse-than-model costs"))
    if a.edge_bps is not None:
        rows.append(("Edge after costs", f"{a.edge_bps - 2 * total * 1e4:+.1f} bps per round trip"))
    out(rows, "Execution cost estimate")


# --------------------------------------------------------------------------- CLI
def build():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)

    x = s.add_parser("size", help="position size from risk budget")
    x.add_argument("--equity", type=float, required=True)
    x.add_argument("--risk", type=float, required=True, help="risk per trade, %% of equity (e.g. 0.5)")
    x.add_argument("--entry", type=float, required=True)
    x.add_argument("--stop", type=float)
    x.add_argument("--atr", type=float, help="ATR value; stop = atr * atr-mult")
    x.add_argument("--atr-mult", type=float, default=2.0)
    x.add_argument("--side", choices=["long", "short"], default="long")
    x.add_argument("--target", type=float)
    x.add_argument("--multiplier", type=float, default=1.0, help="contract multiplier / point value")
    x.add_argument("--lot", type=float, default=1.0)
    x.add_argument("--max-lev", type=float, default=2.0)
    x.set_defaults(fn=cmd_size)

    x = s.add_parser("kelly", help="Kelly fraction")
    x.add_argument("--p", type=float, help="win probability (0-1)")
    x.add_argument("--b", type=float, help="payoff ratio avg win / avg loss")
    x.add_argument("--mu", type=float, help="expected annual return (0.08 = 8%%)")
    x.add_argument("--sigma", type=float, help="annual vol")
    x.add_argument("--rf", type=float, default=0.0)
    x.set_defaults(fn=cmd_kelly)

    x = s.add_parser("expectancy", help="expectancy in R and sample size")
    x.add_argument("--p", type=float, required=True)
    x.add_argument("--win", type=float, required=True, help="avg win in R")
    x.add_argument("--loss", type=float, default=1.0, help="avg loss in R (positive)")
    x.add_argument("--trades", type=int, help="trades observed so far")
    x.set_defaults(fn=cmd_expectancy)

    x = s.add_parser("ruin", help="Monte Carlo drawdown/ruin probability")
    x.add_argument("--p", type=float, required=True)
    x.add_argument("--b", type=float, required=True)
    x.add_argument("--risk", type=float, required=True, help="%% risked per trade")
    x.add_argument("--trades", type=int, default=250)
    x.add_argument("--limit", type=float, default=30.0, help="drawdown %% that counts as ruin")
    x.add_argument("--sims", type=int, default=5000)
    x.add_argument("--fixed", dest="compound", action="store_false", help="fixed $ risk instead of compounding")
    x.add_argument("--seed", type=int, default=7)
    x.set_defaults(fn=cmd_ruin)

    x = s.add_parser("drawdown", help="recovery math and expected max drawdown")
    x.add_argument("--loss", type=float, nargs="*")
    x.add_argument("--sharpe", type=float)
    x.add_argument("--vol", type=float, default=0.15)
    x.add_argument("--years", type=float, default=10)
    x.add_argument("--ppy", type=int, default=252)
    x.add_argument("--sims", type=int, default=2000)
    x.add_argument("--seed", type=int, default=7)
    x.set_defaults(fn=cmd_drawdown)

    x = s.add_parser("sharpe", help="Sharpe significance, PSR, DSR, MinTRL")
    x.add_argument("--sr", type=float, required=True, help="annualized Sharpe")
    x.add_argument("--n", type=int, required=True, help="number of return observations")
    x.add_argument("--ppy", type=int, default=252)
    x.add_argument("--skew", type=float, default=0.0)
    x.add_argument("--kurt", type=float, default=3.0, help="non-excess kurtosis (normal=3)")
    x.add_argument("--trials", type=int, default=1, help="strategy variants tried (for DSR)")
    x.add_argument("--var-sr", type=float, help="variance of annualized Sharpes across trials")
    x.add_argument("--bench", type=float, default=0.0, help="benchmark annualized Sharpe for PSR")
    x.set_defaults(fn=cmd_sharpe)

    x = s.add_parser("perf", help="performance report from CSV")
    x.add_argument("file")
    x.add_argument("--col")
    x.add_argument("--prices", action="store_true", help="column holds prices/equity, not returns")
    x.add_argument("--percent", action="store_true", help="returns are in %% units")
    x.add_argument("--ppy", type=int, default=252)
    x.add_argument("--rf", type=float, default=0.0, help="annual risk-free rate")
    x.add_argument("--trials", type=int, default=1)
    x.add_argument("--var-sr", type=float)
    x.set_defaults(fn=cmd_perf)

    x = s.add_parser("vol", help="volatility estimators from OHLC CSV")
    x.add_argument("file")
    x.add_argument("--window", type=int, help="use last N bars")
    x.add_argument("--ppy", type=int, default=252)
    x.add_argument("--lam", type=float, default=0.94)
    x.set_defaults(fn=cmd_vol)

    x = s.add_parser("meanrev", help="half-life, Hurst, variance ratio")
    x.add_argument("file")
    x.add_argument("--col")
    x.add_argument("--log", action="store_true", help="take log of series first (prices)")
    x.add_argument("--max-lag", type=int, default=100)
    x.set_defaults(fn=cmd_meanrev)

    for name, fn in (("bs", cmd_bs), ("iv", cmd_iv)):
        x = s.add_parser(name, help="Black-Scholes price/Greeks" if name == "bs" else "implied vol")
        x.add_argument("--S", type=float, required=True)
        x.add_argument("--K", type=float, required=True)
        x.add_argument("--days", type=float, required=True, help="calendar days to expiry")
        x.add_argument("--r", type=float, default=0.04)
        x.add_argument("--q", type=float, default=0.0)
        x.add_argument("--kind", choices=["call", "put"], default="call")
        if name == "bs":
            x.add_argument("--vol", type=float, required=True, help="0.20 = 20%%")
            x.add_argument("--mult", type=float, default=100)
        else:
            x.add_argument("--price", type=float, required=True)
        x.set_defaults(fn=fn)

    x = s.add_parser("move", help="expected move from IV or straddle")
    x.add_argument("--S", type=float, required=True)
    x.add_argument("--days", type=float, required=True)
    x.add_argument("--vol", type=float)
    x.add_argument("--straddle", type=float)
    x.add_argument("--event-vol", type=float, help="IV of expiry containing the event")
    x.add_argument("--base-vol", type=float, help="ex-event IV (e.g. from a neighbouring expiry)")
    x.set_defaults(fn=cmd_move)

    x = s.add_parser("impact", help="market impact + spread")
    x.add_argument("--qty", type=float, required=True, help="shares/contracts to trade")
    x.add_argument("--adv", type=float, required=True, help="average daily volume (same units)")
    x.add_argument("--price", type=float, required=True)
    x.add_argument("--daily-vol", type=float, required=True, help="daily vol, 0.02 = 2%%")
    x.add_argument("--spread-bps", type=float, default=2.0)
    x.add_argument("--y", type=float, default=0.7, help="impact coefficient (0.5-1 typical)")
    x.add_argument("--edge-bps", type=float, help="expected gross edge per round trip")
    x.set_defaults(fn=cmd_impact)
    return p


def main(argv=None):
    a = build().parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
