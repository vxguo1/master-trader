# Momentum Trading: Signals, Playbooks, Lifecycle and Crash Risk

*Read when: a user builds, screens, backtests or reviews a momentum, trend, breakout, relative-strength, dual-momentum or intraday-momentum strategy. Also read for CAN SLIM, Minervini (SEPA/VCP), Darvas, Qullamaggie, Weinstein or Turtle rules; for stop, trail and pyramid design on trend trades; for a momentum drawdown or crash; or for "does momentum still work" (2023-2026).*

Tags: evidence grades `[Strong] [Moderate] [Weak] [Contested] [Lore]`. Provenance flags: **(V)** = verified against a primary or fetched source; **(K)** = known citation, not re-fetched; **≈** = magnitude to spot-check before quoting as exact. "UMD" = Kenneth French US momentum factor (long-short, value-weighted, gross of costs).

## Contents
1. Core principles
2. Signal construction and refinements
3. Allocation-style trend and dual momentum
4. Intraday momentum, and what real day traders earn
5. Practitioner playbooks (rule cards)
6. Momentum trade lifecycle (default procedure)
7. Risk and failure modes, and how pros mitigate them
8. Recent performance, 2023-2026
9. Traps in a user's plan or backtest
10. Toolkit hooks
11. Key sources

---

## 1. Core principles

- **The signal is old news; the edge is in implementation.** Raw US UMD compounded +8.05%/yr in 1927-1999 but only +0.46%/yr in 2000-2025 and −0.55%/yr in 2016-2025, gross of costs (computed from French data through Sep-2026, (V) data). A user who buys a plain 12-1 screen is buying a premium that has barely paid for 25 years. Risk management, path quality, diversification and costs now decide the outcome. [Strong]
- **Manage the risk, not the mean.** Momentum's volatility is predictable from its own recent volatility; its mean is not. Vol scaling and dynamic weighting roughly double Sharpe and cut the worst month by tens of points (Barroso & Santa-Clara 2015; Daniel & Moskowitz 2016). [Strong] for momentum specifically.
- **Crashes depend on the market state, and the dangerous states can be spotted.** They come after a bear market with high volatility, at the rebound, when beaten-down losers rip (2009). They also come after narrow-leadership runs, when leadership rotates violently (Nov-2020, Jan-2023, Jul-Aug-2026). Flag these states and de-risk. [Moderate]
- **Path quality picks the winners that keep winning.** Being near the 52-week high, rising smoothly in small steps (frog-in-the-pan) and having a fresh earnings catalyst are what the swing-trading playbook of "leaders near highs" puts into practice. They are also its strongest academic support. [Moderate]
- **Expect a low win rate and a fat right tail.** Breakout and trend systems win about 25-50% of trades. Fewer than 7% of single-stock trend trades produced the majority of profits (Zarattini, Pagani & Wilcox 2025, (V)). The job is to keep losses small and never cut off the tail. Judge a system by its expectancy and its sample size, never by its win rate. [Moderate]
- **Size by risk, then cap by gap.** Risk 0.25-1% of equity per trade and cap the size of any single name held overnight. Momentum returns accrue overnight (Lou, Polk & Skouras 2019), so the overnight gap is both the source of the return and the risk that jumps your stop. [Moderate]
- **Discount everything published, and discount vendors more.** Anomaly returns fall ≈26% out of sample and ≈58% after publication (McLean & Pontiff 2016). Intraday backtests run at 4x leverage by a firm that sells the research are marketing until someone replicates them. Real-account studies find ≈97% of persistent day traders lose money. [Strong]
- **Prefer simple, ensembled parameters.** Lookback fine-tuning is noise next to rebalance-timing luck (≈350 bp/yr between schedules). Prefer ensembles of lookbacks and tranches to a single "optimal" setting. [Moderate]
- **Trend is drawdown insurance, not a return booster.** In allocation, a 10-month SMA or 12-month absolute-momentum filter lags V-shaped recoveries and whipsaws in choppy years. Its job is to avoid the 1973-74 and 2008 kind of loss. [Strong] for diversified trend; [Moderate] for single-index filters.

---

## 2. Signal construction and refinements

### 2.1 Signal menu with evidence grade

| Signal | Construction (published defaults) | What it buys | Grade |
|---|---|---|---|
| 12-1 cross-sectional (XS) | Rank on P(t−1)/P(t−12) − 1; long top decile/30%; rebalance monthly | ≈1%/month historically (JT 6/6); partly reverses in years 2-5 | [Strong] (K) Jegadeesh & Titman 1993/2001 |
| Skip-month | Exclude month t−1 (12-1 or 12-2). The French "Mom" factor uses months −12 to −2 (V) | Avoids the 1-month reversal (bid-ask bounce, liquidity provision) | [Strong] (K) Jegadeesh 1990; Lehmann 1990 |
| "Echo" (months 12-7 beat 6-2) | Use intermediate-horizon return | Better prediction in US data | [Contested]: Novy-Marx 2012 finds it; Goyal & Wahal 2015 find it not robust in 36 non-US markets |
| 52-week-high | P / 52wkH; ≥0.9 = "near high" | Explains much of JT and industry momentum and wins horse races against both; **no long-run reversal** | [Moderate] (K) George & Hwang 2004; no 2021-26 replication found |
| Frog-in-the-pan (FIP) | ID = sign(R12-1) × (%down days − %up days); prefer the lowest ID | Momentum concentrates in continuous-information (smooth) stocks; little in jumpy ones (limited attention) | [Moderate] (K) Da, Gurun & Warachka 2014 |
| Quantitative Momentum (commercial) | Top 12-1 decile → keep the smoothest half by FIP → rebalance quarterly | FIP put into practice | [Weak] (K) Gray & Vogel 2016 |
| Residual momentum | Regress on FF3 over a rolling 36m; sum residuals over 12-1; divide by σ(residuals) | ≈½ the volatility, ≈2× the Sharpe, much smaller crash exposure; holds post-publication and internationally | [Moderate] (K) Blitz, Huij & Martens 2011; Blitz et al. 2020 (same research group) |
| Industry momentum | 6-12m industry return; a 1-month version works (the exception to skip-month) | Accounts for much of stock momentum | [Strong] (K) Moskowitz & Grinblatt 1999. How much it explains is [Contested] (Grundy & Martin 2001) |
| Industry/sector trend | Trend rules on 48 industries, 1926-2024 | 18.5%/yr vs 9.7% for equities, Sharpe 1.46 | [Weak] (V) Zarattini & Antonacci 2024 (co-author has commercial interest) |
| Factor momentum | Long factors with positive trailing 12m return (time series) | "Explains all forms of individual stock momentum". Average factor earns ≈1 bp/month after a losing year vs ≈53 bp after a winning year | [Moderate] (V) Ehsani & Linnainmaa 2022; (K) Gupta & Kelly 2019 (65 factors) |
| Earnings momentum / PEAD | SUE; gap-up on an earnings beat | Captures much of price momentum. **PEAD has largely vanished in large/mid caps** and survives in micro/small caps | [Moderate] (K) Chordia & Shivakumar 2006; Novy-Marx 2015; Martineau 2022 |
| Vol-scaled | w = 12% ÷ σ̂(126 daily returns, annualized); cap leverage | Sharpe 0.53 → 0.97 (V); worst month ≈−79/−80% → −28.4% (≈); excess kurtosis ≈18.2 → 2.7 (K, ≈) | [Strong] for momentum. Vol-management of *generic* factors is [Contested]: Moreira & Muir 2017 find gains; Cederburg et al. 2020 find most fail out of sample |
| Dynamic (Daniel-Moskowitz) | Weight ∝ forecast mean ÷ forecast variance. The mean forecast drops when the bear indicator (24m market return < 0) coincides with high market variance | ≈2× the Sharpe of static; works across asset classes | [Moderate] (K) Daniel & Moskowitz 2016 |
| Risk-adjusted (MTUM-style) | 6m and 12m excess return ÷ 3y weekly vol; rebalance semi-annually | Stock-level version of the Barroso adjustment; benchmark is now "MSCI USA Momentum SR Variant" (V) | Index methodology (K) |
| Time-series (TSMOM) | Sign of 12m excess return; 1m hold; each instrument scaled to 40% vol; 58 futures | Robust in diversified futures | [Strong] for diversified portfolios. Edge over XS is [Contested]: mostly time-varying net-long exposure (Goyal & Jegadeesh 2018); single-asset predictability weak (Huang et al. 2020) |
| Overnight split | Momentum profits accrue overnight; many other anomalies accrue intraday | Holding overnight *is* the trade | [Moderate] (K) Lou, Polk & Skouras 2019 |
| Rebalance tranching | Split the book into staggered sub-portfolios | Best vs worst schedule ≈350 bp/yr apart (US momentum, 1991-2024) | [Weak] (V) Zarattini & Pagani 2025 (working paper) |

### 2.2 Recipes

```
mom_12_1     = P[t-21] / P[t-252] - 1                       # daily bars; skip ~1 month
mom_risk_adj = mom_12_1 / stdev(daily returns, 252) / sqrt(252)
hi52_ratio   = P[t] / max(High, 252)                         # >=0.90 near high; >=0.75 = Minervini 25% rule
FIP_ID       = sign(mom_12_1) * (pct_down_days - pct_up_days) # over the formation window; lower = smoother
resid_mom    = sum(eps[t-12..t-2]) / stdev(eps)              # eps from rolling 36m FF3 regression, monthly
IBD_RS_proxy = 0.4*ROC63 + 0.2*ROC126 + 0.2*ROC189 + 0.2*ROC252   # screener approximation, NOT IBD-official [Lore]
VAA_13612W   = 12*r1m + 4*r3m + 2*r6m + 1*r12m              # Keller fast momentum score
vol_scale    = min(cap, target_vol / realized_vol_126d)      # target 12% (BSC); cap 2x
turtle_N     = (19*N_prev + TrueRange) / 20                  # 20-day Wilder-style ATR
```

### 2.3 What to work on first (ranked by impact)
1. **Risk management of the book**: vol scaling, a bear-state/rebound filter, residualizing or neutralizing industries. These change crash outcomes by tens of percentage points.
2. **Path-quality filters**: 52-week-high proximity and FIP smoothness tilt the book toward continuations.
3. **Lookback fine-tuning**: mostly noise next to ≈350 bp/yr of rebalance-timing luck. Use an ensemble (e.g., 3/6/12m) and tranches instead of hunting for one optimum.

Prior for any published refinement: haircut the backtest edge by ≈⅓-½ (McLean & Pontiff: −26% out of sample, −58% post-publication). [Strong]

### 2.4 Vol scaling on French UMD (crude replication: 12% target, trailing 6-month sd of *monthly* returns, 2x leverage cap, gross) [Moderate]

| Sample | Sharpe static → scaled | Max DD static → scaled | Other |
|---|---|---|---|
| Jul-1927 to Sep-2026 | 0.45 → 0.71 | −78.4% → −46.2% | CAGR 6.0% → 10.6%; skew −3.00 → −0.90; worst month −52.6% → −38.4% |
| 2000 to Sep-2026 | 0.14 → 0.28 | −57.8% → −29.7% | |
| 2016 to Sep-2026 | n/a | n/a | CAGR 0.45% → 2.6% |
| 2023 to Sep-2026 | 0.12 → 0.27 | −22.5% → −18.4% | |

Monthly vol estimates react slowly. The published daily-estimator version cuts crashes far more (worst month ≈−28%). Scaling helps in every sub-period, but it cannot rescue a premium that is near zero.

### 2.5 Across asset classes

| Asset | Robust form | Evidence | Notes |
|---|---|---|---|
| Diversified futures (CTA) | TSMOM with vol scaling | [Strong] Hurst, Ooi & Pedersen 2017: positive in every decade since 1880, "crisis alpha" | Single-market trend is noisy |
| Value + momentum, all assets | Combine; they are negatively correlated | [Strong] Asness, Moskowitz & Pedersen 2013 (8 markets) | The combination is far more stable than either alone |
| FX | XS winners minus losers, up to ≈10%/yr | [Moderate] (K) Menkhoff et al. 2012 | Concentrated in illiquid, high-cost pairs; limits to arbitrage |
| Commodities | Long-short momentum, ≈9%/yr | [Moderate] (K) Miffre & Rallis 2007 | |
| Crypto | TS momentum at 1-4 week horizons; size + momentum factors | [Moderate] (V/K) Liu & Tsyvinski 2021; Liu, Tsyvinski & Wu 2022. XS momentum among 143 coins not significant: Grobys & Sapkota 2019 → [Contested] | Prefer short lookbacks and vol-sized Donchian ensembles (Concretum 2025: Sharpe >1.5 net, [Weak]). 24/7 trading, exchange and gap risk |

---

## 3. Allocation-style trend and dual momentum

| Model | Rules | Backtest claim | Out-of-sample record | Grade |
|---|---|---|---|---|
| **Faber GTAA** | Hold each asset class when month-end price > 10-month SMA, else cash. Check **only at month-end**. 10m ≈ 200-day; results stable for 3-12+ month SMA/EMA. 5 asset classes; bonds can be buy-and-hold (timing them adds little) (V) | Equity-like return, much lower vol and drawdown (1973-74, 2008) (K) | Concretum update to Mar-2025: CAGR 6.05%, Sharpe 0.68, max DD 11.7% (V). The window split and benchmark are not stated, so outperformance is **not** established | [Moderate] |
| **Antonacci GEM** | Monthly: pick the stronger 12m return of US vs ex-US equities. If US 12m return < T-bills → aggregate bonds | ≈17% CAGR, max DD ≈−23% vs ≈−51% S&P (1974-2013) (K, ≈) | Post-2014 lag vs the S&P 500 and costly whipsaws (2015-16, Q4-2018, 2020, 2022) are widely reported, **unverified** (tracker sites unreachable). ReSolve (Butler 2019) tested 324 lookback combinations (18 trend × 18 momentum, 1-18m) and recommends **ensembles over the single 12/12 choice** (V) | [Weak] live; [Moderate] concept |
| **Keller PAA (2016)** | Bond/cash share rises with breadth: the count of risky assets below their 12m SMA | Short-sample optimization | None verified | [Weak] |
| **Keller VAA (2017)** | 13612W score. If *any* risky asset scores < 0 → fully defensive | Strong in-sample | None verified; very frequent defensive switches | [Weak] |
| **Keller DAA (2018)** | Separate "canary" universe (VWO, BND) triggers protection | Strong in-sample | None verified | [Weak] |
| **Long-run trend** | 1/3/12m TS trend, diversified | Positive every decade since 1880 | Long, multi-market | [Strong] (K) Hurst, Ooi & Pedersen 2017 |

**What to tell a user who adopts one:**
- Expect to lag buy-and-hold in strong bull runs and V-shaped recoveries (2020, 2023), and 1-3 whipsaws in choppy years.
- Expect poor protection when stocks and bonds fall together (2022), because the defensive asset falls too. Default to cash/T-bills when bonds are themselves below trend.
- Fix single-lookback fragility with ensembles of 3-12 month lookbacks plus tranching (e.g., four weekly sub-portfolios).
- Credibility order: simple, long-tested rules (Faber, Hurst-Ooi-Pedersen) > optimized multi-parameter canary models > any newsletter "live" claim.
- Test with `techkit.py ruletest FILE --rule sma --params 200` (daily-checked, so it trades more than the month-end rule) and `--rule tsmom --params 252` (tests against 0, not T-bills).

---

## 4. Intraday momentum, and what real day traders earn

### 4.1 The academic effect
- **Market intraday momentum** (Gao, Han, Li & Zhou 2018, *JFE*; SPY 1993-2013). The first half-hour return (prior close → 10:00 ET) predicts the last half-hour (15:30-16:00) with predictive R² 1.6% (out of sample 1.2%) (V). The 12th half-hour adds power. The timing rule earned ≈6-7%/yr with Sharpe ≈1 before costs (K, ≈, unverified). A third-party replication (CXO Advisory) found 6.3% gross annualized vs −0.5% for holding every last half-hour (V, secondary). [Strong] as an effect; [Weak] evidence that it is still tradable after 2013 (no post-publication study found).
- **Replications:** 60+ futures across equities, bonds, commodities and FX, stronger when dealers are **net short gamma** (hedging and leveraged-ETF rebalancing push late flows in the direction of the day) (K, Baltussen, Da, Lammers & Martens 2021). 16 developed equity markets (K, Li, Sakkas & Urquhart 2022). FX (K, Elaut et al. 2018). [Strong]
- **Conditions that strengthen it:** high-volatility days, high-volume days, recessions, macro-news days, negative dealer gamma, high relative volume.

### 4.2 Practitioner intraday strategies (all from Concretum Group, which sells research, software and trading services)

| Strategy | Rules (K = recalled from paper, unconfirmed) | Reported result (V) | Grade |
|---|---|---|---|
| **ORB on QQQ** (Zarattini & Aziz 2023) | Trade in the direction of the first 5-min candle (no trade on a doji), entering at the second candle. Stop at the opposite extreme of the range. Target 10R, else exit at the close. Risk 1%/trade; leverage ≤4x; commission ≈$0.0005/sh (K) | 2016-2023: ≈33%/yr alpha net of commissions. Via TQQQ: 1,484% total vs 169% for QQQ. No drawdown or Sharpe reported | [Weak] |
| **ORB on Stocks in Play** (Zarattini, Barbon & Aziz 2024) | Price > $5; 14d avg volume ≥ 1M; 14d ATR ≥ $0.50. First-5-min relative volume ≥ 100%; take the top 20 by relative volume. Stop-order entry at the range extreme in the first candle's direction. Stop = 10% of 14d ATR. Exit at the close. Risk 1%; ≤4x (K) | 7,000+ US stocks, 2016-2023: >1,600% total net, Sharpe 2.81, 36%/yr alpha vs ≈198% for the S&P | [Weak] |
| **SPY noise-band trend** (Zarattini, Aziz & Barbon 2024) | σ(τ) = 14d mean of abs(P_τ/Open − 1) at each time of day. Upper = max(Open, prev Close)·(1+σ); Lower = min(Open, prev Close)·(1−σ). Check at :00/:30; long above the upper band, short below the lower. Trail at the band or VWAP, whichever is tighter; flat at the close. Size for 2% daily vol, ≤4x; costs $0.0035 + $0.001/sh (K) | 2007 to early 2024 net: 1,985% total, 19.6%/yr, Sharpe 1.33 | [Weak] |
| VWAP system, QQQ/TQQQ | (not detailed) | Jan-2018 to Sep-2023: $25k → $192,656 (QQQ) / $2,085,417 (TQQQ) | [Weak] |
| **Episodic pivot** (Qullamaggie) | See §5.5 | Self-reported | [Lore] |
| Gap-and-go, low-float (Warrior-style) | none rigorous | Marketing only | [Lore] |

**Caveats to state every time:**
- One firm with a commercial interest produced all of these.
- No independent peer-reviewed replication and no live 2024-2026 record was found.
- The headline returns come from 4x intraday leverage or 3x ETFs; Sharpe is the statistic that transfers.
- At the open, spreads on small names in play and partial fills on stop orders erode results.
- The low win rate and high payoff (tight ATR-fraction stops, 10R or the close as target) mean long losing streaks.

### 4.3 Real-account outcomes (set these against any intraday backtest)

| Study | Population | Finding | Grade |
|---|---|---|---|
| Barber, Lee, Liu & Odean 2014 | All Taiwan day traders, 1992-2006 | **< 1%** are predictably profitable net of fees; the group as a whole loses | [Strong] (K) |
| Chague, De-Losso & Giovannetti 2019/20 | 1,551 Brazilians who day-traded mini-index futures 300+ days (2013-15 starters) | **97% lost money**; 1.1% earned more than the minimum wage; ≈0.5% more than a bank teller's starting pay; **no evidence of learning** (V) | [Strong] |

How a master reconciles the two: the effect is real and the backtests are plausible. Execution, costs, leverage discipline and the psychology of 70%-loss-rate trading are where retail traders fail. Before risking size, demand a forward-tested log of 300+ trades for a 25-30% win-rate system (see `expectancy` in §10).

---

## 5. Practitioner playbooks (rule cards)

They all follow one pattern: buy strength near highs, in leaders, in a confirmed uptrend; enter on a breakout from a tight base with volume expansion; cut losers fast; trail winners. Evidence status: the **ingredients** have academic support (52-week high, FIP, earnings momentum, right-tail concentration). The **specific pattern rules** (cup depths, VCP counts, box definitions) have no peer-reviewed or audited validation that I found. Performance claims are anecdotes.

### 5.1 O'Neil CAN SLIM / IBD (O'Neil 2009, (K))
| Field | Rule |
|---|---|
| Universe/screen | **C**: quarterly EPS ≥ +25% y/y, ideally accelerating, with sales growth. **A**: annual EPS growth ≥ 25% for 3 years; ROE ≥ 17%. **N**: new product, management or industry condition, plus a new high. **S**: supply and demand (share supply vs. volume demand). **L**: RS Rating ≥ 80. **I**: rising institutional sponsorship |
| Setup | A proper base. Cup-with-handle: cup ≈7-65 weeks, depth ≈12-33%, handle in the upper half drifting down on light volume |
| Entry trigger | Breakout through the pivot on volume ≥ 40-50% above average; buy no more than ≈5% above the pivot |
| Stop | Always cut at 7-8% below cost |
| Exits | Take most profits at +20-25%. If a stock gains ≥ 20% within 3 weeks of breakout, hold it at least 8 weeks. Sell on climax runs |
| Sizing | Not specified as % risk. At 0.5-1% risk with a 7-8% stop, a position is ≈6-14% of equity |
| Regime filter | **M**: confirmed uptrend via a follow-through day (a big up day on higher volume, day 4+ of a rally attempt). Uptrend in doubt after 4-6 distribution days within ≈4-5 weeks |
| Win rate vs payoff | Break-even win rate ≈24-29% (−8% vs +20-25%) |
| Evidence | [Lore] as a rule set. Real-money proxy FFTY (IBD 50 list, launched Apr-2015): since-inception annualized NAV **+1.88% vs +13.29% for the S&P 500** (fund factsheet, as of 31-Dec-2024; (V) via search snippet). FFTY was reorganized into a Capital-Force ETF Trust series on 27-Apr-2026 (V). A list-based ETF does not test the full discretionary method |

### 5.2 Minervini: Trend Template + VCP + SEPA (Minervini 2013, 2017, (K))
| Field | Rule |
|---|---|
| Universe/screen | **Trend Template, all 8 must hold**: (1) price > 150d and 200d MA; (2) 150d > 200d; (3) 200d rising ≥ 1 month (prefer 4-5+); (4) 50d > 150d and 200d; (5) price > 50d; (6) price ≥ 30% above the 52w low; (7) within 25% of the 52w high; (8) RS ≥ 70 (prefer 80-90s). This is Weinstein Stage 2 |
| Setup | VCP: 2-6 successive pullbacks, each ≈half the depth of the last (e.g., 25% → 12% → 6%), with volume drying up on the right side |
| Entry trigger | Pivot breakout on volume expansion |
| Stop | ≤ 10%, ideally much tighter; average loss ≈5-6% |
| Exits/trailing | Raise the stop to breakeven once the gain is a multiple of initial risk. Keep average gain ≥ 2× average loss |
| Sizing | Risk-based (see §6). The notes give no fixed % |
| Regime filter | The template is a stock-level Stage 2 filter. Add the market gate from §6 |
| Win rate vs payoff | ≈50% at 2:1 → +0.5R/trade (break-even 33%) |
| Evidence | [Lore]. US Investing Championship: 1997 +155%; 2021 +334.8% ($1M+ stock division, a record at the time) (V). Contest results are short-horizon, self-selected winners from many entrants |

### 5.3 Darvas Box (Darvas 1960, (K))
| Field | Rule |
|---|---|
| Universe/screen | Stocks making new highs with improving earnings ("techno-fundamentalist") |
| Setup | Box top = a new high not exceeded for 3 days. Box bottom = a low not violated for 3 days after the top is set |
| Entry trigger | Buy-stop just above the box top on rising volume |
| Stop / trailing | Just below the box bottom; raise it as new boxes stack |
| Sizing / regime | Not specified; used margin; the record comes from the 1957-59 bull market |
| Evidence | [Lore]. ≈$25-36k → ≈$2M is unaudited and margin-assisted |

### 5.4 Weinstein Stage Analysis (Weinstein 1988, (K))
| Field | Rule |
|---|---|
| Universe/screen | Weekly charts, 30-week MA. Stage 1 base (flat MA) → Stage 2 advance (breaks resistance, MA turns up) → Stage 3 top (MA flattens) → Stage 4 decline |
| Order of checks | "Forest to trees": market stage (index vs 30-week MA, breadth/A-D line) → sector → stock |
| Entry trigger | Stage 2 breakout on breakout-week volume ≥ 2× the recent average, with the Mansfield RS line (stock/index vs its own 52-week average) positive and rising |
| Stop / trailing | Initial stop below the base or prior correction low; trail under successive correction lows, with the 30-week MA as backstop |
| Shorts | Mirror rules for Stage 4 breakdowns |
| Win rate / evidence | Not quantified. [Lore] |

### 5.5 Qullamaggie (Kristjan Kullamägi): rules verified from his blog (V)
| Field | Breakout | Episodic Pivot (EP) | Parabolic short |
|---|---|---|---|
| Universe | Top 1-2% of stocks by 1-, 3- and 6-month gains | Gap ≥ 10%, mainly on earnings or guidance; mid-to-triple-digit EPS and revenue growth with a big beat; ideally not up much over the prior 3-6 months | Large caps up 50-100%+ in days or weeks (small caps 300-1000%+), with 3-5+ consecutive up days |
| Setup | Prior move ≈30-100%+ in 1-3 months, then an orderly 2-week to 2-month consolidation: higher lows, tightening range, "surfing" the rising 10/20-day MA (sometimes the 50) | Heavy volume premarket or in the first 5-10 min; the best traded ≈ a full average day's volume within 15-30 min | Exhaustion run |
| Entry | Opening-range high on a 1-, 5- or 60-min chart. Anticipatory entries are "less effective" | Opening-range high (1/5/60-min) | Opening-range low, the first red 5-min candle, or a failed VWAP bounce |
| Stop | Low of day; never wider than the stock's ADR% (or ATR in $) | Low of day | High of day, or a VWAP reclaim |
| Exits | Sell ⅓-½ after 3-5 days and move the stop to breakeven. Trail the rest on the 10- or 20-day MA; beginners use the first close below the 10-day | Trail on the 10/20-day (or 20/50-day) MA | Cover at the 10/20-day MA; R:R ≈5-10x, lower than his long setups |
| Sizing | Positions mostly 10-20% of the account, never > 30% in one name overnight. Risk 0.25-1% per trade, rarely > 1% | same | same |
| Regime | No explicit filter: "fewer or no trades" in lulls and bear markets. The often-repeated Nasdaq-vs-10/20-day-MA filter and ADR minimum are **not in his article** [Lore] | | |
| Win/payoff | 25-30% win rate; winners must average ≥ 2.5-3× losses, and the setup targets 5-10R+ | | |
| Evidence | [Lore]. "Tens of millions" is self-reported. The EP is an earnings-momentum entry, supported in spirit by Chordia-Shivakumar, but PEAD has faded outside small caps | | |

### 5.6 Turtle rules (Faith 2003/2007; Covel 2007, (K); rules page exists (V))
| Field | Rule |
|---|---|
| Universe | Diversified liquid futures |
| Volatility / unit | N = (19·N_prev + TR)/20. Unit = 1% of account ÷ (N × $ per point) |
| System 1 | Enter on a 20-day breakout, but skip it if the previous S1 breakout would have won (failsafe: take the 55-day breakout). Exit on a 10-day opposite breakout |
| System 2 | Enter on a 55-day breakout, always taken. Exit on a 20-day opposite breakout |
| Stop | 2N initial. When adding units, raise all stops to 2N from the latest fill. "Whipsaw" variant: ½N stops with re-entry |
| Pyramiding | Add a unit every ½N of favorable move, up to 4 units |
| Exposure caps | 4 units per market; 6 in closely correlated markets; 10 in loosely correlated; 12 per direction |
| Drawdown rule | For each 10% drawdown, cut the notional account used for sizing by 20% |
| Win rate vs payoff | ≈30-40% hit rate. It works only because pyramiding concentrates size in the rare big trends |
| Evidence | Rules published. The program's ≈$175M over ≈5 years is anecdotal (Covel). Diversified futures trend is [Strong]; single-stock trend [Weak]: Concretum, 66,000+ trades 1950-Nov-2024, <7% of trades made the majority of profits; portfolio 15.19% CAGR, 6.18% alpha gross (1991-2024); hard to run below ≈$1M (V) |

### 5.7 Expectancy arithmetic for coaching (computed with `tradekit.py expectancy`)

| Profile | Expectancy | Break-even win rate | Trades needed for t=2 |
|---|---|---|---|
| 30% win, +3R / −1R (breakout trader) | +0.20R | 25% | ≈337 |
| 25% win, +4R / −1R (Qullamaggie / trend) | +0.25R | 20% | ≈301 |
| 50% win, +2R / −1R (Minervini) | +0.50R | 33% | ≈36 |

Break-even win rate = avg loss ÷ (avg win + avg loss). For low-win-rate systems, risk per trade decides survival. With 25% wins at 4:1 over 250 trades, `ruin` gives P(drawdown ≥ 30%) ≈70% at 2% risk/trade vs ≈0% at 0.5% (median max DD ≈10%).

---

## 6. Momentum trade lifecycle (default procedure)

Defaults synthesize the six playbooks above. Items marked *(synthesis)* are coaching defaults, not tested rules [Lore]. Use them when a user has no rule of their own.

1. **Regime filter.** Take new breakout longs only when the index (S&P 500; Nasdaq for growth names) is above a rising 200-day MA and above its 50-day. Halve risk per trade above the 200 but below the 50; stop new longs below a falling 200 *(synthesis)*. O'Neil's tools: re-engage on a follow-through day; pull back after 4-6 distribution days in 4-5 weeks. **Danger state:** the first violent rally off a bear-market low with high volatility. Losers and junk lead and momentum leaders lag (Daniel-Moskowitz; Nov-2020, Jan-2023). After a long, narrow leadership run (H1-2026 +25.5% UMD), tighten trails and cut gross before the rotation, not after.
2. **Universe and RS ranking.**
   - Liquidity: price > $5 and 14-day average volume ≥ 1M shares (the stocks-in-play floor), or a dollar-volume floor sized to your positions.
   - Rank by 12-1 (or 12-1 ÷ vol). Keep the top ≈20% (RS ≥ 80); Qullamaggie uses the top 1-2% by 1/3/6m.
   - Require the Trend Template 8/8 and P/52wH ≥ 0.75 (prefer ≥ 0.9).
   - Prefer smooth paths (low FIP).
   - Spread across industries, because industry momentum explains much of stock momentum.
   - Run `techkit.py rank` and `techkit.py indicators`.
3. **Setup quality** *(synthesis checklist; score 0-6)*: prior thrust (30-100% in 1-3m, or a fresh Stage 2); base length (2 weeks-2 months tight, or a 7-65-week cup); successive contractions roughly halving; volume dry-up on the right side; higher lows and price riding the 10/20-day MA; a fresh fundamental catalyst. Take full size at 5-6 points, half at 4, pass below that.
4. **Entry.** Buy-stop at the pivot or the opening-range high (1/5/60-min). Require volume expansion: ≥ +40-50% vs average (O'Neil) or ≥ 2× on the breakout week (Weinstein). Don't chase > 5% past the pivot. Avoid anticipatory entries.
5. **Initial stop.** Use the low of day or the last contraction low. Cap it at min(ADR% or 1×ATR(14)/price, 7-8%) for stocks; 2N for futures. If the logical stop is wider than the cap, skip the trade or wait for a tighter setup. Never widen a stop.
6. **Position size.** shares = equity × risk% ÷ (entry − stop). Default risk 0.5% (0.25-1%; experienced traders ≤ 1.25-2%). Caps: 10-20% of equity per name, ≤ 30% overnight in one name; Turtle-style unit caps for correlated clusters. Total open risk ≤ ≈5% *(synthesis)*. Before earnings, size for a gap through the stop. Run `tradekit.py size`.
7. **Partials.** Sell ⅓-½ after 3-5 days or at +2-3R, then move the stop to breakeven (Qullamaggie, Minervini). Exception (O'Neil): if a stock is up ≥ 20% within 3 weeks, hold the core ≥ 8 weeks.
8. **Trailing.** Choose by holding period. Fast: the first close below the 10-day MA. Medium: the 20-day. Position: the 50-day or 30-week MA, or under successive correction lows. Futures/systematic: an opposite 10/20-day Donchian channel. Never trail tighter than the stock's normal daily range.
9. **Pyramiding.** Add only to winners. Futures: +1 unit every ½N, ≤ 4 units, stops to 2N from the last fill. Stocks *(synthesis)*: add on a new base breakout or a low-risk pullback to the 10/20-day MA after the first partial, with combined open risk ≤ the original 1R.
10. **Exit / time stop.** Exit on a trail hit, a climax run (exhaustion gap or parabolic extension, the parabolic-short criteria in reverse), a close below the 50-day for position trades, or a regime flip. Time stop *(synthesis)*: if a breakout is not up ≥ 1R within ≈5-10 sessions, cut to half or exit. Good breakouts usually work fast, which is what the 3-5-day partial assumes.
11. **Review** (every 20-30 trades): log R-multiple, MAE/MFE, setup score, regime and slippage. Recompute expectancy and the t-stat. Check that the win rate and payoff match the system's profile (a 25-30% breakout system that wins 60% is probably cutting winners early). Re-run `ruin` at current risk. Separate bad trades (rule breaks) from bad outcomes (rules followed, loss).

**Intraday adaptation:** trade only names in play (relative volume ≥ 100%, catalyst). Stop at the opposite end of the opening range or ≈10% of the 14-day ATR. Risk ≤ 0.5-1%, flat at the close. Treat 4x as the published ceiling, not a target.

---

## 7. Risk and failure modes, and how pros mitigate them

### 7.1 Crash history (computed from French UMD, (V) data)
| Episode | UMD | Context |
|---|---|---|
| Aug-1932 / Jul-1932 | −52.6% / −45.6% | Post-crash rebound (Daniel-Moskowitz's decile winner-minus-loser portfolio, which UMD's 30/70 sort understates: ≈−91.6% in Jul-Aug 1932) |
| Mar-May 2009 | −49.4% cumulative (Apr −34.4%); 2009 year −52.8% | Losers +≈163% vs winners +≈8% (9-Mar to 28-May, (K)); decile WML ≈−73.4% |
| Jan-2001; Nov-2002 | −25.4%; −16.5% | Dot-com bear rebounds |
| Nov-2020 | −12.6% | Vaccine-day rotation into value/cyclicals |
| Feb / Mar 2021 | −8.0% / −6.1% | Continued rotation |
| Jan-2023 | −16.2% (among the worst months since 1927) | 2022's defensive/energy winners vs beaten-down growth |
| Jul / Aug 2026 | −12.2% / −5.6% (−17.1% Jun→Aug) | Came after a +25.5% H1-2026 run. **Cause and sector drivers unverified.** Sep-2026 +6.7% |
| Full sample 1927-Sep-2026 | Max DD −78.4% (Jun-1932 to Sep-1939); skew −3.0; mean ≈7.4%/yr; vol ≈16.3%/yr | |

Monthly data hide intra-month crashes. The March-2025 hedge-fund momentum degrossing was estimated at a ≈12-13% drawdown (secondary sources, [Weak]), yet UMD shows only −2.6% for the month.

### 7.2 Failure-mode matrix
| Failure mode | Mechanism / evidence | Mitigation |
|---|---|---|
| Crash in the rebound after a bear market | Loser leg acts like a short call; in panic states the rebound destroys short-loser books [Moderate] (Daniel-Moskowitz 2016) | Vol scaling (12% target); dynamic weighting; long-only: stay light below a falling 200-day and don't fight the first junk rally |
| Leadership rotation | Factor autocorrelation breaks (Ehsani-Linnainmaa): Nov-2020, Jan-2023, Jul-Aug-2026 | Residualize or industry-neutralize; cap sector weight; trail tighter after parabolic leadership runs; combine with value/quality (negatively correlated, [Strong]) |
| Crowding | High "comomentum" (excess return correlation among momentum stocks) predicts lower returns and more crash risk [Moderate] (Lou & Polk 2022). MTUM 3y beta 1.34 (as of 31-Oct-2026) | Watch momentum-portfolio beta and leadership concentration; reduce gross when they are extreme |
| False breakouts | Normal: a 25-30% win rate is expected; <7% of trades make the profits | Small fixed-R losses, no re-widening, re-entry allowed on a new setup; volume confirmation; don't buy extended |
| Gap risk | Returns accrue overnight [Moderate], and stops at the low of day get gapped through | ≤ 10-20% per name (≤ 30% max) overnight; size earnings holds for a full-gap loss; prefer liquid names |
| Costs and turnover | [Contested]: Lesmond, Schill & Zhou 2004 say profits are largely illusory after costs; Frazzini, Israel & Moskowitz 2018 use ≈$1T+ of real executions and find costs far below academic estimates | Hold/sell buffers (Novy-Marx & Velikov 2016); patient execution; liquidity weighting (Korajczyk & Sadka 2004); estimate with `tradekit.py impact` |
| Rebalance timing luck | ≈350 bp/yr between schedules [Weak] | Tranche into staggered sub-books |
| Tax drag | Slow factor momentum can be *more* tax-efficient: it holds winners and realizes losers fast (Israel & Moskowitz 2012, [Weak]). Swing and intraday books realize almost everything short-term | Compare strategies after tax; prefer longer holds for taxable accounts; harvest losses |
| Post-publication decay | ≈−58% after publication [Strong] | Haircut backtests ⅓-½; prefer ingredients with economic stories |
| PEAD fade | Drift gone in large/mid caps [Moderate] (Martineau 2022) | Earnings-gap edges are a small-cap game; liquidity limits size |
| Lookback overfitting | 324 GEM variants: performance depends on the parameter choice (ReSolve 2019) | Ensembles, robustness grids, DSR (`ruletest` reports these) |

**Crash-protection checklist** (for a momentum book or a swing trader):
1. Inverse-vol scaling of the strategy (Barroso & Santa-Clara) and of each position (Turtle N sizing).
2. Cut exposure in a bear state with high volatility.
3. Residualize or diversify industries.
4. Watch crowding.
5. Cap overnight and single-name exposure, and assume stops can gap.
6. Control turnover with buffers and tranches.

**Long-only vs long-short:** long-only traders avoid the short-loser squeeze but feel a crash as their leaders falling fast while laggards rip. The drawdown is still severe.

---

## 8. Recent performance, 2023-2026

| Period | UMD (long-short, gross; (V) data) | Context |
|---|---|---|
| 2022 | +20.2% | Energy/defensive leadership |
| 2023 | −20.5% (Jan −16.21%; max DD −22.5% Jan-Jul) | Growth snap-back against 2022 winners |
| 2024 | +18.5% (Jan +5.46, Feb +5.01) | Momentum led |
| 2025 | −2.2% (Mar −2.64, Aug −3.61, Sep +4.62, Dec −2.40) | Value was the top factor; Q4-2025 momentum +0.77% vs value +8.34% (Morningstar via TMX, secondary) |
| 2026 Jan-Jun | +25.5% (Apr +9.51) | Strong, narrow run |
| 2026 Jul-Aug | −12.21%, −5.60% (−17.1% peak-to-trough) | Crash; cause unverified. Secondary reports of larger hedge-fund momentum-basket losses are unverified and conflicting |
| 2026 YTD (Jan-Sep) | +11.0% (Sep +6.70) | French file ends Sep-2026 |
| Jan-2023 to Sep-2026 cumulative | +2.3% | A roller coaster with little net progress |
| CAGR 2016-2025 / 2000-2025 / 1927-1999 | −0.55% / +0.46% / +8.05% | Raw factor premium near zero for 25 years |
| MTUM (long-only, risk-adjusted) | YTD NAV total return +7.14% (as of 10-Nov-2026); 3y SD 21.57%, 3y beta 1.34 (as of 31-Oct-2026); ER 0.15% (V) | Positive for the year despite the summer reversal; high-beta tilt. Don't infer a price collapse from the ≈$69 NAV (11-Nov-2026) vs >$100 in 2024-25 (K); a split is possible but unverified |

Takeaways for a coach: raw US momentum alone has not paid for a decade. Risk-managed or residual momentum, diversification across assets and trend, and pairing with value or quality have done better. Treat the post-run-up reversal of summer 2026 as the archetypal regime risk for swing traders. No international, developed ex-US or CTA-index 2023-2026 figures were verified.

---

## 9. Traps in a user's plan or backtest

- **Signal includes month t−1** in a monthly cross-sectional rank. That adds reversal noise; skip a month (industry momentum is the exception).
- **Universe survivorship**: a test on today's index members or today's "leaders". Demand point-in-time constituents and delisted names.
- **Same-bar execution or no costs.** Breakout fills at the open or at a stop slip. Small caps in play have wide spreads. `ruletest` fills at the next bar's close (`--delay 1`) plus `--cost-bps`; next-open fills are not modelled.
- **Stops assumed filled at the stop price.** Model gaps: earnings, overnight news, limit-down.
- **Profile mismatch**: a breakout system claiming 60%+ wins *and* 5R winners, or a 25%-win system judged after 30 trades (needs ≈300+).
- **Leverage hiding in the headline**: 3x ETFs or 4x intraday. Compare Sharpe and max drawdown, not total return.
- **One "optimal" lookback** picked from a grid. Check the grid's median Sharpe and the DSR; prefer an ensemble.
- **Sample is a single regime** (e.g., 2020-2021 or H1-2026). It must include a momentum crash (2009, Nov-2020, Jan-2023, Jul-Aug-2026).
- **No regime filter, or a regime filter fitted after the fact.**
- **Position size by conviction** instead of by stop distance. **Averaging down** a momentum loser breaks the method.
- **Buying extended** (> 5% past the pivot, or 3-5 straight up days into the entry). The parabolic-short criteria describe a stock to sell, not buy.
- **Treating vendor or contest records as evidence**: Concretum WPs, championship returns, "tens of millions", Darvas, Turtle profits. Use them as idea sources only.
- **Kurtosis input**: momentum returns have skew ≈ −3 and fat tails. `tradekit.py sharpe --kurt` expects **raw** kurtosis (normal = 3); pandas/scipy give excess, so add 3.

---

## 10. Toolkit hooks

Paths are relative to the skill directory: call each script by its absolute path from a working folder. CSVs need open/high/low/close (volume optional), oldest row first.

| Task | Command | Notes |
|---|---|---|
| Trend Template + stage | `python scripts/techkit.py indicators FILE` | 7 template checks (RS not included: use `rank`); approx. Weinstein stage from the slope of the 150-day (≈30-week) SMA; 52w high/low; 12-1 momentum; ATR; Donchian; relative volume |
| RS ranking | `python scripts/techkit.py rank A.csv B.csv ... --by voladj` (or `--by mom`) | 12-1, 6-1, 3m, vol, 12-1/vol, distance from 52w high. A handful of names is a watchlist, not a factor |
| 12m absolute momentum | `python scripts/techkit.py ruletest FILE --rule tsmom --params 252 --cost-bps 5 --oos 0.3` | Default grid 21/63/126/189/252 shows robustness; tests sign vs 0, not T-bills |
| Faber-style SMA | `... --rule sma --params 200` | Checked daily, not at month-end, so it trades more |
| MA crossover | `... --rule cross --params 50,200` | Grid default: fast 10/20/50 × slow 100/150/200 |
| Donchian / Turtle | `... --rule donchian --params 20` (exit = 10, i.e. S1 without the skip filter) or `--params 55` (exit = 27, not the Turtle 20) | Exit is half the entry length; add `--short` for two-sided futures tests |
| Vol-scaled version | add `--vol-target 0.12 --max-lev 2` | Barroso-style scaling at the single-asset level |
| Multiple trials | add `--extra-trials K` if other rules or markets were tried | Feeds the deflated Sharpe |
| Position size | `python scripts/tradekit.py size --equity 100000 --risk 0.5 --entry 50 --stop 47` | Futures: `--atr N --atr-mult 2 --multiplier <pt value>` (2N stop). `--atr-mult 1` gives the Turtle unit (1% per N with `--risk 1`). Warns when the budget is smaller than one contract |
| Expectancy and sample size | `python scripts/tradekit.py expectancy --p 0.3 --win 3 --loss 1 --trades 50` | Expectancy in R, break-even win rate, trades needed for t = 2/3 |
| Risk of ruin | `python scripts/tradekit.py ruin --p 0.25 --b 4 --risk 1 --trades 250 --limit 30` | Use it to set risk/trade for low-win-rate systems |
| Cost of a momentum rebalance | `python scripts/tradekit.py impact --qty --adv --price --daily-vol --spread-bps` | Square-root impact; compare against the edge in bps |
| Track-record significance | `python scripts/tradekit.py perf FILE --trials N` or `sharpe --sr --n --skew --kurt(raw)` | PSR, DSR, MinTRL for any claimed momentum record |

`ruletest` is for daily bars. Intraday rules (ORB break/candle, VWAP, first→last half-hour, noise band) run in `python scripts/daykit.py backtest FILE --rule ...` on intraday bars, with next-bar fills, costs and a deflated parameter grid (`day-trading.md` §6). Evaluate your own intraday systems from trade logs with `daykit.py journal`, `expectancy`, `ruin` and `perf`.

---

## 11. Key sources

- Jegadeesh & Titman 1993, *JF* 48(1) — https://doi.org/10.1111/j.1540-6261.1993.tb04702.x
- George & Hwang 2004, "The 52-Week High and Momentum Investing", *JF* 59(5) — https://doi.org/10.1111/j.1540-6261.2004.00695.x
- Da, Gurun & Warachka 2014, "Frog in the Pan", *RFS* 27(7) — https://doi.org/10.1093/rfs/hhu003
- Blitz, Huij & Martens 2011, "Residual Momentum", *JEF* 18(3) — https://doi.org/10.1016/j.jempfin.2011.01.003
- Moskowitz & Grinblatt 1999, "Do Industries Explain Momentum?", *JF* 54(4) — https://doi.org/10.1111/0022-1082.00146
- Ehsani & Linnainmaa 2022, "Factor Momentum and the Momentum Factor", *JF* — https://www.nber.org/papers/w25551
- Barroso & Santa-Clara 2015, "Momentum Has Its Moments", *JFE* 116(1) — https://doi.org/10.1016/j.jfineco.2014.11.010
- Daniel & Moskowitz 2016, "Momentum Crashes", *JFE* 122(2) — https://doi.org/10.1016/j.jfineco.2015.12.002
- Moskowitz, Ooi & Pedersen 2012, "Time Series Momentum", *JFE* 104(2) — https://doi.org/10.1016/j.jfineco.2011.11.003; critiques: Goyal & Jegadeesh 2018 *RFS*; Huang et al. 2020 *JFE*
- Hurst, Ooi & Pedersen 2017, "A Century of Evidence on Trend-Following", *JPM* — https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing
- McLean & Pontiff 2016, *JF* 71(1) — https://doi.org/10.1111/jofi.12365
- Lou, Polk & Skouras 2019, "A Tug of War", *JFE* 134(1); Lou & Polk 2022, "Comomentum", *RFS* 35(7)
- Gao, Han, Li & Zhou 2018, "Market Intraday Momentum", *JFE* 129(2); Baltussen, Da, Lammers & Martens 2021, *JFE* 142(1)
- Concretum Group papers (ORB, stocks in play, SPY noise band, trend on stocks; commercial) — https://concretumgroup.com/papers/
- Barber, Lee, Liu & Odean 2014, *JFM* 18; Chague, De-Losso & Giovannetti 2019, "Day Trading for a Living?" — SSRN 3423101
- Faber, Timing Model FAQ — https://mebfaber.com/timing-model/; Antonacci 2014, *Dual Momentum Investing*; Butler/ReSolve 2019, "Global Equity Momentum: A Craftsman's Perspective" — https://hedgefundalpha.com/strategies/global-equity-momentum-a-craftsmans-perspective/
- Qullamaggie, "My 3 Timeless Setups…" — https://qullamaggie.com/my-3-timeless-setups-that-have-made-me-tens-of-millions/
- O'Neil 2009; Minervini 2013/2017; Weinstein 1988; Darvas 1960; Faith, Original Turtle Rules — https://www.tradingblox.com/originalturtles/originalturtlerules.htm
- Kenneth French Data Library, momentum factor (data through Sep-2026) — https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_CSV.zip
- iShares MTUM page (as of Nov-2026) — https://www.ishares.com/us/products/251614/ishares-msci-usa-momentum-factor-etf
