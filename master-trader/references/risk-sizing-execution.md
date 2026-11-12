# Risk, Position Sizing, Portfolio Construction & Execution

*Read when: a user asks how big to trade, how much leverage or what vol target to use, how to combine positions or strategies, what drawdown to expect, whether to use stops, drawdown rules or tail hedges, what a trade will cost to execute or how much capital a strategy can absorb; or when reviewing any plan or backtest for survival risk (leverage, concentration, liquidity, crowding, short convexity).*

Tags: [Strong] replicated/consensus · [Moderate] peer-reviewed but limited replication · [Weak] thin, secondary or self-reported · [Contested] credible sources disagree · [Lore] practitioner wisdom, untested. **(math)** = exact given its stated assumptions; the assumptions (known parameters, Gaussian iid returns) are the weak point, never the algebra.

**Contents:** 1 Core principles · 2 Position sizing · 3 Position-sizing decision procedure · 4 Portfolio construction · 5 Risk measurement & drawdown math · 6 Drawdown control & pod-shop rules · 7 Stop losses · 8 Tail hedging · 9 Transaction costs & execution · 10 Leverage, margin, liquidation spirals · 11 Lessons from blowups · 12 Risk rules a master runs by · 13 Failure modes / traps · 14 Toolkit hooks · 15 Key sources

---

## 1. Core principles

- **Survive first, optimize second.** Every blowup in §11 ran a model with positive expected return. Size so the *plausible worst case* (historical worst x 2-3, correlations -> 1, liquidity haircut) is survivable, not so VaR looks acceptable.
- **Size from risk (sigma), which you can forecast. Be humble about edge (mu, SR), which you cannot.** Volatility is persistent; Sharpe ratios have huge sampling error (SR 0.5 over 10 years of daily or monthly data has SE ~0.32) [Strong]. Risk-based sizing is robust and return-based sizing is fragile.
- **Kelly is a ceiling, not a target.** Growth is a symmetric parabola about f* (0.5x and 1.5x Kelly earn the same growth), but volatility and drawdown risk rise steeply above it. Betting 2x Kelly wipes out all excess growth; betting 0.5x Kelly costs only 25% of it (math). Since your edge estimate is noisy, run <= half Kelly on a *haircut* edge.
- **The drawdown budget usually binds before Kelly does.** Expected max drawdown is a predictable function of SR, vol and horizon. Genuine edges routinely produce 2-4 sigma drawdowns, so set the vol target from the drawdown the trader can actually sit through.
- **Count bets, not positions.** At average correlation 0.3, adding positions can never improve the Sharpe by more than 1.83x (math). Correlations rise in sell-offs [Strong], so calm-period diversification overstates crisis diversification.
- **Liquidity is position-relative and time-varying.** Leverage x illiquidity x correlation is the multiplicative killer; remove any one and most historical blowups become survivable [Lore, consistent with the case record].
- **Costs grow faster than size.** Impact per dollar scales with sqrt(size) [Strong], so total cost scales with size^1.5 and every strategy has a capacity. Profit-maximizing AUM is 4/9 of break-even AUM (math).
- **Stops and vol targeting shape risk; they are not alpha.** Stops add value only when returns persist (Kaminski & Lo) [Strong]. Vol targeting reliably thins the tails, but its Sharpe gains outside equities and credit are [Contested].
- **Limits work only if enforced mechanically.** Limits that are routinely waived are the same as no limits (Archegos/Credit Suisse). Pre-commit the drawdown tiers before the drawdown starts.

---

## 2. Position sizing

### 2.1 Fixed-fractional (risk per trade)

```
Units = (Equity x r) / (|Entry - Stop| x Multiplier)        r = fraction of equity lost if the stop is hit (1R)
Drawdown from a k-trade losing streak = 1 - (1 - r)^k
Expected longest losing streak in N trades ~= ln(N) / ln(1/(1-p))      p = hit rate; overstates by ~1-2 (conservative)
```

- **Convention:** r = 0.25-1% per trade for professionals running many, often correlated, positions; 2% is the common retail ceiling. No primary source exists; this is an industry convention from practitioner books (Van Tharp, Elder) [Lore]. The streak arithmetic is what justifies it (math):

| Risk/trade r | 10-loss streak | 12-loss streak | 20-loss streak |
|---|---|---|---|
| 0.25% | 2.5% | 3.0% | 4.9% |
| 0.5% | 4.9% | 5.8% | 9.5% |
| 1% | 9.6% | 11.4% | 18.2% |
| 2% | 18.3% | 21.5% | 33.2% |
| 3% | 26.3% | 30.6% | 45.6% |

- Expected longest streak in 500 trades by the formula: about 9 at p = 0.5, 12 at p = 0.4, 14 at p = 0.35 and 17 at p = 0.3. The formula overstates by about 1-2 trades (simulation gives ~11 at p = 0.4), so it errs conservative. A 40%-hit-rate trader risking 2% should therefore expect a ~22% drawdown from an ordinary streak alone, before counting any correlated losses.
- **Correlated positions are one bet.** Five 1% trades in the same theme behave like one 5% trade on a theme shock. Apply r to the cluster, not to each ticket.
- **A stop does not cap gap risk.** Overnight gaps, halts and limit moves jump through stops. Check notional / equity as well: `size` warns above 2x by default.

### 2.2 ATR / volatility-unit sizing and Turtle units

- **Put stops in volatility units, not fixed percentages:** stop = k x ATR with k ~ 2-3, and size so that the stop distance equals the risk budget. This unifies the stop and the size [Lore; this is the Turtle construction]. Toolkit default is ATR 14 with Wilder smoothing (`techkit indicators`); the Turtles used a 20-day N.
- **Original Turtle rules** (Faith 2003, via secondary transcriptions that agree with each other) [Weak, secondary]:

```
N      = 20-day ATR (Wilder-style smoothing)
Unit   = (1% x Equity) / (N x $ per point)          -> a 1N move = 1% of equity
Stop   = 2N from entry                              -> ~2% of equity at risk per unit
Adds   = +1 unit every 0.5N in favour, max 4 units per market; all stops trail to 2N from the newest entry
Caps   = 4 units per market, 6 in closely correlated markets, 10 in loosely correlated markets, 12 per direction
System 1: 20-day breakout entry, 10-day opposite-extreme exit.  System 2: 55-day entry, 20-day exit.
```

  Sources disagree on 4 vs 5 max units per market and on whether stops trail. Read the caps as risk: 12 units long = 12% of equity per 1N joint adverse move, and a 2N gap against a full book costs ~24% (math). Turtle aggregate risk was far above modern professional norms.
- **Generic vol-target position** (consistent with Carver's books; the Turtle unit is the special case of 1% of equity per daily N):

```
Contracts = (Capital x tau_annual x instrument_weight x DM) / (Multiplier x Price x FX x sigma_annual%)
  tau = portfolio vol target, DM = diversification multiplier (§4.3), sigma_annual% = instrument vol as % of price
```

### 2.3 Kelly and fractional Kelly

```
Discrete binary bet:    f* = p - q/b          b = net payoff ratio, q = 1 - p; f* = fraction LOST if the bet loses
                        p = 0.55 at even money -> f* = 10%
Continuous (Merton/Thorp): f* = (mu - r)/sigma^2    max growth g* = r + S^2/2    Kelly vol = f* x sigma = S (the Sharpe)
Multi-asset:            f* = Sigma^-1 (mu - r)
Fraction c of Kelly:    excess growth = (2c - c^2) x S^2/2      vol = c x S
Thorp drawdown result:  P(wealth EVER falls to fraction x of its start) = x^(2/c - 1)
```

All formulas are (math) under known, constant parameters (Thorp 2006 — https://sites.oxy.edu/lengyel/M330/thorp/paper.htm). The fractional-Kelly figures match the blackjack illustration in MacLean, Thorp & Ziemba (0.75 of growth at c = 0.5, 0.91 at c = 0.7 — https://www.stat.berkeley.edu/~aldous/157/Papers/Good_Bad_Kelly.pdf).

| Kelly fraction c | Growth, % of max | Vol (x Sharpe) | P(ever -50%) | P(ever -80%) |
|---|---|---|---|---|
| 0.25 | 44% | 0.25 S | 0.8% | ~0.001% |
| 0.5 | 75% | 0.5 S | 12.5% | 0.8% |
| 0.7 | 91% | 0.7 S | 28% | 5% |
| 1.0 (full) | 100% | 1.0 S | 50% | 20% |
| 1.5 | 75% | 1.5 S | 79% | 58% |
| 2.0 | 0% | 2.0 S | 100% | 100% |

- Over-betting is strictly dominated: c = 1.5 earns the same growth as c = 0.5 at 3x the volatility.
- **Worked example:** 8% excess return at 16% vol gives S = 0.5, f* = 3.1x leverage, Kelly vol 50% and max excess growth 12.5%/yr. A strategy with S = 0.3 has a Kelly vol of 30%.
- The S&P 500 Kelly leverage is often quoted at ~1.17x (Rotando & Thorp 1992, *Amer. Math. Monthly* 99(10)) [Weak: the figure was confirmed only via secondary sources].
- **Estimation error silently raises your fraction.** Sizing at c x mu_hat/sigma^2 when the true mean is mu gives an effective fraction c x (mu_hat/mu) (math). If the backtest doubled the true edge, your "half Kelly" is really full Kelly, with a 50% chance of halving.

### 2.4 Estimation-error haircuts

- **Sharpe sampling error** (Lo 2002, *FAJ* 58(4)): SE(SR) ~= sqrt((1 + SR^2/2)/T), with SR and T at the same frequency (T = number of observations), iid returns [Strong]; multiply by sqrt(periods per year) to annualize. With daily or monthly data the annualized SE is about 1/sqrt(years), nearly independent of SR. Fat tails, negative skew and autocorrelation widen it, so use `sharpe` with skew and kurtosis.

| Years of data (monthly obs.) | SE if SR = 0.5 | SE if SR = 1.0 |
|---|---|---|
| 3 | 0.58 | 0.59 |
| 5 | 0.45 | 0.46 |
| 10 | 0.32 | 0.32 |
| 20 | 0.22 | 0.23 |

  A true SR of 0.5 measured over 10 years has a 95% interval of roughly -0.1 to +1.1.
- **Carver** (*Systematic Trading* 2015, via CXO summary — https://www.cxoadvisory.com/big-ideas/a-few-notes-on-systematic-trading) [Moderate]:
  - "Far better to use half-Kelly."
  - Cap the Sharpe used for sizing at 1.0 regardless of the backtest.
  - A single-instrument trading subsystem rarely exceeds SR ~0.4 on average.
  - Sharpe is "extremely difficult to predict" while standard deviation is relatively easy.
  - In Dec 2024 he published a formal estimation-error-adjusted sizing method; half Kelly is the crude version of the same idea (https://qoppac.blogspot.com/2024/12).
- **Chan:** halve backtest expected returns before computing Kelly (https://epchan.blogspot.se/2006/10/how-much-leverage-should-you-use.html) [Lore].
- **Selection bias comes on top of this.** If many variants were tried, deflate the Sharpe first (`sharpe --trials`); the backtest SR of the best variant is biased upward.
- **Rational range:** c = 0.25-0.5 for unproven edges, because SR errors of +/-0.3 are routine (math + [Lore]).

### 2.5 Volatility targeting: what the evidence supports

| Study | Finding | Grade |
|---|---|---|
| Moreira & Muir 2017, *JF* 72(4) | Scaling factors by 1/(last month's realized variance) raises alphas and Sharpe for market, value, momentum, profitability and other factors. Mechanism: vol persists, expected returns do not rise with it. | [Contested] |
| Cederburg, O'Doherty, Wang & Yan 2020, *JFE* 138(1) — https://www.lehigh.edu/~xuy219/research/COWY.pdf | Across 103 equity strategies, vol-managed beats unmanaged in 53 and loses in 50. In-sample spanning alphas are not implementable in real time because the parameters are unstable. | [Moderate] |
| DeMiguel, Martin-Utrera & Uppal 2024, *JF* 79(6) — https://lbsresearch.london.edu/id/eprint/3716 | Single-factor vol management fails out of sample (estimation error); a conditional multifactor vol-managed portfolio outperforms out of sample and net of costs. | [Moderate] |
| Harvey, Hoyle, Korgaonkar, Rattray, Sargaison & Van Hemert 2018, *JPM* 45(1) — https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf | 60+ assets, daily data back to 1926. Sharpe gains mainly in equities and credit, negligible in bonds, FX and commodities. Fewer extreme returns and lower vol-of-vol in all assets; smaller max drawdowns for 60/40 and risk parity. Gains are tied to the leverage effect. US equity vol-of-vol falls from 4.6% to 1.8% (Quantpedia summary) [Weak, secondary]. | [Strong] on risk reduction; [Moderate] on Sharpe |
| Barroso & Santa-Clara 2015, *JFE* 116(1) | Vol-scaled momentum nearly doubles the Sharpe (reported ~0.53 -> ~0.97, 1927-2011) and practically eliminates momentum crashes. The exact figures come from a secondary summary; the abstract says "nearly doubles". | [Moderate] |

**Verdict:** use vol targeting as a risk-control tool (stable risk, thinner tails, smaller drawdowns in equity-heavy books). Do not sell it as a dependable alpha source. Toolkit defaults: 20-day realized vol with a leverage cap (`ruletest --vol-target`), EWMA lambda 0.94 (`vol`).

---

## 3. Position-sizing decision procedure

Walk the user through these steps in order. Ask for the inputs rather than assuming them, and run the tools rather than doing mental math.

1. **Inventory the edge evidence.** How many trades or years of data? Backtest or live? How many variants or parameters were tried? What are the hit rate, average win/loss in R, Sharpe, skew and kurtosis? Run `expectancy` (trades needed for t = 2/3) and `sharpe` (PSR/DSR/MinTRL). If t < 2 or DSR < 0.95, treat the edge as **unproven**.
2. **Haircut the edge.** Set SR_sizing = min(0.5 x backtest SR, 1.0). For a single-instrument or discretionary strategy, sanity-check against Carver's ~0.4. If the edge is unproven, use the lower bound of a 1-SE interval or simply SR_sizing <= 0.3.
3. **Compute the Kelly ceiling.** vol_Kelly = c x SR_sizing with c = 0.5 (c = 0.25 if unproven). Check with `kelly --mu --sigma` (continuous) or `kelly --p --b` (per-trade).
4. **Compute the drawdown constraint.** Ask for the **max drawdown at which they would abandon or be forced to stop** (this number, not the hoped-for one) and the horizon. Then tau_DD = tolerable MDD / (95th-percentile MDD multiple from the §5.3 table at SR_sizing and that horizon). Verify with `drawdown --sharpe --vol --years`.
5. **Set the portfolio vol target:** tau = min(vol_Kelly, tau_DD). tau_DD usually binds.
   *Example:* backtest SR 1.0, haircut to 0.5. Half Kelly gives a 25% vol ceiling. The trader tolerates 25% over 5 years, and the 95th-percentile multiple at SR 0.5 over 5 years is 3.40, so tau_DD = 25/3.40 ~ **7.4% vol**. The drawdown budget binds at less than a third of half Kelly.
6. **Allocate risk across positions.** Start with equal risk (inverse vol), cap each correlated cluster, and apply the diversification multiplier (§4). Recompute vol at crisis correlations (0.8-1.0) and make sure that stressed vol still respects the drawdown budget.
7. **Convert to position size.**
   - *Continuous or systematic positions:* use the vol-target formula in §2.2.
   - *Discrete trades with stops:* choose r so that 1 - (1-r)^k at k = the expected longest streak (§2.1) is <= about half the tolerable drawdown. Treat a correlated cluster as one trade.
   - Run `size --equity --risk --entry --stop` or `--atr --atr-mult`.
   - *Example:* p = 0.4, 2R winners, 150 trades/yr for 5 years gives an expected longest streak of ~13 by the §2.1 formula (conservative; a simulation runs ~1-2 shorter). At r = 1% that streak costs 12.2%; at 0.5% it costs 6.3%. For a 25% tolerance, 1% only just passes the streak check, and `ruin --p 0.4 --b 2 --risk 1 --trades 750 --limit 25` shows a ~9% chance of breaching 25% (95th-percentile MDD ~27%). At `--risk 0.5` the chance is ~0% (median MDD ~9%), so 0.5% is the size. The streak check is a floor test; always confirm with `ruin`.
8. **Match the exit to the edge (§7).** For trend or momentum edges, place the stop at 2-3 ATR and size off it. For mean reversion or value, size smaller and control risk with portfolio limits or time stops rather than tight stops.
9. **Check liquidity and cost.** Run `impact` with the expected edge per round trip. Keep orders within the participation heuristics (§9) and require edge after costs > 0 with margin to spare. For larger books, check capacity against 4/9 of break-even.
10. **Stress the book.** Apply historical worst x 2-3, correlations -> 1, a gap through the stops, a liquidity haircut and, if levered, a margin increase. The stressed loss should be <= 20-30% of equity, with unencumbered cash covering the margin call (§10).
11. **Pre-commit the drawdown tiers (§6) and a review cadence in writing.** Recompute sigma on a fixed schedule and whenever vol spikes; never raise size during a drawdown to "win it back".

---

## 4. Portfolio construction

### 4.1 Why raw mean-variance optimization fails

- **Error maximization:** optimizers overweight assets whose returns are overestimated and whose risk is underestimated (Michaud 1989, *FAJ* 45(1)) [Strong].
- **Mean errors dominate.** At typical risk tolerance, errors in means are ~10x as damaging as errors in variances, and errors in variances ~2x as damaging as errors in covariances (Chopra & Ziemba 1993, *JPM* 19(2)) [Moderate].
- **1/N is hard to beat.** None of 14 optimized models consistently beat 1/N out of sample (Sharpe, certainty equivalent or turnover). Sample mean-variance needs an estimation window of ~3,000 months for 25 assets and ~6,000 months for 50 assets to beat 1/N (DeMiguel, Garlappi & Uppal 2009, *RFS* 22(5) — https://econpapers.repec.org/RePEc:oup:rfinst:v:22:y:2009:i:5:p:1915-1953) [Strong].

### 4.2 Robust construction methods

| Method | Mechanics | Needs mu? | Notes / evidence |
|---|---|---|---|
| 1/N | Equal capital | No | Tough out-of-sample benchmark [Strong]; ignores vol differences |
| Inverse vol | w_i proportional to 1/sigma_i | No | Equals ERC when correlations are equal (math) |
| ERC / risk parity | RC_i = w_i(Sigma w)_i / sigma_p, all equal | No | Its vol lies between min-variance and 1/N (Maillard, Roncalli & Teiletche 2010, *JPM* 36(4)) [Strong] |
| Ledoit-Wolf shrinkage | Sigma_shrunk = delta F + (1 - delta) S, delta chosen analytically, F e.g. constant correlation | Covariance only | Pulls extreme coefficients in and stabilizes weights, especially long-only (Ledoit & Wolf 2004 — https://econ-papers.upf.edu/papers/691.pdf) [Strong] |
| HRP | (1) cluster on d_ij = sqrt(0.5(1 - rho_ij)); (2) quasi-diagonalize; (3) recursive bisection by inverse cluster variance | No | No matrix inversion; works on singular matrices; lower out-of-sample variance than the critical-line method in López de Prado's Monte Carlo (*JPM* 2016, SSRN 2708678). Superiority is not universal [Contested]. Shrinkage inside HRP is advocated (Molyboga 2020). |
| Black-Litterman | Pi = delta Sigma w_mkt; E[R] = [(tau Sigma)^-1 + P'Omega^-1 P]^-1 [(tau Sigma)^-1 Pi + P'Omega^-1 Q] | Views only | With no views you hold the market. Typical delta ~2.5 and tau 0.025-0.05 [Weak: typical values unverified] |
| Max diversification | Maximize DR = w'sigma / sqrt(w'Sigma w) | No | DR^2 ~ number of independent risk factors (Choueifaty & Coignard 2008, *JPM* 35(1)) |

**Coaching hierarchy for a small trader:**
1. Equal-risk (inverse-vol) weights across strategies or instruments.
2. Risk caps per cluster (asset class or theme) so that no theme dominates.
3. Full mean-variance only with shrunk covariances and heavily shrunk or Black-Litterman returns.

Forecast-free methods are the default because errors in mu dominate.

### 4.3 Measuring diversification

- **Sharpe multiplier** for N equal-vol, equal-Sharpe bets at average correlation rho: SR_port = SR_single x sqrt(N / (1 + (N-1) rho)) (math). With equal weights this is also Carver's diversification multiplier DM = 1/sqrt(w'Hw).

| Average rho | N = 5 | N = 10 | N = 20 | Cap (N -> infinity) |
|---|---|---|---|---|
| 0.0 | 2.24 | 3.16 | 4.47 | unbounded |
| 0.1 | 1.89 | 2.29 | 2.63 | 3.16 |
| 0.3 | 1.51 | 1.64 | 1.73 | 1.83 |
| 0.5 | 1.29 | 1.35 | 1.38 | 1.41 |
| 0.8 (crisis) | 1.09 | 1.10 | 1.11 | 1.12 |

- Once N is above ~10, lowering correlation matters far more than adding names.
- **Crisis vol blow-up (math):** a 10-asset book levered by DM = 1.64 at a calm rho of 0.3 runs at 1.64/1.10 ~ **1.5x its vol target** if correlations jump to 0.8. Size to the stressed vol.
- **Effective number of bets:** decompose variance into contributions p_i from uncorrelated principal components; ENB = exp(-sum p_i ln p_i) (Meucci 2009, *Risk* 22(5)).

### 4.4 Correlation breakdown

- International equity correlations rise in bear markets but not in bull markets (Longin & Solnik 2001, *JF* 56(2)), and US stock correlations are higher in downturns (Ang & Chen 2002, *JFE* 63(3)) [Strong].
- The stock-bond correlation turned positive in 2022, undermining 60/40 and risk-parity hedging. The episode is well known but not sourced here.
- **Practice:** for the stress test, push all pairwise correlations among risk assets to 0.8-1.0 and recompute. The stressed vol, not the calm vol, must fit the drawdown budget.

---

## 5. Risk measurement & drawdown math

### 5.1 VaR and Expected Shortfall

```
Parametric VaR_alpha = z_alpha x sigma x sqrt(h)          Normal ES_alpha = sigma x phi(z_alpha) / (1 - alpha)
Historical VaR: empirical quantile of revalued P&L.    Monte Carlo VaR: quantile of P&L simulated from a fitted joint model.
```

| Confidence | z | Normal ES (x sigma) |
|---|---|---|
| 95% | 1.645 | 2.063 |
| 97.5% | 1.960 | 2.338 |
| 99% | 2.326 | 2.665 |

- VaR fails subadditivity, so it is not coherent; ES is coherent (Artzner et al. 1999, *Math. Finance* 9(3)) [Strong]. VaR says nothing about losses beyond the threshold.
- **Basel FRTB** replaced 99% VaR with 97.5% ES calibrated to a stress period, with liquidity horizons of 10-120 days (BCBS d457, Jan 2019 — https://www.bis.org/bcbs/publ/d457.htm). Under normality ES97.5 ~ VaR99, which is why 97.5% was chosen (math).
- **VaR backtest (Basel traffic light, 99% VaR, 250 days):** 0-4 exceptions green, 5-9 yellow, 10+ red (BCBS 1996).
- **Use:** VaR and ES describe a normal bad day. They never replace stress tests, and you should never size a levered or short-convexity book on them.

### 5.2 Stress testing

1. **Historical replay:** Oct 1987, 1998, 2008, Aug 2011, Feb 2018, Mar 2020, 2022 rates, Aug 2024.
2. **Hypothetical shocks:** rates +/-100-250bp parallel or twist (~250bp is the post-LDI UK benchmark), equity -20% gap, vol x3, correlations -> 1, FX peg break, and a haircut on liquidation time.
3. **Reverse stress test:** find the scenario that kills the book, then judge its plausibility.
4. **Funding:** always include funding and margin effects (§10), not just mark-to-market.

### 5.3 Drawdown math

**Recovery:** a loss L needs a gain of L/(1 - L) to recover (math).

| Loss | 10% | 20% | 25% | 33% | 50% | 75% | 90% |
|---|---|---|---|---|---|---|---|
| Gain needed | 11.1% | 25% | 33.3% | 50% | 100% | 300% | 900% |

- **Zero-drift benchmark:** E[MDD] = sqrt(pi/2) x sigma x sqrt(T) ~ 1.25 sigma sqrt(T). With positive drift, E[MDD] grows only logarithmically in T and scales with sigma^2/mu. E[MDD]/sigma depends only on SR and T (Magdon-Ismail, Atiya, Pratap & Abu-Mostafa 2004, *J. Appl. Prob.* 41 — https://www.cambridge.org/core/journals/journal-of-applied-probability/article/on-the-maximum-drawdown-of-a-brownian-motion/F9E3B8A454B020DDEBF0AC3390EF7807) [Strong].
- **Expected maximum drawdown in multiples of annual vol (median / 95th percentile).** Monte Carlo with 4,000 paths, Gaussian daily returns and constant-dollar risk; consistent with the Magdon-Ismail scaling. Multiply by the vol target. Real strategies, especially negative-skew ones (short vol, carry), are materially worse.

| SR | 1 yr | 3 yr | 5 yr | 10 yr | 20 yr |
|---|---|---|---|---|---|
| 0.25 | 0.99 / 1.99 | 1.64 / 3.29 | 2.09 / 4.12 | 2.76 / 5.54 | 3.61 / 6.77 |
| 0.5 | 0.90 / 1.82 | 1.45 / 2.91 | 1.79 / 3.40 | 2.25 / 4.12 | 2.81 / 4.96 |
| 1.0 | 0.77 / 1.58 | 1.15 / 2.11 | 1.37 / 2.44 | 1.69 / 2.90 | 1.98 / 3.25 |
| 1.5 | 0.68 / 1.32 | 0.97 / 1.71 | 1.12 / 1.92 | 1.34 / 2.17 | 1.56 / 2.41 |
| 2.0 | 0.61 / 1.15 | 0.83 / 1.41 | 0.95 / 1.58 | 1.13 / 1.74 | 1.30 / 1.95 |

- *Read-offs:* SR 0.5 at 15% vol over 10 years has a median MDD of ~34% and a 1-in-20 chance of ~60%. An SR 1.0 book at 5% vol has a 1-year 95th-percentile MDD of ~7.9%, so ~5% of genuinely skilled SR-1 PMs would breach a 7.5% stop-out in a given year from luck alone (more with fat tails).
- **Sizing rule:** tau ~ tolerable MDD / (95th-percentile multiple at a realistic SR and horizon).
- **First passage (math):** P(ever hitting a drawdown of d annual-vol units from today) = exp(-2 x SR x d). At SR 0.5, a 2-sigma loss (30% at 15% vol) has a 13.5% lifetime probability measured from today, not from every peak. At SR 1.0 it is 1.8%.
- `drawdown --sharpe --vol --years` simulates compounding returns, so its percentages run slightly below the additive table at high vol.

### 5.4 Risk of ruin

- **Gambler's ruin** (Feller 1968): even-money bets with edge A = p - q, starting with N betting units, against an infinitely rich opponent: P(ruin) = ((1-A)/(1+A))^N (math).
  - p = 0.55 gives P(ruin) = 13% with 10 units, 1.8% with 20 units and ~0.004% with 50 units.
  - Ruin probability falls exponentially with the number of units you hold back.
- **Thorp** (continuous): P(reach x of start) = x^(2/c - 1); see §2.3.
- **Define "ruin" as the drawdown at which the trader quits or is stopped out** (often 25-50%), not zero equity [Lore]. Simulate it with `ruin --limit`.

---

## 6. Drawdown control & pod-shop rules

- **Millennium, as reported:** a ~5% drawdown brings a ~50% capital cut, and ~7.5% means the pod is terminated ("you're almost certainly out"). About 15-20% of people leave each year, typically after being stopped out. Citadel reportedly runs a less strict stop-loss (eFinancialCareers citing WSJ — https://www.efinancialcareers.com/news/millennium-hedge-fund-jobs) [Weak: press reports only, no firm documentation; other platforms' rules are undocumented in primary sources].
- **Limits differ by firm and strategy; there is no universal threshold.** Risk controls make platform diversification *conditional*, because many PMs de-risk at once under stress (Resonanz Capital — https://resonanzcapital.com/insights/when-risk-controls-make-diversification-conditional) [Moderate].
- **Recent stress events:** in the Aug 2024 turmoil, BlueCrest and Millennium closed pods quickly (BNN Bloomberg, 30 Aug 2024) [Weak, secondary]. Press reports of a March 2026 stress on pod models exist (HedgeCo, Apr 2026); their contents are unverified.
- **Why pods cut at ~5% and ~7.5%** (inference): pods run low single-digit vol and target high Sharpes. By §5.3, a 7.5% loss in a 5%-vol book is improbable (~5%/yr) for a true SR >= 1 PM and much more likely if the edge is gone. The cut is a Bayesian update on skill plus option-like protection for the platform, which pays winners' incentive fees regardless of the losers. It is platform protection, not proof that tight stops are optimal for an individual.
- **CPPI:** exposure E = m x (V - F), with multiplier m and floor F (Black & Jones 1987; Perold & Sharpe 1988).
  - It is convex: it buys after gains and sells after losses, so it wins in trends and bleeds in chop.
  - **Gap risk:** a fall of more than 1/m between rebalances breaches the floor (m = 5 means a 20% gap).
- **Grossman & Zhou 1993:** under the constraint W_t >= alpha x max W_s, the optimal policy invests in proportion to W_t - alpha x M_t. This is a CPPI with a ratcheting floor.
- **When drawdown de-risking helps:** only if returns are serially correlated or the drawdown is evidence that the edge has decayed (the Kaminski & Lo logic). No rigorous evidence was found that portfolio-level drawdown de-risking improves risk-adjusted returns for diversified systematic strategies.
- **Tiered rule for a coached trader** (synthesis mirroring pod practice, not a sourced standard). Calibrate the levels to the trader's realistic SR with §5.3 so that ordinary luck does not trigger them.

| Drawdown (x annual vol target) | Action |
|---|---|
| ~1x | Review the process; cut risk 25-50% |
| ~1.5-2x | Cut to minimum size; full post-mortem |
| ~2-2.5x | Stop trading the strategy until it is re-validated out of sample |

- **Systemic externality:** when many funds share factor exposures and identical stop rules, a shock produces synchronized liquidation (Aug 2007, Aug 2024). Know who else holds your trade.

---

## 7. Stop losses

- **Kaminski & Lo 2014** (*J. Financial Markets* 18 — https://dspace.mit.edu/bitstream/handle/1721.1/114876/Lo_When%20Do%20Stop-Loss.pdf):
  - Under a random walk, stop-loss rules *reduce* expected return (a negative "stopping premium") [Strong, theorem].
  - With momentum or regime switching, they can add value.
  - In US data from 1950-2004, stopping out of equities into long-term bonds added ~50-100bp/month during stop-out periods [Moderate: working-paper figure].
- **Momentum crashes** (Han, Zhou & Zhu, "Taming Momentum Crashes", SSRN 2407199) [Moderate: working paper, gross of costs]:
  - A 10% monthly stop per stock cuts the worst equal-weighted monthly loss from -49.8% to -11.4%, and the worst value-weighted loss from -65.0% to -23.3% (2016 version).
  - It roughly doubles the Sharpe (0.165 -> 0.369 in the 2014 draft).
- **Costs:** Lo & Remorov 2017 (*JFM* 34) report that tight stops tend to underperform after transaction costs [Weak: details unverified]. Practitioner tests of retail fixed stops often find they reduce returns [Weak].

| Strategy edge | Stop? | Reason |
|---|---|---|
| Trend, breakout, momentum | Yes: 2-3 ATR or opposite breakout (Turtle 10/20-day) | The stop is part of the signal; it exits when the persistence thesis is invalidated |
| Mean reversion, value | Avoid tight stops; use size and portfolio limits plus a wide disaster stop | A stop fires exactly when expected return is highest |
| Event, carry, option theta | Time stop | If the move has not come within the thesis horizon, recycle the capital [Lore: no rigorous evidence on time stops] |

---

## 8. Tail hedging

**The debate is [Contested].**

- Universa reported a +3,612% return on its tail fund for March 2020 (Q1 2020 was reported as about +4,144%) [Weak, self-reported].
- **Spitznagel's case:** judge a hedge by its effect on whole-portfolio CAGR, because a small, highly convex sleeve lets you hold more equity.
- **AQR's case** (Ilmanen, Asness; Israelov's "Pathetic Protection"): puts carry a persistent negative return, protect unreliably and path-dependently, and holding less equity reduces risk more efficiently. Trend following gives comparable crisis protection with a positive long-run expected return. Israelov's details are unverified.
- Sources: Advisor Perspectives, May 2020 — https://www.advisorperspectives.com/articles/2020/05/06/an-aqr-warning-and-a-3-612-return-fire-up-the-black-swan-debate [secondary summary of both sides].
- **Trend as crisis alpha:** time-series momentum did well in most of the largest 60/40 drawdowns over a century (Hurst, Ooi & Pedersen 2017, *JPM* 44(1)) [Moderate; the crisis-count detail is unverified].
- **Behaviour kills hedge programs.** CalPERS ended its Universa program in Oct 2019 as "too costly", months before the March 2020 crash [Weak, secondary].

| Hedge | Pays in | Cost / failure mode |
|---|---|---|
| Hold less risk | Everything | Lower return; the cheapest and most reliable hedge |
| OTM index puts | Fast crashes | Persistent premium bleed |
| Put spreads | Moderate crashes | Cut premium (~40-70%, unsourced [Lore]) but cap the payout, so they fail in a true tail |
| VIX calls | Vol spikes | Very convex, but VIX futures usually sit in contango, so long-vol positions bleed steadily [Lore, unsourced here] |
| Trend following | Slow, grinding bears | Positive expected return; can lag a one-day gap (Oct 1987, Feb 2018) because it needs time to flip |
| Long-vol / tail funds | Tails | Require sitting through many years of losses |

- **Universa's math works only with very high convexity:** the crash multiple must free more equity exposure than the sleeve costs. Most retail-accessible hedges (ETF puts at retail spreads, VIX ETPs) are not that convex, and results depend heavily on whether 2008 or 2020 is in the sample.
- **Rule:** pre-commit a budget (e.g. <= 0.5-1%/yr of NAV) and a review horizon of 5 years or more, or do not start [Lore].

---

## 9. Transaction costs & execution

### 9.1 Cost components and implementation shortfall

- **Implementation shortfall** (Perold 1988, *JPM* 14(3)) [Strong]: the paper-portfolio return at decision prices minus the real return. It decomposes into explicit fees + half-spread + market impact + delay/timing + opportunity cost of unfilled shares, plus borrow and funding carry.
- **Hidden costs backtests omit:** short-borrow fees (general collateral is cheap, but hard-to-borrow names can cost tens of % a year, with recall risk); funding spreads on leverage; futures roll; CFD and swap overnight financing; taxes and stamp duty (e.g. UK); and missed fills, often the largest cost for limit-order strategies. Borrow and funding distributions are not sourced here.

### 9.2 Market impact: the square-root law

```
Impact = Y x sigma_daily x (Q / ADV)^delta       delta ~ 0.5 (empirical range 0.4-0.7), Y "of order unity"
Total one-way cost ~ half-spread + fees + impact
```

- The square-root law is near-universal for meta-orders (Tóth et al. 2011, *PRX* — https://www.arxiv.org/abs/1105.1694v3) [Strong].
  - The explanation is a V-shaped latent liquidity profile, which breaks the linear Kyle model.
  - Bouchaud (2024) says the empirical exponent "remains stubbornly anchored" near 1/2.
- Almgren et al. 2005 (*Risk* 18(7)) find temporary impact scaling as ~3/5 power of trade rate on a large bank's US equity data [Moderate]. A Chinese-market study finds ~0.7.
- Price partially reverts after a meta-order; the permanent share is commonly put at ~2/3 of peak impact (Bacry et al. 2015) [Weak: figure unverified].
- On ~$1.7tn of AQR live trades (1998-2016), realized costs were far below earlier academic estimates, implying larger factor capacity (Frazzini, Israel & Moskowitz 2018, SSRN 3229719) [Moderate; exact figures unverified].
- **Planning parameters:** Y = 0.5-1 (the toolkit default is 0.7), then calibrate to your own fills. No sourced Y calibration by asset class exists here.

| Q/ADV | Impact, sigma_D = 2%, Y = 1 | Y = 0.5 |
|---|---|---|
| 1% | ~20bp | ~10bp |
| 5% | ~45bp | ~22bp |
| 10% | ~63bp | ~32bp |
| 25% | ~100bp | ~50bp |

Halving sigma, or cutting participation to a quarter, halves the impact. Add the half-spread and commissions on top.

### 9.3 Optimal execution (Almgren-Chriss 2000, *J. Risk* 3(2))

```
Minimize E[cost] + lambda x Var[cost]   (linear permanent impact gamma, linear temporary impact eta)
Holdings path: x(t) = X x sinh(kappa(T - t)) / sinh(kappa T),   kappa ~ sqrt(lambda sigma^2 / eta);  1/kappa = trade half-life
```

lambda -> 0 gives a linear (TWAP-like) schedule. Higher risk aversion or fast-decaying alpha front-loads the trading.

| Algo | Use when | Watch for |
|---|---|---|
| VWAP | Benchmark-relative, non-urgent orders | Predictable footprint |
| TWAP | Illiquid names or an unreliable volume curve | Ignores liquidity variation |
| POV / participation | Adapting to liquidity at a fixed % of volume | Completion time uncertain |
| IS / arrival price | Fast alpha decay or high risk aversion (front-loaded) | Higher impact |
| Limit / liquidity-seeking | Slow alpha, spread capture matters | Missed fills, adverse selection |

**Participation heuristics** [Lore, unsourced industry convention]: <= 5-10% of ADV per day is "low impact"; above 20-25%, impact and signalling rise sharply; model impact explicitly for any small-cap daily trade above ~1% of ADV; express a position as days-to-liquidate at <= 10-20% participation.

### 9.4 Capacity: the 4/9 rule

```
Cost per $ traded ~ sqrt(size)  ->  total cost = k A^1.5 per period
Net P&L = alpha A - k A^1.5   ->   A* = (2 alpha / 3k)^2       break-even A_BE = (alpha/k)^2       A* = (4/9) A_BE
```

- Profit-maximizing size is **less than half** the size at which the strategy stops making money net (math under the sqrt law).
- Turnover multiplies k, so high-turnover strategies hit capacity far sooner.
- If impact parameters are uncertain, run below A*.

---

## 10. Leverage, margin & liquidation spirals

- **US rules as cited** (check the current rule text before quoting; thresholds change): Reg T sets 50% initial margin on equity purchases (12 CFR 220). FINRA 4210 sets 25% minimum maintenance (house margin is often 30%+) and a $25,000 pattern-day-trader minimum. Portfolio margin is risk-based: positions are stressed over about +/-15% for single equities and less for broad indexes, with minimum equity commonly $100k+ [Weak: the stress ranges are unverified].
- **Margin and loss spirals** (Brunnermeier & Pedersen 2009, *RFS* 22(6)) [Strong]: losses force sales, prices fall, margins and haircuts rise, and more sales follow. Market liquidity and funding liquidity collapse together.
- **Limits of arbitrage** (Shleifer & Vishny 1997, *JF* 52(1)) [Strong]: capital is withdrawn exactly when mispricings widen.
- **Effective leverage rules** [Lore/synthesis]:
  1. The risk-relevant measure is stressed loss / equity, not gross notional / equity. 2x a 15%-vol asset is riskier than 5x a 3%-vol bond. Size by vol and stress, never by the margin available.
  2. Keep an unencumbered liquidity buffer that covers the margin call from a historical-worst move *plus* a margin increase; exchanges raise margins in vol spikes. The post-2022 UK LDI resilience standard (~250bp yield shock) is the institutional analog.
  3. A position worth multiple days of ADV cannot really be hedged or exited; its liquidation value is well below its mark.
  4. Diversify funding counterparties, and assume they will all pull at once.
- **Broker margin protects the broker, not you.** Brokers can raise house margin and liquidate without notice. Crypto venues auto-liquidate at fixed margin ratios, producing cascades.

---

## 11. Lessons from blowups

| Event | What happened | Mechanism | Generalizable rule |
|---|---|---|---|
| LTCM 1998 | >$125bn assets (Aug 1998) on $4.8bn equity (Jan 1998): >25:1; 28:1 at end-1997, OTC derivatives notional $1.3tn (end-1997). PWG: excessive leverage was "the central public policy issue". 14 firms put in $3.625bn. | Convergence trades that were short liquidity and short crisis correlation, crowded by imitators | Size to the stress scenario, not VaR; know who else holds the trade |
| Amaranth 2006 | ~$6bn lost in Sept 2006 (~$5bn in about a week, WSJ), mostly on one trader's natural-gas calendar spreads. Senate PSI found "excessive speculation" that distorted prices. | A position that was a large share of open interest | You are not liquid at the mark when you are the market; spreads are not low-risk at that size |
| Quant Quake Aug 2007 | Rapid unwind of one or more large quant equity market-neutral books (starting in July, larger from 6 Aug, market makers withdrawing from 8 Aug), then a sharp rebound on 10 Aug | Fire sale of similar portfolios triggering other funds' stops and deleveraging | Crowding is a hidden factor; identical drawdown stops amplify each other |
| Knight Capital, 1 Aug 2012 | Dead "Power Peg" code left live on 1 of 8 servers. More than 4m orders in 45 minutes (~397m shares) to fill 212 customer orders; >$460m lost; 97 warning emails ignored. $12m SEC fine in the first Rule 15c3-5 case. | Failed deployment, testing and pre-trade controls | Hard pre-trade limits (orders, notional, position), a kill switch, change management |
| Volmageddon, 5 Feb 2018 | VIX 17.31 -> 37.32 (+116%); short-vol ETPs lost >90% in a day; XIV was terminated | Leveraged and inverse VIX ETPs had to buy futures at the close in predictable size, creating a feedback loop | Short convexity can lose its whole history of gains in a day; cap it on the gap scenario, never on its realized Sharpe |
| Archegos, Mar 2021 | Credit Suisse lost ~$5.5bn. Potential exposure was more than 10x its $20m limit by Apr 2020, with scenario-limit breaches almost every week, warnings "systematically ignored", and a "fundamental failure of management and controls". | Concentrated, levered single-stock swaps spread across prime brokers so that no bank saw the total | Waived limits are no limits; aggregate exposure across counterparties |
| LME nickel, Mar 2022 | Nickel above $100k/t on 8 Mar against a large short (Tsingshan) and thin inventories. Trading was suspended for 8 days and all of 8 March's trades were cancelled. The FCA fined the LME £9.2m in 2025 (price bands switched off, thin overnight operations). | Squeeze of a dominant short, then venue control failure | Venue risk (trade cancellation, suspension) belongs in the risk register; a dominant short is a squeeze target |
| UK LDI, Sep-Oct 2022 | Long gilt yields rose ~130bp in days, about 3x any comparable move. Leveraged LDI buffers failed, forced gilt sales created a doom loop, and the BoE bought gilts. The FPC then set a ~250bp resilience standard. | A leveraged, margined "hedge" turned into a liquidity call | Stress moves several times the historical worst; a margined hedge is a liquidity risk |
| Yen carry, Aug 2024 | BIS: FX carry, especially yen-funded, was hit hardest and largely forced to unwind after a vol spike from seemingly minor news, amplified by thin August markets. Yen loans to non-residents were at least ~$250bn, but levered positions are hard to measure. Pods were closed fast. | Carry is short vol in disguise; vol-target and VaR deleveraging synchronized the exit | Carry and short vol need gap-sized caps; expect everyone's risk models to sell at once |

**Sources for the table:** LTCM: PWG 1999 (https://www.cftc.gov/tm/tmhedgefundreport.htm) and Fed History (https://www.federalreservehistory.org/essays/ltcm-near-failure). Amaranth: PSI 2007 (https://www.hsgac.senate.gov/imo/media/doc/REPORTExcessiveSpeculationintheNaturalGasMarket.pdf); loss figures are press-reported [Weak]. Quant Quake: Khandani & Lo (https://web.mit.edu/~alo/www/Papers/august07.html). Knight: SEC 2013-222 (https://www.sec.gov/news/press-release/2013-222). Volmageddon: BIS QR Mar 2018 (https://www.bis.org/publ/qtrpdf/r_qt1803t.htm); XIV lost 84% by BIS measurement, ~96% by others. Archegos: Paul Weiss report (https://sec.gov/Archives/edgar/data/1159510/000137036821000064/a210729-ex992.htm). LME: Reuters via Mining.com [secondary]. UK LDI: Hauser, BoE, Mar 2023. Yen carry: BIS Bulletin 90 (https://www.bis.org/publ/bisbull90.htm).
Not sourced here: losses at other Archegos banks, Hwang's conviction, and the 2022 crypto failures (Terra, 3AC, Celsius, FTX). For the crypto cases only the qualitative lesson is offered (rehypothecated and reflexive collateral, opaque cross-margining) [Lore].

**The common pattern:** leverage + concentration or crowding + illiquidity relative to size + a model that assumed historical vol, correlation or liquidity would hold. The operational cases add failed controls.

---

## 12. Risk rules a master runs by

Defaults to propose, then adjust to the trader's evidence. **Basis:** Convention = industry practice without rigorous test; Evidence = studies or case record; Math = derivation under stated assumptions; Synthesis = reasoned from the above.

| # | Rule | Default | Rationale | Basis |
|---|---|---|---|---|
| 1 | Risk per trade | 0.25-1% of equity; <= 0.5% while the edge is unproven; never above 2% | Streak math (§2.1): 2% x 12 losses (conservative formula estimate) = -22% | Convention + Math |
| 2 | Kelly as ceiling | <= 0.5 x Kelly on a haircut SR (min(0.5 x backtest SR, 1.0)); 0.25 x if unproven | 2x over-bet = zero growth; estimation error raises the effective fraction | Math + Evidence (Carver, MacLean-Thorp-Ziemba) |
| 3 | Portfolio vol target | min(half-Kelly vol, tolerable MDD / 95th-pct MDD multiple) | Drawdown tolerance usually binds first (§5.3) | Math (Gaussian; real tails worse) |
| 4 | Correlated clusters | Treat a cluster as one bet. Turtle analog: 6 units (6% per joint 1N move) closely correlated, 12 per direction | Correlations go to 1 in stress | Convention + Evidence |
| 5 | Stress loss | Historical worst x 2-3, correlations -> 1, plus liquidity haircut <= 20-30% of equity | LTCM, LDI, Volmageddon all passed VaR and failed stress | Synthesis from cases |
| 6 | Liquidity | Daily trading <= 5-10% ADV; position exitable in a few days at <= 10-20% participation; model impact above ~1% ADV in small caps | Impact ~ sqrt(Q/ADV); liquidity vanishes in stress | Convention (sqrt law is Evidence) |
| 7 | Drawdown tiers | Cut 25-50% at ~1x annual vol; minimum size at 1.5-2x; stop and re-validate at 2-2.5x | Bayesian update on edge; calibrate to the SR table so luck does not trip it | Synthesis (mirrors pod practice [Weak]) |
| 8 | Short convexity | Hard cap sized on the gap scenario (e.g. a VIX doubling overnight), never on realized Sharpe | Feb 2018, Aug 2024, LTCM | Evidence (cases) |
| 9 | Leverage | Size by vol and stress, never by margin available; unencumbered cash covers worst move plus margin hike | Margin spirals (Brunnermeier-Pedersen); LDI | Evidence + Synthesis |
| 10 | Stops | Trend/momentum: 2-3 ATR, size off the stop. Mean reversion: no tight stops | Kaminski & Lo: stops help only with persistence | Evidence (theory) + Convention (k) |
| 11 | Capacity | Run <= 4/9 of estimated break-even AUM, less if impact is uncertain | Square-root cost scaling | Math |
| 12 | Tail-hedge budget | <= 0.5-1%/yr of NAV, pre-committed for 5+ years, or none | Programs die from bleed fatigue (CalPERS 2019) | Lore |
| 13 | Mechanical enforcement | Pre-trade hard limits, kill switch, no waivers without a written post-mortem | Knight, Archegos | Evidence (cases) |
| 14 | No averaging down to "fix" a loss; no size-up in drawdown | Raise risk only on new equity highs or a re-validated edge | Drawdown recovery is convex (-50% needs +100%) | Lore (not sourced here) + Math |

---

## 13. Failure modes / traps

How to spot each in a user's plan or backtest:

- **Sizing from the backtest Sharpe or win rate.** Ask how many variants were tried and how long the live record is, then run `sharpe --trials` and haircut before running `kelly`.
- **"Half Kelly" on an inflated edge.** If mu_hat is 2x the true mu, "half Kelly" is really full Kelly (§2.3). Look for the in-sample optimized parameters that fed the mu.
- **Counting positions instead of bets.** Five long tech names, or long equities plus short vol plus carry, add up to one risk-on bet. Compute ENB or use cluster caps.
- **Expecting the backtest max drawdown.** A single backtest path understates the drawdown distribution. Quote the §5.3 median and 95th percentile and plan for the 95th.
- **Calm-period vol and correlations in VaR or the vol target.** Recompute at stress correlations, and assume vol x2-3.
- **Fixed-percentage stops not scaled to vol.** Tight stops are whipsawed by noise. Convert the stop to ATR multiples.
- **Tight stops on mean reversion.** They exit at the moment of maximum expected return. Check the strategy type against the §7 table.
- **Treating a stop as max loss.** Gaps, halts and limit moves jump through it. Check notional / equity and the overnight gap scenario.
- **Ignoring impact, borrow and funding in the backtest.** Look for the cost assumption; run `impact` at realistic participation, and use `ruletest --cost-bps`.
- **Scaling AUM to break-even capacity.** Optimal is 4/9 of break-even, and turnover shrinks capacity.
- **Sizing short vol or carry on its realized Sharpe.** A smooth equity curve with negative skew is the warning sign; size on the gap.
- **Selling vol targeting as alpha.** It is risk control; its Sharpe gains outside equities and credit are [Contested].
- **Using margin availability as a sizing rule.** Brokers' maintenance margin is their protection; liquidation comes at the worst moment.
- **Copying pod stop-outs as optimal.** They protect a platform holding hundreds of PMs; an individual needs tiers calibrated to their own SR.
- **Abandoning hedges or rules mid-drawdown,** or waiving limits "just this once". Ask what is pre-committed and in writing.
- **Kurtosis input error.** `sharpe --kurt` takes raw kurtosis (normal = 3); pandas and scipy report excess kurtosis by default, so add 3.

---

## 14. Toolkit hooks

Run these rather than doing mental math (`python scripts/tradekit.py <cmd>`; `--risk` values are percent, while vol and mu are decimals):

- `size --equity 100000 --risk 0.5 --entry 50 --stop 47.5` or `--atr 1.2 --atr-mult 2`, plus `--multiplier` for futures point value, `--target` for R:R and `--side short`. Gives units, cash at risk, notional and leverage warnings.
- `kelly --p 0.55 --b 1` gives discrete f* and full/half/quarter growth. `kelly --mu 0.08 --sigma 0.16 --rf 0` gives Kelly leverage and vol, growth, and P(halving).
- `expectancy --p 0.4 --win 2 --loss 1 --trades 120`: expectancy in R and the trades needed for t = 2 or 3.
- `ruin --p 0.4 --b 2 --risk 1 --trades 750 --limit 25` (add `--fixed` for fixed-dollar risk): Monte Carlo P(DD >= limit) and the drawdown distribution.
- `drawdown --loss 20 33 50` gives recovery math. `drawdown --sharpe 0.5 --vol 0.10 --years 5` gives median, 75th and 95th percentile max drawdown (Gaussian, compounding).
- `sharpe --sr 1.2 --n 1000 --skew -0.5 --kurt 6 --trials 20 --var-sr 0.1`: SE, PSR, DSR and MinTRL before trusting the SR used for sizing.
- `perf FILE [--prices] [--trials N]`: a full performance and significance report on a returns or equity file.
- `vol FILE [--window N] [--lam 0.94]`: sigma inputs for sizing (Yang-Zhang, EWMA and others).
- `impact --qty 50000 --adv 1000000 --price 40 --daily-vol 0.02 --spread-bps 4 --y 0.7 --edge-bps 30`: square-root-law cost and edge after round-trip costs.
- `python scripts/techkit.py indicators FILE` gives ATR14 (Wilder) and related indicators for stop distances.
- `techkit.py ruletest FILE --rule donchian --cost-bps 5 --vol-target 0.15 --oos 0.3`: tests sizing and vol-targeting effects with costs and an out-of-sample split.

---

## 15. Key sources

- Thorp (2006/2011), "The Kelly Criterion in Blackjack, Sports Betting and the Stock Market" — https://sites.oxy.edu/lengyel/M330/thorp/paper.htm
- MacLean, Thorp & Ziemba, "Good and Bad Properties of the Kelly Criterion" — https://www.stat.berkeley.edu/~aldous/157/Papers/Good_Bad_Kelly.pdf
- Carver (2015), *Systematic Trading*, via CXO summary — https://www.cxoadvisory.com/big-ideas/a-few-notes-on-systematic-trading ; qoppac blog (2018, 2024)
- Lo (2002), "The Statistics of Sharpe Ratios", *FAJ* 58(4): 36-52
- Harvey et al. (2018), "The Impact of Volatility Targeting", *JPM* 45(1) — https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf
- Cederburg, O'Doherty, Wang & Yan (2020), *JFE* 138(1) — https://www.lehigh.edu/~xuy219/research/COWY.pdf
- DeMiguel, Garlappi & Uppal (2009), "Optimal Versus Naive Diversification", *RFS* 22(5) — https://econpapers.repec.org/RePEc:oup:rfinst:v:22:y:2009:i:5:p:1915-1953
- Ledoit & Wolf (2004), "Honey, I Shrunk the Sample Covariance Matrix", *JPM* 30(4) — https://econ-papers.upf.edu/papers/691.pdf
- López de Prado (2016), "Building Diversified Portfolios that Outperform Out of Sample", *JPM* 42(4) (SSRN 2708678)
- Maillard, Roncalli & Teiletche (2010), ERC portfolios, *JPM* 36(4)
- Magdon-Ismail, Atiya, Pratap & Abu-Mostafa (2004), "On the Maximum Drawdown of a Brownian Motion" — https://www.cambridge.org/core/journals/journal-of-applied-probability/article/on-the-maximum-drawdown-of-a-brownian-motion/F9E3B8A454B020DDEBF0AC3390EF7807
- Kaminski & Lo (2014), "When Do Stop-Loss Rules Stop Losses?" — https://dspace.mit.edu/bitstream/handle/1721.1/114876/Lo_When%20Do%20Stop-Loss.pdf
- Tóth et al. (2011), "Anomalous Price Impact and the Critical Nature of Liquidity" — https://www.arxiv.org/abs/1105.1694v3
- Almgren & Chriss (2000), "Optimal Execution of Portfolio Transactions", *J. Risk* 3(2)
- Perold (1988), "The Implementation Shortfall", *JPM* 14(3)
- Brunnermeier & Pedersen (2009), "Market Liquidity and Funding Liquidity", *RFS* 22(6)
- Khandani & Lo (2007/2011), "What Happened to the Quants in August 2007?" — https://web.mit.edu/~alo/www/Papers/august07.html
- President's Working Group (1999), LTCM report — https://www.cftc.gov/tm/tmhedgefundreport.htm
- Paul Weiss (2021), Credit Suisse Archegos report — https://sec.gov/Archives/edgar/data/1159510/000137036821000064/a210729-ex992.htm
- BIS Quarterly Review Mar 2018 (Volmageddon) — https://www.bis.org/publ/qtrpdf/r_qt1803t.htm ; BIS Bulletin 90 (Aug 2024 carry) — https://www.bis.org/publ/bisbull90.htm
