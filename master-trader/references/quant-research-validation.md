# Quant Research and Strategy Validation

*Read when: a user shows a backtest, equity curve, Sharpe ratio or "this strategy works" claim; asks whether a result is real or overfit; is designing a walk-forward, hold-out, cross-validation or ML pipeline; needs volatility, stationarity, cointegration, half-life or regime tools; or asks which statistics to report and how much track record is enough.*

Conventions: `SR` is the per-period Sharpe unless marked "ann."; `T` is the number of return observations; `Φ` is the normal CDF and `Z⁻¹` its inverse; `γ_E ≈ 0.5772`. **Kurtosis `γ4` is raw (normal = 3)** in every PSR/DSR/MinTRL formula. pandas `.kurt()` and `scipy.stats.kurtosis` return *excess* kurtosis, so add 3 first. "(computed)" means derived from the formulas here and reproducible with `tradekit.py sharpe`. The DSR, PBO and MinBTL formulas are the standard published forms (the full texts were not re-checked). PSR and MinTRL were cross-checked against a secondary derivation (Portfolio Optimizer).

Strategy-family evidence (which edges exist, their decay and capacity) lives in **strategy-playbook.md**. This file is about deciding whether a *given* result is real.

## Contents
1. Core principles
2. Backtest review checklist (run this)
3. How many trials did you really run?
4. Luck, multiple testing and overfitting statistics
5. Performance statistics and their standard errors
6. Bias audit: look-ahead, survivorship, point-in-time, costs, fills, borrow
7. Walk-forward and out-of-sample protocol design
8. Machine learning in finance
9. Stylized facts of returns
10. Volatility estimation
11. Stationarity, cointegration, half-life
12. Regime detection
13. Failure modes and traps
14. Toolkit hooks
15. Tooling and data sources (as of Nov 2026)
16. Key sources

---

## 1. Core principles

- **Every variant tried is a test, and selecting the best one manufactures Sharpe.** With zero true skill, the best of N trials still has an expected Sharpe that grows roughly like √(2 ln N). A 1,000-point grid search on 10 years of data yields an ann. SR of about 1.0 from noise alone (computed). A backtest Sharpe means nothing without its trial count. [Strong]
- **A Sharpe ratio is an estimate with a wide error bar.** Under IID returns its annualized SE is about 1/√years, so 5 years of data gives ±0.45 and a 5-year SR of 1.0 has a 95% CI of roughly [0.1, 1.9] (computed). Always report the SE or PSR next to the point estimate. [Strong]
- **Explain a great backtest in this order: bug, then bias, then luck, and only then skill.** Look-ahead, survivorship, optimistic fills and data snooping can each create the whole edge. Check the cheap, fatal ones first. [Lore]
- **The hurdle scales with how hard you searched.** t > 3 (Harvey-Liu-Zhu) is calibrated to a field that has mined hundreds of factors. One pre-registered, economically motivated hypothesis tested once can stand on t ≈ 2 (Harvey & Liu 2020). A personal grid search of thousands of variants needs more than 3. [Strong; "most findings are false" is Contested]
- **Out-of-sample means unseen.** A hold-out stops being out-of-sample the moment its result influences a design choice, and every look counts as a trial. Paper trading or small-capital live incubation is the only truly unseen test. [Moderate]
- **Returns are fat-tailed, heteroskedastic and, for illiquid assets, smoothed.** Tests that assume IID-normal returns overstate confidence, and negative skew plus positive autocorrelation inflate the Sharpe. Adjust before judging (PSR with skew and kurtosis, Lo's η(q)). [Strong]
- **Model the user's own costs, not an institution's.** AQR's live data says academic cost estimates are too high for a skilled large executor. Retail traders and small funds pay spreads, impact and borrow that kill high-turnover anomalies. [Contested: the direction depends on who is trading]
- **Published edges decay.** Anomaly returns are about 26% lower out of sample and about 58% lower after publication (McLean & Pontiff 2016). Haircut any strategy lifted from a paper, a blog or a forum. [Strong]
- **Preventing leakage is not alpha.** Purged CV, triple-barrier labels and CPCV make the evaluation honest. They do not create returns. [Logic Strong; evidence of a profit contribution Weak]

---

## 2. Backtest review checklist (run this)

Work from top to bottom. Report at the first fatal finding: there is no point deflating the Sharpe of a look-ahead bug.

**Stage 0. Intake: ask for, or infer, the following.**
1. The return series (CSV of periodic returns, or an equity curve) and its frequency, plus the trade list if there is one.
2. The universe and how it was formed (today's index members? dead names included?), the data vendor and the period.
3. Signal timing: when the signal is computed and when the order fills (same close, next open, next close).
4. The cost model: commissions, spread, impact, borrow, funding and roll, plus position size as a % of ADV.
5. **Everything that was tried** (Section 3).
6. What was fixed before the data was seen, and what was chosen after.

**Stage 1. Sanity statistics.** Run `python scripts/tradekit.py perf returns.csv --ppy 252` (add `--prices` for an equity column, and `--trials N --var-sr V` once N is known).

| Observation | Likely meaning | Action |
|---|---|---|
| Ann. SR > 3 on daily-or-slower bars without HFT infrastructure | Assume a bug or look-ahead until proven otherwise [Lore] | Go straight to Stage 2 |
| Lag-1 autocorrelation > 0.1 | Stale or smoothed prices, or illiquid marks. The annualized SR is biased up (Lo 2002) | Apply η(q) (Sec. 5) or de-smooth |
| High hit rate, avg win < avg loss, negative skew | A short-vol or short-tail payoff whose Sharpe flatters it (Goetzmann et al. 2007) | Stress the tails; compare the worst period with the vol |
| t < 3 after a search, or PSR(0) < 95% | Not distinguishable from luck | Section 4 |
| MinTRL > sample length | Too little evidence even before any trial deflation | Needs more data or live time |
| Max DD well below the median from `drawdown --sharpe --vol --years` | The curve is too smooth: smoothing, overfitting or a hidden tail | Investigate |
| Calmar or max DD compared across different backtest lengths | Invalid, because max DD grows with sample length | Compare over equal horizons |

**Stage 2. Look-ahead and timing audit (fatal if failed).**
1. Every input carries a timestamp before decision time. Check reporting lags, restatements (use as-first-reported values), index membership as of each date and corporate-action dates.
2. Nothing fills at the close used to compute the signal, or at the bar's high or low. The default is next-bar execution.
3. Re-run with an extra 1-bar execution delay. If the Sharpe collapses, the edge lives in the timing assumption.
4. Any z-score, scaler, PCA, hedge ratio or regime model fitted on the full sample is a leak. These must be fitted on expanding or rolling windows using data ≤ t.
5. HMM and Markov-switching models must use *filtered* probabilities, not smoothed ones (Sec. 12).
6. ML labels that span more than one bar require purged CV plus an embargo (Sec. 8).

**Stage 3. Universe and data.**
1. Dead and delisted securities are included, with their delisting returns (Sec. 6).
2. Fundamentals are point-in-time (vendor PIT data, or the Fama-French July-of-year-t lag).
3. P&L uses total-return-adjusted prices. Share counts and price filters (e.g. "price > $5") use unadjusted prices.
4. Re-run excluding microcaps (below the NYSE 20th percentile) and value-weighted. If the edge vanishes, it was probably untradable (Hou-Xue-Zhang 2020; Avramov et al. 2023).

**Stage 4. Costs, fills, borrow.**
1. Spread plus square-root impact: `tradekit.py impact --qty Q --adv V --price P --daily-vol s --spread-bps b --edge-bps e`.
2. Limit orders: fill probability is below 1 and fills are adversely selected. Never assume a fill just because price touched the limit.
3. Shorts: charge borrow fees, model recalls, and exclude hard-to-borrow names or charge them specials rates.
4. Leverage pays a funding spread, and futures roll costs must be modeled.
5. Report the Sharpe at 1× and 2× the assumed costs, plus the breakeven cost per unit of turnover [Lore]. `ruletest --cost-bps` sets the cost per 1.0 of turnover.

**Stage 5. Multiple testing.**
1. Establish N, both the raw count and an effective count (Sec. 3).
2. Run `tradekit.py sharpe --sr S --n T --ppy P --skew g3 --kurt g4 --trials N --var-sr V` for the PSR, MinTRL and DSR. The pass mark is DSR ≥ 0.95.
3. If the full matrix of trial returns exists, compute PBO by CSCV (`pypbo`, or the R package `pbo`). PBO > 0.5 means the selection process is worse than random.
4. Several candidates against one benchmark: use Hansen's SPA or Romano-Wolf StepM (`arch.bootstrap`).
5. If N is uncertain, show the DSR at N = 10, 100 and 1,000.

**Stage 6. Robustness.**
1. Parameter plateau: neighbouring parameters must also work. `techkit.py ruletest FILE --rule R --oos 0.3` prints "plateau" or "spiky". Spiky means the parameters were fitted to noise.
2. Sub-periods and other markets: the sign should be consistent.
3. Out-of-sample vs in-sample Sharpe: expect decay. A collapse toward 0 means the edge was mostly fitted.
4. For ML, the CPCV distribution of OOS Sharpe ratios, not a single path.

**Stage 7. Verdict.** The grouping is judgment [Lore]; the thresholds inside it are sourced.

| Verdict | Criteria |
|---|---|
| Broken | Fails Stage 2 or 3 (look-ahead, survivorship, impossible fills) |
| Likely overfit | DSR < 0.5 at honest N, PBO > 0.5, spiky parameters, or OOS collapse |
| Unproven | Passes the audits, but DSR < 0.95, t is below the hurdle for the search intensity, or the sample is shorter than MinTRL |
| Plausible: incubate | Passes the audits; DSR ≥ 0.95 at honest N; parameter plateau; OOS holds; economic rationale; costs modeled at the user's scale |
| (There is no "proven") | A backtest never proves an edge. Only a live record of at least MinTRL length does |

```
Verdict: <Broken | Likely overfit | Unproven | Plausible - incubate>
Fatal issues: <look-ahead / survivorship / fills ... or none found>
Stats: ann. SR x.xx +/- SE; PSR(0) ..%; DSR ..% at N_eff=..; MinTRL .. yrs vs sample .. yrs
Biggest unmodeled risk: <costs at size / borrow / regime / tail>
Cheapest decisive next test: <+1 bar delay / ex-microcap / 2x costs / fresh hold-out / incubate>
```

---

## 3. How many trials did you really run?

The DSR, MinBTL, BHY and the t > 3 hurdle all need N. Users routinely under-report it by one or two orders of magnitude because they count only the final grid [Lore].

**Hidden-trial inventory. Ask about each source:**

| Source | How it counts |
|---|---|
| Parameter grid points | Each point |
| Abandoned rules or indicator variants ("tried RSI first, didn't work") | Each one |
| Markets, universes, sectors, timeframes | Multiply |
| Entry, exit, stop, target and holding-period variants | Each one |
| Filters added after seeing a drawdown ("skip 2008", "only when VIX < 30") | Each one. Also look-ahead in disguise |
| Start/end dates, IS/OOS split point, walk-forward window length, rebalance frequency | Each one |
| Cost assumptions changed after seeing results | Each one |
| ML feature sets, hyperparameters, architectures, label definitions, random seeds | Each configuration evaluated |
| Each look at the hold-out | +1 per look, and the hold-out is burned for DSR purposes |
| The idea came from a paper, blog or forum | The search is inherited. Apply the post-publication haircut and the t > 3 hurdle |
| Earlier versions of "the same" strategy | Each one |

**Procedure.**
1. **Raw count, N_raw**, from the research log, or reconstructed with the user.
2. **Effective count, N_eff.** Correlated trials count as fewer. The best method is to cluster the trial return series and use the number of clusters as N, with the cross-cluster variance as V[SR] (López de Prado & Lewis 2019, ONC) [Moderate]. A crude version counts distinct idea families × markets and treats adjacent grid points as one family [Lore].
3. **V[SR]** is the variance of the annualized Sharpes across trials; `--var-sr` takes it annualized. If it was not logged, ≈ 1/years is the pure-noise dispersion (computed). Real trial sets with genuine dispersion run higher, and a higher V raises the deflation.
4. Run the DSR at both N_eff and N_raw and report both. `ruletest` deflates by its own grid size; add `--extra-trials k` to multiply by the rules or markets tried before.
5. **If N cannot be reconstructed**, treat the backtest as exploratory. The only valid test left is fresh data: a new hold-out or live incubation, with the strategy frozen.

**What luck alone produces.** Expected ann. SR of the best of N zero-skill trials (computed from the False Strategy Theorem, with σ(SR_ann) = 1/√years):

| N trials | 1 yr | 3 yrs | 5 yrs | 10 yrs | 20 yrs |
|---|---|---|---|---|---|
| 2 | 0.52 | 0.30 | 0.23 | 0.16 | 0.12 |
| 10 | 1.57 | 0.91 | 0.70 | 0.50 | 0.35 |
| 45 | 2.24 | 1.29 | **1.00** | 0.71 | 0.50 |
| 100 | 2.53 | 1.46 | 1.13 | 0.80 | 0.57 |
| 1,000 | 3.26 | 1.88 | 1.46 | 1.03 | 0.73 |
| 10,000 | 3.86 | 2.23 | 1.73 | 1.22 | 0.86 |

**Canonical cautionary case [Strong].** Sullivan, Timmermann & White (1999) built a universe of **7,846** technical rules on 100 years of DJIA data. The best rule chosen as of the end of 1986 was a 5-day moving-average rule. Over 1987-1996 it earned a mean return of 2.8% with a nominal p-value of 0.322 (working-paper version, verified this session). That is the in-sample winner of a large search failing out of sample.

**Questions to ask the user:**
- "Before this version, what else did you try, including the things you threw away in the first hour?"
- "Did you choose the parameters, the market or the dates after seeing any results?"
- "How many times have you looked at the out-of-sample period?"
- "Where did the idea come from?"

---

## 4. Luck, multiple testing and overfitting statistics

### 4.1 Significance hurdles
- **HLZ:** because hundreds of factors have been tested, a new factor needs "a t-ratio greater than 3.0" (Harvey, Liu & Zhu 2016) [Strong as a calibration]. The Sharpe needed to clear a t-hurdle, using t ≈ SR_ann·√years (computed):

| Years | t = 2 | t = 3 |
|---|---|---|
| 1 | 2.00 | 3.00 |
| 3 | 1.15 | 1.73 |
| 5 | 0.89 | 1.34 |
| 10 | 0.63 | 0.95 |
| 20 | 0.45 | 0.67 |

- **Haircut Sharpe** (Harvey & Liu 2015): adjust the Sharpe's p-value for multiple testing with Bonferroni, Holm or BHY. The haircut is nonlinear. Highly significant Sharpes lose little, while marginal ones often lose more than 50%, so the flat "50% haircut" rule of thumb is wrong [Moderate].
- **False vs missed discoveries** (Harvey & Liu 2020): stricter cutoffs trade false positives for missed edges, and the optimal cutoff depends on their relative costs [Moderate].
- **[Contested] Is there a replication crisis?**
  - Hou, Xue & Zhang (2020): 65% of 452 anomalies fail |t| ≥ 1.96 once microcaps are controlled, and 82% fail t ≥ 2.78.
  - Jensen, Kelly & Pedersen (2023): a Bayesian test on 153 factors across 93 countries finds a replication rate of about 82-85% (figures vary slightly by paper version), with 10 of 13 themes above 75%. The exceptions are seasonality, leverage and size.
  - Chen (2021): plausible amounts of p-hacking cannot generate the published t-stat distribution.
  - How to apply this: the debate concerns carefully built academic factors. A user's private grid search, replicated by no one, sits closer to the pessimistic case (inference).
- **Decay:** anomaly returns are about 26% lower out of sample and about 58% lower after publication (McLean & Pontiff 2016) [Strong].

### 4.2 Probabilistic Sharpe Ratio and Minimum Track Record Length
```
SR_hat ~ N(SR, (1 - g3*SR + ((g4-1)/4)*SR^2) / T)        Opdyke 2007; per-period SR, raw kurtosis g4
PSR(SR*) = Phi( (SR_hat - SR*) * sqrt(T-1) / sqrt(1 - g3*SR_hat + ((g4-1)/4)*SR_hat^2) )
MinTRL   = 1 + (1 - g3*SR_hat + ((g4-1)/4)*SR_hat^2) * ( Z^-1(1-alpha) / (SR_hat - SR*) )^2   [observations]
Small-sample bias (normal returns, Miller & Gehr 1978): E[SR_hat] ~ SR * (1 + 3/(4T))
```
PSR = 1 − p-value of the one-sided test SR > SR*. Pass at ≥ 95% [Strong]. PSR is invariant to calendar conventions, and raw Sharpes from different sample lengths are not comparable.

MinTRL in **years** to show SR > 0 at 95% (computed):

| Ann. SR | Daily, normal | Daily, skew −1, kurt 10 | Monthly, normal | Monthly, skew −1, kurt 6 |
|---|---|---|---|---|
| 0.5 | 10.8 | 11.2 | 11.0 | 12.8 |
| 1.0 | 2.7 | 2.9 | 2.9 | 3.9 |
| 1.5 | 1.2 | 1.3 | 1.4 | 2.1 |
| 2.0 | 0.7 | 0.8 | 0.9 | 1.4 |

Fat tails and negative skew bite much harder at low frequency. Worked example (computed, `sharpe --sr 1 --n 136 --ppy 12 --bench 0.75`): an ann. SR of 1.0 over 136 months needs a MinTRL of about 542 months (45 years) to confirm SR > 0.75 at 95%. The ~184 months quoted for a Bitcoin RSI strategy (Portfolio Optimizer) would need an SR of about 1.18; the source's exact SR was not recorded, so do not quote that figure.

### 4.3 Deflated Sharpe Ratio (Bailey & López de Prado 2014)
```
DSR = PSR(SR0),   SR0 = sqrt(V[SR_n]) * ( (1-gE)*Z^-1(1 - 1/N) + gE*Z^-1(1 - 1/(N*e)) )
V[SR_n] = cross-sectional variance of the trials' estimated Sharpes;  N = independent trials
```
Illustration: a 5-year daily backtest with an observed ann. SR of 1.5 and V[SR] at the pure-noise value (computed):

| N | SR0 (ann.) | DSR |
|---|---|---|
| 1 | 0 | ≈ 1.00 |
| 10 | 0.70 | 0.96 |
| 100 | 1.13 | 0.79 |
| 1,000 | 1.46 | 0.54 (a coin flip) |

Skew and kurtosis barely move the DSR at daily frequency: skew −1 with kurtosis 10 takes the N = 100 result from 0.794 to 0.782. They matter far more at monthly frequency [computed].

### 4.4 Minimum Backtest Length (Bailey, Borwein, López de Prado & Zhu 2014)
```
MinBTL ~ ( ((1-gE)*Z^-1(1-1/N) + gE*Z^-1(1-1/(N*e))) / E[max_N] )^2  <  2*ln(N) / E[max_N]^2     [years]
```
E[max_N] is the ann. SR you are willing to accept as an in-sample maximum. For E[max] = 1.0 (computed): N = 10 needs 2.5 years, N = 45 needs **5.0** (the paper's headline: on 5 years of daily data, try no more than about 45 independent configurations), N = 100 needs 6.4 and N = 1,000 needs 10.6. When strategies have "memory" (for example, mean reversion overfitted to noise), overfitting can produce *negative* expected OOS performance, not just zero [Moderate].

### 4.5 Probability of Backtest Overfitting via CSCV (Bailey et al. 2017)
1. Build a T×N matrix of returns for all N trials.
2. Split the rows into S contiguous blocks, with S even. S = 16 is commonly used, giving C(16,8) = 12,870 combinations; the paper's recommended S was not verified.
3. For each combination of S/2 blocks: those blocks are IS and the rest are OOS. Pick the best IS trial and find its relative OOS rank ω̄, then compute λ = ln(ω̄/(1 − ω̄)).
4. PBO = the fraction of combinations with λ ≤ 0, i.e. the IS winner ranks at or below the OOS median.
5. Companion diagnostics: the slope of OOS vs IS performance (degradation) and the probability of an OOS loss.

PBO > 0.5 means selection is worse than random. A practitioner comfort level is ≤ 0.1-0.2 [Lore; no authoritative threshold exists].

### 4.6 Bootstrap data-snooping tests and error-rate control
- **White's Reality Check** (2000) tests H0 that the best of k rules has no superior performance against a benchmark, using the stationary bootstrap over the full search [Strong].
- **Hansen's SPA** (2005) studentizes and recenters so that poor or irrelevant alternatives do not dilute the test, making it more powerful than the RC [Strong]. **Romano-Wolf StepM** (2005) identifies *which* strategies beat the benchmark while controlling the family-wise error rate (FWER). SPA, StepM, the Model Confidence Set and block bootstraps are all in `arch.bootstrap`.
- **FWER control** (Bonferroni, Holm, StepM) suits a single strategy about to be deployed. **FDR control** (Benjamini-Hochberg) suits screening many signals for a combined book (inference).
```
BH:  sort p-values; largest k with p_(k) <= (k/m)*q; reject H_(1..k)
BHY: same with q replaced by q / c(m), c(m) = sum_{i=1..m} 1/i   (valid under arbitrary dependence; used by HLZ)
```

---

## 5. Performance statistics and their standard errors

```
SE(SR_hat)  ~ sqrt((1 + SR^2/2) / T)                          Lo 2002, IID normal
SE non-normal: sqrt((1 - g3*SR + ((g4-1)/4)*SR^2) / T)         Opdyke 2007
SR(q) = eta(q) * SR,  eta(q) = q / sqrt(q + 2*sum_{k=1}^{q-1} (q-k)*rho_k)   (not sqrt(q) when autocorrelated)
Sortino = (R - MAR) / DD,   DD = sqrt(mean(min(0, R - MAR)^2)) over ALL periods
Omega(L) = int_L^inf (1-F(r)) dr / int_-inf^L F(r) dr
IR = alpha / tracking error ~ IC * sqrt(breadth)             Grinold 1989; breadth = INDEPENDENT bets/yr
Expectancy = p*W - (1-p)*L (net of costs);  breakeven hit rate p* = 1/(1 + W/L)
Calmar = annual return / |max drawdown|   (often trailing 36 months)
```

**Annualized SE of Sharpe (IID, computed):** 1 yr ≈ 1.00, 3 yrs ≈ 0.58, 5 yrs ≈ 0.45, 10 yrs ≈ 0.32, roughly independent of SR for SR in 0.5-2. With monthly data, 5 years, SR 1, skew −1 and kurtosis 6, it widens from 0.46 to 0.53.

**Autocorrelation inflation:** naive √12 annualization overstates the Sharpe under AR(1) monthly autocorrelation ρ by:

| ρ | 0.1 | 0.2 | 0.3 | 0.4 |
|---|---|---|---|---|
| Overstatement (computed) | +10% | +20% | +33% | +47% |

Lo (2002) reports hedge-fund annual Sharpes overstated by up to 65% [Strong]. Smoothed marks (hedge funds, private assets) lower measured volatility and inflate the Sharpe (Getmansky, Lo & Makarov 2004) [Strong]. De-smooth them or apply η(q).

**Breakeven hit rate:** at payoff ratios 0.5, 1, 2 and 3 it is 67%, 50%, 33% and 25%. Flag a high hit rate with a payoff below 1 as likely short volatility or short tail risk. Option-selling-like payoffs can manipulate the Sharpe, and the MPPM resists this (Goetzmann, Ingersoll, Spiegel & Welch 2007) [Strong].

**Rules:**
- **The minimum report** is: ann. SR ± SE, PSR(0), DSR with N, skew and *raw* kurtosis, max DD with its length, Calmar over a stated horizon, hit rate together with payoff ratio, turnover and costs.
- **Comparing two strategies' Sharpes** requires their joint distribution, including their correlation (Opdyke 2007). Two overlapping CIs do not settle the question.
- **Calmar and max DD grow with sample length**, so never compare them across different lengths [Lore].
- **Breadth counts independent bets.** Correlated positions or overlapping holding periods inflate the apparent breadth.
- **Trade-count significance:** `tradekit.py expectancy --p --win --loss --trades` gives the number of trades needed for t = 2 or 3.

---

## 6. Bias audit: look-ahead, survivorship, point-in-time, costs, fills, borrow

| Bias | How it enters | Detection | Fix |
|---|---|---|---|
| Look-ahead | Same-bar close fills; restated fundamentals; no reporting lag; index membership as of today; full-sample normalization; smoothed regime probabilities | +1 bar delay test; trace the timestamps of each input; check the scaler's fit window | Next-bar execution; PIT data; expanding-window fits |
| Survivorship | Universe = today's constituents; dead funds or stocks dropped | Count delistings in the universe; compare with a survivorship-free source | Include dead names (Brown, Goetzmann, Ibbotson & Ross 1992) [Strong] |
| Delisting returns | CRSP lacks many performance-delisting returns, which biases small-stock anomaly returns up | Check how missing delisting returns are handled | Shumway (1997): −30% for NYSE/AMEX performance delistings; Shumway & Warther (1999): −55% for Nasdaq [Strong; figures confirmed via secondary sources this session] |
| Point-in-time | Fundamentals used before they were public | Compare announcement dates with signal dates | Fama-French convention: fiscal-year t−1 data used from July of year t [Strong] |
| Corporate actions | Mixing adjusted and unadjusted prices | Check price filters and share counts | Total return for P&L; unadjusted prices for filters and share counts |
| Costs | Zero or flat costs on high-turnover signals | Turnover × cost vs gross edge | Spread + √-impact; 2× cost stress |
| Fills | Trading at highs/lows; limit fills assumed at touch; size larger than the available liquidity | Inspect fills; size vs ADV | Next bar, fill probability < 1, participation caps |
| Borrow and funding | Free shorting; free leverage; no roll cost | Is there a short-side cost line? | Borrow fees, recalls, exclude HTB names; funding spread; roll |
| Data snooping | Undisclosed trials | Section 3 | DSR, PBO, SPA |
| Storytelling and outliers | Narrative fitted after the fact; a few extreme days drive the result | Remove the top 1% of days and re-check | Pre-registered hypothesis; winsorized robustness checks |

**Costs evidence.**
- Trading costs eliminate many anomalies, especially high-turnover ones. Mitigations (buy/hold spreads, less frequent rebalancing) recover part of the return (Novy-Marx & Velikov 2016) [Strong].
- **[Contested, opposite direction]** Frazzini, Israel & Moskowitz (2018) used $1.7 trillion of AQR live equity executions (Aug 1998-Jun 2016, 21 developed markets, about 10,000 stocks) and found costs about an order of magnitude below earlier academic estimates. Value, size, momentum and profitability survive, but capacity is limited. Their estimates exclude shorting costs and do not represent retail or average investors (details verified this session via the SSRN abstract and secondary coverage).
- **The square-root impact law:** impact ≈ Y·σ_daily·√(Q/V_daily), with Y of order 1 across markets (Tóth et al. 2011) [Strong]. The `impact` command defaults to Y = 0.7.

**Checklist origins:** the "Seven sins" (Luo et al. 2014, Deutsche Bank, cited via AFML Ch. 11) are survivorship, look-ahead, storytelling, data mining, costs/turnover/decay, outliers, and asymmetric patterns and shorting costs. Arnott, Harvey & Markowitz (2019) add: an a-priori economic hypothesis, report all trials, guard against CV leakage, keep OOS truly unseen, model costs, and allow for structural change [Moderate].

---

## 7. Walk-forward and out-of-sample protocol design

**Protocol. Fix steps 1-3 before touching the data.**
1. **Hypothesis**: the economic rationale and who is on the other side of the trade. See strategy-playbook.md for known families.
2. **Trial budget and log**: cap N in advance (MinBTL: about 45 independent trials for 5 years at a 1.0 acceptance Sharpe) and log every run, including failures.
3. **Splits**: a development set (purged k-fold or CPCV), a walk-forward validation, and a final hold-out touched **once**. Set the re-optimization frequency and window type before seeing results.
4. **Data**: point-in-time, survivorship-free, with delisting returns.
5. **Costs**: model them at the user's own scale and stress them at 2× [Lore].
6. **Statistics**: DSR at honest N, PBO if a trial matrix exists, and SPA or StepM against benchmarks.
7. **Incubation**: paper trading or small capital until the live record approaches MinTRL, or at least long enough to check that live costs and slippage match the model.
8. **Pre-registered kill criteria**: CUSUM or change-point tests on live P&L (Sec. 12) instead of an ad-hoc "the drawdown feels too big".

| Window | Use when | Risk |
|---|---|---|
| Anchored (expanding) | The relationship changes slowly, data is scarce | Slow to adapt after breaks |
| Rolling | The relationship adapts (microstructure, regimes) | Noisier estimates; window length is itself a trial |

- **Walk-forward produces a single path and can be overfitted.** Researchers iterate until the walk-forward looks good, and "backtesting while researching" is a named failure mode (López de Prado 2018) [Moderate]. CPCV gives a distribution of OOS Sharpes instead (Sec. 8).
- **Pardo's walk-forward efficiency** (OOS ann. return / IS ann. return, with comfort at ≥ 50%) is a heuristic, not a test [Lore].
- **A hold-out is burned** once its result shapes any choice. From then on it is in-sample, and the look counts toward N.

---

## 8. Machine learning in finance

**Expectations [Strong].** Gu, Kelly & Xiu (2020; numbers from NBER w25398, rev. 2019, verified this session):
- Trees and neural networks reach monthly stock-level OOS R² of **0.33-0.40%**. The OLS 3-predictor benchmark reaches 0.16%, and OLS with 900+ predictors goes negative. Elastic net reaches 0.11% and PCR/PLS 0.26-0.27%.
- A value-weighted NN long-short decile strategy has an OOS ann. Sharpe of **1.35**. NN timing of the S&P 500 earns 0.77 against 0.51 for buy-and-hold.
- The gains come from nonlinear interactions. The dominant signals are momentum, liquidity and volatility.
- Coaching rule: expect monthly cross-sectional R² below 1% even for good models. Judge them on portfolio metrics net of costs, not on R² or accuracy.

**Contested.**
- ML profits concentrate in microcaps, distressed stocks and hard-to-arbitrage names, and drop sharply once economic restrictions are imposed (Avramov, Cheng & Metzker 2023) [Contested]. Always re-run without microcaps and value-weighted.
- "Virtue of complexity": over-parameterized models are claimed to improve market timing (Kelly, Malamud & Zhou 2024) [Contested]. Critiques arguing the gains are mechanical (e.g. Nagel, 2025 working paper) were not reviewed.

**Why finance is hard for ML** (Israel, Kelly & Moskowitz 2020): small data, low signal-to-noise, non-stationarity, and adaptive markets that arbitrage predictability away [Moderate].

**The López de Prado toolkit (AFML 2018).** The logic is sound; independent evidence of incremental profit is Weak.

| Technique | Mechanics and defaults |
|---|---|
| Triple-barrier labels (Ch. 3) | Profit-take and stop barriers at multiples of a dynamic vol (e.g. EWMA of daily returns), plus a vertical barrier at the maximum holding period. The label is the first barrier touched, or the sign of the return at the vertical barrier |
| Meta-labeling (Ch. 3) | A primary model (rules or discretion) picks the side. A secondary classifier predicts P(primary signal profitable) and uses it to size or veto. Raises precision and F1 at the cost of recall. **The lowest-risk way for a discretionary trader to add ML** |
| Uniqueness weights (Ch. 4) | Concurrency c_t = number of labels spanning bar t; ū_i = mean over the label's span of 1/c_t. Weight samples by ū (optionally × absolute return) and use a sequential bootstrap for bagging |
| Purged k-fold (Ch. 7) | Drop training observations whose label interval overlaps any test label interval, then embargo after each test fold. **Default embargo = max(label horizon, ≈1% of T)**. The "≥ 2× horizon" rule seen online is unsourced |
| CPCV (Ch. 12) | N groups; test on every combination of k groups. Splits = C(N,k); paths φ = C(N−1, k−1). Gives a distribution of OOS Sharpes |
| Feature importance (Ch. 8) | MDI: in-sample, trees only, biased, diluted by substitution. MDA: permutation on purged OOS folds scored by log-loss; model-agnostic but subject to substitution. SFI: no substitution effects but misses interactions. Clustered MDI/MDA handles correlated features (López de Prado 2020) |

CPCV sizes (computed; check any library against φ = C(N−1, k−1), since one PyPI package's docs contradict its own code): N=6, k=2 gives 15 splits and 5 paths; N=8, k=2 gives 28 and 7; N=10, k=2 gives 45 and 9; N=10, k=3 gives 120 and 36.

**Rules.**
- scikit-learn's `TimeSeriesSplit(gap=...)` approximates an embargo but does **not** purge overlapping labels. Standard k-fold leaks whenever labels span more than one bar.
- Use feature importance for research, not repeated backtests: "backtesting is not a research tool".
- López de Prado's "10 reasons ML funds fail" (2018) to check against a user's pipeline: siloed PMs instead of a research assembly line; integer differencing; time bars instead of information-driven bars; fixed-horizon labels; non-IID weighting; CV leakage; walk-forward overfitting; backtesting while researching.

---

## 9. Stylized facts of returns

| Fact | Evidence | What it changes |
|---|---|---|
| Near-zero linear autocorrelation of returns (except at very short intraday scales) | Cont 2001 [Strong] | Direction is hard to predict from past returns |
| Volatility clustering; slow decay of autocorrelation in \|r\| and r² | Cont 2001 [Strong] | Scale risk by a conditional (forecast) vol, not a long-run average |
| Power-law tails, index ≈ 3 for equities (the "inverse cubic law") | Gopikrishnan et al. 1998; Gabaix et al. 2003 [Moderate]. Cont's range "between two and five" is a secondary quote | Variance is finite, but with a tail index ≈ 3 the 4th moment is infinite. **Sample kurtosis is unstable** |
| Leverage effect: vol rises more after declines | Christie 1982 [Strong] | Use GJR/EGARCH for equities; vol targeting helps most in risk assets |
| Aggregational Gaussianity | Cont 2001 [Strong] | Monthly returns are closer to normal than daily, but not normal |
| Positive weekly autocorrelation in small-cap portfolios | Lo & MacKinlay 1988 [Strong] | Partly stale prices and lead-lag effects, not pure predictability |
| 10 of 11 facts still hold on modern US intraday data; gain/loss asymmetry does not | arXiv 2311.07738 (2023) [Moderate, single study] | Don't assume gain/loss asymmetry in modern intraday data |

- One crash day (e.g. 1987-10-19) can change S&P 500 daily kurtosis by an order of magnitude. Report tail quantiles, expected shortfall or a Hill tail-index estimate rather than kurtosis alone.
- There is **no vetted table of kurtosis or tail index by asset class.** Figures circulating online (e.g. FX excess kurtosis of "5-10") are unverified, so don't quote them as established.
- Stops and position sizing calibrated on normal tails will be hit far more often than the normal model predicts.

---

## 10. Volatility estimation

o, h, l, c are logs of open, high, low and close; u = h − o, d = l − o, c' = c − o.
```
Parkinson:       s2 = mean[(h-l)^2] / (4 ln2)                         zero drift, no gaps
Garman-Klass:    s2 = mean[0.5(h-l)^2 - (2ln2 - 1)(c-o)^2]            zero drift, no gaps
Rogers-Satchell: s2 = mean[u(u-c') + d(d-c')]                         drift-robust, misses gaps (biased low)
Yang-Zhang:      s2 = s2_overnight + k*s2_open-close + (1-k)*s2_RS,  k = 0.34/(1.34 + (n+1)/(n-1))   (k ~ 0.14 for n = 20-252)
EWMA:            s2_t = lam*s2_{t-1} + (1-lam)*r_{t-1}^2             lam 0.94 daily (half-life 11.2 d), 0.97 monthly (22.8)
GARCH(1,1):      s2_t = w + a*e_{t-1}^2 + b*s2_{t-1};  a+b<1;  long-run w/(1-a-b);  shock half-life ln0.5/ln(a+b)
GJR:             add g*1[e_{t-1}<0]*e_{t-1}^2  (g>0 = leverage)
HAR-RV:          RV_{t+1} = b0 + bd*RV_t + bw*RV_t^(5d) + bm*RV_t^(22d) + e     (OLS)
```
Theoretical efficiency relative to close-to-close: Parkinson 5.2, GK 7.4, RS 8.0, **YZ 14.0** [Strong in theory; live gains are smaller, Moderate]. GARCH α+β = 0.98 implies a shock half-life of about 34 days; α+β near 1 on daily equities is common, which is why EWMA is a good approximation (computed). The typical fitted ranges quoted online (α ≈ 0.05-0.10, β ≈ 0.85-0.94) are an unverified rule of thumb.

| Situation | Use | Defaults |
|---|---|---|
| Closes only, monthly risk | Close-to-close | 60-252 days. Relative SE ≈ 1/√(2n): ±16% at 20 d, ±9% at 60 d, ±4.5% at 252 d (computed) |
| Daily OHLC with gaps (single stocks, session futures) | Yang-Zhang | 20-63 bars |
| 24h markets without gaps (spot FX, crypto) | GK or RS | 20-63 bars |
| Risk scaler for sizing | EWMA | λ = 0.94 |
| Mean-reverting multi-day forecasts, option or VaR horizons | GARCH(1,1) or GJR, Student-t innovations | `arch` package |
| Intraday data available | 5-minute RV plus HAR; bipower variation if jumps matter | 5-minute sampling is hard to beat (Liu, Patton & Sheppard 2015) [Strong] |

- **Nothing beat GARCH(1,1)** among 330 models on DM/USD. Leverage-capturing models beat it on IBM stock (Hansen & Lunde 2005) [Strong]. RV-based models forecast better than GARCH on daily horizons (Andersen et al. 2003) [Strong].
- **Clean the data before using range estimators.** Bad high or low prints and bid-ask bounce corrupt them, and Parkinson is biased low under discrete sampling and when overnight gaps are ignored.
- **[Contested] Vol targeting:**
  - Man AHL finds it cuts left tails and lifts the Sharpe in equities and credit, with little effect in bonds, FX and commodities (Harvey et al. 2018).
  - Moreira & Muir (2017) report alpha from vol-managed factors, but Cederburg et al. (2020) find the real-time-implementable versions do not systematically beat unmanaged portfolios.

---

## 11. Stationarity, cointegration, half-life

**Run ADF (null: unit root) and KPSS (null: stationarity) together:**

| ADF rejects? | KPSS rejects? | Read |
|---|---|---|
| Yes | No | Stationary |
| No | Yes | Unit root |
| Yes | Yes | Near-unit-root, fractionally integrated, or structural breaks |
| No | No | Low power; need more data |

- Both tests have low power in short samples, and failing to reject is not evidence [Strong]. ADF uses Dickey-Fuller/MacKinnon critical values, not t-tables. With a constant, the asymptotic values are about −2.86 at 5% and −3.43 at 1%; use the library-reported values.
- **Engle-Granger** (`statsmodels coint`) runs OLS and then a unit-root test on the residuals. It needs cointegration-specific critical values and depends on which variable is the dependent one. **Johansen** (`coint_johansen`) suits more than 2 series, is robust to normalization, and returns the hedge vectors [Strong].
- **OU half-life:** regress Δx_t = a + b·x_{t−1} + ε; then θ = −ln(1+b) ≈ −b, and half-life = ln2/θ. Setting the z-score lookback and holding period near the half-life is a heuristic (Chan 2013) [Lore].
- **Variance ratio:** VR(q) = Var(q-period return) / (q·Var(1-period)). VR = 1 is a random walk, VR < 1 mean reversion and VR > 1 trending. Use heteroskedasticity-robust statistics (Lo & MacKinlay 1988).
- **Hurst:** H < 0.5 is anti-persistent and H > 0.5 persistent. Classical R/S is biased by short-range dependence, and Lo's (1991) modified R/S finds little long memory in stock returns [Moderate]. Treat Hurst and VR as descriptive.
- **Fractional differentiation (FFD):** apply (1−B)^d with ω_0 = 1 and ω_k = −ω_{k−1}(d−k+1)/k, truncating when |ω_k| < 1e-5. Pick the minimum d that passes ADF at 95%. It is theoretically motivated, but no independent OOS evidence shows it beats returns-plus-level features [Weak]. The "d ≈ 0.3-0.6 for liquid futures" claim is unverified.

**Pairs and stat-arb protocol:**
1. Pre-select pairs on an economic link (same industry, supply chain, ETF vs basket). Every pair tested adds to N.
2. Test cointegration in the formation window only.
3. Reject pairs whose half-life is longer than the intended hold, or only a few bars (costs dominate there).
4. Trade in a separate window and re-test periodically, because cointegration breaks (Sec. 12).

---

## 12. Regime detection

- **What works.** Markov-switching models (Hamilton 1989), Gaussian HMMs and mixture models describe risk states well in sample, such as a low-vol bull state and a high-vol, high-correlation crash state. Ang & Bekaert (2002) find that regime-switching allocation adds value, mainly through defensive positioning in the bad regime [Moderate].
- **[Contested] Out-of-sample forecasting.** Regime models often forecast worse than random-walk or linear models even when they fit better in sample, because misclassifying the regime is costly (Dacco & Satchell 1999).
- **Practitioner use** is descriptive and for risk management. Two Sigma has written on Gaussian mixtures on factor returns ("crisis", "steady state", "inflation", "walking on ice"); the URL is unverified.
- **Structural breaks and change points:**
  - Bai-Perron (1998, 2003) estimates and tests multiple unknown break dates.
  - PELT (Killick et al. 2012) segments exactly, at linear cost, under a penalty.
  - Bayesian online change-point detection (Adams & MacKay 2007) is causal and fit for live use.
  - In Python, use `ruptures`.
  - Use these as **model-invalidation alarms** (CUSUM on strategy returns, cointegration breaks), not as alpha sources.

**Look-ahead traps (critical):**
1. Smoothed probabilities (forward-backward) and Viterbi paths use the whole sample, future included. Backtests may only use **filtered** P(s_t | data ≤ t) from models refitted on expanding or rolling windows. In statsmodels, check that the code reads `filtered_marginal_probabilities`, not `smoothed_marginal_probabilities`. Any library call that decodes the full sequence at once leaks.
2. State labels switch across refits (state 0 and state 1 swap). Normalize by sorting the states on variance.
3. Value comes mostly from risk scaling and de-risking in the high-vol state, not from return forecasting. That is consistent with volatility clustering.

---

## 13. Failure modes and traps

| Trap | How to catch it in a user's work |
|---|---|
| Reporting the best grid cell's Sharpe as "the" Sharpe | Ask for the full grid. Run `ruletest` to check for a plateau, and compute the DSR at the grid size |
| "I only tried a few things" | Walk through the hidden-trial inventory (Sec. 3) |
| Same-bar close execution | +1 bar delay test |
| Full-sample z-scores, scalers or hedge ratios | Ask where `.mean()`, `.std()` and `fit()` are called and on which window |
| Smoothed HMM probabilities or Viterbi path in a backtest | grep for `smoothed_` or full-sequence `predict` |
| Today's index constituents as the universe; no delisting returns | Ask for the source and the count of dead names |
| Microcap-driven edge | Re-run excluding names below the NYSE 20th percentile, value-weighted |
| Costs flat or zero; shorts free; limit fills at the touch | `impact` command; 2× cost stress; borrow line item |
| Repeatedly peeking at the hold-out | Count the looks; treat the hold-out as in-sample |
| Excess kurtosis passed as raw into PSR/DSR | If kurtosis is near 0 for daily returns, it is excess: add 3 |
| √252 annualization of autocorrelated returns | `perf` flags lag-1 autocorrelation > 0.1; apply η(q) |
| A high-win-rate strategy with negative skew praised for its Sharpe | Hit rate vs payoff; worst period; tail stress |
| Standard k-fold or TimeSeriesSplit with multi-bar labels | Require purging plus an embargo |
| Judging ML on accuracy or R² | Demand net-of-cost portfolio Sharpe with a CPCV distribution |
| Comparing Calmar or Sharpe across different sample lengths | Normalize the horizon; use PSR |
| Walk-forward re-run until it "works" | Count each walk-forward configuration as a trial |
| A strategy from a paper treated as fresh | Apply the post-publication haircut (≈58%) and t > 3 |
| Cointegration tested on the full sample, then traded on it | Formation and trading windows must be separate |

---

## 14. Toolkit hooks

Run these instead of doing mental math. Paths are relative to the skill directory: call each script by its absolute path from a working folder.

| Need | Command |
|---|---|
| Full performance report plus significance | `python scripts/tradekit.py perf FILE --ppy 252 [--prices] [--percent] [--rf 0.04] [--trials N --var-sr V]`. It computes raw kurtosis and flags lag-1 autocorrelation |
| SE, CI, PSR, MinTRL, DSR from summary stats | `python scripts/tradekit.py sharpe --sr ANN_SR --n OBS --ppy 252 --skew S --kurt RAW_K --trials N --var-sr V_ANN [--bench 0.5]`. `--kurt` is **raw** (normal = 3) |
| Rule backtest with grid robustness, DSR and OOS split | `python scripts/techkit.py ruletest FILE --rule sma\|cross\|donchian\|tsmom\|rsi2\|bbrev [--params ...] [--cost-bps 5] [--short] [--vol-target 0.15] [--oos 0.3] [--delay 1] [--ppy 252] [--extra-trials k]`. Fills at the next bar's close (`--delay 1`); `--delay 0` fills at the signal close (optimistic, only for a real market-on-close process); next-open fills are not modelled. Set `--ppy` for non-daily bars |
| Expected max drawdown for a Sharpe/vol/horizon | `python scripts/tradekit.py drawdown --sharpe 1 --vol 0.15 --years 10` |
| Trades needed for t = 2/3 | `python scripts/tradekit.py expectancy --p 0.45 --win 1.8 --loss 1 --trades 120` |
| Volatility estimators from OHLC | `python scripts/tradekit.py vol FILE [--window 63] [--lam 0.94]` |
| Half-life, Hurst, variance ratios | `python scripts/tradekit.py meanrev FILE [--col spread] [--log]` (use `--log` for prices). Confirm with ADF/Johansen in statsmodels |
| Cost and impact vs edge | `python scripts/tradekit.py impact --qty Q --adv V --price P --daily-vol 0.02 --spread-bps 2 [--y 0.7] --edge-bps E` |

Not in the toolkit: ADF/KPSS/Johansen (statsmodels), GARCH/HAR and SPA/StepM/MCS (`arch`), PBO (`pypbo`, R `pbo`), purged CV/CPCV (custom code). Write short scripts for these rather than estimating by hand.

---

## 15. Tooling and data sources (as of Nov 2026; versions from conflicting secondary sources; check PyPI/GitHub)

- **Core stack:** pandas, NumPy, statsmodels (ADF, KPSS, `coint`, Johansen, Markov switching), `arch` (GARCH/GJR/EGARCH with t or skew-t innovations, HAR via `HARX`, and bootstrap SPA/StepM/MCS with stationary or circular block bootstraps), scikit-learn (`TimeSeriesSplit` gap ≠ purge), `ruptures` (change points), and R `PerformanceAnalytics` (`MinTrackRecord`, `ProbSharpeRatio`).
- **No mainstream backtester natively implements purged CV, CPCV, DSR or PBO.** mlfinlab (Hudson & Thames) went commercial, so check its licence.
- **Backtesters (status as of Nov 2026, secondary sources):**
  - **NautilusTrader** is the most actively developed: Rust core, Python API, live trading. Reported versions include 1.231.0 (Aug 2026) and a 2.0 release candidate; GA status unverified.
  - **QuantConnect LEAN**: historically Apache 2.0; its 2026 status was not re-checked.
  - **zipline-reloaded** is an active community fork. Reported releases range from 3.1.1 (Jul 2025) to 3.2.x (Oct 2026); the sources conflict.
  - **vectorbt**: the open-source version is reportedly in maintenance, with development in the paid PRO edition; the sources conflict.
  - **backtrader** has been effectively frozen since its last release in Apr 2023. Don't start new projects on it unless the user accepts that.
  - Workflow: vectorized code for screening (log every run), then an event-driven engine for fills, order types and live parity.
- **Data:**
  - **Polygon.io became Massive** on 2025-10-30. `api.polygon.io` remains supported alongside `api.massive.com`, and existing keys remain valid. A third-party listing (Aug 2026) reports a free tier of 5 calls/min with EOD data and 2 years of history, and a $29/mo Stocks Starter plan; verify on massive.com.
  - **IEX Cloud shut down in 2024.**
  - **yfinance** is an unofficial scraper. It breaks, is rate-limited, is survivorship-biased (no delisted tickers) and is not point-in-time. It is fine for prototyping and unfit for a final validation (inference).
  - 2026 pricing for Databento, Tiingo, Alpha Vantage, EODHD and Nasdaq Data Link was not verified.
- **Free research data:** Open Source Asset Pricing (Chen & Zimmermann, openassetpricing.com), JKP Global Factor Data (jkpfactors.com), the Kenneth French Data Library, and FRED.

---

## 16. Key sources

- Harvey, Liu & Zhu 2016, "…and the Cross-Section of Expected Returns", RFS — https://doi.org/10.1093/rfs/hhv059
- Harvey & Liu 2015, "Backtesting", JPM (haircut Sharpe) — https://papers.ssrn.com/abstract=2345489
- Bailey & López de Prado 2012, PSR/MinTRL, J. of Risk — https://ssrn.com/abstract=1821643
- Bailey & López de Prado 2014, "The Deflated Sharpe Ratio", JPM — https://papers.ssrn.com/abstract=2460551
- Bailey, Borwein, López de Prado & Zhu 2014, MinBTL, Notices of the AMS — https://www.ams.org/notices/201405/rnoti-p458.pdf
- Bailey, Borwein, López de Prado & Zhu 2017, "The Probability of Backtest Overfitting", J. Comp. Finance — https://papers.ssrn.com/abstract=2326253
- Portfolio Optimizer, PSR bias, CIs and MinTRL (secondary derivation used to cross-check formulas) — https://portfoliooptimizer.io/blog/the-probabilistic-sharpe-ratio-bias-adjustment-confidence-intervals-hypothesis-testing-and-minimum-track-record-length/
- López de Prado 2018, *Advances in Financial Machine Learning*, Wiley — https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086
- López de Prado 2018, "The 10 Reasons Most Machine Learning Funds Fail", JPM — https://papers.ssrn.com/abstract=3104816
- Lo 2002, "The Statistics of Sharpe Ratios", FAJ — https://doi.org/10.2469/faj.v58.n4.2453
- White 2000, Reality Check, Econometrica — https://doi.org/10.1111/1468-0262.00152 ; Hansen 2005, SPA, JBES — https://doi.org/10.1198/073500105000000063
- Sullivan, Timmermann & White 1999, data-snooping in technical rules, JF — https://doi.org/10.1111/0022-1082.00163
- Arnott, Harvey & Markowitz 2019, "A Backtesting Protocol in the Era of Machine Learning", JFDS — https://papers.ssrn.com/abstract=3275654
- McLean & Pontiff 2016, post-publication decay, JF — https://doi.org/10.1111/jofi.12365
- Hou, Xue & Zhang 2020, "Replicating Anomalies", RFS — https://doi.org/10.1093/rfs/hhy131 ; Jensen, Kelly & Pedersen 2023, JF — https://nber.org/system/files/working_papers/w28432/w28432.pdf
- Gu, Kelly & Xiu 2020, "Empirical Asset Pricing via Machine Learning", RFS — https://doi.org/10.1093/rfs/hhaa009 (NBER w25398)
- Novy-Marx & Velikov 2016, anomaly trading costs, RFS — https://doi.org/10.1093/rfs/hhv063 ; Frazzini, Israel & Moskowitz 2018, "Trading Costs" — https://papers.ssrn.com/abstract=3229719
- Yang & Zhang 2000, JB — https://doi.org/10.1086/209650 ; Hansen & Lunde 2005, JAE — https://doi.org/10.1002/jae.800
- Cont 2001, "Empirical properties of asset returns: stylized facts", Quant. Finance — https://ideas.repec.org/a/taf/quantf/v1y2001i2p223-236.html
