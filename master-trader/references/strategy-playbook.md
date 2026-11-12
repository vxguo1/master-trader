# Systematic Strategy Playbook: Families, Evidence, Failure Regimes

*Read when: a user proposes, backtests or asks about a systematic strategy (trend, momentum, value, carry, quality, low-vol/BAB, size, stat arb/pairs, short-vol, PEAD, merger arb, index or FOMC effects, crypto carry/momentum, LLM or alt-data signals); asks "does X still work?", "what Sharpe should I expect?", "why did my strategy blow up?"; or wants to combine strategies into a portfolio.*

Depth elsewhere: momentum trading mechanics in `momentum-trading.md`; option and volatility structures in `options-volatility.md`; backtest validation, deflated Sharpe and overfitting tests in `quant-research-validation.md`. This file is the map of the families and their evidence.

## Contents
1. Core principles
2. How to evaluate any strategy family (procedure)
3. Trend following / time-series momentum
4. Cross-sectional momentum
5. Value
6. Quality, profitability, investment
7. Low volatility / betting against beta
8. Size
9. Carry
10. Statistical arbitrage, pairs, short-term reversal
11. Volatility risk premium (summary)
12. Event-driven and seasonality
13. Factor decay, crowding and the factor zoo
14. Crypto systematic strategies
15. LLM, NLP and alternative-data signals
16. Strategy family comparison
17. Diversifying across families
18. Failure modes / traps
19. Toolkit hooks
20. Key sources

---

## 1. Core principles

- **Every durable premium has a payer.** Hedgers paying speculators, insurance buyers, leverage-constrained or leverage-hungry investors, impatient traders who need liquidity. If the user cannot name who is on the other side and why they keep paying, assume the backtest is data-mined.
- **Most premia are paid for bearing bad-times risk.** Carry, short volatility, merger arb and liquidity-providing stat arb pay steadily and crash together in recessions and funding squeezes. Trend following is the main exception (it tends to profit in prolonged crises). Skew and crash regime matter more than headline Sharpe.
- **Haircut every published backtest by 30-60%.** Out-of-sample returns are about 26% lower and post-publication returns about 58% lower on average (McLean & Pontiff 2016) [Strong]. Require t > 3 for new signals (Harvey, Liu & Zhu 2016) [Strong].
- **Turnover and costs decide what survives.** Anomalies with monthly turnover above about 50% mostly earn insignificant net spreads. Low-turnover factors (value, profitability, investment) survive (Novy-Marx & Velikov 2016) [Strong].
- **Diversification is part of the strategy, not an add-on.** Trend on a single market averages Sharpe ~0.4; the 50+-market portfolio ~0.77 net [Moderate]. Value and momentum are negatively correlated, and that pairing is the most robust diversification in factor investing [Strong].
- **Crowding causes crashes, not just slow decay.** Correlated deleveraging hit quant equity in August 2007 and momentum in March 2025. Crowded trades unwind together.
- **Decade-long droughts are normal.** US value drew down about 50-59% (by method) from 2007 to 2020. SG Trend fell 20.4% from May 2024 to May 2025. Never judge a factor on 1-3 years of data, and do not expect valuation-spread timing to rescue you.
- **Textbook anomalies in liquid US large caps are mostly arbitraged away.** PEAD, the S&P 500 inclusion effect and the pre-FOMC drift have faded or are contested. Remaining edge sits where arbitrage capital is scarce (microcaps, crypto, less-covered markets), which is also where costs, capacity limits and tail risk are worst.
- **Negative-skew strategies are sized by stress loss, not by volatility.** A Sharpe ratio flatters a short-put payoff until the day it does not.

## 2. How to evaluate any strategy family (procedure)

Run this on any strategy a user brings:

1. **Name the payer.** Is there a risk-transfer, behavioral or liquidity reason someone pays? Is it still there? (Crypto carry: retail leverage demand. Pairs: impatient traders, now competed away by HFT.)
2. **Match construction to the canonical rules** below. Deviations (equal-weighting, all-stock breakpoints, no month skip, lagged prices) usually inflate results.
3. **Locate the evidence grade and its period.** A 1990s Sharpe ratio is an upper bound for today.
4. **Identify the crash regime and the worst historical drawdown.** Ask the user: "What happens to this in 1932, Aug 2007, Mar 2009, Mar 2020, Feb 2018, Aug 2024, Apr 2025?"
5. **Check decay and crowding status** (section 13). Haircut accordingly.
6. **Model costs at realistic turnover**, then capacity (`tradekit.py impact`).
7. **Validate significance** with deflated Sharpe, counting all variants tried (`tradekit.py sharpe`, see `quant-research-validation.md`).
8. **Decide its role in a portfolio** (section 17): return engine, diversifier or crisis hedge.

---

## 3. Trend following / time-series momentum (TSMOM)

*Depth: `momentum-trading.md`.* **Grade: [Strong]** for existence across asset classes and a century of data; **[Moderate]** for future net-of-fee magnitude.

**Rationale (who pays).** Speculators following trends profit at hedgers' expense (Moskowitz, Ooi & Pedersen 2012). Returns persist for 1-12 months and partly reverse over longer horizons. The strategy does best in extreme markets, so it sells "crisis alpha" to the rest of the portfolio.

**Canonical construction**
```
signal_i   = sign(excess return of instrument i over lookback L)
             MOP 2012: L = 12 months, hold 1 month
             HOP century study: equal-weight blend of L = 1, 3, 12 months
weight_i   = signal_i * (sigma_target_i / sigma_i,ex-ante)
             MOP: 40% annualized vol per instrument
portfolio  = scaled to constant vol, 10% annualized (HOP); 10-15% in practice
universe   = 50+ liquid futures/forwards in 4 asset classes (MOP used 58)
rebalance  = monthly in papers; daily/weekly in practice
```
Moving-average crossovers are an equivalent way to build the signal.

**Historical performance**

| Evidence | Period | Result | Grade |
|---|---|---|---|
| MOP 2012, 58 futures/forwards | paper sample | Significant TSMOM in every one of the 58 instruments; little exposure to standard factors | [Strong] |
| Hurst, Ooi & Pedersen, diversified | Jan 1880-Dec 2013 | 14.9%/yr gross; 11.2% net of 2/20; net Sharpe 0.77 | [Moderate] [SECONDARY: figures from a search excerpt of the PDF] |
| HOP JPM 2017, 67 markets | 1880-2016 | Positive every decade; worst decade ~+5.7% net (1910s); did well in 8 of the 10 largest 60/40 drawdowns | [Moderate] |
| Single-market average | 1880-2013 | Net Sharpe ~0.4 per market (not comparable with the 0.77 portfolio figure) | [Moderate] |

**Recent index record (SG Trend Index unless noted; all secondary sources, no primary SG publication fetched)**

| Year | Return | Note |
|---|---|---|
| 2022 | +27.3% | Best year on record; SG CTA +20.2% |
| 2023 | not verified | No reliable full-year figure found |
| 2024 | ~+2.4% to +2.6% | Sources conflict on index and decimal |
| 2025 | ~+2.4% | H1 -10.48% (to 26 Jun); Barclay Systematic Traders +1.66% vs Discretionary +8.72% |
| 2026 YTD | +15.80% (to 30 Sep 2026) | Sep +4.26%; trailing 12m +21.33%; BTOP50 +14.81% YTD. April and May 2026 YTD prints from different sources do not reconcile; treat intra-year figures with caution |

**Failure regimes and worst drawdowns**
- **Fast V-reversals and policy whipsaws.** March 2020, and April 2025 ("Liberation Day" tariffs: SG Trend about -4.9% for the month, -7.3% through 3 April; the figures differ by cut-off date). A breakout followed by a sharp reversal is close to the worst case for a trend system. Diversification did not protect in that broad sell-off (Transtrend). One outlier fund lost 40.67% in April 2025.
- **Trendless chop and rates reversals.** Fixed income and rates were the recurring weak spot in 2024-25.
- **Worst recent drawdown:** -20.4%, May 2024-May 2025, the second-largest since the index began in 2000 (Cambridge Associates). The trailing 12 months to 30 Apr 2025 were -18.7%, reported as the worst in 25 years [SECONDARY].
- March 2026 equity de-risking: diversified CTAs down about 4% for the month (HFR) [SECONDARY].
- Crisis alpha shows up in **slow-burn** crises (2008, 2022 inflation), not in **gap events**.

**Decay / crowding.** AQR's century study examines post-2008 AUM growth and higher cross-market correlations. Cambridge Associates concludes trend is "not structurally broken", but most such commentary comes from managers and allocators with a stake in the answer [Moderate]. The strong 2026 run is consistent with that view but is one year.

**Coaching defaults.** Expect 15-20% peak-to-trough drawdowns and multi-year flat stretches (2023-25 after 2022). Manager dispersion is huge: in mid-May 2025 Aspect Diversified was down more than 14% YTD while AQR Managed Futures outperformed. Speed, sector mix and non-trend sleeves explain most of it. Benchmark properly: SG Trend is pure trend; BTOP50 and SG CTA are broader.

---

## 4. Cross-sectional momentum (stocks, industries)

*Depth: `momentum-trading.md`.* **Grade: [Strong]** for the long-run premium and for crash predictability; **[Contested]** on the rationale.

**Rationale (who pays).** Not settled. Candidates are slow information diffusion and under-reaction (behavioral) and compensation for crash risk. The loser leg behaves like a written call on a market rebound (Daniel & Moskowitz 2016), so part of the premium pays for that option.

**Canonical construction**
```
formation  = cumulative return t-12 to t-2 ("12-1"; skip latest month to avoid 1-month reversal)
sort       = NYSE breakpoints, 30/70 (Fama-French UMD) or top/bottom decile/tercile
weighting  = value-weighted within size groups
rebalance  = monthly
vol-scaled = scale by trailing 6-month realized vol to 12% annualized target (Barroso & Santa-Clara)
residual   = rank on FF3 residuals, 36-month window, 12-1 formation, scaled by residual vol
```

**Historical performance**

| Evidence | Period | Result | Grade |
|---|---|---|---|
| Jegadeesh & Titman 1993, 6/6 strategy | 1965-1989 | ~1% per month | [Strong] |
| Daniel & Moskowitz, US decile WML | 1927:01-2013:03 | 17.9%/yr excess, 30.0% vol (Sharpe ~0.6), CAPM beta -0.58; monthly skew about -4.7 (NBER w20439 Table 1, verified this session; JFE version may differ slightly) | [Strong] |
| Barroso & Santa-Clara 2015, vol-managed | ~1927-2011 | Sharpe "nearly doubles" and crashes "virtually" vanish (abstract, verified); 0.53 to 0.97 per a Swedroe summary [SECONDARY for the decimals] | [Strong] |
| Daniel & Moskowitz dynamic (mean/variance-forecast scaling) | multi-asset | Dynamic momentum across all markets and asset classes: Sharpe 1.18, about four times static US-equity momentum over the same period (verified) | [Moderate] |
| Blitz, Huij & Martens 2011, residual momentum | US | About twice the risk-adjusted return of total-return momentum, less crash risk | [Moderate] |
| Moskowitz & Grinblatt 1999 | US | Industry momentum explains much of stock momentum | [Moderate] |
| Lou, Polk & Skouras 2019 | US | Momentum profits accrue overnight; most other anomalies earn intraday | [Moderate] |

**Failure regimes and worst drawdowns** [Strong]
- **Panic-state rebounds:** after a market decline, with high volatility, when the market snaps back. Losers "crash up".
- **1932:** the two worst WML months ever are consecutive, Jul 1932 -61.0% and Aug 1932 -74.4% (about -90% compounded; commonly cited as -91.6%). The market rose 82%, losers +232%, winners +32%.
- **2009:** March -42.3% and April -45.5% (7th and 4th worst months); Mar-May 2009 about -73%. The market rose 26%, losers +163%, winners +8%.
- **Recent, all low-confidence [SECONDARY]:** March 2025 crash of about 12-13% on forced degrossing, the worst two weeks in over three years. Q4 2025: momentum +0.77% vs value +8.34%; momentum led in 2024, value in 2025. May 2026: the Goldman high-beta momentum basket fell 8%, its biggest unwind in five years. A claimed -36% from a June 2026 peak is **[UNVERIFIED]** and conflicts with reports of momentum leading YTD in July 2026. No primary 2025-26 UMD data were retrieved.

**Decay / crowding.** High comomentum (abnormal return correlation among momentum stocks) signals crowding and predicts lower returns and higher crash risk (Lou & Polk 2022) [Moderate]. SSGA finds momentum rebounds over the 12 months after crashes, though on average not fully [Weak].

**Coaching defaults.** Run 12-1 with a monthly rebalance. Vol-target the strategy, or cut gross exposure in the "bear market, high VIX, sharp rebound" state. Prefer residual or industry-neutral momentum. Always pair with value.

---

## 5. Value

**Grade: [Strong]** for the multi-asset, long-run premium; **[Contested]** for standalone US equity HML since 2007 and for its redundancy given profitability and investment factors.

**Rationale.** Not settled in the evidence here. Value and momentum returns co-move more across asset classes than passive exposures do, consistent with a common global factor partly linked to funding liquidity (Asness, Moskowitz & Pedersen 2013). Value is not just an interest-rate bet (AQR) [Moderate].

**Canonical construction**
- **Equities:** book-to-market using the **current** price, not a 6-month-lagged one (Asness & Frazzini 2013 "HML Devil"). This improves value and changes its correlation with momentum. Composites adding earnings and cash-flow yields are common practice.
- **Fama-French HML:** 2x3 sorts on size (NYSE median) and B/M (NYSE 30th/70th percentiles), value-weighted, rebalanced annually each June.
- **Other asset classes (AMP 2013):** commodities use 5-year reversal (log of average price 4.5-5.5 years ago over today's price); currencies use the 5-year change in the PPP-adjusted real exchange rate; bonds use the 5-year change in 10-year yields.
- **Rebalance:** annually or quarterly. Low turnover means high capacity, and the factor survives costs.

**Historical performance**
- AMP 2013, ~1972-2011: consistent value premia in US, UK, Europe and Japan stocks, country indices, government bonds, currencies and commodities. Value is negatively correlated with momentum within and across asset classes [Strong]. Paper Sharpe decimals were not retrieved; do not quote them from memory.
- Fama & French 2015, US from 1963: HML becomes largely redundant once RMW and CMA are included [Moderate].

**Worst drawdown and recovery**
- The longest and deepest drawdown in HML's history ran from 2007 to 2020 (AQR). Depth depends on method: -50.0% vs growth since 2007 (Research Affiliates); -55% to the Nov 2020 trough (BlackRock); about -51% from Jan 2007; -59% for a univariate sort, Jan 2007-Mar 2020 (Alpha Architect).
- Value rebounded decisively in 2021 and in 2022, but was still about 30% below its prior peak in Nov 2022 (BlackRock).
- 2025 was the top factor year for value (Q4 2025 +8.34%). SimCorp (Dec 2025): if gains held, 2025 would be value's best year since 2001 in its 44-year model. FTSE Russell Q4 2025: value outperformed across regions. US factor performance overall "has disappointed for over a decade" (Evidence Investor). No verified 2026 value return is available.

**Timing.** AQR's value spread was near the 95th percentile in 2022, near tech-bubble levels; no later reading was found. AQR itself calls spread-timing a "sin" (a "venial" one). Historical reliability is weak [Moderate].

**Coaching defaults.** Use current-price B/M or a composite. Pair with profitability/quality and momentum. Hold through decade-long droughts or do not hold it at all.

---

## 6. Quality, profitability, investment

**Grade: [Strong]** for profitability; **[Moderate]** for QMJ; rationale **[Weak]**, since the evidence here does not establish who pays.

- **Profitability:** Novy-Marx 2013 finds gross profits / assets predicts returns about as strongly as B/M and is **negatively correlated with value**, which makes the two attractive to combine.
- **Fama-French 2015:** RMW (robust minus weak operating profitability) and CMA (conservative minus aggressive asset growth) absorb much of HML in the US.
- **Quality Minus Junk** (Asness, Frazzini & Pedersen 2019): long profitable, growing, safe, high-payout firms. Significant risk-adjusted returns in the US and 24 other countries.
- **Costs:** a low-turnover factor that survives costs (Novy-Marx & Velikov 2016).
- **Joint view:** in JKP 2023's tangency portfolio of 13 themes, profitability and investment are among the three themes displaced once all others are controlled for. Read them mainly as hedges of value's junk exposure, not as independent engines [inference].
- **Practical role:** the quality leg keeps a value book from loading up on distressed junk.

---

## 7. Low volatility / betting against beta (BAB)

**Grade: [Contested]**, on implementability rather than existence.

**Rationale (who pays).** Leverage-constrained investors who want more return reach for high-beta assets instead of levering low-beta ones, bidding them up. BAB returns are lower when funding constraints tighten (Frazzini & Pedersen 2014).

**Construction (FP 2014).** Market-neutral: long low-beta assets levered to beta 1, short high-beta assets delevered to beta 1, rank-weighted. FP report significant positive risk-adjusted returns in US equities, 20 international equity markets, Treasuries, credit and futures.

**The dispute**

| Side | Claim |
|---|---|
| Novy-Marx & Velikov 2022 | Rank-weighting plus leverage hedging effectively equal-weights stocks. On average $1.05 per $1 of BAB sits in the bottom 1% of market cap. Transaction costs cut profitability by almost 60%. FP beta estimates are predictably biased. Value-weighted BAB earned 0.56%/month vs 1.08%/month rank-weighted (Jan 1968-Dec 2017), and the residual premium comes through profitability and investment tilts. |
| Alpha Architect (counterpoint) | NMV's trading-cost estimates "might be significantly overstated" or specific to one implementation. |
| JKP 2023 | A dollar-neutral low-beta factor has near-zero raw return but positive alpha, so HXZ's "failure to replicate" on raw returns actually supports BAB theory. |

**Coaching.** If a user's low-vol backtest is rank- or equal-weighted, rerun it value-weighted with realistic costs before believing it. Expect half or less. Plan for funding squeezes, the documented bad state.

---

## 8. Size

**Grade: [Weak]** standalone; **[Contested]** when paired with quality.

- The raw size premium is weak or absent after the early 1980s and outside January.
- It revives once you control for junk (Asness et al. 2018, "Size Matters, If You Control Your Junk").
- In JKP 2023, size is one of only two of 13 themes with a Bayesian replication rate below 50% (the other is low leverage), and it is displaced from the tangency portfolio.
- FTSE Russell, Q4 2025: "(Small) Size lags".
- **Coaching:** do not sell a small-cap tilt as a factor premium. If used, combine it with a quality screen, and test with NYSE breakpoints and value-weighting so microcaps do not drive the result.

---

## 9. Carry

**Grade: [Strong]** for predictive power across asset classes; Sharpe decimals not verified here.

**Rationale (who pays).** Carry pays whoever will bear the risk of a global-recession and funding-crash state. It behaves like a short-volatility premium: steady accrual, joint crashes. Currency carry returns are negatively skewed (Brunnermeier, Nagel & Pedersen 2008, as cited by Daniel & Moskowitz).

**Definition (Koijen, Moskowitz, Pedersen & Vrugt 2018).** Carry is the expected return if the price stays unchanged. For futures, `carry = (Spot - Futures) / Futures`.

| Asset class | Carry signal |
|---|---|
| FX | Interest-rate differential (forward discount) |
| Commodities | Roll yield from futures-curve slope |
| Bonds | Yield minus financing rate, plus roll-down |
| Equity indices | Dividend yield minus risk-free, implied by futures vs spot |

**Evidence.** Carry predicts returns in the cross-section and time series across global equities, global bonds, currencies, commodities, US Treasuries, credit and index options. Cross-asset correlations are low in normal times, **but carry in every asset class performs poorly together during global recessions** [Strong].

**Failure regime.** Global recessions and funding squeezes, which is when diversification across carry sleeves fails. Size carry as a short-volatility book and pair it with trend (section 17).

---

## 10. Statistical arbitrage, pairs, short-term reversal

**Grade: [Strong]** that it worked historically; **[Weak]** for current net edge outside fast, low-cost implementations. No post-2010 peer-reviewed return estimate was retrieved.

**Rationale (who pays).** Impatient traders who demand immediacy pay you to provide liquidity. Competition from other quants and HFT liquidity providers has been eroding the payment.

**Canonical rules**
- **Short-term reversal:** weekly (Lehmann 1990) and monthly (Jegadeesh 1990) losers beat winners the next period. Profits are concentrated in illiquid stocks and are extremely cost-sensitive.
- **Pairs, distance method (Gatev, Goetzmann & Rouwenhorst 2006):** 12-month formation, choose pairs with the minimum sum of squared deviations of normalized prices, trade for 6 months, open at a 2-sigma divergence, close at convergence.
- **Residual stat arb (Avellaneda & Lee 2010):** model residuals from PCA or sector-ETF factor regressions as Ornstein-Uhlenbeck processes and trade on s-scores.
- **Defaults:** factor- or industry-neutral residuals; cointegration or distance selection with periodic re-estimation; enter at z = 1.5-2, exit near the mean; time stop at a multiple of the OU half-life.

**Historical performance and decay**

| Study | Period | Result |
|---|---|---|
| GGR 2006 | 1962-2002 | Up to 11%/yr excess for top pairs, lower in the later sub-period |
| Do & Faff 2010 (FAJ) | extended GGR sample | Profitability declined over time but strengthened in bear and turbulent markets |
| Avellaneda & Lee, PCA, after costs | 1997-2007 | Sharpe 1.44, stronger before 2003; **0.9 over 2003-07** |
| Avellaneda & Lee, ETF | 1997-2007 | Sharpe 1.1, similar degradation since 2002; 1.51 with volume information (2003-07) |

Treat these as strong upper bounds for today.

**Failure regimes**
- **Crowded deleveraging: the August 2007 quant quake.** Khandani & Lo's simulated contrarian strategy (about 8:1 leverage) lost heavily in the week of 6 Aug 2007, then recovered most of it later that week. A secondary summary puts the unleveraged loss at about 12 daily standard deviations [SECONDARY]. Their "unwind hypothesis" (forced liquidation of large portfolios) is, by their own description, speculative. A follow-up finds the stress began in July and lasted to year-end.
- **Structural breaks** (mergers, regime shifts) and **momentum regimes** in which spreads keep widening.

---

## 11. Volatility risk premium (summary)

*Depth, structures and Greeks: `options-volatility.md`.* **Grade: [Strong]** that implied exceeds realized on average; **[Moderate]** for net, implementable returns.

**Rationale (who pays).** Hedgers buy index puts and variance as insurance. Option sellers collect the premium and take the crash risk. Carr & Wu 2009 find large negative variance risk premia on the S&P 500.

| Evidence | Period | Result |
|---|---|---|
| CBOE PUT (Bondarenko) | 1986-2015, gross | 10.1%/yr vs S&P 500 TR 9.8%; vol 10.1% vs 15.3%; Sharpe 0.67 vs 0.47 [SECONDARY] |
| BXM (Callan) | 1988-2006 | 11.77%/yr, slightly above the S&P; monthly Sharpe 0.22 vs 0.16 (old data) |
| BXM (Hewitt EnnisKnupp) | 1986-2012 | S&P-like return at much lower vol |
| BXM-tracking ETPs | | Substantially underperform the index |

Cboe itself notes that Sharpe ratios overstate these strategies because of negative skew. Teach put-writing as **equity beta with a different payoff shape**, not alpha. No 2022-2026 PUT/BXM calendar-year data were verified.

**Crash record**
- **5 Feb 2018 (Volmageddon):** VIX 17.31 to 37.32 (+116%) in one session while the S&P fell 4.1%. Inverse-VIX ETP rebalancing amplified the move, and XIV fell about 96% and was terminated [SECONDARY for the 96%].
- **5 Aug 2024:** VIX pre-market peak about 66, inflated by thin pre-market SPX option liquidity (BIS). Intraday high 65.73, close 38.57. Short-vol funds lost about 10% on the day. Short-vol ETP assets were about $100bn (Mar 2024). From 31 Jul to 5 Aug the inverse VIX futures index fell 28.21% and SVOL fell 10.2%.
- In both episodes the damage came from leverage and path, not from the long-run premium disappearing. The premium was harvested back afterwards.

**Sizing rule.** Size by stress loss (VIX +100% in a day; a 20%+ index gap), never by historical vol. Prefer defined-risk structures. No leverage on VIX futures.

---

## 12. Event-driven and seasonality

| Effect | Original evidence | Current status | Grade |
|---|---|---|---|
| **PEAD** | 60-day post-earnings drift | Gone in all but microcaps, and in microcaps since ~2016; prices absorb news on the announcement day; analyst surprises fail to predict since 2006 (Martineau 2022). Alternative explanation: declining earnings persistence (Zhao 2022) | [Moderate] that it is dead in liquid names |
| **S&P 500 inclusion** | Additions ~+7.4% abnormal (1990s) | Under 1% recently. Deletions: -4.6% (1980s), -16.1% (1990s), -12.4% (2000-09), -0.6% (2010-20), despite growth in indexed assets. Causes: offsetting MidCap migrations, more arbitrage liquidity, better anticipation (Greenwood & Sammon, JF 2025) | [Strong] |
| **Pre-FOMC drift** | 24h before scheduled FOMC = >80% of US equity premium, Sep 1994-Mar 2011 (Lucca & Moench 2015) | Disappeared after 2015, with or without press conferences (Kurov, Wolfe & Gilbert 2021, sample to Dec 2019); still present for press-conference meetings (Ignatieva & Ohashi 2025) | [Contested] |
| **Overnight vs intraday** | US equity premium earned close-to-open, 1993-2006 (Cliff, Cooper & Gulen 2008); momentum overnight, other anomalies intraday (Lou, Polk & Skouras 2019) | No post-2019 decay study retrieved; robust but hard to monetize after costs | [Moderate] |
| **Turn of month** | Last day + first 3 days captured essentially all of the US equity premium, 1926-2005; present in most of 35 other countries (McConnell & Xu 2008) | No post-2008 replication retrieved | [Moderate] historical |
| **Merger arbitrage** | ~4%/yr excess after costs, 4,750 deals, 1963-1998 (Mitchell & Pulvino 2001) | HFRI Merger Arb +8.2% through Sep 2025 (best first three quarters since 2021, few breaks); GMO event-driven +11.1% net 2025 vs HFRX Merger Arb +9.6%; median annualized US spread 7.7% (Goldman, Aug 2025); spread compression from inflows is the 2026 headwind (AllianceBernstein). No 2026 index returns found | [Moderate] |

**Merger arb rationale and risk.** Target holders who want out before the close hand deal-break risk to arbitrageurs. The payoff is short-put-like: uncorrelated with the market in flat or rising markets, correlated in severe declines (Mitchell & Pulvino). Diversify across many deals and size against a break-loss scenario. Breaks cluster in crises and in hostile regulatory regimes.

**Coaching.** Treat calendar and event effects as **execution and rebalancing overlays** (time your rebalance trades; avoid trading into known flows), not as standalone strategies in liquid US large caps. Residual edge requires less-covered markets, microcaps or a faster, better-informed implementation.

---

## 13. Factor decay, crowding and the factor zoo

*Validation methods: `quant-research-validation.md`.*

**Decay (verified this session)**
- **McLean & Pontiff 2016** (97 predictors): returns are **26% lower out-of-sample** (an upper bound on data-mining bias) and **58% lower post-publication**, implying about 32% decay from informed trading. Decay is larger for anomalies with high in-sample returns and those concentrated in liquid stocks [Strong].
- As cited in JKP 2023: Chen & Zimmermann (2020) estimate a bias-corrected post-publication drop of only about 12%, and Jacobs & Müller (2020) find the US is the only country with a reliable post-publication decline [Contested]. JKP find higher in-sample alpha predicts higher out-of-sample alpha, with attenuation somewhat stronger than their Bayesian model predicts.

**The replication debate [Contested]**

| Study | Method | Finding |
|---|---|---|
| Hou, Xue & Zhang 2020 (RFS) | 452 anomalies, NYSE breakpoints, value-weighted, raw returns | 65% fail \|t\| >= 1.96, including 96% of trading-friction anomalies; 82% fail at the multiple-testing hurdle t >= 2.78 (abstract, verified) |
| Jensen, Kelly & Pedersen 2023 (JF) | 153 factors, 93 countries, CAPM alpha, Bayesian multiple-testing correction | Starting from HXZ's 35% replication rate: 61.3% after dropping factors the original papers found insignificant; 82.4% using CAPM alpha; 75.6% under a Benjamini-Yekutieli correction; **82.4%** under their Bayesian model (US and global). Above 50% in 11 of 13 themes; the exceptions are low leverage and size (published version, verified) |
| Harvey, Liu & Zhu 2016 (RFS) | 300+ factors | New factors need t > 3.0 |

**Synthesis.** The disagreement is mostly about microcaps, weighting, raw return vs alpha, and statistical method. Both camps agree that large-cap, value-weighted, after-cost effects are much smaller than headline anomaly returns. Theme-level factors (value, momentum, quality, low-risk) are robust. Single obscure signals are not.

**Costs and capacity**
- Novy-Marx & Velikov 2016: anomalies with monthly turnover above ~50% mostly earn insignificant net spreads; value, profitability and investment survive [Strong].
- Frazzini, Israel & Moskowitz 2018: AQR's live execution data (~$1.7tn of trades, 1998-2016) show costs well below academic estimates, implying more capacity for value, momentum and size than thought [Moderate; the source is a large manager's own data].

**Crowding monitors**
1. Comomentum or pairwise correlation among a factor's stocks (Lou & Polk 2022).
2. Short interest in anomaly short legs, which tracks arbitrage capital. Anomaly returns fell as that capital grew (Hanson & Sunderam 2014).
3. Valuation spreads of long minus short legs.
4. AUM flows into the style.
5. Event evidence: arbitrage capital killed the index effect (Greenwood & Sammon), while scarce capital keeps crypto carry high (section 14).

**Rules of thumb.** Haircut any backtested anomaly by 30-60%. Require t > 3 plus an economic rationale. Test with NYSE breakpoints and value-weighting. Model realistic costs. Expect crowded trades to crash together (2007; March 2025).

---

## 14. Crypto systematic strategies

**Grades:** crypto TSMOM **[Weak]** to **[Moderate]** (in-sample, short histories, no peer-reviewed post-2018 test retrieved); funding/basis carry **[Moderate]** as the most robust crypto-specific premium.

**Time-series and cross-sectional momentum**
- Liu & Tsyvinski (RFS 2021), data to May 2018, in-sample. Strong TSMOM in Bitcoin and Ripple, weaker in Ethereum. For BTC, the top quintile of past-week returns is followed by an average 11.2% next-week return (Sharpe 0.45) vs 2.6% (Sharpe 0.19) for the bottom quintile (per paper). Momentum and investor attention are the strongest crypto-specific predictors, with little exposure to traditional factors.
- Liu, Tsyvinski & Wu (JF 2022): a three-factor model (crypto market, size, momentum) captures the cross-section.
- arXiv 2024 broad-panel study: momentum-spread Sharpe about 0.75-0.87 over a five-year sample [SECONDARY, methodology unverified].
- **Mechanics:** same as futures trend (vol-scaled, multi-lookback). Crypto vol of 60-100%/yr forces much smaller notional. Haircut heavily.

**Carry: futures basis and perpetual funding**
- **Who pays:** trend-chasing small investors who want leveraged upside pay a convenience yield, and scarce arbitrage capital keeps it high (Schmeling, Schrimpf & Todorov, BIS WP 1087, rev. Oct 2025).
- **Size:** futures carry averages above 10%/yr and reaches up to 60%/yr, far above carry in traditional assets. Interest-rate differentials explain little of it.
- **Warning signal:** high carry predicts price crashes and higher crash-insurance prices. Margin spikes and liquidations make cash-and-carry risky.
- **Perpetuals** (He, Manela, Ross & von Wachter, arXiv 2212.06888): longs pay shorts a funding rate proportional to the perp-spot gap. Deviations from no-arbitrage are far larger than in FX. A funding-arbitrage strategy reportedly earned Sharpe ~1.8 at retail costs and ~3.5 for fee-free market makers. Those figures come from earlier versions; the current abstract (v7, Sep 2026) says only "high Sharpe ratios", so treat the decimals as unverified. The trade is **not risk-free**, because a perpetual has no maturity at which to converge.
- **Regime (low confidence):** April 2026 commentary reports BTC perp funding turning sharply negative during a rally [SECONDARY]. Vendor commentary describes basis compression triggering liquidation cascades [SECONDARY]. The Barclay Cryptocurrency Traders Index returned -12.32% in 2025, largely tracking Bitcoin. How post-Jan-2024 spot-ETF arbitrage capital changed carry levels has not been verified.

**Crypto-specific risk checklist**
- Exchange default (FTX 2022)
- Auto-deleveraging and liquidation-engine cascades
- Margin calls on the short-perp leg during spikes
- Premium compression as institutional capital arrives
- 24/7 trading with weekend liquidity gaps
- Funding settled every 1-8 hours depending on venue
- Fragmented venues with different prices

---

## 15. LLM, NLP and alternative-data signals

**Grade: [Moderate]** for short-horizon predictability before costs; **[Weak]** for net, live, durable edge. No systematic evidence on 2024-26 live commercial NLP/alt-data products was found.

| Evidence | Window | Result |
|---|---|---|
| Lopez-Lira & Tang (arXiv 2304.07619 v6, Oct 2025) | Oct 2021-Dec 2023 (post training cutoff) | GPT-4 headline scores: ~90% hit rate on the direction of the initial reaction (portfolio-day level); predict subsequent drift, strongest in small stocks and negative news; ability rises with model size; daily long-short on overnight news **~34 bps/day before costs**; **returns decline as LLM adoption rises** |
| Chen, Kelly & Xiu (WP 2022/23) | | Contextual LLM embeddings beat bag-of-words and dictionaries. A third paper reports the CKX intraday long-short at Sharpe 4.91 (vs 5.51 for its own method) [SECONDARY, pre-cost] |
| Chen, Tang, Zhou & Zhu (arXiv 2502.10008) | | LLM news sentiment correlates with aggregate market returns, but negative news lacks predictive value for the aggregate |
| Ke, Kelly & Xiu (NBER w26186) | | Supervised newswire sentiment predicts returns, concentrated at short horizons and in small, volatile firms |
| Gu, Kelly & Xiu (RFS 2020) | | Trees and neural nets roughly double linear-model Sharpe through nonlinear interactions; gains concentrated in less liquid stocks |
| Jiang, Kelly & Xiu (JF 2023) | | CNNs on price-chart images predict returns |
| Katona et al. (JFQA) | | Satellite parking-lot data carries information (vendors released it on staggered dates); specific numbers not retrieved |

**Rationale.** Faster processing of public information. The payer is slower traders, and the edge shrinks as more traders adopt the tools.

**Validation rules (non-negotiable)**
1. **Look-ahead contamination:** use an LLM whose training cutoff precedes the test window, or anonymize company names and dates (Glasserman & Lin 2023 also document a "distraction effect"). Otherwise assume the results are contaminated.
2. Apply realistic costs. The edge lives in small, illiquid names held for about a day, where costs bite hardest.
3. Expect decay: headline figures (34 bps/day, Sharpe ~5) are pre-cost and falling.
4. Alt-data value peaks before a dataset is widely sold. Durability depends on exclusivity, processing advantage and integration with fundamentals, not on the raw data.

---

## 16. Strategy family comparison

Sharpe figures are paper or index values for the stated period; gross unless marked. "n/q" means not quoted: paper decimals were not verified, so do not invent them. The capacity column is a qualitative judgment from turnover and market liquidity [inference], not a measurement.

| Family | Rationale (who pays) | Typical Sharpe (period) | Skew | Crash regime | Capacity | Status (Nov 2026) |
|---|---|---|---|---|---|---|
| Trend / TSMOM | Hedgers pay speculators; crisis-alpha buyers | 0.77 net, diversified (1880-2013) [SECONDARY]; ~0.4 single market | Positive [inference: does best in extreme markets] | V-reversals, whipsaws, gap events (Mar 2020, Apr 2025) | High (liquid futures), with crowding concern since 2008 | SG Trend +15.8% YTD to Sep 2026 after a -20.4% May 2024-May 2025 drawdown |
| XS momentum | Contested: under-reaction vs crash-risk compensation | ~0.6 static US WML (1927-2013); ~0.97 vol-managed [SECONDARY]; 1.18 dynamic multi-asset | Strongly negative (monthly ~-4.7) | Panic rebounds after bear markets (1932, 2009); degrossing (Mar 2025) | Medium-high (monthly turnover; larger per AQR cost data) | Choppy; Mar 2025 crash; May-Jul 2026 unwind reports [UNVERIFIED] |
| Value | Contested: risk / funding-liquidity factor vs behavioral | n/q | n/q | Growth/tech bubbles; 2007-2020 (-50% to -59%) | High (low turnover) | Top factor in 2025; no verified 2026 data |
| Quality / profitability | Unsettled; hedges value's junk exposure | n/q | n/q | Junk rallies | High | No 2026 data |
| Low-vol / BAB | Leverage-constrained investors overpay for beta | n/q; VW BAB 0.56%/mo vs 1.08% rank-weighted (1968-2017) | n/q | Funding squeezes | Low as published (microcap-heavy); higher value-weighted | Contested implementability |
| Size | Weak; only with a junk control | n/q | n/q | Long droughts | High in large caps, low in microcaps | Lagged in Q4 2025 |
| Carry (multi-asset) | Bearers of recession and funding-crash risk | n/q | Negative | Global recessions, funding squeezes; all sleeves together | High in FX/bond futures | No 2026 data |
| Stat arb / pairs / reversal | Impatient traders pay liquidity providers | 1.44 (1997-2007) falling to 0.9 (2003-07), after costs | Negative under crowding [inference] | Crowded deleveraging (Aug 2007); structural breaks | Low (high turnover, illiquid names) | Heavily decayed; no post-2010 peer-reviewed estimate |
| Short vol / VRP | Hedgers buy insurance | 0.67 PUT vs 0.47 S&P (1986-2015, gross) [SECONDARY] | Strongly negative | Vol spikes (Feb 2018, Aug 2024); leverage and path | Medium; ETP crowding (~$100bn, Mar 2024) | Premium persists; no verified 2022-26 index data |
| Merger arb | Target holders shed break risk | ~4%/yr excess (1963-1998); n/q Sharpe | Negative (short-put-like) | Severe market declines; break clusters; regulation | Medium; inflows compress spreads | Strong 2025; 7.7% median spread (Aug 2025); 2026 compression risk |
| PEAD / index / FOMC | Arbitraged away in liquid US names | Effectively ~0 net in large caps | n/a | n/a | n/a | Dead or contested; overlays only |
| Crypto carry | Leveraged retail longs; scarce arbitrage capital | ~1.8 retail perp funding arb (earlier arXiv versions; unverified) | Negative (liquidation, exchange risk) | Margin spirals, ADL, exchange default | Low-medium; compresses as capital arrives | Funding sharply negative in Apr 2026 [SECONDARY] |
| Crypto TSMOM | Attention and trend-chasing | BTC top-quintile weekly 0.45 (to 2018, in-sample) | n/q | Sharp reversals; 24/7 gaps | Medium (BTC/ETH), low in alts | Barclay crypto traders -12.32% in 2025 |
| LLM news signals | Slower traders of public information | ~34 bps/day pre-cost (2021-23); intraday ~4.9 [SECONDARY] | n/q | Adoption-driven decay; cost blowouts | Low (small caps, 1-day holds) | Decaying as adoption rises |

---

## 17. Diversifying across families

**Pairings with the best support**
1. **Value + momentum** [Strong]. Negatively correlated within and across asset classes (AMP 2013). This is the core multi-asset style portfolio.
2. **Value + profitability/quality** [Strong]. Novy-Marx: negatively correlated, each about as predictive as the other.
3. **Carry + trend** [Moderate, inference]. Carry crashes in global recessions and funding squeezes. Trend tends to profit in prolonged crises and did well in 8 of the 10 worst 60/40 drawdowns.
4. **Trend + equity-heavy books** [Moderate]. Trend is the main positive-skew diversifier for equity beta, but not for gap events.

**Think in two sleeves, not N strategies**
- **Negative-skew sleeve:** carry, short vol, merger arb, liquidity-providing stat arb, crypto basis. In a global recession or funding squeeze these correlate toward 1. Carry crashes in all asset classes together, merger arb turns market-correlated in severe declines, and quant books unwound together in 2007. Size the whole sleeve by a **joint stress loss**, not by summed individual volatilities.
- **Positive-skew sleeve:** trend, plus explicit tail hedges (`options-volatility.md`). It pays in slow-burn crises and loses in V-reversals.
- Cross-asset style returns co-move more than passive exposures (AMP), so value across eight asset classes is less diversified than eight asset classes of beta.

**Allocation procedure**
1. Start with equal risk across families as a neutral prior [Lore]. Tilt only for evidence grade and cost-adjusted, haircut Sharpe.
2. Scale each sleeve to a vol target (10-15% for trend), then cap the negative-skew sleeve by a joint scenario: VIX +100% in a day, a 20% equity gap, a funding squeeze, a 2007-style degrossing.
3. Check correlations in **stress windows** (2008, Mar 2020, 2022, Aug 2024, Apr 2025), not full-sample averages.
4. Monitor crowding (section 13) and cut exposure where comomentum, short-leg short interest or flows are extreme.
5. Do not "diversify" into decayed anomalies (PEAD, index effect) or unverified alt-data. They add cost and false comfort.
6. Rebalance across families on a schedule. Do not cut a sleeve just because it is in a multi-year drought (value 2007-2020, trend 2023-25), since droughts that long are in the historical record. Cut it only if the payer has gone (section 2, step 1).

---

## 18. Failure modes / traps

Catch these in a user's plan or backtest:

- **Quoting 0.77 for single-market trend.** That is the diversified-portfolio figure; per-market Sharpe is about 0.4.
- **Sharpe as the metric for short-vol, carry or merger arb.** Ask for skew, worst day and stress loss. Sharpe flatters short-put payoffs.
- **Momentum without the skip month,** or value with a 6-month-lagged price.
- **Microcap-driven results:** equal-weighting, all-stock breakpoints, rank-weighted BAB. Rerun with NYSE breakpoints and value weights.
- **Ignoring turnover costs:** above about 50% monthly turnover, assume no net edge until proven otherwise.
- **No crash-state control in momentum:** no vol scaling and no de-risking after bear markets with high vol.
- **Backtesting LLM signals with a model trained after the test window,** or with company names left in.
- **Trading PEAD, index inclusion or pre-FOMC drift in US large caps** as if it were the 1990s.
- **Treating crypto basis or funding as risk-free.** Ask where the collateral sits, the ADL policy and the margin buffer for a sharp spike.
- **Leveraged VIX futures, or short-vol sized by historical vol** (XIV, Feb 2018).
- **Abandoning a factor after a 1-3 year drawdown, or timing value on spreads.** Both have weak historical reliability.
- **Trusting stakeholder commentary.** Most "trend isn't broken" or "value is back" research comes from managers selling the strategy. Weigh accordingly.
- **Benchmark mismatch:** judging a pure-trend fund against BTOP50 or SG CTA, or the reverse.
- **Counting only the final variant:** every lookback, universe and filter tried goes into the deflated Sharpe trial count.
- **Assuming crowded trades stay diversified:** in a degrossing (2007, Mar 2025), "uncorrelated" quant books fall together.

---

## 19. Toolkit hooks

Run these instead of doing mental math:

- **Trend rule test (single market):** `python scripts/techkit.py ruletest FILE --rule tsmom --params 21 63 126 252 --short --vol-target 0.15 --cost-bps 5 --oos 0.3`. The rule is the sign of the k-bar price return; the default grid is 21/63/126/189/252 bars. Use futures (excess-return) data. A multi-lookback blend and the cross-market portfolio have to be built outside this command. Add `--extra-trials N` if other rules or markets were tried first.
- **Cross-sectional momentum ranking:** `python scripts/techkit.py rank A.csv B.csv ... --by voladj` (12-1, 6-1, 3m, vol-adjusted, distance from 52-week high).
- **Significance of any family's backtest:** `python scripts/tradekit.py sharpe --sr 0.8 --n 240 --ppy 12 --skew -1.0 --kurt 6 --trials 20 --var-sr 0.05`. DSR needs `--var-sr`, the variance of annualized Sharpes across the trials. Kurtosis is raw (normal = 3); pandas and scipy report excess kurtosis, so add 3. Negative-skew families need the skew and kurtosis inputs, or PSR/DSR will flatter them.
- **Full report from a returns series:** `python scripts/tradekit.py perf returns.csv --ppy 252 --trials 20` (add `--prices` for an equity curve).
- **Expected drawdowns for a family's Sharpe:** `python scripts/tradekit.py drawdown --sharpe 0.6 --vol 0.10 --years 10`. Use it to set expectations. For Sharpe 0.6 at 10% vol over 10 years it gives a median max drawdown of ~20% and a 95th percentile of ~33%, assuming iid normal returns, and real tails are worse.
- **Recovery math:** `python scripts/tradekit.py drawdown --loss 50 20` (percent: value's -50% needs +100%; trend's -20% needs +25%).
- **Pairs and stat-arb spread diagnostics:** `python scripts/tradekit.py meanrev spread.csv` (OU half-life for time stops; Hurst; variance ratios).
- **Capacity and cost per rebalance:** `python scripts/tradekit.py impact --qty 50000 --adv 2000000 --price 40 --daily-vol 0.02 --spread-bps 5 --edge-bps 30`.
- **Vol estimates for inverse-vol sizing:** `python scripts/tradekit.py vol FILE` (EWMA or Yang-Zhang for ex-ante sigma).

---

## 20. Key sources

- Moskowitz, Ooi & Pedersen 2012, "Time Series Momentum," JFE — http://pages.stern.nyu.edu/~lpederse/papers/TimeSeriesMomentum.pdf
- Hurst, Ooi & Pedersen, "A Century of Evidence on Trend-Following Investing" (AQR) — https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing
- Top Traders Unplugged, SG Trend performance report Sep 2026 (pub. 26 Oct 2026) — https://www.toptradersunplugged.com/trend-following-performance-report-september-2026/
- Cambridge Associates on the 2024-25 trend drawdown — https://publishedresearch.cambridgeassociates.com/?p=19140
- Daniel & Moskowitz 2016, "Momentum Crashes," JFE (NBER w20439) — https://www.nber.org/papers/w20439
- Barroso & Santa-Clara 2015, "Momentum Has Its Moments," JFE — https://doi.org/10.1016/j.jfineco.2014.11.010
- Asness, Moskowitz & Pedersen 2013, "Value and Momentum Everywhere," JF — http://pages.stern.nyu.edu/~lpederse/papers/ValMomEverywhere.pdf
- Fama & French 2015, "A Five-Factor Asset Pricing Model," JFE — https://doi.org/10.1016/j.jfineco.2014.10.010
- Koijen, Moskowitz, Pedersen & Vrugt 2018, "Carry," JFE — http://pages.stern.nyu.edu/~lpederse/papers/Carry.pdf
- Frazzini & Pedersen 2014, "Betting Against Beta," JFE — https://doi.org/10.1016/j.jfineco.2013.10.005
- Novy-Marx & Velikov 2022, "Betting Against Betting Against Beta," JFE — https://mysimon.rochester.edu/novy-marx/research/BABAB.pdf
- Avellaneda & Lee 2010, "Statistical Arbitrage in the US Equities Market," QF — https://www.math.nyu.edu/faculty/avellane/AvellanedaLeeStatArb20090616.pdf
- Khandani & Lo 2007, "What Happened to the Quants in August 2007?" — https://web.mit.edu/~alo/www/Papers/august07.html
- Greenwood & Sammon 2025, "The Disappearing Index Effect," JF — https://www.nber.org/system/files/working_papers/w30748/w30748.pdf
- Martineau 2022, "Rest in Peace Post-Earnings Announcement Drift," CFR — https://cfr.ivo-welch.info/published/papers/martineau2021rest.pdf
- McLean & Pontiff 2016, "Does Academic Research Destroy Stock Return Predictability?" JF — https://doi.org/10.1111/jofi.12365
- Hou, Xue & Zhang 2020, "Replicating Anomalies," RFS — https://doi.org/10.1093/rfs/hhy131
- Jensen, Kelly & Pedersen 2023, "Is There a Replication Crisis in Finance?" JF — https://doi.org/10.1111/jofi.13249
- Schmeling, Schrimpf & Todorov, "Crypto Carry," BIS WP 1087 — https://www.bis.org/publ/work1087.htm
- Lopez-Lira & Tang, "Can ChatGPT Forecast Stock Price Movements?" arXiv v6 — https://arxiv.org/abs/2304.07619v6
