# Strategy Orchestration: Choosing Strategies and Finding Opportunities

*Read when: the user asks "what should I trade now?", wants a universe or watchlist scanned, asks which strategy, setup or indicator to run in the current regime, wants to add, switch, weight, scale up or kill strategies, runs or reads `scanner.py regime` / `scan` / `select`, or shows a selection process (screens, regime switching, "best backtest" picks, rotation systems) that needs review.*

**Tags.** Grade first, then provenance: `[Strong | V-PR]`. **V** = source read during the research session; **K** = prior knowledge with a full citation, not re-fetched; **SC** = spot-check the number or DOI before quoting it to a user. Evidence class: **PR** peer-reviewed, **WP** working paper/preprint, **PM** practitioner method, **L** lore. **[computed]** = arithmetic or simulation from the stated formulas (re-run 12 Nov 2026). **[inference]** = a synthesis default with no controlled study behind it: tune it on the user's data and log the tuning as a trial. As of 12 Nov 2026.

**Cross-references (not restated here).** DSR, PSR, MinTRL, PBO, trial counting, walk-forward mechanics, HMM look-ahead: `quant-research-validation.md` §3-4, 7, 12. Family evidence, crowding, two-sleeve allocation: `strategy-playbook.md` §13, 16-17. Regime diagnosis: `macro-regimes.md` §2-3. 1/N, ERC, HRP, pod drawdown rules: `risk-sizing-execution.md` §4, 6. Setup rule cards: `momentum-trading.md` §2, 5; `technical-analysis.md` §7.

## Contents
1. Core principles
2. The orchestration loop (procedure, defaults, commands)
3. Can strategies be timed? Evidence and the bounded regime dial
4. Selection without overfitting, and reading `scanner.py select`
5. Capital allocation across strategies: staging, alarms, kill rules
6. Opportunity scanning, and reading `scanner.py scan`
7. Failure modes and red flags in a user's selection process
8. Toolkit hooks
9. Key sources

---

## 1. Core principles

- **Timing a strategy's return is weak; timing its risk works.** Value-spread timing mostly re-creates a static value position, and many timing models stop being significant once realistic data lags and costs are applied (Asness et al. 2017; Ilmanen et al. 2021). The robust regime results are all about risk: momentum crashes in panic states, liquidity provision pays when VIX is high, and regime models cut drawdowns. So the regime sets a **bounded multiplier (0.5x-1.5x)** on each family's risk budget. It is never an on/off switch. [Strong that timing is fragile; the bounds are inference]
- **The in-sample winner is a biased pick; averaging is the cure.** With zero skill, the best of 20 variants still shows t ≈ 1.9. Picking the best k of n signals is nearly as bad as picking the single best of n^k (Novy-Marx 2015). Out of sample, equal-weight ensembles across parameters and plausible strategies beat "optimal" estimated weights (the forecast combination puzzle). [Strong]
- **Sharpe differences between plausible strategies cannot be detected on realistic histories.** Separating strategies whose Sharpes differ by 0.2 at t = 2 takes 40-200 years [computed]. Default to equal risk, and tilt only on shrunk, deflated evidence, with a cap.
- **Every screen is a trial.** Each setup × universe × parameter set adds to N. A scanner that has not itself been validated is a watchlist generator, not a signal. To validate it, test its historical top-k performance net of costs, with DSR at N = the number of screens tried.
- **Breadth carries the edge.** IR ≈ TC·IC·√BR, and single-stock ICs are small. A 5-name screen book is mostly idiosyncratic noise (about 16% tracking noise against a plausible 3-6% alpha). Act on 20 or more names, or on every eligible futures market for trend and carry. [Strong theory; computed]
- **Correlated names are one bet.** Ten semiconductor breakouts are a single cluster. Size the cluster, not the names, and cap total open risk ("heat"). [Logic Strong; heat caps Lore]
- **Expect live results at 40-70% of the backtest.** Published anomalies lose about 26% out of sample and about 58% after publication, and factor premia about 30% out of sample. That shortfall is the baseline, not an alarm. [Strong]
- **Drawdowns are weak evidence against low-Sharpe sleeves.** A true SR 0.5 sleeve can stay under water for about 11 years with no decay at all. A kill needs two independent alarms, or one alarm plus a broken payer. [Moderate; formulas SC]
- **Pre-register the loop.** Families, definitions, ensembles, the cost model and alarm thresholds are fixed before the data is seen, and every later change is logged as a trial. Automate the arithmetic. Keep judgment for the payer test, regime calls at turning points, and kills, each with a written reason. [inference]

---

## 2. The orchestration loop

Run it on a fixed schedule (weekly scan, quarterly re-selection) [inference]. Commands are relative to the skill directory. Add `--fetch` on the first run and reuse `--data-dir` (default `scan_data`) after that.

**Step 0. Trial ledger (automate).** Keep an append-only log in the user's project folder. Each row records date, universe, families or setups, parameter grids, cost model, result, and running counts N_raw and N_eff (correlated variants collapse into fewer effective trials; `quant-research-validation.md` §3). Every `scan` run, `select` run, re-optimization and override gets a row. Feed the counts into `tradekit.py sharpe --trials N --var-sr V`. For `techkit.py ruletest --extra-trials M`, M is a *multiplier* on the grid's own trial count (rules, markets or screens tried before). **scanner.py does not keep this ledger, so Claude must.**

**Step 1. Regime read (automate the calculations; a human confirms the label when it flips).**
- `scanner.py regime --universe etf-core sectors --fetch --bench SPY` gives the benchmark trend, breadth and the 20-day vol percentile (§3.3 lists exactly what it computes).
- `fetch.py macro` gives growth, inflation, HY OAS, VIX, NFCI, the curve and policy uncertainty. Make the quadrant call with `macro-regimes.md` §2.
- Add what scanner.py does not compute:
  - **Funding stress:** `fetch.py fred BAMLH0A0HYM2 --start <8 weeks ago>`. HY OAS up about 100 bp or more within roughly 4 weeks is a flag.
  - **Stock-bond correlation:** 63-day; above +0.2 means bonds do not hedge.
  - **Daniel-Moskowitz panic state:** benchmark trailing 24-36-month return below 0 and vol in the top tercile.
  - **Goulding momentum state** from the signs of the 12-month and 1-month returns: Bull (+,+), Correction (+,−), Bear (−,−), Rebound (−,+).
- Use filtered (real-time) values only. Before relabeling, require persistence: a minimum dwell of about 1 month, or a jump-penalized model.

**Step 2. Family eligibility (automate the multipliers; overrides are judgment, written and logged).**
- `scanner.py select --universe etf-core futures --fetch --years 20 --short`, or run it on the user's own markets. It gives a per-family verdict (*timing edge*, *risk overlay* or *drop*) and inverse-vol weights (§4.5).
- Base budget = equal risk across correlation clusters of families. Then apply the regime multipliers (§3.3), staying inside 0.5x-1.5x.
- No family goes to zero on a return forecast. A family goes to zero only through a kill decision (Step 8).

**Step 3. Universe and liquidity gate (automate).** Any backtest needs point-in-time constituents, delisted names included. Gates per asset class are in §6.1. scanner.py defaults to `--min-price 5 --min-adv 20e6`; the ADV test uses the 50-day mean of close × volume and is skipped for files without volume (Yahoo FX, for example).

**Step 4. Scan (automate).** `scanner.py scan --universe sectors megacap --fetch --equity 100000 --risk 0.5 --top 20 --out scan.csv`. Use canonical definitions with the source paper's default parameters. Families the scanner lacks (carry, pairs, PEAD, short-term reversal, multi-asset TSMOM portfolios) need the definitions in §6.3.

**Step 5. Rank (automate).** Keep per-family lists, each with its own risk budget; build a cross-family composite only for a single integrated book (§6.4). Act on the top 10-20% of a stock universe (at least 20-30 names) for cross-sectional sleeves, every eligible market for futures trend and carry, and slot-limited lists for swing setups. Never lower the threshold to fill slots.

**Step 6. Candidate checks (automate the checks; judgment on news and event context).** For each shortlisted name:
- **Snapshot:** `techkit.py indicators FILE` (trend template, Weinstein stage, RSI, ATR, relative volume, partial-bar warning).
- **Does the setup's rule family work on this instrument at all?** `techkit.py ruletest FILE --rule donchian --params 55 --oos 0.3 --extra-trials M`.
- **Liquidity at the intended size:** at most 1% of ADV for daily swing trades, at most 5% for slower ones. Price the cost with `tradekit.py impact`.
- **Events inside the hold** (earnings, FOMC, CPI): reject, or size for a gap through the stop. For geopolitical exposure use Workflow H and `eventkit.py study`.
- **Lookback agreement:** at least 2/3 of the ensemble lookbacks should agree on the sign; otherwise cut size by half.
- **Signal quality:** the signal is not driven by one outlier day, and there are no crowding flags (`strategy-playbook.md` §13).
- **Meta-label gate:** only if one has already been validated (§4.6).

**Step 7. Sizing (automate).**
- Per idea: `tradekit.py size --equity E --risk R --entry X --stop S`, where R = base risk × regime multiplier × evidence multiplier × track-record stage (§5.1).
- **Clusters:** a correlation cluster is one bet, and no cluster may carry more than 30-35% of total risk. Size to stressed correlations (ρ → 0.8 among risk assets).
- **Total heat:** at most about 5-6% of equity [Lore].
- **Negative-skew sleeve:** cap it by its joint stress loss (`strategy-playbook.md` §17).

**Step 8. Monitor (automate the alarms; the kill is judgment, with a written payer test).** Monthly, per sleeve: CUSUM against h, drawdown and time under water against expectations, live/backtest SR ratio, realized vs modeled cost, participation rate, crowding. Run `tradekit.py perf live.csv --ppy 252 --trials N`; the rules are in §5.4.

**Step 9. Re-validate (automate the re-estimation; judgment on adopting the result).** Re-run `select` quarterly or annually, re-run DSR/PBO at the updated N, and refit any regime model on schedule (for example every 6 months). A changed deployed parameter set is a new trial and is incubated before it scales. Retire setups that stop working; do not re-optimize them.

**Judgment only (never automate):** naming each family's payer and checking it still exists; calling a regime flip when indicators disagree; overriding a multiplier for a known event; kill and restart decisions; adding a family (it opens a new trial budget).

**Answer shape (SKILL.md Workflow I):** regime read → strategy verdicts with the walk-forward table as evidence → ranked shortlist of 5-10 names, clusters marked → per-candidate confirmation notes → heat and allocation → what would change the plan, plus the trial count behind any significance claim.

---

## 3. Can strategies and factors be timed?

### 3.1 Evidence

| Approach | Finding | Grade |
|---|---|---|
| Value-spread (contrarian) timing | Looks promising alone but mostly duplicates value. Added to a multi-style book that already holds value it is "disappointing" and cuts diversification. Weak even at extremes or with longer holds (Asness, Chandra, Ilmanen & Israel 2017). Asness 2016: at most "sin a little" [SC DOI] | [Contested \| V-PR]. Pro-timing side: Haddad, Kozak & Santosh 2020 time principal-component anomaly portfolios by their own B/M spreads and report large OOS gains, but in frictionless long-short tests with gains concentrated in the dominant PCs [K-PR, SC; do not quote a Sharpe]. Baba Yara, Boons & Tamoni 2021: value spreads predict value across asset classes [K-PR, SC]. Research Affiliates (Arnott et al. 2016-17): valuation predicts 5-year factor returns [K-PM] |
| A century of premia | Premia about 30% lower OOS, "more likely" from overfitting. Little reliable link to macro, liquidity, sentiment or crash risk. "Mildly predictable" under theory restrictions, but "many timing strategies are not significantly profitable" after proper data lags and costs (Ilmanen, Israel, Lee, Moskowitz & Thapar 2021) | [Strong \| V-PR] |
| Parametric multi-predictor timing | Gains largely vanish after turnover and estimation error; static tilts are hard to beat (Dichtl et al. 2019, conclusion as recalled) | [Moderate \| K-PR, SC] |
| Factor momentum | Average factor earns about 1 bp/month after a losing year vs about 53 bp/month after a winning year, and factor momentum explains stock momentum (Ehsani & Linnainmaa 2022). Own 1- and 12-month returns predict in 65 factors (Gupta & Kelly 2019). The 1-month version is strongest (Arnott, Clements, Kalesnik & Linnainmaa WP) | [Moderate \| K-PR, SC]. The best-supported timing signal, but it overlaps stock momentum. Investors who chase strategy returns lose (Dichev 2007; Hsu, Myers & Whitby 2016) [K-PR, SC] |
| Vol scaling of factors | Moreira & Muir 2017: 1/variance scaling raises Sharpe for market, value, momentum and profitability. Cederburg et al. 2020: real-time versions of 103 strategies win 53 times and lose 50. After costs it survives mainly for market and momentum (Barroso & Detzel 2021 [SC]). A conditional multifactor version works net of costs (DeMiguel, Martín-Utrera & Uppal 2024) | [Contested \| K-PR] in general; [Strong] for momentum (`momentum-trading.md` §2) |
| Vol targeting by asset class | Raises Sharpe where there is a leverage effect (equities, credit) but not for bonds, FX or commodities; cuts left tails everywhere (Harvey et al. 2018) | [Moderate \| K-PR, SC DOI] |
| Market state × XS momentum | Momentum earns about +0.93%/month after UP 36-month markets vs about −0.37% after DOWN markets (Cooper, Gutierrez & Hameed 2004) [SC numbers]. It crashes in panic states (after declines, with high vol, as markets rebound); dynamic scaling roughly doubles alpha and Sharpe (Daniel & Moskowitz 2016) | [Strong \| K-PR] |
| VIX × short-term reversal | Reversal returns proxy the returns to liquidity provision and are "highly predictable with the VIX index". Expected returns and Sharpe rise in turmoil as intermediaries withdraw (Nagel 2012) | [Moderate \| V-PR]; coefficients not retrieved |
| Trend across regimes | TSMOM "smile": best in extreme up and down markets (Moskowitz, Ooi & Pedersen 2012). A 1/3/12-month blend is positive in every decade since 1880 and strong in most 60/40 drawdowns (Hurst, Ooi & Pedersen 2017) | [Strong \| K-PR] |
| Momentum speed by state | In the disagreement states (Correction, Rebound) a state-conditioned blend of slow and fast momentum beats static speeds (Goulding, Harvey & Mazzoleni 2023) | [Moderate \| K-PR, SC] |
| Regime-switching allocation | Adds value mainly by moving defensive in the high-vol, high-correlation regime (Ang & Bekaert 2002; Kritzman, Page & Turkington 2012 [SC]). Cuts drawdowns OOS, and jump penalties fix the HMM's excess switching (Nystrup et al. 2018, 2020 [SC]). Regime models often forecast worse than simple models (Dacco & Satchell 1999) | [Moderate \| K-PR] |
| Trend-strength regimes (ADX, Hurst, variance ratio) choosing trend vs mean reversion | No peer-reviewed support at daily-to-monthly horizons | [Lore] |
| Crypto regime-conditional performance | No fetched evidence | none |

**Penalized (jump) regime model, out of sample.** Shu, Yu & Mulvey 2024 [Moderate | V-PR]:
- Test period 1990-2023, 10 bp one-way cost; the signal at close t is applied from t+2.
- Features use returns only: EWM downside deviation (10-day half-life) and EWM Sortino (20- and 60-day).
- The jump penalty is re-chosen monthly by validation Sharpe over 8 years, and the model is refit every 6 months on 3,000 days.

| Index (OOS) | Buy & hold SR / MDD | HMM SR / MDD | Jump model SR / MDD |
|---|---|---|---|
| S&P 500 | 0.48 / −55.2% | 0.54 / −28.9% | 0.68 / −26.6% |
| DAX | 0.30 / −72.7% | 0.35 / −40.5% | 0.44 / −39.4% |
| Nikkei 225 | 0.12 / −79.1% | 0.19 / −48.6% | 0.31 / −45.3% |

- **Robustness:** S&P jump-model SR is 0.71 with a 5-day delay and 0.70 with a 10-day delay. The HMM underperforms at a 5-day delay on DAX and Nikkei.
- **Limits:** signals lag crash starts and ends by about half a month; long turbulent periods are misread; only 3 indices; part of the drawdown cut comes from about 80% average exposure.
- **Lesson:** persistent-state models work as a drawdown dial, and the penalty search is itself a selection step, so count it as trials.

**Also:**
- **Minimum regime performance** (Alexander & Fabozzi 2026) [Weak | V-WP]: the worst risk-adjusted return across distinct regimes. A high long-run Sharpe does not imply it is high, so use it as a fragility diagnostic.
- **Man/Duke "Regimes"** (Mulliner, Harvey et al. 2025) [K-WP, SC; not fetched]: times factors by how similar today's state variables are to past months', and reports that "anti-similar" months also carry information. Do not quote numbers.

### 3.2 What a master concludes
- **Regime information is a risk dial.** Scale risk down in bad states. Do not use it to pick next month's best strategy.
- **Factor momentum is at most a ±25% tilt, never a switch.** Chasing a sleeve that is in a drought (value 2007-2020) is exactly where investors lose.
- **Use persistent-state labels and filtered probabilities only.** Smoothed HMM probabilities are look-ahead (`quant-research-validation.md` §12).

### 3.3 Default family multipliers [inference; thresholds Lore]

| Family | Condition | Multiplier |
|---|---|---|
| XS momentum, plus 52w-high, trend-template and breakout longs that load on it | Panic state: benchmark 24-36-month return below 0 **and** realized vol in the top tercile | 0.5x (else 1.0x); vol-scale continuously on top |
| Short-term reversal / liquidity provision | VIX in its top quintile (Nagel) | Up to 1.25-1.5x, with a gross cap (widest spreads, gap risk) |
| Trend / TSMOM | All regimes (the crisis diversifier) | 1.0x; blend speeds rather than switching lookbacks |
| Carry | Funding stress: HY OAS +100 bp within weeks, USD/JPY carry-unwind signals (`macro-regimes.md` §2, Step 5) | 0.5x |
| Value, quality, defensive | Static | ±25%, and only when the valuation spread is above its 90th percentile |
| Any sleeve | Sign of the sleeve's own trailing 12-month return (factor momentum) | ±25% |

Keep the product of all multipliers inside 0.5x-1.5x of the strategic budget.

**What `scanner.py regime` actually computes** (so Claude can describe it precisely):
- **Trend.** The benchmark is `--bench`, or else the instrument with the highest $ADV. It is "up" if price > SMA200 and SMA200 is above its value 21 bars earlier, "down" if both conditions are reversed, and "mixed" otherwise.
- **Breadth.** The share of loaded instruments above their SMA200. Instruments need at least 260 bars.
- **Vol.** The benchmark's 20-day realized vol against its own 3-year history, sampled every 5 days. "High" means at or above the 80th percentile, "low" at or below the 30th. These cut-offs differ from the tercile split used in Step 1, so say which one you are using.
- **Tilts.** Up trend with breadth ≥ 60%: longs 1.0x, shorts 0.5x. Down trend with breadth ≤ 40%: longs 0.5x, shorts 1.0x. Otherwise 0.75x for both. High vol only adds advice text ("cut size, widen stops, expect more false breakouts"); it applies no numeric tilt.
- **Limits.** The tilt never goes above 1.0x. The script has no funding-stress, stock-bond, panic-state or Goulding inputs. **The tilt scales the scan score (rank order), not the units column, so apply the multiplier to `--risk` yourself.** Its "Next" line points to `fetch.py macro` and `macro-regimes.md` §2, because a price-based read is not a macro call.

---

## 4. Selection without overfitting

### 4.1 Why "pick the best backtest" fails
- **Best t-stat from N independent zero-skill trials** [computed; False Strategy Theorem form]: N = 5 → 1.19; 10 → 1.57; 20 → 1.90; 50 → 2.28; 100 → 2.53; 500 → 3.05; 1,000 → 3.26. Correlated variants count as fewer effective trials.
- **Combining signals** (Novy-Marx 2015) [Strong (logic) | V-WP]. Each signal is oriented to have worked in sample, so combinations of *random* signals look "highly significant". Critical values "can be several times standard levels", and the best k of n ≈ the best single signal of n^k.
- **Decay by vintage and complexity** (Falck, Rej & Thesmar 2021/22) [Moderate | V-PR, SC journal]. Publication year alone explains 30% of the variance in Sharpe decay, and each year newly published factors decay 5 ppt more. Signal complexity and in-sample outlier sensitivity add about 15% more explanatory power.
- **Multiple-testing haircuts are non-linear** (Harvey & Liu 2015) [Strong | K-PR, SC DOI]. Marginal Sharpes are often cut by more than 50%; very high ones are cut proportionally less. A flat "halve it" rule is wrong in both directions.

### 4.2 Combinations and ensembles beat selection
- **Equal weights win.** Equal-weight forecast combinations routinely beat estimated weights out of sample, most of all when individual models are unstable (Timmermann 2006) [Strong | K-PR, SC DOI].
- **Pooling weak predictors works.** Single equity-premium predictors fail out of sample (Welch & Goyal 2008) [Strong | K-PR]. Combining them gives significant OOS gains "consistently over time" (Rapach, Strauss & Zhou 2010) [Strong | V-PR; R² not retrieved].
- **Why the combination puzzle exists.** Estimating near-equal weights adds variance and bias (Smith & Wallis 2009; Claeskens et al. 2016) [Moderate | K-PR, SC]. Invalid weighting formulas and model screening also contribute, so always include the simple average as a candidate (Qian et al. 2015) [Weak | V-WP]. Tests that compare combination schemes have low power (Frazier et al. 2023) [Weak | V-WP].
- **Parameter ensembles.** Moving-average crossovers and TSMOM are the same family of weighted past returns, and diversified lookback blends are robust (Levine & Pedersen 2016) [Strong | K-PR, SC DOI]. Hurst-Ooi-Pedersen use an equal 1/3/12-month blend, not a "best" lookback.
- **Carver's handcrafting** (Carver 2015) [Lore | K-PM]:
  - forecasts scaled to an average absolute value of 10 and capped at ±20;
  - forecasts combined across rules and lookbacks, then rescaled by a diversification multiplier;
  - weights equal within correlated groups, then equal across groups;
  - Sharpe tilts only when a difference is statistically meaningful, which is rare.
- **Ensembles across lookbacks and rebalance dates** cut "parameter luck" (ReSolve) [Lore | PM; articles not verified].

### 4.3 Shrink before you compare
**Normal-normal shrinkage** [computed]: posterior = w·SR̂ + (1−w)·m, with w = τ²/(τ² + Var(SR̂)) and a skeptical prior m = 0.3, τ = 0.3. From daily or monthly data, Var(SR̂) ≈ 1/T (years), which matches the `tradekit.py sharpe` SE. The values in [brackets] use the more skeptical annual-observation form, (1 + SR̂²/2)/T. If the strategy is the best of N, deflate it first (DSR or haircut) and then shrink.

| Backtest SR̂ | T = 3 y | T = 5 y | T = 10 y |
|---|---|---|---|
| 1.0 | 0.45 [0.41] | 0.52 [0.46] | 0.63 [0.56] |
| 1.5 | 0.56 [0.44] | 0.67 [0.51] | 0.87 [0.66] |
| 2.0 | 0.66 [0.44] | 0.83 [0.52] | 1.11 [0.69] |

**Years needed to tell two strategies apart at t = 2** [computed]: T ≈ 8(1−ρ)/d².

| Sharpe difference d | ρ = 0 | ρ = 0.5 | ρ = 0.8 |
|---|---|---|---|
| 0.2 | 200 y | 100 y | 40 y |
| 0.5 | 32 y | 16 y | 6.4 y |

Choosing between plausible strategies by backtest Sharpe is almost always choosing on noise. Default to equal risk, and allow Sharpe tilts only after shrinkage, capped at 0.5x-1.5x.

### 4.4 Walk-forward and robustness design
- **Walk-forward is one path.** It tests a single historical path and is easy to overfit by iterating on it (López de Prado 2018) [Moderate | K-PM].
- **CPCV.** Split the data into N groups and use k of them as test groups, with purging and embargo. That gives φ = (k/N)·C(N,k) backtest paths: N = 6, k = 2 → 15 splits, 5 paths [computed].
- **CPCV vs walk-forward.** In synthetic markets with a known truth, CPCV showed lower PBO and better-calibrated DSR than walk-forward or k-fold, and walk-forward had more false discoveries (Arian, Norouzi & Seco 2024) [Moderate | K-PR, SC].
- **Re-optimization frequency.** No rigorous study sets it, or settles anchored vs rolling windows [gap]. Practice: re-estimate on a fixed calendar (quarterly or annually) with ensembles. Mechanics are in `quant-research-validation.md` §7.
- **Deployment gate for a variant set** [inference; thresholds Lore]. Every condition must hold:
  1. an economic rationale, with a named payer;
  2. DSR ≥ 0.95 at an honest N;
  3. PBO ≤ 0.2;
  4. a positive Sharpe in at least about 2/3 of CPCV paths;
  5. neighbors within ±20-30% of each parameter keep at least 50% of the peak Sharpe (a plateau, not a spike).

  Then deploy the equal-weight ensemble of all passing variants, not the best one.

### 4.5 Reading `scanner.py select` output
**How it runs.**
- **Windows.** For each instrument, after a 260-bar warm-up, it rolls a `--train` window (default 3 years) and a `--test` window (default 1 year) forward, one test window at a time.
- **Execution.** Fills at the next close (`--delay 1`), `--cost-bps 5` per unit of turnover, long/flat unless `--short`.
- **Grids** (techkit defaults): sma 20/50/100/150/200/250; cross fast 10/20/50 × slow 100/150/200; tsmom 21/63/126/189/252; donchian 20/40/55/80/100; rsi2 thresholds 5-25 in steps of 5; bbrev 10/20/30/50.

| Column | What it is | How to read it |
|---|---|---|
| IS best SR | Best full-period Sharpe in the grid (hindsight) | What a "best backtest" would advertise |
| WF pick SR | OOS Sharpe from trading each window's training winner | What "pick the best" really delivers |
| WF ens SR | OOS Sharpe of the equal-weight average of every grid member | What parameter averaging delivers; the verdicts use this |
| ens CAGR / maxDD | Ensemble OOS growth and drawdown | Compare with the buy&hold row, measured over the same OOS span |
| stability | Share of windows that chose the most common parameter | Below about 50%, the "optimal" parameter is noise [inference] |
| usual pick | The most common parameter | Do not deploy it alone; deploy the ensemble |
| optimism gap | Mean of (IS best − WF pick) across rules | The measured cost of picking the best; with few windows it can be negative by luck |

Family verdicts use medians across instruments. PSR is measured against 0; DSR is deflated for the number of families compared on each instrument.

| Verdict | Conditions in the code | Meaning |
|---|---|---|
| ELIGIBLE: timing edge vs B&H | median ens SR > 0; median (SR − B&H SR) > 0; beats B&H on ≥ 60% of instruments; median PSR ≥ 90%; median DSR ≥ 60% | Adds Sharpe over holding the instrument |
| RISK OVERLAY | median ens SR > 0; median PSR ≥ 80%; median drawdown cut ≥ 30%; median (SR − B&H) > −0.15 | Similar Sharpe with much smaller drawdowns. Run it as risk management, not as alpha |
| drop | anything else | Does not earn its risk here |

**Allocation.** Survivors get inverse-vol weights: the eligible families, or the overlay families if none is eligible. Each runs as an ensemble of its parameters. If nothing survives, the script prints "the honest answer is buy & hold, cash, or a different market/strategy menu". Relay that answer. Do not go hunting for another menu without logging the search as trials.

**Caveats Claude must state:**
- **History length.** The default `--years 6` (about 1,510 bars) leaves a single OOS window, so stability prints 100% and means nothing [computed this session]. Use `--years 15-20` where the data exists; 15 years gives about 10 windows.
- **A median DSR ≥ 60% is a screening bar, not approval to deploy.** Its footer says DSR "deflates for the [k] families compared on each instrument, not for screens run before this one". Before calling a family deployable, run `tradekit.py sharpe --trials N` with the ledger's N and require at least 95%.
- **Long/flat vs buy & hold.** In rising equity markets, long/flat trend rules usually trail B&H on Sharpe but cut drawdowns, so "risk overlay" is the expected honest verdict there. Use `--short` for futures and FX, where both sides are the strategy.
- **Universe survivorship.** The built-in `megacap` and `sectors` lists are today's names, so a tournament on them inherits survivorship. Prefer broad, long-lived instruments (`etf-core`, `futures`) for family verdicts.
- **Costs and calendar.** 5 bps suits liquid ETFs and futures. Raise it for small caps, EM and crypto. Crypto trades 365 days a year, so pass `--ppy 365`.
- **Calibration** [computed this session]. On synthetic random-walk-with-drift data (3 series, 6 and 15 years), every family came back "drop". Optimism gaps were +0.30 to +0.67 Sharpe on most series, and −0.51 on one 6-year series whose single OOS window happened to favor the rules. The gap appears even when there is no edge, and one window can flip its sign.
- **The printed demotion rule** ("demote a family whose live Sharpe falls >1 SE below its walk-forward Sharpe") is loose early on. The SE of an annualized Sharpe is about 1/√years (1.0 after 1 year, 0.5 after 4; `tradekit.py sharpe`), so only large shortfalls trigger it in the first years. Pair it with the §5.4 alarms.

### 4.6 Meta-labeling and bandits (weak evidence)
**Meta-labeling** (López de Prado 2018 ch. 3; Joubert 2022 and follow-ups) [Weak | K-PM / K-PR, SC].
- **How it works.** A secondary classifier, trained on the triple-barrier outcomes of a primary signal, outputs P(primary is right). That probability filters and sizes trades, raising precision at the cost of recall.
- **Evidence.** Mostly synthetic. Hudson & Thames ES futures test, OOS 2018-19 [Weak | V-PM]: mean reversion accuracy 17% → 63% but precision only 0.17 → 0.20; trend accuracy 48% → 55%, precision 0.48 → 0.54. One instrument, a short period, manual tuning, imbalanced classes.
- **How to use it** [inference]. Only on a primary signal that passes validation on its own. Train with purged CV on the primary's own events. Judge it on net Sharpe and drawdown across CPCV paths, not on classifier accuracy. Skip it with fewer than a few hundred labeled events per regime.

**Bandits and online allocation** [Weak | V-WP]. The evidence is arXiv self-reports: Thompson sampling over classic strategies claims superiority with no figures; sliding-window "Bandit Networks" report OOS Sharpe 20% above classical allocators; in a live test on 373 stocks, stock choice mattered more than the weighting rule; an anytime-valid factor referee needed about 500 days to certify factors, and its certified book trailed the ungated one. Switching-bandit regret bounds also need few change points (Garivier & Moulines 2011) [K-PR, SC]. If used at all, use a discounted or sliding-window variant, and only as a bounded tilt on a 1/N or ERC prior.

---

## 5. Capital allocation across strategies

### 5.1 Allocation stack [inference; parameters Lore]
1. **Equal risk contribution across families**, after clustering them by return correlation (HRP, or a cap of 30-35% of total risk per cluster). For example, XS momentum, 52w-high and trend-template longs form one "equity momentum" cluster. HRP: López de Prado 2016 [Moderate | K-PR]. For 1/N vs optimizers see `risk-sizing-execution.md` §4.
2. **× regime multiplier** (§3.3), bounded 0.5x-1.5x.
3. **× evidence multiplier** from the shrunk, deflated SR relative to the family median, bounded 0.5x-1.5x.
4. **× track-record stage:**
   - **Paper / incubation:** no real risk.
   - **Stage 1, 25% of target:** until live PSR(0) ≥ 0.8, or about 6-12 months with costs and slippage within 1.5x the model.
   - **Stage 2, 50%:** until live PSR(0) ≥ 0.9.
   - **Stage 3, 100%:** once live months ≥ MinTRL(SR* = 0) for the *haircut* backtest SR, with no open CUSUM alarm.
5. **Normalize** to the portfolio vol target using stressed correlations (`risk-sizing-execution.md` §4.4).

Supporting evidence:
- **Fundamental law** (Grinold 1989; Clarke, de Silva & Thorley 2002) [Strong | K-PR, SC DOIs]: IR ≈ TC·IC·√BR. Constraints and costs that lower the transfer coefficient cut IR proportionally, which favors high-breadth, low-constraint sleeves.
- **Vol-target each sleeve** (Harvey et al. 2018).
- **MinTRL** [Strong]: a daily SR 1.0 strategy needs about 2.7 years of track record to show SR > 0 at 95%; SR 0.5 needs about 11 years (`tradekit.py sharpe`).

### 5.2 Triple penance: how deep and long a normal drawdown is
Bailey & López de Prado 2015 [Moderate | K-PR, SC: formulas recalled, paper not fetched]. For iid normal returns with mean μ, vol σ and quantile Z_α:

```
t*_α     = (Z_α·σ / (2μ))²          time to reach the α-quantile max drawdown
MaxDD_α  = (Z_α·σ)² / (4μ)
MaxTuW_α = (Z_α·σ / μ)² = 4·t*_α    recovery takes ~3x as long as the fall
```

| True annual SR | t* (years) at 95% | MaxDD₉₅ (× annual vol) | MaxTuW₉₅ (years) |
|---|---|---|---|
| 0.5 | 2.71 | 1.35σ | 10.8 |
| 1.0 | 0.68 | 0.68σ | 2.7 |
| 1.5 | 0.30 | 0.45σ | 1.2 |
| 2.0 | 0.17 | 0.34σ | 0.68 |

[computed, Z = 1.645]

- **Low SR:** a true SR 0.5 sleeve at 10% vol can sit about 13.5% under water for about 11 years with no decay.
- **High SR claims:** an "SR 2" sleeve that breaches about 3.4% drawdown or 8 months under water is evidence against SR 2.
- **Serial correlation:** positive serial correlation lengthens both.

**Caveat** [computed this session]. These are per-episode confidence bands measured from a high-water mark, not the distribution of the worst drawdown over a multi-year run.

| Sharpe, vol, horizon (`tradekit.py drawdown`) | Median max DD | 95th percentile max DD | Triple-penance MaxDD₉₅ |
|---|---|---|---|
| SR 1.0, 10% vol, 5 years | 12.8% | 22.5% | 6.8% |
| SR 0.5, 10% vol, 10 years | 21% | about 35% | 13.5% |

Treat a triple-penance breach as a *review* trigger. Answer "is this drawdown abnormal for a strategy of this age?" with the Monte Carlo horizon distribution (see also Magdon-Ismail & Atiya 2004 [K-PR, SC]).

### 5.3 CUSUM decay alarm
CUSUM goes back to Page 1954; Philips, Yashchin & Stein 2003 applied it to managers' rolling information ratios, setting thresholds by average run length [Moderate | K-PR, SC]. The statistic runs on monthly returns in σ units: S_t = max(0, S_{t−1} + k − z_t), where k is half the "good" monthly mean. The alarm fires when S_t > h.

| Good SR (annual) | h | Median months to false alarm if truly good | Median months to detect SR = 0 |
|---|---|---|---|
| 0.5 | 4 | ~26 | ~16 |
| 0.5 | 6 | ~56 | ~29 |
| 1.0 | 6 | ~85 (7 y) | ~24 (2 y) |
| 1.0 | 8 | ~180 (15 y) | ~34 (2.8 y) |

[computed: Gaussian simulation, 3,000-4,000 paths; re-simulated 12 Nov 2026 and matched within a few months]

- **SR 0.5 sleeves:** CUSUM cannot separate "decayed" from "unlucky" quickly; false alarms arrive within 2-5 years.
- **SR ≥ 1:** with h ≈ 6-8, it detects a dead strategy in about 2-3 years.
- **Calibration:** fat tails and autocorrelation shorten false-alarm times. Calibrate h on the strategy's own bootstrapped backtest returns.

### 5.4 Pre-registered review and kill rules [inference; levels scale with the haircut backtest SR]
**Review.** Any one alarm triggers a review: cut risk 50% and run a post-mortem (is the payer still there, is the trade crowded, has the regime left the backtest's range?). The alarms are:
- drawdown > MaxDD₉₅;
- time under water > MaxTuW₉₅;
- a CUSUM alarm (h = 6, monthly);
- 12-month live SR below the 5th percentile of the backtest's bootstrapped 12-month SR distribution;
- realized costs above 1.5x the model.

**Kill and re-validate.** Two independent alarms (for example CUSUM plus time under water), *or* one alarm plus evidence that the rationale has broken (structural change, capacity exhausted, arbitraged away). Restart only on new out-of-sample evidence, with the strategy frozen.

**Never kill an SR ≤ 0.6 sleeve on drawdown alone.** Value, trend and carry droughts of 3-10 years sit inside their sampling distributions. Use the payer test instead.

**Live/backtest ratio.** A live SR at 40-70% of the backtest is the *expected* outcome:
- McLean & Pontiff 2016 [Strong | K-PR]: −26% out of sample, −58% after publication;
- Ilmanen et al. 2021 [V]: about −30%;
- Falck et al. [V]: worse for recently published, complex, outlier-driven signals.

Below about 25% after MinTRL-scale time is an alarm [Lore].

**Also:**
- Strategy-level stop rules add value only when returns are serially correlated or regimes switch; under a random walk they cost return (Kaminski & Lo 2014) [Moderate | K-PR, SC].
- Pod-shop drawdown rules (about 5% cut / 7.5% out, press-sourced) are in `risk-sizing-execution.md` §6. No primary documentation of how platforms decide capital *increases* was found.

---

## 6. Opportunity scanning

### 6.1 Universe and liquidity defaults [Lore; tune to account size]

| Asset class | Gate |
|---|---|
| US single stocks | Price ≥ $5. Market cap ≥ NYSE 20th percentile (about $1-2bn in 2026 [SC]) unless the strategy is explicitly microcap. 20-day median dollar volume ≥ $20M. Position ≤ 1% of ADV for daily swing trades, ≤ 5% for slower ones. Quoted spread ≤ 10-20 bp. Exclude names with earnings inside the hold unless the strategy is event-based |
| ETFs | AUM ≥ $250M, ADV ≥ $10M. One ETF per exposure: remove near-identical clones before ranking |
| Futures | Front or most liquid contract by open interest. Roll on the volume/OI crossover. Daily notional ≥ $50M |
| FX | G10 plus liquid EM |
| Crypto | Top 20-30 by regulated-venue spot volume, ex-stablecoins. Daily volume ≥ $50M. Check exchange concentration |

Evidence behind the gates:
- **Microcaps** (below the NYSE 20th percentile) are about 60% of stocks but about 3% of market cap, and they drive many anomaly results. Use NYSE breakpoints and test size groups separately (Fama & French 2008) [Strong | K-PR, SC numbers].
- **Delisting bias.** Missing delisting returns bias small-stock and loser returns upward, so backtests need delisted names and their delisting returns (Shumway 1997) [Strong | K-PR]. The $5 filter is standard in momentum work (Jegadeesh & Titman 2001 and replications) [K-PR, SC].

**scanner.py's built-in universes** are current lists, not point-in-time: `etf-core` (23 cross-asset ETFs), `sectors` (15 sector/industry ETFs), `megacap` (25 US megacaps), `futures` (17 Yahoo continuous contracts), `crypto` (9 coins), `fx` (8 pairs). `--bench` must name an instrument that was loaded; otherwise the script falls back to the instrument with the highest $ADV. Fetched files are named after the symbol, with `=` and `/` replaced by `_` and `^` removed (ES=F → `ES_F.csv`).

### 6.2 The ten setups in `scanner.py scan`

| Setup | Definition (as coded) | Entry / stop | Wt | Grade and basis |
|---|---|---|---|---|
| trend_long | Price > SMA200 and 12-1 momentum > 0 | close / −3 ATR(14) | 1.0 | [Moderate] TSMOM (MOP 2012); single-market trend SR about 0.4 |
| xs_momentum | Vol-adjusted 12-1 momentum in the universe's top decile and positive; needs ≥ 10 instruments | close / −3 ATR | 1.0 | [Moderate] Jegadeesh-Titman 1993; crash risk in panic states |
| near_52w_high | Within 5% of the 52-week high, with ≥ 5 of 6 trend-template checks | buy at max(close, 52w high) / −2.5 ATR | 0.8 | [Moderate] George & Hwang 2004 for the ingredient; the template itself is practitioner |
| breakout_55 | Close above the prior 55-bar high; relative volume ≥ 1.2 when volume exists | close / level − 1 ATR | 0.8 | [Moderate] Donchian/Turtle; edge persists in diversified futures, simple rules largely stopped working in developed large-cap equities (`technical-analysis.md` §2) |
| squeeze | Uptrend, with Bollinger bandwidth in the lowest decile of the last 6 months | buy-stop close + 0.5 ATR / close − 2 ATR | 0.4 | [Weak] pattern rule, untested |
| rsi2_pullback | Uptrend with RSI(2) < 10 | close / −2.5 ATR | 0.5 | [Weak] short-term reversal, decayed in liquid US equities |
| trend_short | Price < SMA200, 12-1 momentum < 0, and close below the prior 55-bar low | close / 55-bar low + 1 ATR | 0.8 | [Moderate] TSMOM short side |
| breakdown_55 | Close below the prior 55-bar low; relative volume >= 1.2 when volume exists | close / level + 1 ATR | 0.7 | [Moderate] Donchian short side; same caveats as breakout_55 |
| xs_momentum_short | Vol-adjusted 12-1 momentum in the bottom decile and negative; needs >= 10 instruments | close / +3 ATR | 0.7 | [Moderate] loser leg of Jegadeesh-Titman; it crashes in sharp rebounds (Daniel-Moskowitz 2016) |
| rsi2_rally_short | Downtrend (price < SMA200, 12-1 < 0) with RSI(2) > 90 | close / +2.5 ATR | 0.4 | [Weak] mirror of rsi2_pullback, decayed |

**Put positions (`scan --puts`).** The best bearish candidates (up to `--put-top`, default 5, ranked or not) get two expressions from Yahoo's listed chain near `--put-dte` (35 days): a long put struck nearest the entry, and a bear put spread from that strike to the strike nearest the 2R target. Contracts = floor(risk budget / (premium x 100)), with the budget = risk% x equity x the short regime dial. Premiums are priced at the ask, with the short leg at the bid. A put's maximum loss is its premium; the setup's stop still marks where the idea is wrong. Rows warn when the bid-ask exceeds 10% of the price, open interest is under 100, or one put costs more than the budget.

**Definitions used above:**
- **Uptrend:** price > SMA200 and 12-1 momentum > 0.
- **Trend template** (6 checks): price > SMA200; SMA50 > SMA200; SMA200 rising over 21 bars; price > SMA50; price ≥ 1.3 × the 52-week low; price ≥ 0.75 × the 52-week high.
- **Target:** 2R.
- **Units:** floor(equity × risk% ÷ |entry − stop|), capped at `--max-weight` (default 25%) of equity in notional. A `*` marks a capped row.

**Score and shortlist.** Score = weight × (0.5 + 0.5 × strength) × the regime tilt for that side. Each symbol keeps its best-scoring setup; its other hits are listed under "also" and each adds 0.1 to its rank score. The list is cut at `--top 20`. Strength: |vol-adjusted 12-1|/1.5 capped at 1 (trend long/short); universe percentile (xs_momentum); template checks/6 (52w high); ATRs above the level, capped at 1 (breakout: the most extended breakout scores highest but has the worst entry); 1 − bandwidth rank (squeeze); (10 − RSI2)/10 (pullback); bearish mirrors use the same rules on the other side.

**Know its limits:**
- **Bar-count calendar.** "12-1" means 252 bars, the 52-week high uses 252 bars, and vol is annualized with √252. On crypto (365 bars a year) that is really about 8-month momentum and a 36-week high, and vol is understated by about 17%. Say so, or re-check with `techkit.py indicators FILE --ppy 365`.
- **No contract multipliers.** The units column ignores them. Re-size futures with `tradekit.py size --multiplier` (for example 50 for ES).
- **Regime tilt.** It reorders the list but does not resize anything (§3.3).
- **Clusters** use 60-day correlations, whose standard error is about 0.13, so treat them as coarse.
- **Mixed universes.** Scanning several asset classes at once turns xs_momentum into a cross-asset ranking and breadth into a cross-asset count, and the default benchmark is whichever instrument has the most $ADV (arbitrary for FX, which has no volume). Scan asset classes separately for clean regime reads, and pass `--bench` explicitly.
- The footer frames it correctly: "This is a screen: confirm each candidate (techkit indicators/ruletest, catalysts, liquidity), then plan it."

### 6.3 Families the scanner does not implement: canonical definitions
Build these outside the scanner with the published defaults (not tuned variants), or decline:

| Family | Canonical definition | Status |
|---|---|---|
| Earnings drift (PEAD) | Long high, short low standardized unexpected earnings (Bernard & Thomas 1989). Earnings momentum and price momentum are distinct predictors (Chan, Jegadeesh & Lakonishok 1996) | [Moderate, decayed \| K-PR, SC]. Largely gone in large and mid caps since the mid-2000s, with residual drift in microcaps (Martineau 2022) [SC]. "Gap-and-go" as something distinct from PEAD: [Lore] |
| Short-term reversal | 1-week or 1-month losers minus winners (Jegadeesh 1990; Lehmann 1990). Stronger on residual returns and within industries (Da, Liu & Schaumburg 2014) | [Moderate \| K-PR, SC]. Pays more when VIX is high (Nagel); turnover costs dominate |
| Multi-asset TSMOM | Sign of the trailing 12-month excess return, or an equal 1/3/12-month blend, vol-scaled per market | [Strong \| K-PR]. `techkit.py ruletest --rule tsmom` per market; build the portfolio outside |
| Carry | The return if prices stay unchanged (Koijen, Moskowitz, Pedersen & Vrugt 2018): FX = rate differential; commodities = (F_near − F_far)/F_far × 12/months apart; bonds = yield + roll-down; equity indices = dividend yield − rate | [Strong \| K-PR]. Crashes in recessions and funding squeezes. Commodity term structure: Erb & Harvey 2006; Szymanowska et al. 2014. A momentum × term-structure double sort beats either alone (Fuertes, Miffre & Rallis 2010) [SC] |
| Pairs / cointegration | 12-month formation by minimum sum of squared deviations of normalized prices; trade for 6 months; open at 2σ, close at convergence (Gatev, Goetzmann & Rouwenhorst 2006). Orchestrator default: cointegration p < 0.05 and half-life 5-60 days [Lore] | [Moderate, decayed \| K-PR]. Profits fell after the 1990s but held up better within refined industries (Do & Faff 2010 [SC]). Distance and cointegration perform alike before costs, and all decline after costs (Rad, Low & Faff 2016 [SC]). Use `tradekit.py meanrev` for half-life |
| Value / quality / defensive | Static tilts (`strategy-playbook.md` §5-7) | Not timeable on a scan horizon |

### 6.4 Composite ranking
- **Within a family** [inference]: z-score each signal cross-sectionally within peer groups (industry for stocks, asset class for futures), winsorize at ±3, and average a small lookback ensemble equally (for example momentum 3/6/12-1).
- **Across families, for one integrated book:** signal blending (one composite score, then select) beat portfolio blending in long-only style investing (Fitzgibbons et al. 2017) [Contested | K-PR, SC]. Ghayur, Heaney & Platt 2018 find portfolio blending competitive at low tracking error; Bender & Wang 2016 side with integration. A 50/50 value-momentum mix beats either alone in all 8 asset classes (Asness, Moskowitz & Pedersen 2013) [Strong | K-PR].
- **Otherwise keep per-family lists separate,** so each keeps its own risk budget. scanner.py's single cross-setup score is a triage ordering, not a validated composite.
- **Every signal added to a composite multiplies the effective trials** (Novy-Marx). Use equal weights and few signals; never fit the weights.

### 6.5 Breadth math: how many to act on
- **Fundamental law:** IR ≈ TC·IC·√BR, with single-digit-percent ICs [Strong | K-PR].
- **Idiosyncratic tracking noise** of an equal-weight N-name book ≈ σ_idio/√N [computed, σ_idio = 35%]:

| Names | 5 | 10 | 20 | 30 | 50 |
|---|---|---|---|---|---|
| Tracking noise | 15.7% | 11.1% | 7.8% | 6.4% | 4.9% |

  A screen alpha of 3-6% a year is buried below about 20 names.
- **Skewed wealth creation:** about 4% of US listed stocks created all net wealth over 1926-2016. A concentrated screen mostly holds "average" stocks that trail T-bills (Bessembinder 2018) [Strong | K-PR, SC].
- **Defaults** [inference]:
  - **Cross-sectional stock sleeves:** the top 10-20% of the eligible universe, at least 20-30 names, equal risk.
  - **Swing scans** (breakouts, RSI(2)): concurrent positions = sleeve risk budget ÷ per-trade risk (0.25-0.5% each). Take the best-ranked first, and never lower the threshold.
  - **Futures trend and carry:** every eligible market.

### 6.6 Clusters and total heat
- **How scanner.py clusters.** It works greedily down the ranked list. Each unassigned name seeds a new cluster, and any later name whose 60-day return correlation with that seed exceeds `--cluster-corr` (default 0.7) joins it. The output says: "size each cluster as ONE bet."
- **Cluster cap:** at most 30-35% of total risk per cluster, sized on stressed correlation (ρ → 0.8 among risk assets) [inference].
- **Heat:** total open risk at most about 5-6% of equity across all ideas [Lore]. The defaults `--risk 0.5` and `--top 20` would mean 10% heat if every row were taken, so act on about 10-12 risk units, counting each cluster as one.

### 6.7 Screens are trials: the retail screener record
- **Luck from screening.** With N screens, the best one shows t ≈ 1.6 (N = 10), 1.9 (20) or 2.5 (100) from noise alone [computed].
- **Validate the screen, not its output.** Log every definition you run. Test the screen's historical top-k performance across a point-in-time universe, net of costs, with DSR at N = screens tried. Until it passes, its output is a watchlist.
- **FFTY** (the IBD 50 ETF, a CAN SLIM-style list; launched 9 Apr 2015, 0.80% expense ratio): since-inception average annual return 1.86%, 1-year return −21.28% (stockanalysis.com, checked 12 Nov 2026) [V]. The S&P 500 returned roughly low-teens percent a year over the same span [K, SC: from memory], a shortfall of about 10 points a year. Ingredients with academic support (earnings and price momentum, new highs) do not make a concentrated, high-turnover list robust.
- **Active retail trading:** the most active retail households earned about 11.4% a year after costs vs about 17.9% for the market, 1991-96 (Barber & Odean 2000) [Strong | K-PR, SC numbers].
- **Published paper-portfolio screen records** (AAII-style) have no costs and carry survivorship and look-ahead bias [Lore].

---

## 7. Failure modes and red flags

**Red flags in a user's strategy-selection process.** Check each one; any "yes" changes the advice.
1. "Which strategy is working now?" is answered with the trailing backtest winner. → Show the optimism gap from `select` and use ensembles.
2. Switching families after each drawdown, or chasing last year's best sleeve. → Chasing loses (Dichev; Hsu et al.); factor-momentum tilts stay within ±25%.
3. Binary regime switching, e.g., all-in trend when ADX says "trending" and all-in mean reversion when it says "ranging". → This is [Lore]; use bounded multipliers.
4. A regime model fitted on the full sample, smoothed HMM probabilities, or a penalty chosen on the test period. → Look-ahead. Use filtered values only and count the grid as trials.
5. No trial count: screens, setups, universes, lookbacks and re-optimizations went unrecorded. → Reconstruct N, then deflate.
6. The universe is today's index, today's megacaps, or a watchlist of stocks that went up. → Survivorship bias; use a point-in-time universe with delisted names.
7. Many correlated names counted as diversification. → Cluster them; one bet per cluster.
8. Lowering the threshold to fill slots, or acting on 3-5 names from a cross-sectional screen. → Breadth math (§6.5).
9. Sharpe-weighted or optimizer-weighted allocation built from backtests. → Equal risk, with shrunk and capped tilts.
10. Killing an SR 0.5 sleeve after a 1-2 year drawdown, or having no kill rule at all. → Triple penance, the two-alarm rule and the payer test.
11. Re-optimizing after every bad quarter. → Each re-optimization is a trial; use a fixed calendar and ensembles.
12. Treating live results at 50% of the backtest as failure. → That is the expected haircut.
13. A composite score with fitted weights across many signals. → Novy-Marx; use equal weights and few signals.
14. Meta-labeling or a bandit sold on classifier accuracy or a short sample. → Judge it on net Sharpe and drawdown across CPCV paths.
15. Trading PEAD, RSI(2) or gap-and-go in US large caps as if it were the 1990s. → Decayed.

**Traps when Claude uses the scanner:**
- taking `select` verdicts from the default 6 years of data (a single window);
- treating a median DSR of 60% as deployment-grade;
- quoting futures units without the contract multiplier;
- reading crypto "12-1" as twelve months;
- assuming the regime tilt resized positions;
- re-running `scan` across universes until something looks good, without logging each run;
- presenting a 20-name list when the heat cap allows about 10.

---

## 8. Toolkit hooks

Paths are relative to the skill directory; `-h` on any command shows every flag. Run these instead of doing the arithmetic by hand.

```
# Regime (price-based), then macro confirmation
python scripts/scanner.py regime --universe etf-core sectors --fetch --bench SPY
python scripts/fetch.py macro
python scripts/fetch.py fred BAMLH0A0HYM2 VIXCLS --start 2026-09-01     # funding stress, VIX path

# Which families to run: walk-forward tournament (use long histories)
python scripts/scanner.py select --universe etf-core futures --fetch --years 20 --short
python scripts/scanner.py select --universe crypto --fetch --years 10 --ppy 365 --cost-bps 20
python scripts/scanner.py select A.csv B.csv C.csv --rules tsmom donchian sma --train 3 --test 1

# Opportunity scan (multiply --risk by the regime and stage multipliers yourself)
python scripts/scanner.py scan --universe sectors megacap --fetch --equity 100000 --risk 0.5 \
    --max-weight 0.25 --min-price 5 --min-adv 20e6 --top 20 --cluster-corr 0.7 --out scan.csv
python scripts/scanner.py scan --symbols-file watchlist.txt --fetch --bench SPY   # include SPY in the list

# Confirm a candidate
python scripts/techkit.py indicators scan_data/XLE.csv
python scripts/techkit.py ruletest scan_data/XLE.csv --rule donchian --params 55 --cost-bps 5 --oos 0.3 --extra-trials 7
python scripts/tradekit.py impact --qty 5000 --adv 2000000 --price 40 --daily-vol 0.02 --spread-bps 5 --edge-bps 30
python scripts/eventkit.py study --assets XLE=scan_data/XLE.csv SPY=scan_data/SPY.csv \
    --events-file assets/geopolitical_events.csv --type oil_supply_political --bench SPY

# Size: risk = base x regime x evidence x stage; futures need --multiplier
python scripts/tradekit.py size --equity 100000 --risk 0.25 --entry 95.2 --stop 89.6 --target 106.4
python scripts/tradekit.py size --equity 250000 --risk 0.5 --entry 6050 --atr 60 --atr-mult 3 --multiplier 5
#   MES (x5) -> 1 contract; with --multiplier 50 (ES) one contract risks $9,000 = 3.6% of equity -> 0 units

# Significance at the ledger's N; staging (PSR, MinTRL); drawdown expectations
python scripts/tradekit.py sharpe --sr 0.9 --n 1260 --ppy 252 --skew -0.5 --kurt 5 --trials 30 --var-sr 0.1
python scripts/tradekit.py perf live_returns.csv --ppy 252 --trials 30
python scripts/tradekit.py drawdown --sharpe 0.6 --vol 0.10 --years 5
python scripts/tradekit.py meanrev spread.csv                              # pairs half-life
```

Input notes: kurtosis in `sharpe` is raw (normal = 3; pandas and scipy report excess, so add 3); `--var-sr` is the variance of annualized Sharpes across trials; `--extra-trials` in `ruletest` multiplies that run's grid count. scanner.py output is a screen, not a verdict: say so in those words.

---

## 9. Key sources

- Asness, Chandra, Ilmanen & Israel 2017, "Contrarian Factor Timing is Deceptively Difficult," JPM — https://www.aqr.com/Insights/Research/Journal-Article/Contrarian-Factor-Timing-is-Deceptively-Difficult
- Ilmanen, Israel, Lee, Moskowitz & Thapar 2021, "How Do Factor Premia Vary Over Time? A Century of Evidence," JIM — https://www.aqr.com/Insights/Research/Journal-Article/How-Do-Factor-Premia-Vary-Over-Time-A-Century-of-Evidence
- Haddad, Kozak & Santosh 2020, "Factor Timing," RFS — https://doi.org/10.1093/rfs/hhaa017 [SC]
- Ehsani & Linnainmaa 2022, "Factor Momentum and the Momentum Factor," JF — https://doi.org/10.1111/jofi.13131 [SC]
- Daniel & Moskowitz 2016, "Momentum Crashes," JFE — https://doi.org/10.1016/j.jfineco.2015.12.002
- Nagel 2012, "Evaporating Liquidity," RFS — https://ideas.repec.org/a/oup/rfinst/v25y2012i7p2005-2039.html
- Shu, Yu & Mulvey 2024, "Downside Risk Reduction Using Regime-Switching Signals: A Statistical Jump Model Approach" — https://arxiv.org/html/2402.05272v3
- Goulding, Harvey & Mazzoleni 2023, "Momentum Turning Points," JFE — https://doi.org/10.1016/j.jfineco.2023.05.007 [SC]
- Novy-Marx 2015, "Backtesting Strategies Based on Multiple Signals," NBER WP 21329 — https://www.nber.org/papers/w21329
- Falck, Rej & Thesmar 2021/22, "Why and How Systematic Strategies Decay" — https://arxiv.org/abs/2105.01380
- Timmermann 2006, "Forecast Combinations," Handbook of Economic Forecasting — https://doi.org/10.1016/S1574-0706(05)01004-9 [SC]
- Rapach, Strauss & Zhou 2010, equity-premium combination forecasts, RFS 23(2) — https://ideas.repec.org/a/oup/rfinst/v23y2010i2p821-862.html
- Levine & Pedersen 2016, "Which Trend Is Your Friend?" FAJ — https://doi.org/10.2469/faj.v72.n3.3 [SC]
- Bailey & López de Prado 2015, "Stop-Outs under Serial Correlation and 'The Triple Penance Rule'," J. of Risk — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2201302 [SC]
- Philips, Yashchin & Stein 2003, "Using Statistical Process Control to Monitor Active Managers," JPM — https://doi.org/10.3905/jpm.2003.319923 [SC]
- Koijen, Moskowitz, Pedersen & Vrugt 2018, "Carry," JFE — https://doi.org/10.1016/j.jfineco.2017.11.002
- Grinold 1989, "The Fundamental Law of Active Management," JPM — https://doi.org/10.3905/jpm.1989.409211 [SC]
- Bessembinder 2018, "Do Stocks Outperform Treasury Bills?" JFE — https://doi.org/10.1016/j.jfineco.2018.06.004 [SC]
- FFTY fund data (checked 12 Nov 2026) — https://stockanalysis.com/etf/ffty/
