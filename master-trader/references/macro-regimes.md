# Macro Regimes and Cross-Asset Frameworks

*Read when: a user asks "what regime are we in", wants a macro or cross-asset view, is trading around FOMC/CPI/NFP, asks whether bonds still hedge stocks, is building or reviewing a 60/40, risk-parity, sector-rotation, curve, dollar, carry, credit, oil, gold or valuation-timing idea, or is citing net liquidity, the yield curve, the LEI or CAPE as a signal.*

**Contents:** Core principles · 1 Growth/inflation quadrants · 2 Regime diagnosis procedure · 3 Regime playbook · 4 Monetary policy transmission · 5 Liquidity and FCIs · 6 Yield curve · 7 Stock–bond correlation · 8 Dollar and carry · 9 Credit and defaults · 10 Commodities · 11 Macro event trading · 12 Valuation · 13 Sector rotation and leading indicators · 14 2026 regime read · 15 Data checklist · Failure modes · Toolkit hooks · Key sources

---

## Core principles

- **The direction of change defines the regime, not the level.** The Investment Clock dates phases by the *direction* of the output gap and of CPI. Neville et al. define inflation regimes by inflation *rising* through 2% toward 5%+. AQR stresses inflation *news* over inflation already priced. A 3% CPI that is falling is a different regime from a 3% CPI that is rising.
- **Only surprises against pricing move prices.** An unexpected 25bp Fed cut moves equities about 1%. An expected one does very little (Bernanke & Kuttner). Every event read starts with "what was priced?" [Strong]
- **The stock–bond correlation is the most important portfolio fact of a regime.** Its sign depends on inflation uncertainty relative to growth uncertainty. It decides whether bonds hedge equities or add to their risk, which is what broke 60/40 and risk parity in 2022. [Moderate]
- **Macro samples are tiny.** There were 8 US inflation regimes since 1926, about 5 Clock cycles in 1973–2004, and a handful of recessions. Treat regime tilts as conditional priors with wide error bars. Confirm with price (trend), and size modestly.
- **Leading indicators signal how restrictive policy is, not when a recession starts.** In 2022–24 the curve, the LEI, the Sahm rule and ISM all flashed recession, and none came by Oct 2026. Lead times of 6–24 months make even correct signals useless for equity timing. Require coincident confirmation.
- **Valuation sets long-run expected returns, not entry timing.** CAPE explains roughly 40% of 10-year return variation and close to nothing at 1 year. [Strong for the 1-year null result]
- **Macro relationships come and go, so re-test before relying on one.** Gold vs real yields (since 2022), dollar vs commodities (2026), net liquidity vs equities (2023) and the curve vs recessions (2022–24) all broke recently.
- **Leverage and positioning set how big the move is.** In August 2024 one weak payroll print plus the yen carry unwind sent the Nikkei −12.4% in a day. Check crowding and implied vol, not just the macro sign.
- **Use only real-time data.** Output gaps and GDP get revised heavily. Ex-post regime dating flatters every backtest, so nowcasts (ISM, claims, CPI momentum, breakevens) are what you can trade on.

---

## 1. Growth/inflation quadrants

### Merrill Lynch Investment Clock (Greetham & Hartnett 2004)

The four phases are defined by the direction of the OECD US output gap and the direction of headline CPI y/y. The sample is 375 months (Apr 1973–Jul 2004). Each phase lasted about 20 months, so a full cycle took about 6 years. An ANOVA rejects equal returns across phases at 99.9% confidence. [Moderate: published sell-side backtest with ex-post dating, revised output gaps and no costs]

**US real total returns by phase, % p.a., geometric (Table 4):**

| Phase | Growth | Inflation | Bonds | Stocks | Commodities (GSCI TR) | Cash | Winner |
|---|---|---|---|---|---|---|---|
| I Reflation | ↓ | ↓ | **9.8** | 6.4 | −11.9 | 3.3 | Bonds |
| II Recovery | ↑ | ↓ | 7.0 | **19.9** | −7.9 | 2.1 | Stocks |
| III Overheat | ↑ | ↑ | 0.2 | 6.0 | **19.7** | 1.2 | Commodities |
| IV Stagflation | ↓ | ↑ | −1.9 | −11.7 | 28.6* | **−0.3** | Cash |
| Long-run avg | | | 3.5 | 6.1 | 5.8 | 1.5 | |

*The Stagflation commodity return is driven by the two 1970s oil shocks. Non-oil commodities fell in that phase.

**Sectors and the curve by phase (Tables 1, 6 and 8).** Sector figures are returns relative to the market, % p.a. Curve figures are annualised bp changes in Fed funds / 3m / 2y / 10y+.

| Phase | Style | Best sectors | Worst sectors | Curve shift |
|---|---|---|---|---|
| Reflation | Defensive growth | Staples +13.3, Financials +11.0, Cons. Disc. +8.9 | Oil & Gas −12.8, Telecoms −10.2 | −324/−225/−141/−43: **bull steepening** (the only shift significant at 95%) |
| Recovery | Cyclical growth | Cons. Disc. +3.8, Telecoms +3.7, Tech +3.3 | Pharma −4.5, Oil & Gas −4.4 | −60/−56/−44/−45: mild bull steepening |
| Overheat | Cyclical value | Tech +4.7, Industrials +4.3, Oil & Gas +4.2 | Cons. Disc. −5.8 | +122/+102/+107/+54: **bear flattening** |
| Stagflation | Defensive value | Oil & Gas +14.7, Pharma +11.6, Utilities +6.4 | Tech −12.5, Cons. Disc. −8.9 | +86/+51/−13/+20: bear flattening |

- Only 5 of 10 sectors are significantly explained by phase. Consumer Discretionary and Oil & Gas are the most macro-driven. Telecoms, Utilities and Materials are poorly explained. [Weak at the sector level]
- Suggested pairs: Cons. Disc. vs Energy (inflation axis), Financials vs Industrials, Telecoms vs Utilities.
- The framework is still in use. Greetham carried it to Fidelity and then Royal London AM, which still publishes Clock analysis in 2026 (RLAM 2026).

### Bridgewater All Weather / risk parity
- It balances *risk* across the four growth/inflation "seasons" rather than balancing capital, using leverage on low-volatility bonds (Bridgewater, background).
- The popular 10%-vol version **lost 22% in 2022** (InvestmentNews, snippet). Risk parity lagged global 60/40 every year from 2019 into 2024, and investors withdrew billions (Fortune, Apr 2024, snippet).
- Lesson: the design assumes bonds diversify equities. A positive stock–bond correlation turns levered bonds into levered equity-like risk (§7).

### Inflation regimes: Neville, Draaisma, Funnell, Harvey & Van Hemert (2021)
The regime definition is US y/y inflation rising materially above 2%, to 5% or more. There are 8 US regimes since 1926; the paper also studies UK and Japan. [Moderate: peer-reviewed, but n = 8]

| Real annualised return in US inflation regimes | Value (normal times) |
|---|---|
| US equities | **−7%** |
| 10y Treasuries | **−5%** (longer maturities worse) |
| 60/40 | **−6%** |
| Commodities | **+14%** (+1%) |
| All-asset trend-following | **+25%** |
| US housing | −2% (+2%) |
| Size (SMB) | −4% (+1%) |
| Cross-sectional momentum | +8% (not significant) |
| Value, profitability | roughly held their own |
| Art / wine / stamps | +7% / +5% / +9% |

- Equities and bonds were both profitable in only 2 of the 8 regimes (AIMA, snippet).
- Not extracted from the source: figures for gold, TIPS, commodity sub-sectors and equity sectors, and the regime dates. Do not quote numbers for these.

### AQR, "Inflation Redux?" (Q3 2026; sample 1972–Jun 2026) [Moderate]
- Broad equities and most sectors sit in the "good growth news / bad inflation news" quadrant, so most portfolios carry an implicit bet on growth and low inflation.
- **Core inflation surprises hurt equities, bonds, credit and illiquids more than food and energy surprises do.** Breakevens gave the most potent protection against core shocks. Diversified commodities and trend also helped.
- In 2022 (Jan–Sep), commodities, trend and long/short value did best. **Gold, TIPS and breakevens disappointed**, because real yields soared while long-run expectations stayed anchored.
- Trend outperformed in both inflationary and disinflationary bear markets: 2022, the GFC, 2000–02, 1990 and 2020. [Moderate, consistent with Neville et al.]
- Popular commodity indices are energy-dominated, the GSCI more so than BCOM. A sector-balanced basket has similar inflation sensitivity. A risk-balanced active commodity backtest returned 11.9% vs 3.6% for BCOM (Sharpe 0.57 vs 0.12, May 1990–Jun 2026, gross of fees). [Weak: vendor backtest]
- AQR advises against aggressive tactical bets on the direction of inflation. It prefers strategic resilience: linkers, commodities and trend.

---

## 2. Regime diagnosis procedure

Run this whenever a user asks for a regime view or a trade depends on one. Use the latest *real-time* print of each series and state its as-of date. The scores are defaults to tune, not tested rules. [Lore for the thresholds, except where the rule itself is the source's definition]

**Step 1. Growth direction.** Score each item +1 (improving), −1 (deteriorating) or 0 (flat or unclear).
1. ISM Manufacturing and Services PMI: 3-month average vs the prior 3 months. The side of 50 sets the level.
2. Initial claims (ICSA), 4-week average vs 13 weeks earlier. A rising trend counts −1.
3. Payrolls (PAYEMS), 3-month average change vs 12-month average. Check revisions.
4. Real-time Sahm rule (SAHMREALTIME). ≥0.50 is the trigger and counts −2. 0.30–0.49 is a watch zone.
5. GDPNow (Atlanta Fed) vs the previous quarter's GDP. GDP itself is old news.
6. Conference Board LEI "3Ds": a recession signal needs the 6-month diffusion index ≤50 **and** 6-month annualised growth below the threshold. The threshold was −4.3% in the Oct 2026 release and has varied from −4.2% to −4.4%. The LEI leans on goods and manufacturing and false-signalled in 2022–24, so give it half weight.

**Step 2. Inflation direction.** Score the same way.
1. Core CPI (CPILFESL): 3-month annualised vs 12-month y/y. Default rule: more than 0.5pp above counts +1 (accelerating), more than 0.5pp below counts −1.
2. Core PCE (PCEPILFE): 6-month annualised vs 12-month.
3. Headline CPI y/y: 6-month change. If it is rising **and** at or above about 5%, flag a **Neville inflation regime**.
4. 10y breakeven (T10YIE) and 5y5y (T5YIFR): 3-month change.
5. ISM prices paid: direction.
6. Brent (DCOILBRENTEU) and diesel: 3-month change. This drives headline, but AQR finds core matters more for assets, so weight core items above energy.

**Step 3. Place in a quadrant.** Use the sign of the net growth score and the sign of the net inflation score. If either |net score| ≤ 1, call it "transition, low confidence" and name the two candidate phases. Clock phases average about 20 months, so a flip after 2–3 months of data needs strong evidence.

**Step 4. Policy overlay.**
1. What does the market price for the next 3–4 meetings (FedWatch, SOFR futures, OIS)? Compare that with the dots.
2. Is the central bank reacting to inflation persistence or to growth? In 2026 the Fed hiked into an oil supply shock instead of looking through it (§4).
3. Real policy rate vs a Taylor-rule estimate (Atlanta Fed Taylor Rule Utility).
4. Curve move type over 20 and 60 trading days (formula in §6). Split the 10y move into real yield vs breakeven and into expectations vs term premium (ACM).

**Step 5. Financial-conditions and stress overlay.**
1. NFCI sign: above 0 means tighter than average.
2. HY OAS: level and **4-week change**. A widening of 100–150bp within weeks, alongside equity weakness, confirms a growth scare [Lore].
3. CCC–BB spread, EBP, BDC discounts to NAV, private-credit default rates.
4. Broad dollar (DTWEXBGS) trend. A strong dollar tightens global conditions.
5. USD/JPY, CFTC yen positioning and implied vol, for carry-unwind risk (§8).

**Step 6. Correlation regime.** Compute the rolling 63-day and 252-day correlation of equity returns vs bond *price* returns (not yields). Above about +0.2 means an inflation-dominated regime where bonds do not hedge. Below about −0.2 means bonds hedge. These cut-offs are defaults.

**Step 7. Valuation context.** Excess CAPE yield = 1/CAPE − DFII10. Use it only to set long-run expected returns and gross exposure (§12).

**Step 8. Output.** Give:
- the regime label and a confidence level;
- the 3–5 decisive data points, each dated;
- the playbook row from §3;
- the hedge choice from Step 6;
- **explicit flip triggers**: which data change would move you to the next phase.

Re-run after each CPI, payrolls and FOMC, and at least monthly.

---

## 3. Regime → asset / sector / strategy playbook

Asset and curve columns come from the Clock [Moderate]. Sectors come from Clock Table 6 [Weak]. Strategy rows come from Neville et al. and AQR [Moderate]. The dollar column is [Lore]. Tilts are tilts: Stangl et al. show phase-based rotation earns only about 2% a year *with perfect foresight* (§13).

| Regime | Favour | Avoid | Curve | Stock–bond corr / hedge | Strategies | Dollar (smile) |
|---|---|---|---|---|---|---|
| **Reflation** (g↓ π↓) | Long duration bonds, defensive growth, staples, quality | Commodities, energy | Bull steepening | Negative, so Treasuries hedge | Long duration, receive front end, quality | Left side if panic, else falling |
| **Recovery** (g↑ π↓) | Equities (19.9% real), cyclical growth, cons. disc., tech; growth/tech led 2023–24 | Commodities, energy, pharma | Mild bull steepening | Negative, so bonds hedge | Equity beta, momentum | Bottom (synchronized growth): dollar down |
| **Overheat** (g↑ π↑) | Commodities (19.7%), energy, industrials, cyclical value, commodity carry; 2026 example | Bonds (0.2%), long duration, cons. disc. | Bear flattening (term-premium bear steepening in 2026) | Tends positive, so bonds don't hedge: use commodities, trend, options | Long commodity curves (backwardation roll), trend, value | Right side (US rates up) |
| **Stagflation** (g↓ π↑) | Cash/T-bills, energy, pharma, utilities, defensive value | Equities (−11.7%), tech, cons. disc., 60/40, risk parity | Bear flattening | Positive, so bonds don't hedge | Trend (+25% real in inflation regimes), commodities (oil-shock caveat), short duration | Mixed: left side if stress |
| **Inflation-regime overlay** (π rising to ≥5%) | Commodities (+14%), trend (+25%), breakevens vs core shocks, momentum (n.s.) | Equities (−7%), 10y (−5%), 60/40 (−6%), small caps | Usually bear | Positive | Trend, commodities; value and profitability hold up | n/a |
| **Funding / deleveraging shock** (carry unwind, credit gap-out) | Cash, short-dated Treasuries if growth-led, long vol (bought beforehand) | Crowded carry, levered longs, illiquid credit | Bull steepening if the Fed is expected to ease | Depends on driver: growth-led is negative | Cut gross first | USD vs high-yielders and funders (JPY) up; USD/JPY fell 160→142 in Aug 2024 |

---

## 4. Monetary policy transmission

**Instruments and pricing.** Fed funds futures and CME FedWatch give meeting probabilities. SOFR futures and OIS price the path. Always frame a decision as *actual vs priced*: before the 28 Oct 2026 meeting, futures priced only about a 7% chance of a move, so a hold carried no surprise and the information was in the two dissents for a hike.
- An unanticipated 25bp cut ≈ +1% in broad US equities. The expected component has little effect (Bernanke & Kuttner 2004). [Strong]

**Reaction function.** Taylor-type rules set the policy rate from the inflation gap and the output or unemployment gap (Taylor 1993; Atlanta Fed utility).
- In 2026 the Fed responded to inflation persistence. Warsh cited "65 months of sustained, elevated inflation" at Jackson Hole. The Fed hiked on 16 Sep 2026 despite an oil supply shock. **Do not assume an oil shock produces cuts.**
- Warsh discourages forward guidance, and reports say the Fed will hold fewer rate-setting meetings from 2027 [Contested: the Fed's published 2027 calendar still lists eight; see market-context-2026.md]. Expect each meeting to carry more information and bigger surprise components. [Weak: inference]

**Yield decomposition.**
```
10y nominal  = 10y real (DFII10) + 10y breakeven (T10YIE)
10y nominal  = avg expected short rate over 10y + term premium (ACM or Kim–Wright)
```
- ACM (Adrian, Crump & Moench) term premia are published daily and monthly by the NY Fed. FRED **THREEFYTP10 is Kim–Wright, a different model**. The two give different numbers, so always name the model.
- 2026 readings conflict [Contested]:
  - Resonanz: ACM 10y about +0.9% in Sep 2026, the highest since 2014, having turned positive in Oct 2024.
  - Kim–Wright (FRED THREEFYTP10): 0.46% (27 Feb) to a 2026 peak of 1.10% (5 Oct); 0.87% on 6 Nov.
  - Rabobank's decomposition: the term premium *fell* from 0.78% to 0.57% in early Sep 2026 while yields rose, so real rates drove that leg.
- The record low was about −1.3% to −1.65% in 2020 (sources disagree).

**Real yields → assets.**
- Higher real yields compress long-duration equity multiples. This is the canonical channel behind 2022's growth/tech underperformance. [Moderate]
- Strong earnings can override it. In 2026 equities absorbed a 10y real yield of **2.95% (5 Oct 2026 peak, a 20-year-plus high; 2.66% on 9 Nov)** on AI capex and productivity.
- Gold no longer follows real yields reliably (§10).
- **Term-premium-led bear steepening** is a fiscal or inflation-risk signal. It hurts bonds and equity multiples together and supports a positive stock–bond correlation. [Weak–Moderate]

**QE/QT.**
- The first LSAP cut the 10y term premium by an estimated 30–100bp (Gagnon et al. 2011). [Moderate: wide range]
- QT timeline: began Jun 2022 → Treasury cap cut to $5bn/month in Mar 2025 → ended 1 Dec 2025.
- Reserve-management T-bill purchases (RMPs) then ran about $40bn/month from Dec 2025 → $25bn → $10bn (Jul 2026) → **zero for a third month as of Oct 2026**, with $14.6bn of maturities still reinvested (snippet).
- The NY Fed says RMPs are reserve management, not stimulus. Do not trade them as QE.
- Warsh's plans to shrink and shorten the balance sheet are proposals, not policy (as of Nov 2026). If adopted they would add upside risk to term premium.

---

## 5. Liquidity frameworks and financial conditions

**"Net liquidity"** [Weak / Contested]
```
Net liquidity = WALCL − WTREGEN (TGA) − RRPONTSYD (ON RRP)
Check units on FRED before subtracting: WALCL is in millions; TGA and RRP are in billions (background, verify).
```
- **For:** vendor or tool sellers report a level correlation of 0.81 with the S&P 500 over 2020–22 (0.74 for WALCL alone), and 4-week-change correlations often above 0.7 in 2020–24. These are in-sample and self-published.
- **Against:** the 26-week correlation collapsed to "almost negative" by Mar 2023. Since 2004 it has had negative and zero stretches that look random. Both series trend upward, which is the classic spurious-regression setup.
- It "worked" in 2021–23 because huge one-way RRP and TGA swings lined up with equity trends. With RRP near zero by late 2025 and the balance sheet stable, the series has little variance left to explain anything.
- **Use** reserves (WRESBAL), TGA and RRP changes around debt-ceiling, tax-date and quarter-end windows to watch for repo and funding stress, **not** to forecast equity direction.

**Financial conditions indices.**
- Chicago Fed NFCI: weekly, 105 measures of money-market, debt, equity and banking conditions. 0 = average; positive = tighter. ANFCI removes the business-cycle component. [Moderate as a measurement tool]
- GS-style FCI: a weighted mix of the short rate, long yields, credit spreads, equities and the trade-weighted dollar (Hatzius et al. 2010).
- FCIs contain equity prices and spreads, so **using an FCI to predict equities is circular**. Use it to judge whether the Fed is getting the tightening it wants. A loose FCI with a hawkish Fed, as in 2026, implies more hikes.

**Global liquidity and the dollar.** The BIS Global Liquidity Indicators track cross-border bank credit and USD, EUR and JPY credit to non-residents. A stronger dollar goes with less cross-border bank leverage and wider CIP deviations, so the dollar works as a global financial-conditions variable (Avdjiev, Du, Koch & Shin). [Moderate]

**Leverage is the transmission risk.** The BIS on Aug 2024: "procyclical deleveraging and margin increases" amplified a single data surprise.

---

## 6. The yield curve

**Track record.**
- The 10y–3m spread predicted US recessions 2–6 quarters ahead better than other indicators (Estrella & Mishkin 1996). The NY Fed publishes a 12-month-ahead recession probability built on it. [Strong pre-2022; now Moderate]
- **The 2022–24 false signal:**
  - The 10y–2y inverted from Jul 2022 for about 26 consecutive months, un-inverting Sep/Oct 2024. This is described as the longest postwar 10y–2y inversion.
  - The NY Fed probability peaked around **70.85% in May 2023**, the highest since 1982 (secondary sources, checked this session).
  - No NBER recession followed through at least Oct 2026. The last trough was Apr 2020.
  - Some 2026 articles date the "definitive" un-inversion of other spreads to Dec 2025 or Apr 2026, which conflicts with the dates above.
- The 10y–3m was 0.44 (Feb 2026) → 0.80 (Aug 2026) → **0.86 (20 Oct 2026)**.
- Candidate reasons for the miss [Contested; none formally tested]: a negative term premium distorted the curve's information about expected rates; large fiscal deficits; debt termed out at low fixed rates; excess savings and immigration-driven labour supply.
- **Teach:** inversion means policy is restrictive relative to neutral. It does not guarantee a recession. Lead times historically ran about 6–24 months. Equities often fell *after* un-inversion, as the bull steepener arrived with the recession. Pair the curve with claims, the Sahm rule and credit.

**Classifying a curve move** (defaults: window 20 and 60 trading days; ignore |Δslope| < 5bp):
```
d2, d10 = change in 2y and 10y yields over the window
level = (d2 + d10)/2 ;  dslope = d10 - d2
dslope>0 & level<0 -> bull steepener   dslope>0 & level>0 -> bear steepener
dslope<0 & level>0 -> bear flattener   dslope<0 & level<0 -> bull flattener
```

| Shape | Typical driver | Clock phase | Favours | Hurts |
|---|---|---|---|---|
| Bull steepener | Front end rallies; Fed cutting into weakness | Reflation (strongest, significant) / recession onset | Bonds, defensives, quality | Cyclicals, banks |
| Bear steepener | Long end sells off. Growth-led = early-cycle reflation; term-premium or fiscal-led = 2026 | Early Recovery, or fiscal stress | Growth-led: cyclicals, banks, value | Term-premium-led: duration and long-duration equities |
| Bear flattener | Fed hiking | Overheat, Stagflation | Commodities, energy, industrials | Bonds, front-end longs |
| Bull flattener | Long end rallies on growth or disinflation fears | Late cycle | Long-duration growth, defensives | Banks (net interest margin), cyclicals |

---

## 7. Stock–bond correlation regimes

- **Model (Brixton et al. 2023, AQR).** Growth news moves stocks and bonds in opposite directions. Inflation news moves them in the same direction. The correlation is positive when inflation volatility exceeds growth volatility. This explains about 70% of the long-term variation in the US correlation and works similarly abroad, but it explains short-term swings poorly. The secular fall in real rates was *not* a driver. [Moderate] Nominal bond betas also depend on whether inflation is pro- or counter-cyclical and on the policy regime (Campbell, Pflueger & Viceira).
- **History.** The correlation was positive before 2000, negative from 2000 to 2021, and positive again from 2022 on rolling 5-year windows (AQR 2026).
- **Rates–credit correlation** has also risen since 2022, a "diversification deficit" for bond-heavy holders. When inflation news dominates, **commodities diversify both stocks and bonds strongly** (AQR 2026).
- **Implications for 60/40 and risk parity.** 60/40 averaged −6% real in inflation regimes. Stocks and bonds both made money in only 2 of 8 regimes. Risk parity's levered bonds became levered equity-like risk in 2022 (All Weather −22%).
- **2026 readings conflict** [Contested]:
  - rolling 36-month S&P vs 10y Treasury return correlation of +0.40 (Voronoi);
  - a 2-month S&P vs 10y *yield* correlation of −0.70 in May 2026, "lowest since 1999", which is a *positive* price correlation (low-quality source);
  - Scotiabank (via Axios, 4 Sep 2026): the correlation turns negative once the 10y exceeds about 5% [Weak: single-bank heuristic];
  - 70% of equity down days after 1 Jun 2026 also saw bonds sell off (anecdotal).
- **Sign-convention trap.** "Stocks vs yields" has the opposite sign to "stocks vs bond prices", and several 2026 headlines mix them up.
- **Hedge selection rule.** When core-inflation surprises dominate the data flow, treat bonds as a risk asset. Hedge with commodities, trend, the dollar (if it is in a smile state) or options. When growth scares dominate, Treasuries hedge again. Re-check with the Step 6 rolling correlation.

---

## 8. The dollar and carry

- **Dollar smile** (Stephen Jen, Morgan Stanley; no primary source retrieved) [Lore]. Left side: global panic, when USD funding demand lifts the dollar. Bottom: synchronized global growth, dollar down. Right side: US outperformance or higher US rates, dollar up. 2025 was the bottom plus policy and fiscal credibility worries (DXY −9.4%). Early 2026 was the left side (Iran war). A hawkish Fed in H2 2026 points to the right side.
- **DXY is about 58% EUR** (background, unverified), so it is largely EUR/USD. Use the Fed broad index **DTWEXBGS** for macro or EM work.
- **2026 path (dated):** four-year low in late Jan 2026, then about +5% on war safe-haven and oil flows; about 99.5 after the Iran strikes (Mar); above 101.8 on 1 Oct and 102.4 on 12 Oct; slipped after the 3 Nov midterms.
- The dollar moved *with* Brent, which is "hardly how a haven reacts". The US is now a net energy exporter, so in a supply shock the dollar behaves partly like a petrocurrency. The usual strong-dollar → weak-commodities link broke. [Weak: inference]
- **Carry unwind case study (Aug 2024).** Triggers: the BoJ hike on 31 Jul, then weak July payrolls on 2 Aug (114k, unemployment 4.3%). On 5 Aug the Nikkei fell 12.4%, its worst day since 1987. VIX hit 65.73 intraday and closed at 38.57; S&P −3.0%, Nasdaq −3.4%; USD/JPY went from about 160 to about 142. The BIS put yen carry at about ¥40tn (~$250bn), likely an underestimate. Markets stabilised quickly. [Moderate]
- **Carry-crash warning checklist** [Lore]: (1) a narrowing rate differential (funder hiking or high-yielder cutting); (2) crowded positioning (CFTC yen shorts); (3) low implied vol; (4) a growth scare in the high-yielder; (5) intervention risk.
- **2026 setup (as of Nov 2026):** BoJ at 1.25% (hiked 18 Sep 2026, held 30 Oct, Dec hike nearly priced). The 10y JGB was near 3% (Sep 2026), the highest since 1996. Japan intervened in Apr–May 2026 with USD/JPY above 160. The ingredients resemble Jul 2024.

---

## 9. Credit spreads and the default cycle

- **Excess bond premium (Gilchrist–Zakrajšek).** The part of corporate spreads not explained by default risk is a validated predictor of recessions and activity declines. [Strong] Raw OAS is pro-cyclical: **weak for timing, strong for confirmation**. Tight spreads can persist for years late in a cycle.
- **Reference levels (HY OAS, BAMLH0A0HYM2):** Dec 2008 peak about 1,990–2,180bp (sources disagree); 23 Mar 2020 peak about 1,087bp (secondary sources, checked this session).
- **2026 levels. Always state the date:**

| Date | IG OAS | HY OAS | Note |
|---|---|---|---|
| 22 Jan 2026 | 73bp | — | 2026 tight; lowest since 1998 |
| Feb–May 2026 | 94bp (16 Mar, Iran war) | ~262–300bp (Apr) | HY tightest since Jun 2007 (aggregators) |
| 2 Oct 2026 | ~85bp | ~310bp | Wider than 25 Sep (FRED via CryptoSlate) |
| 15 Oct 2026 | ~80–85bp | ~310bp | CCC widening; 3 US HY deals pulled in Oct |
| ~23 Oct 2026 | Global corporate 129bp | — | Widest since May 2025 |
| 5 Nov 2026 | 93bp | 348bp | 2026 HY wide (AI selloff day) |
| 11 Nov 2026 | 90bp | 330bp | Latest (FRED, via market-context-2026.md) |
- **Defaults (Fitch).**
  - US private-credit default rate **6.0% (TTM to Apr 2026)**, a series high since the index launched in 2024. A 6.1% July print appears in one secondary source only; the 2026-context research found nothing after April.
  - July 2026 TTM: leveraged loans about 3.8%, HY bonds about 2.7%.
  - Fitch year-end forecasts: loans 4.5–5.0%, HY 2.5–3.0%.
- **Why public HY looks healthier.** Riskier borrowers migrated to private credit and leveraged loans. Stress shows up first in PIK usage, maturity extensions and distressed exchanges, not in public OAS, and private marks lag. Software makes up 20–25% of BDC books. The IMF flagged the roughly $2tn private-credit market for opacity, stale valuations, layered leverage and links to banks and insurers (Apr 2024).
- **Watchlist:** HY OAS 4-week change; CCC–BB spread; loan defaults and distressed exchanges; BDC discounts to NAV and redemption gates; the EBP.

---

## 10. Commodities

**Oil.**
- Supply shocks, aggregate-demand shocks and precautionary-demand shocks have different macro and asset effects. Identify which one you face before mapping to equities or the Fed (Kilian 2009). [Strong]
- Collateralised commodity futures historically earned equity-like premia, with negative correlation to stocks and bonds and positive correlation to inflation (Gorton & Rouwenhorst). [Moderate]
- Term structure: backwardation signals tight inventories, and holders earn positive roll.
  ```
  futures total return ≈ spot change + roll yield + collateral (T-bill) yield
  annualised roll yield ≈ (F_near − F_next) / F_next × 365 / days_between_expiries
  ```
- **2026 roll example, YTD to mid-Aug 2026 (Saxo, fetched):**

  | Contract | Front-month price | Total return |
  |---|---|---|
  | Brent | +46.6% | **+75.7%** |
  | WTI | +45.5% | +75.4% |
  | Gasoil | +98.4% | +154.8% |
  | ULSD | +100% | +140.4% |

  Backtests on continuous front-month *price* series miss this roll entirely.
- **2026 balance (IEA via Saxo, Aug 2026):** inventories down about 410mb since the war began (about 2.7 mb/d); Q3 deficit about 1.8 mb/d; 2026 demand *down* 1.6 mb/d. Demand destruction is already large, so the downside on reopening is sharp.
- **Headline-gap risk.** The 8 Apr 2026 ceasefire knocked Brent down about 16% in a day, its biggest one-day fall since 1991. Size flat-price oil for 15%+ overnight gaps, and pair it with EIA weekly and IEA monthly inventories and Brent M1–M6 spreads.
- **OPEC+.** Spare capacity is likely overestimated because output lags quotas. Next ministerial meeting: 29 Nov 2026.

**Gold.**
- Working model: price ≈ f(real yields, USD, Western ETF flows) + a **structural central-bank bid**. That bid comes from reserve diversification after the 2022 Russian reserve freeze, sanctions risk, and fiscal and Fed-independence fears. When the central-bank bid is strong, real yields set the direction but not the level.
- Decoupling from real yields:
  - 2022–23: real yields surged and ETFs sold, but central banks held the price up.
  - 2026: real yields hit 2.95% (5 Oct) *and* ETF holdings rose. Saxo reads high long yields as a fiscal-risk signal.
  - [Contested] Saxo says the link is broken. Janus Henderson says it is weaker but still drives short-horizon direction.
  - The rolling gold vs real-yield correlation reportedly went from −0.7/−0.85 to −0.2/−0.3 [Weak: low-rigour sources].
- **WGC Q3 2026 (3 Nov 2026):** average price $4,262/oz; central banks 321t (+42% y/y), 675t YTD; ETF inflows 211t, holdings a **record 4,256t**; jewellery 313t (−17%), bar and coin 268t (−19%). The demand mix has shifted to official and ETF buyers as price-sensitive demand collapses.
- **The Fed-credibility channel cuts both ways.** Gold fell about 11.4% on 30 Jan 2026 when the Warsh nomination landed, its worst day since 1983, after an ATH near $5,595 on 29 Jan. Gold hedges *loss* of central-bank credibility and gets hit when credibility is restored. For current levels see market-context-2026.md.
- Gold is a poor short-run inflation hedge. Its real price mean-reverts over very long horizons, and a high real price predicts low future real returns (Erb & Harvey). [Moderate]

**Copper.**
- Copper/gold ratio vs the 10y yield and the China credit impulse are common growth heuristics [Lore; no source retrieved].
- In 2026 copper is distorted by US tariff arbitrage: record COMEX stocks, thin LME stocks, records of about $14.5–14.7k/t. **Do not read copper as a clean growth signal this year.** See market-context-2026.md.

---

## 11. Macro event trading guide (FOMC, CPI, NFP)

**Established effects.**
- **Announcement-day premium** [Strong]:
  - The equity excess return averaged 11.4bp on CPI, PPI, employment and FOMC days vs 1.1bp on other days (1958–2009), with more than 60% of the annual premium earned on announcement days (Savor & Wilson 2013).
  - Extended to 1961–2023: 10.68bp vs 0.93bp (NBER w31923).
- **Surprises cause quick conditional-mean jumps** in FX and other assets. Bad news has a bigger impact than good news, and US news dominates (Andersen, Bollerslev, Diebold & Vega 2003). [Strong]
- **Pre-FOMC drift** [Contested]:
  - The S&P rose about 49bp in the 24h before scheduled FOMC announcements (1994–2011, Lucca & Moench).
  - It **essentially vanished after 2015**, explained by lower uncertainty (Kurov, Wolfe & Gilbert 2021).
  - Others find it concentrates in high-uncertainty periods, so it may reappear in regimes like 2026. Do not trade it as a standing edge.

**Release hierarchy by regime.**
- **Inflation-dominated** (2022, 2026): CPI and core PCE (core m/m is *the* number) → wages (AHE, ECI) → breakevens, ISM prices paid.
- **Growth-dominated** (Aug 2024): NFP, the unemployment rate and Sahm → weekly claims → ISM new orders → retail sales.
- GDP is usually old news; GDPNow and nowcasts move markets more.

**Pre-event procedure (T−1).**
1. **What's priced.**
   - FOMC: FedWatch odds for this meeting and the next 3, the OIS/SOFR path, and the last dots.
   - CPI/NFP: consensus median and range, plus the nowcast or "whisper" (Cleveland Fed inflation nowcast for CPI).
2. **Implied move.** Use the straddle expiring just after the release. An ATM straddle ≈ 0.8·σ√T·S, which is the expected *absolute* move. **One standard deviation ≈ 1.25 × straddle.** Back out the event-day vol vs normal days with `move --event-vol --base-vol`.
3. **Positioning.** How crowded is the trade (CFTC, recent run-up), and where is skew?
4. **Scenario grid.** Write hot / in-line / cool outcomes with the expected sign for the 2y, the 10y (real vs breakeven), USD, equities (growth vs value) and credit. Pre-commit the action for each.
5. **Size for the gap.** A 2× implied-move gap against the position must fit inside the risk limit. Stops do not protect across a release.

**Reading the result.**
- Surprise z = (actual − consensus) / σ(historical surprises). Also read revisions (NFP revisions can swamp the headline), the unemployment rate, AHE, and core vs headline.
- AQR finds core inflation surprises are more damaging to equities and bonds than energy surprises. A hot headline driven by gasoline is less bad than a 0.1pp core beat. [Moderate]
- Read the **2y first** (policy repricing), then USD, then the real/breakeven split of the 10y, then equities and credit [Lore]. A move in the 2y that equities ignore is information.
- **FOMC.** Read four things: the decision vs priced; dots vs the market path; statement wording changes; the press conference. Under Warsh (no forward guidance) the presser and dissents carry more weight.
- **Worked examples:**
  - 13 Sep 2022 CPI: core 6.3% vs 6.1% expected y/y. S&P −4.3%, its worst day since Jun 2020 (verified this session).
  - 2 Aug 2024 NFP: 114k with unemployment at 4.3% triggered the Sahm rule (background) and fed the carry unwind.
  - Aug 2026 CPI: +0.4% m/m, 3.4% y/y, gasoline-led. It cemented the Sep 2026 hike, which was "widely expected".
  - 6 Nov 2026 NFP: +165k vs about 65k consensus.
- **Data-quality trap.** BLS could not publish most 12-month CPI changes for Oct 2026 (released 10 Nov 2026) because Oct 2025 data were never collected during the shutdown. Any "Oct 2026 y/y CPI" is derived; trade the m/m.

**Economic surprise indices (Citi CESI).**
- Bloomberg describes CESI as weighted historical standard deviations of surprises vs the survey median, over a rolling 3-month window. Weights come from high-frequency FX impact, with a time decay (secondary description; no Citi primary document found).
- It mean-reverts by construction as forecasters adjust. Use it as a short-horizon contrarian or momentum gauge for yields and USD, **never as a level signal**. [Lore/Weak: no track-record study retrieved]

---

## 12. Valuation: CAPE, ERP, real yields

| Claim | Evidence | Grade |
|---|---|---|
| CAPE explains ~40–43% of the variation in subsequent 10-year real returns (1926–2011) | Vanguard (Davis, Aliaga-Díaz & Thomas 2012). The paper notes annualised returns inflate R² by about 0.05 | [Moderate] |
| ~No 1-year timing power | Same paper: 1-year-ahead correlations of most metrics close to zero. One secondary summary says about 10% for P/E10 (unverified) | [Strong] for "unreliable" |
| Real-time 10-year CAPE forecasts did worse than the historical mean | Since 1985: 7.8% vs 6.2% RMSE (Vanguard 2018) | [Moderate] |
| CAPE "explains 85%" (Finke) | Overlapping 10-year windows inflate R² through autocorrelation | [Contested] |
| The Fed model (earnings yield vs *nominal* yield) | No long-run forecasting power, and suffers from inflation illusion. Use real yields (Asness 2003) | [Strong] |

```
Excess CAPE yield (ECY) = 1/CAPE − 10y real yield (DFII10)
```
- **2026 levels (sources vary):** CAPE about 38.2 (Mar), 39.8 (22 Jul) and about 42 (Aug 2026); ECY about 0.5–0.8% in H1 2026, ≈0 to negative by Aug–Oct as real yields rose (1/CAPE ≈ 2.4% vs DFII10 2.6–2.95%, computed). Long-run ERP average 6.2% (1926–2024, CFA Institute). One analyst computes a negative ERP from consensus 2026 EPS of $330 [Weak].
- **Rule:** use CAPE, ECY or ERP for 7–10-year expected returns and for sizing strategic equity exposure, **never as a sell signal**. CAPE sat above 30 for most of 2017–2026 while the index compounded. Take short-term timing from trend, breadth, credit and surprises.
- With 10y TIPS at 2.6–2.95% (Sep–Nov 2026; peak 2.95% on 5 Oct, 2.66% on 9 Nov), equities have their thinnest margin of safety in about 25 years. Sensitivity to growth disappointments and to further real-yield rises is higher.
- Buffett indicator: distorted by foreign earnings and the rate level. Long-horizon only. [Lore]

---

## 13. Sector rotation and leading indicators

- **Perfect-foresight rotation is barely worth it** (Stangl, Jacobsen & Visaltanachoti; 1948–2007):
  - knowing NBER phases perfectly, conventional rotation beat the market by **2.3%/yr gross**;
  - one month early or late: about 1.9–2.2%; two months off: about 1.0–1.8%;
  - an "unconventional" rotation made 7.3% gross, about 6.1% net (treat as in-sample).
  - Molchanov & Stangl (IJFE 2023/24), "The Myth of Business Cycle Sector Rotation": the gains "quickly diminish" after costs and mistiming, and cross-industry predictability is no better than chance. [Moderate]
- **Framing:** sector calls are regime-conditional tilts with modest expected alpha. Most of the edge comes from catching shifts in the *inflation direction*, the Clock's east–west axis, which drives Cons. Disc. vs Energy. Example: 2026 energy was +30.7% YTD by early May.
- **LEI** [Weak as a standalone signal]. The Conference Board's own rule signalled recession continuously from about mid-2022, and no recession followed. Yardeni argues the Board then tweaked the rule to the 3Ds. Reports of a 21-month signal with a −4.6% 6-month decline are unverified. Sep 2026: no recession signal (diffusion slightly above 50).
- **The 2022–24 false-positive cluster:** curve inversion, LEI, the Sahm trigger (Aug 2024 release) and long stretches of ISM manufacturing below 50. These indicators lean on goods and manufacturing and under-weighted a services- and fiscal-driven expansion.
- **Rule:** before acting on a recession call, require coincident confirmation from the claims trend, payroll breadth, real income and credit.

---

## 14. 2026 regime read (as of 12 Nov 2026)

For the full dated snapshot (levels, events, forecasts) read **market-context-2026.md**. This section gives only the regime call.

- **Call: Overheat, with stagflation tail risk.** Growth is strong: Q3 GDP +3.4% SAAR (advance), and the 28 Oct FOMC statement said "expanding at a strong pace". Inflation is rising on an energy shock: CPI 3.7% y/y in Sep 2026. The Fed is hiking: to 3.75–4.00% on 16 Sep, held 28 Oct with 2 dissents for a hike, about 78–80% odds of a Dec hike (late Oct–early Nov).
- **What fits the Clock:** energy and commodity carry led. Bonds sold off: 10y above 5% (peak about 5.3% in Oct; 4.87% on 9 Nov), 10y real yield peaking at 2.95% (5 Oct; 2.66% on 9 Nov), and a term-premium/fiscal bear steepener (10y–3m 0.86 on 20 Oct). Equities still rose on earnings.
- **Portfolio implications:** assume a positive or unstable stock–bond correlation, so Treasuries are an unreliable hedge. Favour trend, commodities and options for protection. Do not expect oil shocks to bring cuts. Watch yen carry and private credit as amplifiers.
- **Flip triggers:**
  - Hormuz reopening → oil collapse → inflation direction turns down → toward Recovery/Reflation, with bonds hedging again.
  - AI-financing selloff + HY widening + rising claims → growth turns down while inflation is still high → Stagflation.

---

## 15. Data checklist

IDs marked † are standard FRED IDs not listed in the research notes. Confirm each on FRED before scripting. FRED's ICE BofA OAS series may carry only limited history (background, unverified).

| Block | Series | Source / ID |
|---|---|---|
| Policy pricing | Meeting probabilities; path | CME FedWatch; SOFR futures; OIS; effective FF (DFF†), SOFR† |
| Yields | 2y, 10y, 10y TIPS, 10y breakeven, 5y5y | DGS2, DGS10, DFII10, T10YIE, T5YIFR† |
| Curve | 10y–3m, 10y–2y; recession probability | T10Y3M, T10Y2Y; NY Fed yield-curve model |
| Term premium | ACM (daily/monthly); Kim–Wright | NY Fed term-premia page; THREEFYTP10 (KW) |
| Liquidity | Fed assets, TGA, ON RRP, reserves | WALCL, WTREGEN, RRPONTSYD, WRESBAL; NY Fed SOMA/RMP schedules |
| Fin. conditions | NFCI, ANFCI; global liquidity | NFCI, ANFCI; BIS Global Liquidity Indicators |
| Credit | HY OAS, IG OAS, BB, CCC; EBP; defaults | BAMLH0A0HYM2, BAMLC0A0CM, BAMLH0A1HYBB†, BAMLH0A3HYC†; Fed EBP data; Fitch/Moody's reports |
| Growth | Claims, payrolls, unemployment, Sahm, nowcast, LEI, PMIs | ICSA, PAYEMS†, UNRATE†, SAHMREALTIME; Atlanta Fed GDPNow; Conference Board LEI; ISM |
| Inflation | CPI, core CPI, core PCE, nowcast | CPIAUCSL†, CPILFESL†, PCEPILFE†; Cleveland Fed nowcast; ISM prices paid; AAA/EIA diesel |
| Policy rule | Taylor-rule estimates | Atlanta Fed Taylor Rule Utility |
| FX | Broad dollar, DXY, positioning, intervention | DTWEXBGS; ICE DXY; CFTC COT; BoJ/MoF data |
| Oil | Prices, inventories, balances, spreads | DCOILBRENTEU†, DCOILWTICO†; EIA Weekly Petroleum Status; IEA OMR; OPEC MOMR; Brent M1–M6 |
| Gold | Central-bank and ETF demand | WGC Gold Demand Trends; WGC central-bank statistics |
| Valuation | CAPE; ECY | Shiller data; 1/CAPE − DFII10 |
| Recession dating | NBER | NBER business-cycle dates; USREC† |
| Real-time vintages | As-first-reported data | ALFRED (St. Louis Fed), for any regime backtest |

---

## Failure modes / traps

1. **Look-ahead regime labels.** The backtest dates phases with revised GDP or output gaps, or with NBER dates announced months later. *Catch:* ask which vintage was used. Insist on ALFRED or real-time nowcasts, and lag NBER dates by their announcement delay.
2. **Trading levels instead of changes or surprises.** "CPI is 3%, so buy TIPS" ignores direction and pricing. *Catch:* every macro thesis needs "vs consensus" and "vs priced".
3. **Curve or LEI as a timing trigger.** *Catch:* point to the 6–24-month lead times and the 2022–24 miss. Demand coincident and credit confirmation.
4. **Net-liquidity or FCI regressions on trending levels.** *Catch:* re-run on changes and out-of-sample, and show the rolling correlation. FCIs contain equity prices, so they are circular.
5. **Assuming bonds hedge.** This is the 60/40 or risk-parity plan built on 2000–2021 correlations. *Catch:* compute the current rolling correlation, check whether the data flow is inflation- or growth-led, and stress-test a 2022 replay.
6. **Sign-convention errors** between stock–yield and stock–bond-price correlations.
7. **"Oil shock → Fed cuts"** reasoning. 2026 is the counterexample: the reaction function followed inflation persistence.
8. **DXY as "the dollar"** for EM or commodity work. Use the broad index.
9. **Gold as a pure real-yield trade.** It ignores the central-bank bid and the Fed-credibility channel (30 Jan 2026).
10. **Commodity backtests on front-month prices.** These miss roll yield, which was worth about 29pp of Brent return in 2026 YTD, or the reverse in contango. Use total-return or properly rolled series.
11. **Sector-rotation backtests with perfect phase knowledge.** One or two months of mistiming removes most of the edge (Stangl et al.).
12. **Treating public HY OAS as the whole credit picture** while private credit defaults hit records.
13. **CAPE as a sell signal**, or R² claims from overlapping windows. Use non-overlapping samples or HAC errors.
14. **Small-n overconfidence and data mining.** There are 8 inflation regimes and a few recessions. If a user tried many indicators and thresholds, deflate the result (`sharpe --trials`).
15. **Data-quality blind spots:** NFP revisions, the missing Oct 2026 y/y CPI, and model differences in term premium (ACM vs Kim–Wright).
16. **Ignoring positioning on event days.** Aug 2024 shows a modest surprise plus crowded carry produces a crash-sized move.

---

## Toolkit hooks

- **Live regime data first:** `python scripts/fetch.py macro` prints a dated dashboard (fed funds, SOFR, 2y/10y, real yield, breakeven, 10y-2y and 10y-3m curves, CPI/core CPI/core PCE YoY, unemployment, claims, VIX, HY/IG OAS, NFCI, broad USD, Fed assets, TGA, RRP, Brent/WTI, S&P 500) with 1m/3m/1y changes and mechanical regime flags. Any other series in the §15 checklist: `python scripts/fetch.py fred ID1 ID2 --start YYYY-MM-DD [--yoy] --out file.csv`; find IDs with `fetch.py search "text"`. Daily prices for cross-asset proxies (TLT, GLD, UUP, HYG, sector ETFs, ES=F, CL=F): `fetch.py prices SYMBOL --out file.csv`. The FRED key is found automatically and must never be printed.
- Event-implied move: `python scripts/tradekit.py move --S <px> --days <d> --straddle <straddle_px>` for the 1 SD (≈1.25 × straddle). Use `move --S <px> --days <d> --vol <iv>` for a vol-based move. Use `move --event-vol --base-vol` to isolate the release-day vol.
- Event-day option pricing: `tradekit.py bs ...` and `tradekit.py iv --price ...` to compare pre- and post-event IV and price the vol crush.
- Realised vs implied before a release: `tradekit.py vol FILE` (Yang-Zhang, EWMA).
- Sizing a macro trade against the gap: `tradekit.py size --equity E --risk 0.5 --entry P --stop S` (or `--atr --atr-mult`; `--multiplier` for futures).
- Testing the trend sleeve used as an inflation hedge: `techkit.py ruletest FILE --rule tsmom --vol-target ... --cost-bps ... --oos 0.3`.
- Sector or asset momentum as a price-based check on macro rotation: `techkit.py rank FILE...`.
- Evaluating a regime-timing backtest: `tradekit.py perf FILE --trials <n>`, and `tradekit.py sharpe --sr --n --trials --var-sr` for the DSR when many indicators or thresholds were tried.
- 60/40 or risk-parity drawdown expectations: `tradekit.py drawdown --sharpe --vol --years`.
- No script computes rolling correlations, curve classification or regime scores. Do those in pandas with the formulas above, and state the windows used.

---

## Key sources

- Greetham & Hartnett 2004, "The Investment Clock", Merrill Lynch — https://ks3-cn-beijing.ksyun.com/attachment/114caaf9991619a15e81a0a4b590837f
- Neville, Draaisma, Funnell, Harvey & Van Hemert 2021, "The Best Strategies for Inflationary Times", SSRN 3813202 — https://www.man.com/maninstitute/when-inflation-hits
- AQR 2026, "Inflation Redux?", Alternative Thinking Q3 — https://www.aqr.com/-/media/AQR/Documents/Alternative-Thinking/AQR-Alternative-Thinking-Q3-2026---Inflation-Redux.pdf?sc_lang=en
- Brixton et al. 2023, "A Changing Stock–Bond Correlation", AQR — https://www.aqr.com/Insights/Research/Journal-Article/A-Changing-Stock-Bond-Correlation
- Bernanke & Kuttner 2004, FEDS 2004-16 — https://www.federalreserve.gov/pubs/feds/2004/200416/200416pap.pdf
- Lucca & Moench, "Pre-FOMC Announcement Drift", NY Fed SR 512 — https://www.newyorkfed.org/research/staff_reports/sr512.html
- Kurov, Wolfe & Gilbert 2021, "The Disappearing Pre-FOMC Announcement Drift", FRL 40 — https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html
- Savor & Wilson 2013, JFQA 48(2) — https://ideas.repec.org/a/cup/jfinqa/v48y2013i02p343-375_00.html
- Andersen, Bollerslev, Diebold & Vega 2003, AER — https://www.aeaweb.org/articles?id=10.1257/000282803321455151
- Estrella & Mishkin 1996, NY Fed Current Issues 2(7) — https://www.newyorkfed.org/research/current_issues/ci2-7.html
- Gilchrist–Zakrajšek EBP, FEDS Note 2016 — https://www.federalreserve.gov/econres/notes/feds-notes/recession-risk-and-the-excess-bond-premium-20160408.html
- ACM term premia, NY Fed — https://www.newyorkfed.org/research/data_indicators/term-premia-tabs
- Gagnon, Raskin, Remache & Sack 2011, IJCB — https://www.ijcb.org/journal/ijcb11q1a1.htm
- BIS Bulletin 90 (Aug 2024 turmoil) — https://www.bis.org/publ/bisbull90.htm
- Kilian 2009, AER — https://www.aeaweb.org/articles?id=10.1257/aer.99.3.1053
- Erb & Harvey, "The Golden Dilemma", NBER w18706 — https://www.nber.org/papers/w18706
- Vanguard (Davis, Aliaga-Díaz & Thomas 2012) via Monevator — https://monevator.com/methods-of-making-stock-market-predictions-dont-work/ ; Vanguard fair-value CAPE — https://alphaarchitect.com/a-qa-discussion-with-vanguard-researchers-on-the-fair-value-cape-ratio/
- Asness 2003, "Fight the Fed Model" — https://www.aqr.com/Insights/Research/Journal-Article/Fight-the-Fed-Model
- Stangl, Jacobsen & Visaltanachoti (via CXO) — https://www.cxoadvisory.com/economic-indicators/perfect-sector-rotation ; Molchanov & Stangl — https://mro.massey.ac.nz/handle/10179/69590
- World Gold Council, Q3 2026 Gold Demand Trends — https://gold.org/news-and-events/press-releases/central-bank-buying-and-etf-inflows-support-gold-demand-q3
