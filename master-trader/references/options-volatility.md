# Options and Volatility Trading

*Read when: a user asks about option pricing or Greeks, implied vs realized vol, which structure fits a view, selling premium (covered calls, put-writing, condors), earnings/FOMC/CPI trades, VIX futures/ETPs, variance swaps, dispersion, 0DTE, or wants an options position or book stress-tested.*

Evidence tags: `[Strong]` `[Moderate]` `[Weak]` `[Contested]` `[Lore]`. Formulas marked *(identity)* are math, not empirical claims.

## Contents
1. BSM and where it fails · 2. Greeks (incl. vanna, volga, charm) · 3. Gamma-theta and delta-hedged P&L ·
4. Expected move from straddles · 5. Volatility surface · 6. Volatility risk premium ·
7. Variance swaps, VIX futures/ETPs, Volmageddon · 8. Strategy selection matrix · 9. Covered calls and put-writing ·
10. Event vol · 11. Dispersion and correlation · 12. Options-book risk management · 13. 0DTE ·
14. Data sources and metrics · Pre-trade options checklist · Worked examples · Failure modes · Toolkit hooks · Key sources

## Core principles
- **An option is a bet on realized variance against implied variance; direction is a separate delta bet.** A delta-hedged option earns ½ΓS²(σ_realized² − σ_implied²) per unit time. If the user cannot state their realized-vol forecast, they don't yet have an options trade.
- **Theta is the rent you pay for gamma.** With r ≈ 0, Θ ≈ −½ΓS²σ². You cannot be long gamma and collect theta. Any pitch of "income with no downside" is selling gamma, and therefore selling crash risk.
- **Convert every premium into a breakeven move before judging it.** The daily breakeven is σ/√252. The ATM straddle ≈ the expected *absolute* move. One SD ≈ 1.25 × the straddle.
- **Short-dated options are realized-vol (gamma) trades; long-dated options are implied-vol (vega) trades.** Gamma scales with 1/√T and vega with √T. A position can be long gamma and short vega at the same time, and that explains most calendar P&L.
- **The volatility risk premium is real but short-tailed.** SPX implied has beaten subsequent realized by about 3.8 vol points on average, and on about 84% of days, 1996–2026. Episodes of −20 or worse wipe out sellers, so the position size *is* the strategy.
- **Trade the surface, not just the level.** Watch skew, term structure, and how both move when spot moves. Quote skew normalized (vol points vs ATM, a ratio, or a 1-year percentile), never as raw IV differences.
- **IV rank is context, not a signal.** The real trigger is IV versus *forecast* realized vol, plus skew and term-structure richness, plus regime (a backwardated term structure means stress).
- **Run the book on scenario grids, not single Greeks.** Stress spot and vol together, with realistic co-movement. Size to the worst one-day vol shock and to the margin required *under stress*, because margin calls arrive exactly when the VRP turns negative.
- **Popular heuristics often invert the evidence.** Academic data show earnings straddles bought shortly before the event earned positive average returns. Protective puts hedge less efficiently than holding less equity. Covered calls are equity beta plus short vol, not "income".

## 1. BSM and where it fails
BSM is a no-arbitrage replication argument. It maps one number (IV) to a price. It is a quoting convention, not a forecast [Strong] (Black & Scholes 1973; Merton 1973; Hull).

| BSM assumption | Reality | Consequence for the trader |
|---|---|---|
| Constant σ | Vol is stochastic and negatively correlated with equity returns [Strong] | Equity put skew; BSM delta mis-hedges; vanna and volga matter |
| Continuous GBM paths | Jumps, fat tails [Strong] | Short-dated OTM options carry jump premia; gap loss can't be hedged |
| Continuous, free hedging | Hedging is discrete and costly | Hedging error adds noise; costs consume thin edges |
| Price set by replication alone | Demand pressure moves option prices (Gârleanu, Pedersen & Poteshman 2009) [Moderate] | End-user put demand plus capital-constrained dealers make index puts rich |
| Known r and q, free borrow | Borrow costs, dividend uncertainty | The parity-implied forward reveals borrow cost |

The smile exists because the market prices these failures (Gatheral 2006).

**Put-call parity** *(identity)*: `C − P = S·e^(−qT) − K·e^(−rT)`. With discrete dividends: `C − P = S − PV(D) − PV(K)`.
- A cash-secured put ≈ a covered call at the same strike and expiry. PUT and BXM are economic near-substitutes.
- The call and put at the same strike must share one IV, apart from American exercise, hard-to-borrow, and dividend uncertainty. If they don't, check borrow first, not "mispricing".
- Conversions and reversals arbitrage any violation. A gap between the parity-implied forward and the actual forward is how desks infer borrow.

## 2. Greeks (BSM with continuous q)
```
d1 = [ln(S/K) + (r − q + σ²/2)T] / (σ√T)      d2 = d1 − σ√T
Delta  call = e^(−qT)N(d1)      put = −e^(−qT)N(−d1)
Gamma  = e^(−qT)φ(d1) / (Sσ√T)                     peaks ATM, ∝ 1/√T
Vega   = S e^(−qT) φ(d1) √T   (÷100 per vol pt)    ∝ √T
Theta  (call, r=q=0) = −Sφ(d1)σ / (2√T)
Vanna  = ∂Δ/∂σ = ∂Vega/∂S = −e^(−qT)φ(d1)·d2/σ
Volga  = ∂Vega/∂σ = Vega·d1·d2/σ                   > 0 in the wings
Charm  = ∂Δ/∂t  ("delta decay")
ATM shortcuts (Brenner & Subrahmanyam 1988): call ≈ 0.4·S·σ√T; straddle ≈ 0.8·S·σ√T;
  vega per vol pt ≈ 0.004·S·√T  (S=100, T=0.25 → ≈ $0.20)
```

| Greek | What it is | Where it bites |
|---|---|---|
| Vanna | How delta changes with vol, and vega with spot | In a selloff IV rises, so OTM put deltas grow. Short puts get "longer" exactly when you least want it. Dealers re-hedge into the move. |
| Volga | Vega convexity | Positive for OTM wings. Wings carry a convexity premium, and a smile exists even with symmetric vol-of-vol. Short wings means short vol-of-vol. |
| Charm | Delta drift as time passes | Largest in short-dated OTM options. Drives dealer hedging flows into OPEX and 0DTE afternoons. A delta-neutral weekend position isn't neutral on Monday. |

**Scaling** (toolkit `bs`, S=K=100, σ=20%, r=0, values per share; $ gamma column per contract):

| Days | Price | Gamma | Vega/pt | Theta/cal day | $ gamma P&L on a 1% move |
|---|---|---|---|---|---|
| 0.25 | 0.21 | 0.762 | 0.010 | −0.42* | 38.1 |
| 1 | 0.42 | 0.381 | 0.021 | −0.21 | 19.1 |
| 7 | 1.10 | 0.144 | 0.055 | −0.079 | 7.20 |
| 30 | 2.29 | 0.0695 | 0.114 | −0.038 | 3.48 |
| 365 | 7.97 | 0.0198 | 0.397 | −0.011 | 0.99 |

\*An instantaneous rate. The whole 0.21 premium decays in the remaining quarter-day, so for 0DTE use the premium itself as the decay. Gamma at 1 day is √30 ≈ 5.5× the 30-day gamma. Vega at 1 year is about 3.5× the 30-day vega.

**Vanna in action** (toolkit `bs`): take a 30-day 95 put at 24.4% IV, delta −0.208, vanna −0.87 per 1.00 of vol. A +5 vol-point shock with spot unchanged moves delta to about −0.25 (re-run gives −0.245). The spot drop that comes with that shock adds more.

## 3. Gamma-theta and delta-hedged P&L
```
BSM PDE:            Θ + ½σ²S²Γ + (r − q)SΔ − rV = 0
Hedged, r ≈ 0:      Θ ≈ −½ΓS²σ²
Daily $ theta ≈ −½·Γ·S²·σ²/252 (trading-day)  or  /365 (calendar). State the convention.
Instantaneous:      dP&L ≈ ½ΓS²[(dS/S)² − σ_i²dt]
Over the life:      P&L ≈ ∫ ½e^(−rt) Γ_t S_t² (σ_r,t² − σ_i²) dt     (hedged at implied)
Desk attribution:   ΔV ≈ ΔΔS + ½ΓΔS² + ΘΔt + VegaΔσ + VannaΔSΔσ + ½VolgaΔσ² + rho/div/residual
```
- **Path dependence** [Strong]. You earn the variance spread weighted by *dollar gamma along the path*. Realized vol that happens while the option sits far from the strike earns little, so "right on vol" can still lose. Variance swaps remove this (section 7).
- **Choice of hedge vol.** Hedging at implied gives path-dependent P&L. Hedging at the (unknown) realized vol locks in V(σ_r) − V(σ_i) but gives noisier mark-to-market (Ahmad & Wilmott 2005).
- **Separate the P&L sources daily.** "Gamma vs theta" is realized vs implied. "Vega P&L" is the re-marking of implied. A user who lost on a long straddle despite a big move has usually lost on vega (IV crush), not on gamma.

**Rule of 16 / breakeven daily move** *(identity)*: the one-day SD = σ_i/√252, and √252 ≈ 15.87.

| IV | 16 | 20 | 25 | 32 | 48 |
|---|---|---|---|---|---|
| Daily breakeven move | 1.0% | 1.26% | 1.58% | 2.0% | 3.0% |

- The P&L is in *squared* moves, so one 3-SD day pays as much as nine 1-SD days. Long-gamma P&L is lumpy, and short-gamma P&L is a steady bleed until it isn't.
- **Convention check.** `bs` reports theta per *calendar* day, while the breakeven move uses *trading* days. Theta over weekends and holidays has to be earned on trading days. Spread across trading days, theta is calendar theta × 365/252.

**Empirics.** Delta-hedged S&P 500 options lose money on average, consistent with a negative volatility risk premium, and losses are larger when vol is higher [Strong] (Bakshi & Kapadia 2003). Zero-beta ATM S&P straddles lost about 3% per week [Strong] (Coval & Shumway 2001, abstract verified Nov 2026). Gap: there's no good published split of hedged-option P&L into discrete-hedging error vs variance spread, and it varies with hedging frequency.

## 4. Expected move from straddles (corrected)
```
E|S_T − S| ≈ √(2/π)·σ√T·S ≈ 0.798·σ√T·S ≈ ATM straddle price      (driftless normal)
1-SD move   = σ√T·S ≈ 1.25 × straddle
```
| S=100, σ=20%, 30 calendar days | Value |
|---|---|
| ATM straddle (`bs` call 2.45 + put 2.12) | 4.57 = expected absolute move |
| 1 SD / 2 SD (`move`) | ±5.73 / ±11.47 |
| P(finish inside ± straddle), normal | ≈ 57% (computed) |
| P(finish inside ± 1 SD), normal | ≈ 68% |
| Daily breakeven | 1.26% |

- **Correction:** "1 SD ≈ 0.8 × straddle" is inverted. The straddle *is* about 0.8 SD, and **1 SD ≈ 1.25 × straddle**.
- Retail platforms' "expected move" numbers (e.g., 0.85 × straddle) are heuristics, not the normal identity. Ask which convention a quoted number uses, and recompute with `move --straddle`.
- Real returns are fat-tailed, and equity skew prices a heavier left tail, so normal-based probabilities are a first cut only.

## 5. Volatility surface
**Skew by asset**

| Market | Typical shape | Why / status |
|---|---|---|
| Equity indices | Put skew: 25Δ put IV > ATM > 25Δ call IV | Spot-vol correlation plus structural crash-insurance demand [Strong] |
| Gold, some commodities | Can show call skew | GLD 30-day skew was call-rich through 2024–2025 per ORATS, later flipping to puts at a premium per Cboe. The dates on those pages conflict [Weak] |
| Meme, squeeze, takeover names | Call skew ("crash-up" risk) | Practitioner knowledge, no quantitative source [Lore] |

- **SPX skew moves fast.** Per Cboe's weekly notes (as an IV ratio and percentile): the 1M 25Δ skew went from the 14th to the 82nd percentile in the week of 7/20/2026; it "collapsed on upside chasing" in the week of 8/10/2026; and it sat at the 73rd percentile before FOMC in the week of 9/14/2026. Realized skew inverted in May 2026 [Moderate, dated data points].
- **Typical SPX 1M 25Δ put-minus-ATM level:** not confirmed from a reliable series. Third-party snapshots range from about 3 to 9 vol points [Weak]. Source a level from OptionMetrics, ORATS or Cboe DataShop before quoting one.

**Term structure**
- The normal state is contango (back IV > front). In stress the curve inverts. Events show up as kinks or humps [Strong].
- VIX futures were in contango more than 80% of the time and in backwardation less than 20% since 2010 [Moderate] (Cboe, Jul 26 2022, verified Nov 2026). Third-party estimates of 80–85% agree.
- Backwardation flags stress but is *not* a reliable predictor of further equity declines. Markets often recover quickly after it, and some of the best periods follow selloffs [Moderate] (Cboe 2022). Use it as a short-vol risk filter, not a sell-stocks signal.
- **Rough vol:** ATM skew decays roughly as T^(−0.4) (H ≈ 0.1), which is why very short-dated skew is so steep [Moderate] (Gatheral, Jaisson & Rosenbaum 2018).

**Surface dynamics: what happens to IV when spot moves** (Derman 1999 regimes [Moderate, practitioner framework])

| Rule | IV behaviour as spot moves | True delta vs BSM (equity index) | Regime it fits |
|---|---|---|---|
| Sticky strike | Each strike's IV stays fixed | BSM delta is "correct" | Range-bound |
| Sticky delta (moneyness) | IV fixed in K/S; ATM vol unchanged | Call delta > BSM | Trending |
| Sticky local vol / implied tree | ATM vol rises as spot falls, along the skew | Delta < BSM | Jumpy, panicky |

- Local vol moves with spot about twice as fast as implied vol moves with strike (Derman, Kani & Zou 1996, approximation).
- The minimum-variance delta for SPX options is below BSM delta, because vol tends to rise when spot falls [Moderate] (Hull & White 2017). **Rule:** the minimum-variance (MV) delta ≈ BSM delta + vega·∂σ/∂S sits below BSM delta for calls and puts alike, so in index options a BSM hedge over-hedges calls and under-hedges puts (the put's MV delta is more negative). Use a skew-adjusted delta.

**Models (when to name which)**

| Model | Use | Known flaw |
|---|---|---|
| Local vol (Dupire 1994; Derman & Kani 1994) | Fits today's whole surface; consistent vanilla and barrier pricing | Forward smiles flatten, so it misprices forward-starts and cliquets |
| Heston (1993) | ρ < 0 gives skew, ξ gives curvature, κ sets how fast skew flattens with maturity | Fits very short-dated skew poorly |
| SABR (Hagan et al. 2002) | Standard in rates (swaptions), common in FX and commodities; α, β, ρ, ν | Its closed form is an approximation |
| SVI (Gatheral) | w(k) = a + b{ρ(k − m) + √((k − m)² + σ²)}; no-arbitrage conditions in Gatheral & Jacquier 2014 | Parameterization only, no dynamics |

**CBOE SKEW index.** SKEW = 100 − 10·(risk-neutral skewness of 30-day SPX returns). It typically runs about 100–150+. It measures how much tail hedges cost, **not** a crash timer.
- One test found SKEW-implied 2-SD and 3-SD down-move probabilities overstated realized frequencies, with no exploitable pattern in the errors (R-bloggers 2020).
- A vendor reports the relationship shifted across eras (1994–2004, 2005–2013, 2014+).
- No peer-reviewed confirmation of timing value was found [Weak].

## 6. Volatility risk premium (VRP)
| Measure | Value | Grade |
|---|---|---|
| SPX: VIX minus next-30-day realized, 1996–2026 (7,655 days) | Positive 83.7% of days; mean 3.82 pts (the same article also cites 4.52, unreconciled); mean VIX 20.15, median 18.5 (OptionMetrics, Jun 2026) | [Strong] |
| Practitioner rule of thumb | SPX 30-day implied exceeds subsequent realized by about 2–4 pts on average | [Moderate] |
| Negative episodes | About −22 pts (Sep 1998, LTCM); longest in 2008; deeply negative in Feb 2018 and Mar 2020; most negative runs last about 4 trading days | [Strong] |
| Index variance swaps | Variance risk premium (realized − swap rate) strongly negative; not explained by CAPM beta, size, value or momentum (Carr & Wu 2009) | [Strong] |
| Cross-asset short vol, 34 markets, 1995–2013 | Sharpe about 0.6 equities, 0.5 rates, 0.5 FX, 1.5 commodities, 1.0 composite; scaled to 1% vol and before costs (Fallon, Park & Yu 2015) | [Moderate] |
| VRP as a return predictor | Implied-minus-realized variance predicts quarterly equity returns (Bollerslev, Tauchen & Zhou 2009) | [Moderate] |
| 2026 context | VIX averaged about 19 YTD through late June 2026, near its 5-year average (IFR) | dated |

**Why the premium exists**
- Vol rises when wealth falls, so long vol is a hedge and investors pay for it [Strong].
- Jump and crash risk carry a large share of the pricing. Cremers, Halling & Weinbaum (2015) find both aggregate jump risk and volatility risk are negatively priced. Per the abstract (checked Nov 2026), a 2-SD rise in factor loading lowers expected annual stock returns by 3.5–5.1% for jump risk and 2.7–2.9% for volatility risk [Moderate].
- Structural end-user demand (portfolio insurance, structured products, pensions) meets capital-constrained dealers (Gârleanu et al. 2009) [Moderate].
- Index VRP exceeds single-stock VRP because index options also embed a correlation risk premium (Driessen, Maenhout & Vilkov 2009) [Moderate]. This is the basis of dispersion trading.

**When the premium fails**
- In crises: 1998, 2008, Feb 2018, Mar 2020.
- In single stocks it is thin or ambiguous.
- Before scheduled events it can be negative ex post (section 10).

**How a master measures it**
- Use the ex-ante VRP: IV minus a *forecast* of realized vol (HAR-RV, GARCH, or a blend of 10/20/60-day realized). IV minus trailing realized is contaminated by vol clustering.
- Size short vol so that a one-day VIX doubling is survivable (Feb 5 2018: +116%).
- An average edge of 3–4 points sitting beside −20 to −60 point episodes means survival, not the average, determines the outcome.

## 7. Variance swaps, VIX futures/ETPs, Volmageddon
```
Fair variance  K_var ≈ (2/T)·∫ O(K)/K² dK   (OTM puts + calls, plus forward adjustment)
Payoff = N_var·(σ_realized² − K_var);   vega notional = N_var·2K_vol
VIX ≈ √(30-day variance swap rate), computed this way
```
- The 1/K² weighting means equity var swaps are dominated by OTM puts, so the var swap strike sits above ATM vol. "Typically 1–3+ pts in SPX" is a practitioner magnitude, not verified [Lore].
- **Short variance is short convexity.** Losses grow quadratically in a crash (Demeterfi, Derman, Kamal & Zou 1999).
- **VIX futures converge to spot VIX at expiry.** A constant-maturity long (e.g., VXX) sells the cheaper front future and buys the dearer second every day, so it loses in contango even with spot VIX flat.
  - Roll cost of about 5–10% per month in normal contango [Weak, low-authority sources].
  - The basis predicts *futures returns* (roll-down), not changes in spot VIX. Shorting in contango and buying in backwardation was profitable but needed equity hedges [Moderate] (Simon & Campasano 2014).
- **Rules for VIX ETPs:** they are futures-roll products, not spot VIX. Long VXX/UVXY is a short-horizon hedge with structural decay. Short-vol ETPs embed path-dependent rebalancing risk.

**Volmageddon, Feb 5 2018** (BIS Mar 2018) [Strong]
- **Moves:** VIX went 17.31 → 37.32 (+116%), its largest daily rise since 1987. The S&P 500 fell about 4.1% (a 3.8-SD day). Models attribute the spike largely to the risk premium, not to expected vol.
- **Mechanism:**
  - Leveraged and inverse VIX ETPs both had to *buy* VIX futures into 16:00–16:15, and others front-ran them from about 15:30.
  - 115,862 contracts traded in the single minute of 16:08, about a quarter of the market.
  - Dealers hedged by selling E-minis, which fed back into equities.
  - Leveraged and inverse vol-ETP AUM was about $4bn at end-2017.
- **Products:**
  - XIV lost 84% (BIS; other sources say 90–96%) and was terminated under its 80%-loss acceleration clause.
  - SVXY fell about 96%.
  - ProShares cut SVXY to −0.5x and UVXY to 1.5x, effective Feb 27 2018.
- **Lesson:** the feedback loop came from the homogeneity and predictability of rebalancing flows, not their size (CFA FAJ 2021). Before any crowded short-vol trade, ask who is forced to buy vol, and when.

## 8. Strategy selection matrix
**Procedure** (decompose the view, then pick the structure):
1. State direction, magnitude and horizon.
2. Compare the forecast move with the implied move (straddle ≈ 0.8σ√T·S). If forecast RV > IV, buy gamma; if below, sell gamma.
3. Locate IV versus its own history (IVP preferred) **and** versus forecast RV (VRP).
4. Read skew (percentile). Steep put skew: sell puts, buy put spreads. Flat skew: outright downside protection is cheap.
5. Read term structure. Contango with a front event favors calendars and selling the front. Inversion means stress, so be wary of short vol.
6. Prefer defined risk unless the book survives gaps.
7. Size by the worst-case scenario, not by margin (section 12).

| Direction | Vol / time view | Preferred structures | Conditions that favor it |
|---|---|---|---|
| Strong up | IV cheap vs forecast RV | Long call; call spread if IV mid-range | Low IVP, flat call wing, no event premium |
| Up | IV rich, expect drift | Short put or bull put spread; covered call; cash-secured put | High IVP **and** positive ex-ante VRP; steep put skew (selling rich puts); contango |
| Up, moderate | Neutral vol | Bull call spread; call diagonal; risk reversal (sell 25Δ put / buy 25Δ call) | Steep put skew makes the RR near-zero cost or a credit, and long vanna. The RR has naked downside |
| Strong down | IV cheap | Long put; put spread | Flat skew = cheap outright puts; low IVP |
| Down | Skew steep / IV rich | Bear put spread (skew-efficient: sells the higher-IV strike); bear call spread | Steep put skew. Put ratio spreads sell skew but leave a naked tail |
| Neutral, range | IV rich vs forecast RV, short horizon | Iron condor, iron fly; short strangle only if the book survives a gap | Positive VRP, contango, no event inside expiry; avoid when VIX/VIX3M > 1 |
| Neutral, target price | Pin view into expiry | Butterfly at target | Cheap convexity; low cost of being wrong |
| Big move, direction unknown | Forecast RV > IV, or event under-priced | Long straddle or strangle | Implied event move below the name's historical moves; low IVP |
| Vol up (vega, not gamma) | Expect IV to rise | Long-dated options; long calendars; VIX calls/futures as a short-horizon hedge | Low IV in a contango curve; long VIX positions bleed roll |
| Front IV rich vs back | Short gamma, long vega | Calendar (sell front, buy back same strike); diagonal for a tilt | Event in front month, term kink; hurt by a big move or an inversion |
| Hedge a long stock | Protection | Put spread, collar, or simply holding less equity | Zero-cost collars give up a lot of upside under steep skew; protective puts are costly (section 9) |
| Correlation | Implied corr high (low) vs expected realized | Dispersion (reverse: long index vol / short single names) | COR1M/COR3M percentile, crowding (section 11) |

**Structure Greeks** [Strong, textbook: Natenberg; Sinclair]

| Structure | Δ | Γ | Vega | Θ | Key risk |
|---|---|---|---|---|---|
| Long call / put | ± | + | + | − | Theta and IV crush |
| Vertical | ± | small | small | small | Capped payoff; skew paid or collected |
| Long straddle / strangle | 0 | + | + | − | Realized < implied |
| Short strangle | 0 | − | − | + | Unbounded tail |
| Iron condor / fly | 0 | − | − | + | Max loss on a gap; P(max loss) not small |
| Calendar | ~0 | − | + | + | Big move; term-structure inversion |
| Ratio (1×2) | varies | − beyond short strikes | − wings | + | Naked tail beyond short strikes |
| Covered call / CSP | + | − | − | + | Full downside, capped upside |

**IV rank and percentile.** `IVR = (IV − 52w low)/(52w high − 52w low)×100`. `IVP = % of the last ~252 days with IV below today`.
- IVR is distorted by single spikes, so IVP is more robust. In single stocks use ex-earnings IV.
- "Sell premium when IVR > 50" is a retail-platform rule with no academic validation found [Lore].
- Sinclair (2020) argues the edge is implied versus *forecast* realized vol. Rank alone ignores whether high IV is justified by high expected RV [Moderate, practitioner consensus].
- High IVR in a backwardated regime is when realized vol has often *exceeded* implied.

## 9. Covered calls and put-writing evidence
| Finding | Detail | Grade |
|---|---|---|
| Cboe PUT index vs S&P 500, Jul 1986 – Dec 2015 | 10.1% vs 9.8% per year; vol 10.1% vs 15.3%; Sharpe 0.67 vs 0.47 (Cboe-sponsored Bondarenko study; CXO summary) | [Moderate] |
| PUT, BXM, CLL | About 30% lower vol than the S&P 500 (Cboe-commissioned; Wilshire 2016 covers 1986–2016) | [Moderate] |
| Conflicts and limits | Exchange-commissioned; results depend heavily on start and end dates; lags strong bull markets; no independent post-2020 net-of-cost study found | caveat |
| Covered call decomposed (Israelov & Nielsen 2015) | Long equity + short vol + an uncompensated equity-reversal (delta-timing) exposure. Delta-hedging the short call raises Sharpe and cuts downside beta. Authors were AQR managers (disclosed) | [Moderate] |
| Protective puts (Israelov 2019, "Pathetic Protection") | Reduce drawdowns less efficiently than holding less equity, because of the VRP cost | [Moderate] |

**Coaching rule:** overwriting earns roughly the equity premium plus the VRP, minus capped upside. It has lower vol but *similar crash drawdowns*. It is not "free income" (Israelov's "Devil's Bargain", 2023). Check that income-seekers understand they keep the full left tail.

## 10. Event volatility
```
Total variance:   σ_T²·T = σ_base²·(T − Δe) + σ_e²·Δe        (Δe = 1 day)
Event variance ≈ σ_T²·T − σ_base²·(T − 1 day);  event 1-SD move = √(event variance)
Two expiries:   event var ≈ σ_post²·T_post − σ_pre²·T_pre − σ_base²·(T_post − T_pre − 1 day)   (σ_base = ex-event vol between the expiries)
Expected |event move| ≈ 0.8 × event SD
```
- **Example** (trading-day convention): base vol 30%, a 10-day expiry over earnings at 60%. Event SD ≈ 10.5%, expected |move| ≈ 8.4%, annualized event-day vol ≈ 167%.
- The toolkit uses *calendar* days: `move --S 100 --days 14 --event-vol 0.60 --base-vol 0.30` returns 10.3%. Pick one convention and keep it.
- **Sanity check:** after removing the event, the ex-earnings term structure should be smooth (Moontower).

**Earnings: does buying the straddle lose? Present this carefully: the evidence runs against the popular heuristic.**
- **Gao, Xing & Zhang (2018, JFQA):** ATM straddles bought 3 days before earnings and held to the announcement returned **+3.34% on average** (highly significant). Returns were higher in small, high-vol, high-kurtosis, illiquid names and in names with volatile past surprises. The authors read this as investors *under*-estimating earnings uncertainty [Moderate].
- **Liquidity and tradability:** the same literature finds straddles held *outside* earnings windows lose (the ordinary VRP). Liquidity is the strongest predictor of the earnings return, and even the most liquid (tightest-spread) quintile earns about 1.14%. The best returns sit in the least liquid names, so the edge may be consumed by spreads or impossible to scale [Moderate].
- Option prices embed a distinct earnings-jump component that the term structure reveals (Dubinsky et al. 2019) [Moderate]. Weekly-option earnings straddles are not fully efficient (FIU) [Weak].
- **Practitioner counter-view:** "IV crush, so always sell earnings." The crush is real, but it is *already priced*. The question is whether the implied move exceeds the realized move. No peer-reviewed source found shows systematic overpricing. Desk results reportedly vary by sector and mega-cap status (vendor) → overall **[Contested]**. There is no large 2020–2026 mega-cap study.
- **How to say it:** "On average the academic data show earnings moves were slightly *under*-priced, mostly in small, illiquid names. For your mega-cap, compare the implied move with its own last 8–12 absolute earnings moves, after spreads."

**Macro events**
- 1-day NDX ATM straddles were overpriced in 10 of the 12 FOMC meetings studied, but one outlier (Dec 2024) could erase a streak of short wins [Weak, single vendor study].
- CPI: one newsletter says CPI-day straddles paid less than FOMC; a vendor says NDX CPI straddles under-price the typical move [Contested].
- Single 2025 observations: an SPX straddle priced about 100 bp for one FOMC and about 55 bp for another, versus about 150 bp for one NFP/CPI [Weak].

**Rules**
- Sell an event only when the implied move is clearly above the name's historical distribution after costs. Buy when it is below, especially in names with fat-tailed reaction histories.
- The pre-event IV ramp (buy a few days before, sell into the event) is a different trade from holding through the jump and the crush.
- For macro events, prefer defined-risk short structures (iron flies) to naked short straddles, because of the streak-then-blow-up pattern.

## 11. Dispersion and correlation trading
```
ρ_impl ≈ (σ_I² − Σ w_i²σ_i²) / (2·Σ_{i<j} w_i w_j σ_i σ_j)     (Cboe implied-correlation methodology)
```
- **Cboe indices:**
  - COR3M launched Jul 2021 (3M ATM SPX IV vs the top 50 names).
  - COR1M/6M/9M/1Y and the delta-skew indices COR10D/30D/70D/90D were added Jul 2022.
  - DSPX measures expected constituent dispersion.
- **Classic dispersion:** short index vol, long constituent vol (straddles or variance, vega- or theta-weighted, deltas hedged) = short implied correlation. A vega-neutral variance dispersion ≈ short correlation plus residual vol-level exposure.
- **P&L drivers:** realized correlation below the implied correlation sold; mispricing of single-stock vs index vol; basket selection (names with idiosyncratic events).
- **Costs:** single-stock option spreads are the main drag.
- **Main risk:** correlation spikes in selloffs. Index vol rises far more than average stock vol, so the short index leg gaps. The loss profile resembles short index puts [Moderate] (Driessen et al. 2009; Bossu 2014).
- **State of play (dated):**
  - S&P implied correlations were near record lows across tenors in Feb 2025.
  - In Aug 2025, commentary noted 1M constituent correlation "extremely low" while the trade kept growing, with crowding warnings.
  - In 2026 dispersion was a "major windfall" (IFR, late Jun 2026). It drew down when correlation surged in the Feb–Mar 2026 war-driven selloff; clients mostly stopped adding and took profits by late June; reverse-dispersion positions were about 5% of original size.
  - COR3M was near all-time lows in late June 2026.
  - DSPX neared a 3-year high and, per a secondary source, hit levels seen only in Covid 2020 and the April 2025 tariff shock.
  - Whether COR1M set a true record is disputed between sources [Weak].
- **Coaching:** explain dispersion as selling the correlation-crash insurance embedded in index options. Crowding plus a low entry correlation means poor risk/reward. Low implied correlation makes index vol cheap relative to single stocks, so reverse dispersion or plain index puts become cheap hedges ("downside hedging is cheap", 2026 commentary).

## 12. Options-book risk management
**Gamma into expiry.** ATM gamma ∝ 1/(Sσ√T), and theta scales the same way. Short ATM options in the last days carry the most P&L variance per dollar of premium. 0DTE puts this on every business day.

**Settlement and assignment**

| Product | Style / settlement | Early assignment | Pin-to-stock risk |
|---|---|---|---|
| SPX, XSP, NDX, RUT | European, cash | None | None. AM-settled SPX monthlies settle on the opening print (SET/SOQ), which can differ materially from the prior close |
| SPY, QQQ, single stocks | American, physical | Yes | Yes. OCC exercise-by-exception auto-exercises options ≥ $0.01 ITM, and holders can submit contrary instructions after the close, so a writer can wake up with unwanted stock over a weekend |

**Early exercise** [Strong, textbook]
- A call on a dividend payer is rationally exercised just before ex-div when the dividend exceeds its remaining time value (≈ the same-strike put value plus interest on the strike). Short ITM calls with little extrinsic value are at high assignment risk the day before ex-div, and the short leg of a spread can leave you short stock and owing the dividend.
- Deep ITM American puts may be exercised early when interest on the strike exceeds their time value.

**Vega buckets.** Vega is not fungible across tenors. Front IV moves more than back IV, roughly ∝ 1/√T by many desks' conventions, so report weighted vega (vega × √(30/T_days)) bucketed by tenor and underlying [Lore, practitioner convention]. A flat-vega calendar is still exposed to term-structure twists.

**Scenario grid procedure**
1. Spot axis: −20% to +10% for indices, wider for single names. Include ±1, ±2 and ±3 SD of the period move.
2. Vol axis: +5, +10 vol points, and doubling. Move vol *with* spot: in equities, spot down means vol up and skew steeper. Templates: Feb 5 2018 (VIX +116%, SPX −4%), Mar 2020, Apr 2025.
3. Time axis: today, +1 day, expiry week (the gamma path).
4. Overlay gap risk (overnight and weekend), ex-div dates on short calls, settlement style, and liquidity: spreads widen in stress.
5. Recompute margin at each stressed point. The binding constraint is margin under stress, not today's margin.

**Margin** (rule text checked Nov 2026; brokers may set higher house requirements)
- **Portfolio margin**, FINRA 4210(g)(2)(F), OCC TIMS: the largest theoretical loss across valuation points of **+6%/−8%** for high-cap broad-based indices, **±10%** for non-high-cap broad-based indices, and **±15%** for individual equities and narrow-based indices. FINRA has flagged firms that don't monitor intraday PM exposure.
- **Strategy-based margin** on a short listed option, FINRA 4210(f)(2)(E): 100% of the option's market value plus **20%** of the underlying (equity) or **15%** (broad index), less the out-of-the-money amount, with a **10%** minimum.
- **Rule:** size short vol so the worst historical one-day vol shock doesn't force liquidation.

## 13. 0DTE
| Fact (dated) | Value | Source |
|---|---|---|
| SPX 0DTE share of SPX volume | Record 66.2% (Jul 2026); about 63% Feb 2026, about 60% Mar 2026 | Cboe; SIFMA |
| Q3 2026 SPX 0DTE ADV | 3.2M of 4.9M SPX ADV (about 65%, computed); Sep record 3.4M | Cboe |
| Oct 2026 | SPX 0DTE ADV record 3.6M; SPX ADV record 5.5M (about 65%, computed); XSP 303K | Cboe, Nov 4 2026 |
| All US options, Q3 2026 | 0DTE 24.2M of 70.6M ADV (about 34%); index 0DTE 56% of index flow | Cboe, Oct 19 2026 |
| Daily SPX expiries | Every business day since mid-May 2022 | CXO |

- **Participants** (Cboe, May 2025) [Moderate, interested party]:
  - Retail is about 50–60% of SPX 0DTE. It fell from 57% to 47% in the early-April 2025 turmoil, then recovered to about 60%.
  - Over 95% of trades are limited-risk, and about 4% are naked shorts.
  - Flow is "extremely balanced". Net market-maker gamma is at most about 0.2% of SPX daily liquidity.
- **Retail P&L** (Beckmeyer, Branger & Gayda 2023):
  - Over Jan 2021 – Feb 2023, retail lost about $70M in aggregate (as quoted). This does not reconcile with the daily rates below, which imply about $134M over the window, so check the paper before quoting a total.
  - Average daily loss rose from about $184K to $358K after daily expiries began.
  - Gross P&L was sometimes positive, but net of fees and spreads it was about zero or negative. Market makers earned the spread [Moderate].
  - The magnitude is debated because retail identification is hard (AEA 2026). A hedge-fund analysis argues 0DTE *selling* was profitable [Weak]. No post-2023 study was found.
- **Pricing:** 0DTE prices track time-varying underlying vol despite a nontrivial risk premium (Chong & Todorov) [Moderate].
- **Effect on index vol [Contested, tilting toward no amplification]:**
  - Adams et al.: S&P vol is about 60 annualized bp lower on 0DTE days; MMs hold positive net gamma; higher MM gamma predicts lower 10-minute vol.
  - Dim, Eraker & Vilkov (2024): no unconditional vol amplification.
  - JPM and BofA later said 0DTE suppresses intraday vol.
  - Against: BoE staff flagged vulnerability (Dec 2024), and a 2026 Princeton thesis links activity to intraday vol, but not via gamma feedback.
  - The primary texts were read only via summaries.
- **Rules:**
  - The edge is tiny relative to costs, so trade liquid strikes with limit orders only.
  - Gamma and charm dominate: an ATM 0DTE option goes from 0.5Δ to 0 or 1 within hours. At a quarter-day left, ATM gamma is about 11× the 30-day gamma (`bs` table above).
  - Defined risk caps the loss, but the probability of a max loss on each trade is real. Size each trade as a 100% loss of max risk.
  - Treat dealer-gamma/GEX forecasts skeptically, given Cboe's 0.2% figure.

## 14. Data sources and metrics
| Source | What | Notes |
|---|---|---|
| OptionMetrics IvyDB (WRDS) | Academic-standard IV history, surfaces | Institutional cost |
| Cboe DataShop / LiveVol | Trades, quotes, ADV statistics | Paid |
| ORATS | IV, skew, earnings-vol research | Paid, with research blog |
| Cboe indices: VIX, VIX9D, VIX1D (launched Apr 2023), VIX3M, VVIX, SKEW, COR1M/COR3M, DSPX | Regime dashboard; Cboe weekly skew notes in percentiles | Free history CSVs (verify current availability) |
| FRED VIXCLS; CME CVOL; Barchart, Market Chameleon; broker chains | Daily VIX; futures-options vol; IVR/IVP; live chains | Free or cheap; verify |

**Standard dashboard**
1. ATM IV and its 1-year IVP (ex-earnings for single stocks).
2. VRP = IV minus a blended RV forecast (10/20/60-day or HAR). Get the realized side from `vol FILE`.
3. Term slope: VIX/VIX3M or 1M/3M IV. Above 1 flags stress.
4. 25Δ skew in vol points and percentile.
5. Implied event move vs historical event moves.
6. For indices: COR1M/COR3M and DSPX.
7. Breakeven daily move σ/√252 and implied period move (straddle).

## Pre-trade options checklist
1. **View decomposed:** direction (Δ), realized vs implied (Γ/Θ), IV change (vega), skew and term (vanna/volga, calendar). Which one is the real bet?
2. **Breakeven stated:** daily σ/√252; period straddle ≈ 0.8σ√T·S; 1 SD = 1.25 × straddle. Is the forecast RV above or below it, and why?
3. **VRP ex-ante:** IV vs a forecast RV, not trailing RV. IVP noted, but not used as the trigger.
4. **Skew percentile and term slope checked;** structure chosen to sell what is rich and buy what is cheap.
5. **Events inside expiry** (earnings, FOMC, CPI, ex-div) identified; event move extracted and compared with history.
6. **Max loss on a gap** (overnight or weekend) computed; defined risk unless the book survives it.
7. **Scenario grid run:** spot ±1/2/3 SD with the skew-consistent vol response; IV +5/+10/doubling; P&L at +1 day and in expiry week.
8. **Settlement and assignment:** European cash vs American physical; short ITM calls vs ex-div; pin risk at short strikes into the close.
9. **Liquidity:** bid-ask as % of premium; total spread cost vs expected edge; limit orders only.
10. **Margin under stress** (PM ±15% single names, +6/−8% high-cap broad indices), not today's figure.
11. **Size** by worst-case loss (`size`). For high-win-rate premium selling, check expectancy and drawdown odds (`expectancy`, `ruin`).
12. **Exit plan:** profit target, loss limit and time stop (e.g., close before the expiry-week gamma ramp), written down before entry.

## Worked examples
**A. Is this straddle worth buying?** `bs --S 100 --K 100 --days 30 --vol 0.20 --r 0.04` for the call and put gives 2.45 + 2.12 = 4.57, with gamma 0.0693 each.
- `move --S 100 --days 30 --vol 0.20` gives 1 SD ±5.73, expected |move| 4.57, and a daily breakeven of 1.26%.
- The straddle's theta is about $7.60 per calendar day per contract pair, or about $11.0 per trading day. Its gamma P&L is about $6.93 × (move %)².
- Breakeven is therefore √(11.0/6.93) ≈ 1.26% per trading day, matching σ/√252. Buy only if you forecast realized vol above 20% *and* expect IV not to fall (vega 0.23 per vol point on the pair).

**B. Reading skew from prices** (hypothetical 30-day chain, S=100):
- `iv --S 100 --K 95 --days 30 --price 0.85 --kind put` → 24.4% (about 21Δ).
- `iv --S 100 --K 100 --days 30 --price 2.30 --kind put` → 21.6%.
- `iv --S 100 --K 105 --days 30 --price 0.55 --kind call` → 18.0%.
- The put is 2.9 vol points over ATM (ratio 1.13), and put minus call is 6.4 points.
- Compare with the name's 1-year skew percentile. If steep, a 100/95 bear put spread sells the rich strike, and a bullish risk reversal is cheap but carries naked downside.

**C. Earnings move.** Back out the event expiry's IV and a neighbouring ex-event expiry's IV with `iv` (from ATM option prices), then run `move --S 100 --days 14 --event-vol 0.60 --base-vol 0.30` → event SD 10.3%, expected |move| ≈ 8.2%.
- `move --S 100 --days 14 --straddle 8.20` confirms 1 SD = 1.25 × straddle = 10.3%.
- If the name's last 8–12 absolute earnings moves average well under 8%, after spreads, selling (defined risk) is supported. If they average above it, the Gao-Xing-Zhang direction applies.

**D. Short-premium plan sanity check.** A user wins 85% of the time, makes 0.2R per win and loses 1R per loss.
- `expectancy --p 0.85 --win 0.2 --loss 1` → +0.02R per trade, breakeven win rate 83.3%, and about 1,837 trades needed for t = 2. The edge is two points of win rate.
- At 5% risk per trade, `ruin --p 0.85 --b 0.2 --risk 5` → about 40% probability of a 30% drawdown within 250 trades.
- Sizing a credit spread with $3.60 max loss per share: `size --equity 100000 --risk 1 --entry 3.60 --stop 0 --multiplier 100` → 2 contracts.

## Failure modes / traps
- **Using "1 SD = 0.8 × straddle"** (inverted) or a platform's 0.85 heuristic as if it were the normal identity.
- **Calling IV rank "edge".** High IVR in backwardation is when realized vol most often beats implied. Ask for the ex-ante VRP.
- **"Theta income" framing.** Theta is gamma rent. Ask the user for their P&L on a 3-SD day and on a VIX doubling.
- **High win rate mistaken for edge.** Short-premium books show 80–90% win rates with negative skew. Check the breakeven win rate (`expectancy`) and the tail.
- **Judging an option P&L on direction alone.** A long straddle that "was right" on the move often lost to the IV crush. Attribute delta, gamma vs theta, and vega separately.
- **Path blindness.** Realized vol far from the strike earns little gamma P&L, so "vol was high" doesn't mean the hedged option made money.
- **Raw skew comparisons** when ATM vol has changed. Normalize first.
- **BSM delta hedging on index options.** MV delta sits below BSM delta, so a BSM hedge over-hedges calls and under-hedges puts. Use a skew-adjusted delta.
- **Treating VIX ETPs as spot VIX.** Roll decay in contango; short-vol ETPs carry path-dependent rebalancing risk (2018).
- **Naked short wings or ratio spreads** sized on margin, not on the gap scenario.
- **Ignoring American-style mechanics:** ex-div assignment on short ITM calls, weekend pin risk, after-hours exercise decisions. Cash-settled European index options avoid these. AM settlement can gap from the prior close.
- **Backtests that mark at mid, ignore spreads, and skip 2008, Feb 2018 and Mar 2020.** For 0DTE and single-stock event trades, spreads *are* the result.
- **"Always sell earnings IV"** stated as fact. The academic average points the other way [Contested]; demand name-specific history.
- **Reading CBOE SKEW or GEX as a timing signal** [Weak].
- **Crowded dispersion at record-low implied correlation:** short-put-like risk with a thin entry premium.

## Toolkit hooks
- `python scripts/tradekit.py bs --S --K --days --vol --r --q --kind` gives price, Δ, Γ, vega/pt, theta per calendar day, rho, vanna (per 1.00 vol), volga (per vol pt), P(ITM), $ gamma per 1% move, and the daily breakeven.
  - Charm: re-run with `--days` reduced by 1 and difference the deltas.
  - Vanna and scenario checks: re-run with `--vol` ±0.05 and `--S` shocked.
  - Scenario grid: loop `bs` over S × vol, moving vol up as spot falls for equities.
- `iv --price --S --K --days --kind` gives implied vol, implied daily move, and the 1-SD move to expiry. Use it for skew, parity checks and event-expiry IV. `--r` defaults to 0.04, so set it.
- `move --S --days --vol` gives 1/2 SD and the expected |move|. `--straddle` gives the implied SD (×1.25) and approximate IV. `--event-vol --base-vol` gives the event-day SD, using the calendar-day convention.
- `vol FILE` gives realized-vol estimators (Yang-Zhang, EWMA, etc.) for the ex-ante VRP.
- `size` (`--multiplier 100`, entry = max loss per share, stop 0) sizes defined-risk spreads by max loss. `expectancy` and `ruin` stress-test high-win-rate premium selling.
- No toolkit command computes IVR/IVP, var-swap strikes or implied correlation. Use the formulas above with vendor data.

## Key sources
- Black & Scholes (1973) JPE; Merton (1973) Bell J. Econ. Hull, *Options, Futures, and Other Derivatives*; Natenberg, *Option Volatility and Pricing* (2015).
- Sinclair, *Volatility Trading* (2013) and *Positional Option Trading* (2020). Gatheral, *The Volatility Surface* (2006).
- Brenner & Subrahmanyam (1988) FAJ 44(5): ATM and straddle approximations.
- Ahmad & Wilmott (2005) Wilmott Magazine: delta-hedging P&L. Carr & Madan (1998): volatility trading.
- Bakshi & Kapadia (2003) RFS 16(2): delta-hedged gains and the negative VRP.
- Coval & Shumway (2001) JF 56(3): expected option returns — https://econpapers.repec.org/RePEc:bla:jfinan:v:56:y:2001:i:3:p:983-1009
- Carr & Wu (2009) RFS 22(3): variance risk premiums — https://econpapers.repec.org/RePEc:oup:rfinst:v:22:y:2009:i:3:p:1311-1341
- Demeterfi, Derman, Kamal & Zou (1999), GS: variance swaps. Derman (1999) Risk: regimes of volatility. Hull & White (2017) JBF: optimal delta.
- Friedman (OptionMetrics, Jun 2026): VRP 1996–2026 — https://optionmetrics.com/blog/how-accurate-is-implied-volatility/
- Driessen, Maenhout & Vilkov (2009) JF 64(3): price of correlation risk. Cremers, Halling & Weinbaum (2015) JF 70(2).
- Fallon, Park & Yu (2015) FAJ 71(5): global volatility premium — https://www.cfainstitute.org/research/financial-analysts-journal/2015/asset-allocation-implications-of-the-global-volatility-premium
- BIS Quarterly Review (Mar 2018): Volmageddon — https://www.bis.org/publ/qtrpdf/r_qt1803t.htm
- Simon & Campasano (2014) J. Derivatives: VIX futures basis. Cboe (Jul 2022): contango/backwardation — https://www.cboe.com/insights/posts/inside-volatility-trading-is-vix-backwardation-necessarily-a-sign-of-a-future-down-market
- Israelov & Nielsen (2015) FAJ 71(6): covered calls uncovered — https://www.aqr.com/Insights/Research/Journal-Article/Covered-Calls-Uncovered. Israelov (2019) JAI: pathetic protection.
- Gao, Xing & Zhang (2018) JFQA 53(6): earnings straddles — https://econpapers.repec.org/RePEc:cup:jfinqa:v:53:y:2018:i:06:p:2587-2617_00
- Beckmeyer, Branger & Gayda (2023) SSRN 4404704: retail 0DTE. Cboe "0DTEs Decoded" (May 2025) — https://www.cboe.com/insights/posts/0-dt-es-decoded-positioning-trends-and-market-impact
- Cboe Q3 2026 options industry state — https://www.cboe.com/insights/posts/state-of-the-options-industry-q-3-2026-volume-growth-concentrated-in-index-and-etf-options
- FINRA Rule 4210 (portfolio margin and option margin) — https://www.finra.org/rules-guidance/rulebooks/finra-rules/4210
