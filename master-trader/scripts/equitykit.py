#!/usr/bin/env python3
"""equitykit -- single-stock analysis: earnings-move history, reverse/forward DCF, probabilistic projection.

Companion to fetch.py (fundamentals, earnings-dates, prices) and tradekit.py (iv, move, bs). Standard library only.

Commands
  earnings    reaction to each past earnings release (close before -> first close after, using AMC/BMO
              timing from `fetch.py earnings-dates`), gap, next-week drift, and a comparison of the
              historical move distribution with today's implied move (--straddle/--spot or --implied).
  dcf         reverse DCF: the starting FCF growth rate (fading to terminal growth) that today's price
              implies; or forward DCF value per share for a given growth path, with a WACC x growth grid.
  projection  price distribution at a horizon: (a) market-implied from IV (optionally a separate
              earnings jump and put/call-side vols), (b) your scenario tree (scenario,prob,price) with
              dispersion around each scenario; percentiles, P(above/below levels) and the gap between
              your view and the market's. Monte Carlo, seeded.

The market-implied distribution is risk-neutral: index options usually overstate realized vol (the VRP),
while single-stock earnings moves have historically been priced about fairly or slightly cheap. Treat
it as the market's starting point, not truth. Point price targets are the wrong format; give bands.
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import random
import statistics
import sys
from statistics import NormalDist

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tradekit import out, pct  # noqa: E402

N = NormalDist()


# --------------------------------------------------------------------------- io
def read_prices(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        r = csv.DictReader(fh)
        low = {k.strip().lower(): k for k in r.fieldnames or []}
        dk = low.get("date") or low.get("time") or list(low.values())[0]
        ck = low.get("adj close") or low.get("close")
        ok_ = low.get("open")
        if not ck:
            sys.exit(f"{path}: needs a close column")
        rows = []
        for row in r:
            try:
                rows.append((row[dk][:10], float(row[ok_]) if ok_ and row.get(ok_) else None, float(row[ck])))
            except (ValueError, TypeError):
                continue
    rows.sort()
    return rows


def read_dates(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        r = csv.DictReader(fh)
        out_ = []
        for row in r:
            low = {k.strip().lower(): v for k, v in row.items() if k}
            if low.get("date"):
                out_.append((low["date"][:10], (low.get("timing") or "AMC").upper()))
    return sorted(out_)


# --------------------------------------------------------------------------- earnings
def earnings_reactions(px, evs):
    """[(release, timing, reaction_date, move, gap, next5d)]; anchor = last close before the news."""
    dates = [d for d, _, _ in px]
    res = []
    for d, timing in evs:
        # anchor = last close before the information; reaction = first close after it
        j = next((i for i, x in enumerate(dates) if x >= d), None)
        if j is None:
            continue
        if timing == "AMC":
            if dates[j] == d:
                i0, i1 = j, j + 1
            else:
                i0, i1 = j - 1, j
        else:  # BMO / DMH: reaction on the release day
            i0, i1 = j - 1, j
        if i0 < 0 or i1 >= len(px):
            continue
        c0, (o1, c1) = px[i0][2], (px[i1][1], px[i1][2])
        r = c1 / c0 - 1
        gap = (o1 / c0 - 1) if o1 else None
        drift = (px[i1 + 5][2] / c1 - 1) if i1 + 5 < len(px) else None
        res.append((d, timing, dates[i1], r, gap, drift))
    return res


def cmd_earnings(a):
    res = earnings_reactions(read_prices(a.prices), read_dates(a.dates))
    if len(res) < 4:
        sys.exit(f"only {len(res)} earnings events overlap the price file -- fetch more price history")
    print(f"\n== Earnings reactions: {a.prices} ({len(res)} releases) ==")
    print(f"  {'release':<12}{'timing':<7}{'reaction':<12}{'move':>8}{'gap':>8}{'next 5d':>9}")
    for d, t, d1, r, g, dr in res[-a.show:]:
        print(f"  {d:<12}{t:<7}{d1:<12}{r:>+8.1%}{(f'{g:+.1%}' if g is not None else 'n/a'):>8}"
              f"{(f'{dr:+.1%}' if dr is not None else 'n/a'):>9}")
    moves = [r for *_, r, _, _ in res]
    absm = [abs(x) for x in moves]
    sd = statistics.pstdev(moves)
    rows = [
        ("Mean / median |move|", f"{pct(statistics.mean(absm), 1)} / {pct(statistics.median(absm), 1)}"),
        ("Std dev of moves (~1 SD)", pct(sd, 1)),
        ("Up / down reactions", f"{sum(1 for x in moves if x > 0)} / {sum(1 for x in moves if x < 0)}"),
        ("Largest up / down", f"{pct(max(moves), 1)} / {pct(min(moves), 1)}"),
    ]
    drifts_up = [dr for *_, r, _, dr in res if dr is not None and r > 0]
    drifts_dn = [dr for *_, r, _, dr in res if dr is not None and r < 0]
    if drifts_up and drifts_dn:
        rows.append(("Median next-5d drift after up / down", f"{pct(statistics.median(drifts_up), 1)} / "
                                                            f"{pct(statistics.median(drifts_dn), 1)}  (drift is weak for mega-caps; small n)"))
    implied_abs = None  # the market's expected ABSOLUTE move (what an ATM straddle prices)
    if a.straddle and a.spot:
        implied_abs = a.straddle / a.spot
    elif a.implied:
        implied_abs = a.implied * (0.798 if a.implied_is_sd else 1.0)
    if implied_abs:
        exceed = sum(1 for x in absm if x > implied_abs) / len(absm)
        ratio = statistics.mean(absm) / implied_abs  # fair = 1.0 (mean |move| vs expected |move|)
        rows += [
            ("Implied |move| now", f"{pct(implied_abs, 1)} expected absolute move (1 SD ~ {pct(implied_abs * 1.25, 1)})"),
            ("History vs implied", f"mean |move| = {ratio:.2f}x implied (fair ~1.0); {exceed:.0%} of past moves exceeded it "
                                   "(fair ~42% if normal, ~37% with fat tails)"),
            ("Read", ("options price a BIGGER move than this stock's past reactions (rich vs its own history)" if ratio < 0.85
                      else "options price a SMALLER move than its past reactions (cheap vs its own history)" if ratio > 1.15
                      else "implied is about in line with history")
                     + f"; n={len(absm)}, small sample, regimes change -- weigh against today's catalysts"),
        ]
    out(rows, "Summary")


# --------------------------------------------------------------------------- dcf
def dcf_value(fcf0, g0, tg, wacc, years):
    if wacc <= tg:
        return float("nan")
    v, f = 0.0, fcf0
    for t in range(1, years + 1):
        g = g0 + (tg - g0) * (t - 1) / max(1, years - 1)  # linear fade from g0 (year 1) to tg (final year)
        f *= 1 + g
        v += f / (1 + wacc) ** t
    tv = f * (1 + tg) / (wacc - tg)
    return v + tv / (1 + wacc) ** years


def implied_growth(fcf, target_ev, tg, wacc, years, lo=-0.5, hi=3.0):
    """Starting FCF growth (fading linearly to tg) whose DCF equals target_ev; None if above hi."""
    if dcf_value(fcf, hi, tg, wacc, years) < target_ev:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if dcf_value(fcf, mid, tg, wacc, years) > target_ev:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def cmd_dcf(a):
    fcf = a.fcf - (a.sbc or 0)
    if fcf <= 0:
        sys.exit("FCF (after the SBC adjustment, if given) must be positive for a DCF; use scenarios instead")
    mcap = a.price * a.shares
    target_ev = mcap - a.net_cash
    rows = [
        ("Inputs", f"price {a.price:,.2f} x {a.shares / 1e9:,.3f}bn shares = mcap {mcap / 1e9:,.0f}bn; net cash {a.net_cash / 1e9:,.1f}bn"),
        ("FCF base", f"{fcf / 1e9:,.2f}bn" + (f" (= FCF {a.fcf / 1e9:,.2f} - SBC {a.sbc / 1e9:,.2f})" if a.sbc else "")),
        ("Assumptions", f"WACC {pct(a.wacc, 1)}, terminal growth {pct(a.tg, 1)}, {a.years}y explicit, growth fades linearly to terminal"),
        ("FCF yield (TTM)", pct(fcf / mcap, 2)),
    ]
    g = implied_growth(fcf, target_ev, a.tg, a.wacc, a.years)
    if g is None:
        rows.append(("Implied starting growth", "> 300% -- price is not justified by any growth path at this WACC"))
    else:
        f, path = fcf, []
        for t in range(1, a.years + 1):
            f *= 1 + g + (a.tg - g) * (t - 1) / max(1, a.years - 1)
            path.append(f)
        rows += [
            ("Implied starting FCF growth", f"{pct(g, 1)}/yr, fading to {pct(a.tg, 1)} by year {a.years}"),
            ("Implied FCF in year 5 / 10", f"{path[4] / 1e9:,.0f}bn / {path[-1] / 1e9:,.0f}bn ({path[-1] / fcf:.1f}x today)"),
        ]
        if a.fcf_margin:
            rows.append(("Implied revenue in year 10", f"{path[-1] / a.fcf_margin / 1e9:,.0f}bn at a {pct(a.fcf_margin, 0)} FCF margin"))
        tv_share = (path[-1] * (1 + a.tg) / (a.wacc - a.tg) / (1 + a.wacc) ** a.years) / target_ev
        rows.append(("Terminal value share of EV", f"{pct(tv_share, 0)} (above ~70% means the price rests on the far future)"))
    out(rows, "Reverse DCF: what the price implies")
    if a.growth:
        print(f"\n== Forward DCF value per share (rows: WACC; cols: starting growth) ==")
        waccs = [a.wacc - 0.01, a.wacc, a.wacc + 0.01]
        print("  " + f"{'WACC':<8}" + "".join(f"{pct(g, 0):>10}" for g in a.growth))
        for w in waccs:
            vals = [(dcf_value(fcf, g, a.tg, w, a.years) + a.net_cash) / a.shares for g in a.growth]
            print("  " + f"{pct(w, 1):<8}" + "".join(f"{v:>10,.0f}" for v in vals))
        print(f"  vs price {a.price:,.2f}. A DCF is a map of assumptions, not a forecast -- argue about the inputs.")


# --------------------------------------------------------------------------- projection
def sample_log_return(rng, T, iv, iv_dn, iv_up, ev_sd):
    """One draw of log(S_T/S_0) under a split-vol lognormal with an optional earnings jump; zero-drift (martingale)."""
    sd_dn, sd_up = (iv_dn or iv) * math.sqrt(T), (iv_up or iv) * math.sqrt(T)
    z = rng.gauss(0, 1)
    x = z * (sd_dn if z < 0 else sd_up)
    if ev_sd:
        x += rng.gauss(0, ev_sd)
    var = ((sd_dn ** 2 + sd_up ** 2) / 2) + (ev_sd ** 2 if ev_sd else 0)
    return x - 0.5 * var


def pctiles(xs, qs=(0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95)):
    xs = sorted(xs)
    return [xs[min(len(xs) - 1, int(q * len(xs)))] for q in qs]


def simulate(spot, T, base_iv, iv_down=None, iv_up=None, ev_sd=None, scenarios=None, scenario_vol=None,
             sims=100000, seed=7):
    """Market-implied price samples and, if scenarios [(name, prob, price)] are given, scenario-mixture samples."""
    rng = random.Random(seed)
    mkt = [spot * math.exp(sample_log_return(rng, T, base_iv, iv_down, iv_up, ev_sd)) for _ in range(sims)]
    k_ = spot / statistics.mean(mkt)  # exact martingale: E[S_T] = spot under zero drift
    mkt = [x * k_ for x in mkt]
    mine = None
    if scenarios:
        tot = sum(p for _, p, _ in scenarios)
        probs = [p / tot for _, p, _ in scenarios]
        disp = (scenario_vol or base_iv * 0.6) * math.sqrt(T)
        cum = [sum(probs[:i + 1]) for i in range(len(probs))]
        mine = []
        for _ in range(sims):
            u = rng.random()
            k = next((i for i, c in enumerate(cum) if u <= c), len(cum) - 1)
            mine.append(scenarios[k][2] * math.exp(rng.gauss(0, disp) - 0.5 * disp * disp))
    return mkt, mine


def cmd_projection(a):
    T = (a.trading_days / 252) if a.trading_days else a.days / 365
    ev_sd = None
    if a.event_move:
        ev_sd = math.log(1 + a.event_move)  # 1-SD earnings move
    elif a.event_straddle and a.spot:
        ev_sd = math.log(1 + 1.25 * a.event_straddle / a.spot)
    base_iv = a.base_iv or a.iv
    sc = None
    if a.scenarios:
        with open(a.scenarios, newline="", encoding="utf-8-sig") as fh:
            raw = list(csv.DictReader(fh))
        low = lambda r, k: next((v for kk, v in r.items() if kk and kk.strip().lower() == k), None)
        probs = [float(low(r, "prob")) for r in raw]
        scale = 100 if max(probs) > 1 else 1
        sc = [(low(r, "scenario") or f"s{i}", p / scale, float(low(r, "price"))) for i, (r, p) in enumerate(zip(raw, probs))]
    mkt, mine = simulate(a.spot, T, base_iv, a.iv_down, a.iv_up, ev_sd, sc, a.scenario_vol, a.sims, a.seed)
    cols = [("market-implied", mkt)]
    if mine:
        tot = sum(p for _, p, _ in sc)
        names, probs, prices = [n for n, _, _ in sc], [p / tot for _, p, _ in sc], [x for _, _, x in sc]
        cols.append(("your scenarios", mine))
        print(f"\n== Scenario tree ({a.scenarios}) ==")
        for n_, p, pr in zip(names, probs, prices):
            print(f"  {n_:<24}{p:>6.0%}{pr:>12,.2f}{pr / a.spot - 1:>+9.1%}")
        ev_px = sum(p * pr for p, pr in zip(probs, prices))
        print(f"  {'probability-weighted':<24}{'':>6}{ev_px:>12,.2f}{ev_px / a.spot - 1:>+9.1%}")
    print(f"\n== Price distribution in {a.trading_days or a.days} {'trading' if a.trading_days else 'calendar'} days "
          f"(spot {a.spot:,.2f}; {a.sims:,} sims) ==")
    print(f"  {'percentile':<20}" + "".join(f"{n_:>18}" for n_, _ in cols))
    labels = ["5th", "10th", "25th", "median", "75th", "90th", "95th"]
    ps = [pctiles(xs) for _, xs in cols]
    for i, lab in enumerate(labels):
        print(f"  {lab:<20}" + "".join(f"{p[i]:>12,.2f} {p[i] / a.spot - 1:>+5.0%}" for p in ps))
    print(f"  {'mean':<20}" + "".join(f"{statistics.mean(xs):>12,.2f} {statistics.mean(xs) / a.spot - 1:>+5.0%}" for _, xs in cols))
    if a.levels:
        print(f"\n  {'P(price > level)':<20}" + "".join(f"{n_:>18}" for n_, _ in cols) + ("      gap" if len(cols) > 1 else ""))
        for L in a.levels:
            pr = [sum(1 for x in xs if x > L) / len(xs) for _, xs in cols]
            gap = f"{(pr[1] - pr[0]) * 100:>+8.0f}pt" if len(pr) > 1 else ""
            print(f"  {L:<20,.2f}" + "".join(f"{p:>18.0%}" for p in pr) + gap)
    iv_txt = f"IV {pct(base_iv, 1)}" + (f" (down {pct(a.iv_down, 0)} / up {pct(a.iv_up, 0)})" if a.iv_down or a.iv_up else "")
    print(f"\n  Market-implied: zero-drift lognormal, {iv_txt}" + (f", plus an earnings jump of 1 SD {pct(math.exp(ev_sd) - 1, 1)}" if ev_sd else "") + ".")
    print("  It is risk-neutral (no equity premium, includes any vol premium). The gap column is where your view")
    print("  disagrees with the market -- that gap, not the price target, is the trade idea. Probabilities are judgments.")


# --------------------------------------------------------------------------- CLI
def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("earnings", help="earnings-day move history vs today's implied move")
    x.add_argument("--prices", required=True, help="daily OHLC CSV (fetch.py prices)")
    x.add_argument("--dates", required=True, help="earnings dates CSV (fetch.py earnings-dates)")
    x.add_argument("--straddle", type=float, help="current ATM straddle price for the earnings expiry")
    x.add_argument("--spot", type=float)
    x.add_argument("--implied", type=float, help="implied expected |move| as a fraction, e.g. 0.07")
    x.add_argument("--implied-is-sd", action="store_true", help="--implied is a 1-SD move (converted x0.798)")
    x.add_argument("--show", type=int, default=16)
    x.set_defaults(fn=cmd_earnings)
    x = s.add_parser("dcf", help="reverse / forward DCF")
    x.add_argument("--price", type=float, required=True)
    x.add_argument("--shares", type=float, required=True, help="diluted shares (count, e.g. 24.3e9)")
    x.add_argument("--fcf", type=float, required=True, help="TTM free cash flow in $ (e.g. 127e9)")
    x.add_argument("--sbc", type=float, help="subtract stock-based comp from FCF (owner-earnings view)")
    x.add_argument("--net-cash", type=float, default=0.0, help="cash + securities - debt, $")
    x.add_argument("--wacc", type=float, default=0.09)
    x.add_argument("--tg", type=float, default=0.03, help="terminal growth (keep <= long-run nominal GDP / risk-free)")
    x.add_argument("--years", type=int, default=10)
    x.add_argument("--fcf-margin", type=float, help="to translate implied FCF into implied revenue")
    x.add_argument("--growth", type=float, nargs="*", help="starting growth rates for the forward-DCF grid")
    x.set_defaults(fn=cmd_dcf)
    x = s.add_parser("projection", help="market-implied vs scenario price distribution")
    x.add_argument("--spot", type=float, required=True)
    x.add_argument("--days", type=float, default=30, help="calendar days to the horizon")
    x.add_argument("--trading-days", type=int, help="use trading days instead (T = n/252)")
    x.add_argument("--iv", type=float, required=True, help="implied vol for the horizon (annualized, incl. event if no --base-iv)")
    x.add_argument("--base-iv", type=float, help="ex-event vol when adding an explicit earnings jump")
    x.add_argument("--event-move", type=float, help="1-SD earnings move as a fraction (e.g. 0.08)")
    x.add_argument("--event-straddle", type=float, help="earnings straddle price (1 SD ~ 1.25 x straddle)")
    x.add_argument("--iv-down", type=float, help="vol for the downside half (put skew)")
    x.add_argument("--iv-up", type=float, help="vol for the upside half")
    x.add_argument("--scenarios", help="CSV: scenario,prob,price")
    x.add_argument("--scenario-vol", type=float, help="dispersion around each scenario (annualized; default 0.6 x IV)")
    x.add_argument("--levels", type=float, nargs="*", help="price levels for P(above)")
    x.add_argument("--sims", type=int, default=100000)
    x.add_argument("--seed", type=int, default=7)
    x.set_defaults(fn=cmd_projection)
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
