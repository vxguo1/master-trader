# Single-Stock Equity Analysis

*Read when: a user asks to analyze one stock (fundamentals, "is it cheap?", an earnings preview or post-mortem, a news item, a price target or projection); wants a reverse DCF, multiples or a sensitivity grid; asks whether an earnings implied move is rich; brings a headline and asks whether it is priced; or asks about a semiconductor / AI-hardware name such as NVDA.*

Tags. Evidence grade: `[Strong]` `[Moderate]` `[Weak]` `[Contested]` `[Lore]`. Provenance: [V] fetched or verified on 12 Nov 2026; [V-calc] arithmetic on [V] data; [V-snip] seen only in a search summary; [K] model knowledge, not re-fetched; [SC] spot-check before quoting; [Computed] run with the toolkit on 12 Nov 2026. Evidence class: (PR) peer-reviewed, (WP) working paper, (Pract) practitioner or vendor, (Lore) no formal test. Fact types in the worked example: Reported / Guidance / Consensus / Opinion / Derived / FORECAST.

## Contents
Core principles · 1. Deep-dive procedure · 2. Financial statements, red flags, EDGAR mechanics · 3. Valuation ·
4. Earnings and estimates · 5. News triage · 6. Projection as a distribution · 7. Semiconductor / AI-hardware drivers ·
8. Worked example: NVDA, 11-12 Nov 2026 · 9. Failure modes · 10. Toolkit hooks · 11. Key sources

Neighbours (not repeated here): `options-volatility.md` §4 (straddle identity), §8 (structure choice), §10 (event-vol extraction, Gao-Xing-Zhang); `strategy-playbook.md` §5-6 (value, quality, profitability as portfolio factors), §12 (PEAD row), §15 (LLM/news signal returns); `risk-sizing-execution.md` (sizing, stops, gap risk); `market-context-2026.md` §8 (macro and AI-capex backdrop); `geopolitics-macro.md` §9 (geopolitical news triage).

## Core principles
- **Dated facts first, opinions last.** Build the snapshot, with a date and source on every number, before forming a view. Stale inputs are the most common single-stock error: on 12 Nov 2026 the NVDA "consensus target" (~$305-325) predated a 27% fall and a CEO resignation.
- **What is priced matters more than what is good.** A great business is a good trade only if reality beats the expectations in the price. Firm-level returns are mostly cash-flow news (Vuolteenaho 2002) and value-vs-glamour returns cluster on earnings days, when expectations meet results (La Porta et al. 1997). Always ask what the price assumes and what will revise it.
- **Projections are distributions, never points.** 12-month analyst targets are met 38% of the time, with a 45% mean absolute error (Bradshaw, Brown & Huang 2013). At 30% vol only ~26% of 1-year outcomes land within ±10% of the median. Give quantiles and P(levels).
- **The gap versus the market is the idea.** Start from the option-implied distribution. Deviate only for a named, sourced reason, and keep your dispersion at or above the market's unless a scored record says otherwise. A scenario tree that reproduces the market is not an edge.
- **Check filings before headlines.** EDGAR submissions update within about a second of dissemination, and web summaries lag. On 12 Nov 2026, search summaries still said "no resignation reported" hours after NVIDIA's 08:52 ET 8-K (Item 5.02). The "$250bn backstop" in July press reports was a $105bn capped, contingent guarantee in the August 8-K.
- **Keep facts, guidance, consensus and opinion in separate columns.** Only facts update the cash-flow model; narrative updates the variance. Never compute a surprise from GAAP XBRL EPS against a Street (adjusted) consensus.
- **Guidance and revenue outrank EPS.** The next-quarter sales-guidance surprise is the most informative item on the day (Hand et al. 2022). With a 78% base beat rate, an ordinary beat is a non-event.
- **Valuation is a long-horizon tool.** Cheap or expensive barely times one stock over days to months. It sets multi-year expected return and tells you which data (capex, margins) will revise expectations.
- **Red flags change size, not sign.** Cash-conversion and working-capital flags raise the evidence bar and cut size. On their own they are not a short thesis.
- **Judge an implied earnings move against the name's own history with the right benchmark.** The straddle ≈ the expected |move|, and 1 SD ≈ 1.25 × straddle. A fair exceedance rate of the straddle is ~42% (normal) or ~37% (fat tails), not 32%.

## 1. Deep-dive procedure (Workflow J in depth)
Run from a scratch folder. Paths are relative to the skill directory.

1. **Dated snapshot.**
   ```
   python scripts/fetch.py prices TICKER --years 7 --out px.csv          # Yahoo daily; drops today's partial bar
   python scripts/techkit.py indicators px.csv                            # trend template, 52w, ATR, stage
   python scripts/tradekit.py vol px.csv                                  # Yang-Zhang, EWMA: base-vol candidates
   python scripts/fetch.py fundamentals TICKER --quarters 8 --out f.csv   # SEC XBRL quarters + TTM
   python scripts/fetch.py earnings-dates TICKER --out d.csv              # 8-K Item 2.02 times, AMC/BMO/DMH
   python scripts/equitykit.py earnings --prices px.csv --dates d.csv --straddle X --spot S
   ```
   Filings list only past releases, so get the next date from the company's own release or IR page. Options: `tradekit.py iv`, `move --straddle`, `move --event-vol --base-vol`. Record the retrieval time of every number.
2. **Drivers.** Name 3-6 cash-flow drivers and the metric that tracks each (§7 for semis).
3. **News triage (§5).** Check EDGAR submissions first (new 8-Ks and their items), then the company release, then T2 wires. Classify each item, test its novelty and measure the reaction (abnormal return in σ units, ΔIV, Δskew).
4. **What is priced (§3).** Run `equitykit.py dcf` for a reverse DCF; compare multiples with growth and peers; grid WACC × growth or margin. Ask what growth, margin and duration the price needs, and whether that sits inside base rates.
5. **Earnings setup (§4).** Compare the guide, consensus and the company's beat history. Compare the implied move with realized history. Define what the bar really is.
6. **Projection (§6).** Run `equitykit.py projection` for the market-implied distribution against your scenario tree, and read the gap column.
7. **Expression and risk.** Only if the gap is material: choose stock or options (`options-volatility.md` §8, §10), size so that a 1-2 SD event gap is survivable (`risk-sizing-execution.md`; `tradekit.py size`), and name the signposts.

Output order: dated snapshot → drivers → news (new vs priced) → fundamentals table with flags → valuation (what is priced) → earnings setup → projection table (market vs scenarios, gap) → catalyst calendar → view, expression and risk → what would change it. Label any worked numbers as illustrative, not a recommendation.

## 2. Financial statements for traders
For a single stock the price-moving numbers are: (1) revenue growth and its acceleration against guidance, (2) gross and incremental margins, (3) cash conversion, and (4) working capital, which shows a cycle turn before the income statement does. (Pract; Koller, Goedhart & Wessels 2020; Damodaran)

### 2.1 Formula sheet
| Metric | Formula | What it tells you |
|---|---|---|
| Growth | YoY = Rev_q/Rev_{q−4} − 1; QoQ; TTM = Σ last 4 q; acceleration = Δ YoY; guide-implied = guide mid / last q − 1 | The second derivative and the guide drive re-ratings |
| Revenue mix | volume × ASP × mix; organic vs acquired; FX; segment / platform | Which driver the guide relies on |
| Margins | GM = GP/Rev; OM = EBIT/Rev; incremental OM = ΔEBIT/ΔRev; DOL = %ΔEBIT / %ΔRev | GM = pricing power; DOL > 1 = operating leverage, both ways |
| FCF | Street FCF = CFO − capex; owner FCF = CFO − capex − SBC; FCFF = EBIT(1−t) + D&A − capex − ΔNWC | Show FCF and FCF − SBC side by side; use TTM because quarters swing with working capital |
| Cash conversion | CFO / NI (TTM) | Below 0.8 is a flag; find what absorbed the cash |
| Working capital | DSO = AR/Rev_q × 91; DIO = Inv/COGS_q × 91; DPO = AP/COGS_q × 91; CCC = DSO + DIO − DPO | AR or inventory growing faster than sales is a cycle or quality tell |
| Balance sheet | net cash = cash + securities − debt (− leases); EV = mcap + debt + preferred + minority − cash − non-operating investments | Count new debt, guarantees and purchase commitments as off-ratio leverage |
| ROIC | NOPAT / IC; NOPAT = EBIT(1 − cash tax); IC = NWC + net PP&E + intangibles, or debt + equity − excess cash | Compare with WACC; economic profit = (ROIC − WACC) × IC |
| Dilution | Δ diluted shares; buyback yield; buybacks vs SBC | Net issuance predicts lower returns [Moderate] |
| Concentration | top-customer % of revenue and % of AR (10-Q/10-K note) | Demand and credit risk sit with a few buyers |

### 2.2 Earnings-quality red flags, with evidence
| Signal | Evidence | Grade | Status today |
|---|---|---|---|
| High accruals, (NI − CFO)/avg TA | Sloan 1996 (~10%/yr hedge, 1962-91 [SC]); Richardson et al. 2005 (broader NOA accruals predict more strongly) | [Moderate] (PR) | The hedge return largely decayed in the 2000s (Green, Hand & Soliman 2011). The information about earnings persistence survives |
| AR or inventory growing faster than sales; GM falling; SG&A rising vs sales | Lev & Thiagarajan 1993; Abarbanell & Bushee 1997/98 [SC]; Thomas & Zhang 2002 (inventory is the key accrual) [SC] | [Moderate] (PR) | Cheap from EDGAR; best used to forecast the next prints |
| Bloated balance sheet (high NOA/TA) | Hirshleifer, Hou, Teoh & Zhang 2004 | [Moderate] (PR) | Long-run negative returns |
| Cash-based operating profitability | Ball et al. 2016 (subsumes accruals); Novy-Marx 2013 (gross profitability, holds in large caps) | [Strong] (PR) | The most robust quality signal, including in large caps |
| Beneish M-score > −1.78 (practitioners use −2.22) | Beneish 1999; Beneish, Lee & Nichols 2013 (predicts lower returns; magnitude [SC]) | [Moderate] (PR) | A manipulation veto, not alpha |
| Piotroski F-score | Piotroski 2000 (~23%/yr high-minus-low within value [SC]) | [Moderate] (PR) | Concentrated in small, cheap, under-followed firms; little expected edge in mega-caps. No 2024-26 large-cap test found |
| Net share issuance | Pontiff & Woodgate 2008; Daniel & Titman 2006; buyback announcements are followed by positive drift (Ikenberry et al. 1995) | [Moderate] (PR) | |

Anomaly returns are ~26% lower out of sample and ~58% lower after publication (McLean & Pontiff 2016) [Moderate][SC]. Read these as diagnostics, not alpha.

```
Beneish M = −4.84 + 0.920·DSRI + 0.528·GMI + 0.404·AQI + 0.892·SGI + 0.115·DEPI − 0.172·SGAI + 4.679·TATA − 0.327·LVGI   [K][SC coefficients]
DSRI = (AR/Sales)_t / (AR/Sales)_{t−1}; GMI = GM_{t−1}/GM_t; SGI = Sales_t/Sales_{t−1}; TATA = (income from cont. ops − CFO)/TA
```

**Flag rule** (Pract; a combination from the notes, not itself tested). Raise a quality flag when two or more hold:
- TTM CFO/NI < 0.8;
- ΔDSO > +10 days QoQ;
- inventory growth > revenue growth for 2+ quarters;
- GM guided down outside a known product ramp;
- non-operating income > 10% of pre-tax income;
- M-score > −1.78.

Response: raise the evidence bar and size down. Name the benign explanations (ramp timing, payment terms on large contracts, prepayments) and the print that will tell them apart.

### 2.3 SBC, dilution, non-operating income, non-GAAP drift
- **SBC is an economic expense** (Damodaran; Mauboussin & Callahan [SC date]). Street FCF adds it back implicitly. Either subtract SBC and use current diluted shares, or value the options and use future diluted shares. Never do both, which double counts. `equitykit.py dcf --sbc` takes the first route. SBC is small for NVDA (2.4% of revenue) but often 10-25% of revenue in software and internet [SC].
- **Strip non-operating gains** (investment marks) from run-rate earnings; use EV/EBIT or operating EPS. NVIDIA's Q1 FY27 GAAP net income ($58.3bn) exceeded operating income ($53.5bn) because of $15.9bn of investment gains [V].
- **Non-GAAP definitions move.** From Q1 FY27, NVIDIA's non-GAAP no longer excludes SBC, and history was restated. Older non-GAAP series are not comparable [V].

### 2.4 Reading `fetch.py fundamentals`
- **The printed table** shows revenue, YoY/QoQ, GM, OpM, net income, diluted EPS, FCF, FCF%, inventory days and DSO. The summary gives TTM revenue, NI, FCF, EPS, SBC and buybacks, diluted shares, and cash + securities − debt.
- **The `--out` CSV** has every quarter, with raw AR, inventory, CFO, capex, R&D and debt. Compute CFO/NI from its `cfo` and `net_income` columns.
- **Derived values.** Q4 = FY − 9M, and YTD cash-flow items are de-cumulated. XBRL is as filed: restatements and segment detail are not applied.
- **Distortions.**
  - Charges booked in COGS distort DIO. NVDA Q1 FY26 shows 59 days because of the $4.5bn H20 charge, against ~115 days in surrounding quarters.
  - Quarterly FCF% swings with working capital (NVDA 59.5% → 22.2% in one quarter). Use TTM.
- **Not in the output:** segments, customer concentration, the non-operating split, purchase commitments. Read the 10-Q for those.
- **Coverage.** About 45 large caps are in the built-in CIK map. Others need `--cik` or `SEC_USER_AGENT`.

### 2.5 EDGAR mechanics and pitfalls [V] (Pract)
- **Endpoints** (no key; no CORS; declare a User-Agent with contact details; ≤ 10 requests/s):
  - `data.sec.gov/submissions/CIK##########.json` for filings with `form`, `items` and `acceptanceDateTime`;
  - `data.sec.gov/api/xbrl/companyfacts/CIK##########.json` for all XBRL facts;
  - `companyconcept` and `frames` for one tag or one calendar period across firms.
  - Use a 10-digit zero-padded CIK, from `www.sec.gov/files/company_tickers.json`.
- **`fy`/`fp` describe the filing, not the fact.** NVIDIA's FY2026 10-K re-reports FY2024 revenue with `fy=2026`. Key durations on (`start`, `end`) and instants on `end`.
- **Duplicates and restatements.** NVIDIA's Revenues tag had 280 entries for 121 distinct periods, and 9 periods carry more than one value (rounding, restatements). EPS must be split-adjusted (4:1 in Jul 2021, 10:1 in Jun 2024 [K]).
  - For point-in-time backtests keep the earliest `filed`. For valuation keep the latest.
  - Frames use the last-filed value, so they contain look-ahead.
- **Classify durations by length:** 84-98 days = quarter, ~182 = 6M, ~273 = 9M, 357-371 = FY.
  - Cash-flow items are YTD-only in 10-Qs: Q2 = 6M − 3M, Q3 = 9M − 6M, Q4 = FY − 9M.
  - No standalone Q4 is filed. NVIDIA's Q4 FY26 revenue = 215.938 − 147.811 = $68.127bn.
- **Calendar frames shift fiscal labels.** NVIDIA FY2026 (Feb 2025-Jan 2026) is frame `CY2025`. Align peers by period-end dates, never by fiscal labels.
- **Tag drift needs fallback lists.** NVIDIA examples:

  | Item | Current tag | Older / alternate |
  |---|---|---|
  | Revenue | `Revenues` | `RevenueFromContractWithCustomerExcludingAssessedTax` (to FY2022), `SalesRevenueNet` (pre-ASC 606) |
  | Capex | `PaymentsToAcquireProductiveAssets` | `PaymentsToAcquirePropertyPlantAndEquipment` (most common market-wide [K]) |
  | Securities | `AvailableForSaleSecuritiesDebtSecurities` (from Jan 2026) | `MarketableSecuritiesCurrent`, `MarketableSecurities` |
  | COGS / D&A | `CostOfRevenue` / `DepreciationDepletionAndAmortization` | `CostOfGoodsAndServicesSold` / `DepreciationAndAmortization` |
  | Commitments | `PurchaseObligation` (stops after Jul 2025) | text only since |

- **What companyfacts lacks.** It excludes dimensional facts: segments, market platforms, geography, customer concentration (`ConcentrationRiskPercentage1`). Get them by parsing the filing's XBRL instance (via `Archives/edgar/data/{cik}/{accession}/index.json`, `FilingSummary.xml`, `R*.htm`) or the HTML. Press-release (Ex. 99.1) numbers and guidance are HTML only.
- **Timing.**
  - `acceptanceDateTime` is UTC; convert it to America/New_York. After 16:00 = AMC, before 09:30 = BMO.
  - Do not use `filingDate`: filings after ~17:30 ET carry the next business day's date.
  - NVIDIA's 10-Q follows its 8-K ~15 minutes later, but at many firms the 10-Q comes days or weeks later. A same-night beat/miss cannot rely on companyfacts.
  - Item 2.02 also captures pre-announcements (NVIDIA 8 Aug 2022, 09:16 ET, BMO).

## 3. Valuation

### 3.1 DCF mechanics (Pract; Koller et al. 2020; Damodaran 2012)
```
EV        = Σ_{t=1..N} FCFF_t/(1+WACC)^t + TV_N/(1+WACC)^N        (mid-year: exponent t − 0.5)
Equity    = EV + cash & non-operating assets − debt − leases − minority − options/dilutive claims
Gordon TV = FCFF_{N+1}/(WACC − g)
Value-driver TV = NOPAT_{N+1}·(1 − g/RONIC)/(WACC − g)      (reinvestment rate = g/RONIC; RONIC = WACC → growth adds 0)
Exit-multiple TV: back out implied g = (TV·WACC − FCFF_N)/(TV + FCFF_N); reject g > risk-free or nominal GDP
WACC = E/V·k_e + D/V·k_d·(1−t);  k_e = r_f + β·ERP (+ CRP);  β_U = β_L/[1 + (1−t)D/E]
Justified EV/Sales = m(1−t)(1 − g/ROIC)/(WACC − g);  justified fwd P/E = (1 − g/ROE)/(r − g)
Duration (Gordon) = −∂lnP/∂r = 1/(r − g)
```

### 3.2 Defaults
| Input | Default | Source / note |
|---|---|---|
| Risk-free | Current 10-yr Treasury: 4.88% on 9 Nov 2026; 10-yr real 2.66% | FRED via `market-context-2026.md` §4 [Strong]. Damodaran's page shows a 5.29% "T-bond rate" that looks like a pre-tax cost of debt; do not use it as r_f unchecked [SC] |
| ERP | Implied ERP 4.41% (1 Nov 2026) | Damodaran monthly implied ERP [V][SC]; prefer the implied figure to historical averages |
| WACC by industry (Jan 2026) | Semis 10.55% (β 1.52, stock SD 55.8%); semi equipment 9.89%; software 9.34%; computers 9.71%; market ex-financials 7.72% | Damodaran wacc.html, updated 9 Jan 2026 [V] |
| Terminal growth | ≤ risk-free and ≤ long-run nominal GDP; 2.5-3% typical | Damodaran stable-growth rule (Pract) |
| Terminal ROIC | = WACC unless there is a defensible moat, then modestly above | Damodaran (Pract) |
| Explicit horizon | 5 yrs for stable firms, 10 (to 15) for high growth, so growth fades before the TV | (Pract) |
| TV share of EV | 60-80%+ is common for growth firms [K][SC]; above ~70%, the price rests on the far future | `equitykit dcf` prints it |
| R&D, SBC | Expense SBC; capitalize R&D for tech/pharma ROIC (amortize 3-10 yrs by industry [SC]) | Damodaran (Pract) |
| Beta, terminal phase | Moves toward 1, and cost of capital toward market-like levels | Damodaran (Pract) |

### 3.3 Reverse DCF / expectations investing (Mauboussin & Rappaport 2021) (Pract)
1. **Invert the model.** Solve for the growth, margin and competitive-advantage period (market-implied forecast period, MIFP) that equate value to price. `equitykit.py dcf` solves for the starting FCF growth that fades linearly to terminal over `--years`. It prints implied FCF in years 5 and 10, implied revenue (`--fcf-margin`) and the TV share, plus a forward grid (WACC ±1pt × `--growth`).
2. **Test plausibility against base rates.** Few firms sustain high growth for 5-10 years, and growth rates show little persistence beyond chance (Chan, Karceski & Lakonishok 2003) [Strong]. Profitability mean-reverts (Fama & French 2000) [Moderate]. The highest analyst long-term-growth stocks underperform (La Porta 1996; Bordalo et al. 2019) [Moderate].
3. **Find the "turbo trigger"**, the driver most likely to be revised (usually sales), and trace it through volume, price/mix and operating leverage. Act only when the expected revision gives a margin of safety.
4. **Decompose the price.** Value = NOPAT/WACC (steady state) + PVGO. A large PVGO share means the price is a bet on growth duration.
5. **Grid the inputs.** Cross WACC with margin, or terminal g with ROIC: these dominate growth-stock values. For NVDA, 1pt of WACC moves the implied growth 4-5pt (§8).
- **The FCF base matters.** A working-capital-depressed FCF (NVDA Q2 FY27) raises the implied growth versus a NOPAT-based model. Show which base you used.

### 3.4 Multiples
| Multiple | Use when | Trap |
|---|---|---|
| Forward P/E (NTM) | Profitable, stable capital structure | Approximates prices best (Liu, Nissim & Thomas 2002) [Moderate]; exclude non-operating gains; GAAP vs Street |
| EV/EBIT, EV/NOPAT | D&A ≈ capex; cross-capital-structure comparison | Lead with this for NVDA-type stocks, plus FCF − SBC yield |
| EV/EBITDA | Capital-intensive firms | Misleads when capex or SBC are large |
| EV/Sales | Unprofitable, early-stage, or trough margins | Worst accuracy of the common multiples (LNT 2002); use only growth- and margin-adjusted |
| FCF yield | Cash-generative firms | Use FCF − SBC; use TTM |
| PEG | Quick screen | Valid only under restrictive assumptions (Easton 2004) [Moderate]; "PEG ≈ 1 is fair" is [Lore]; "Rule of 40" is a software heuristic [Lore] |

- **Comparables.** Use the same end markets and business model; industry peers work about as well as matching on risk and growth (Alford 1992 [SC]). Use NTM figures and align fiscal calendars (NVIDIA's year ends in January). A cross-section regression of EV/Sales or EV/EBIT on growth and margin shows the residual mispricing.
- **"Is it cheap, or is the E wrong?"** A falling multiple with rising forward EPS means the market doubts the EPS durability. Argue about the E before you call the stock cheap.

### 3.5 When valuation matters
| Horizon | What drives one stock | Valuation's role | Evidence |
|---|---|---|---|
| Days to months | Cash-flow news, guidance, catalysts, flows | Close to none for timing | Vuolteenaho 2002: firm-level cash-flow news variance ~2× expected-return news [SC] [Moderate] |
| Around earnings | Expectations meeting results | Value/glamour gaps resolve here | La Porta et al. 1997: ~25-30% of the value-glamour spread is earned in announcement windows [SC] [Moderate] |
| 3-5+ years | Base rates of growth and margins; starting multiple | Sets expected return | Lakonishok, Shleifer & Vishny 1994 [Moderate]; aggregate valuation forecasts long-horizon returns (Cochrane 2011) [Strong] |
| Rates shocks | Discount-rate news for long-duration growth stocks | Duration = 1/(r − g) | r − g = 2.5% → duration ~40 yrs, so +50bp ≈ −18-20%; r − g = 6% → ~−8% [derived]. High-duration stocks earn lower returns (Dechow, Sloan & Soliman 2004; Weber 2018 [SC]; Gormsen & Lazarus 2023) [Moderate] |

- **Rule:** never present "undervalued/overvalued" as a near-term signal for one stock. Express it as (a) implied expectations that upcoming prints will confirm or refute, and (b) a multi-year expected return given base rates. For value, quality and profitability as portfolio factors see `strategy-playbook.md` §5-6.

## 4. Earnings and estimates

### 4.1 What moves the stock on the day
- **Order of importance** (Hand, Laurion, Lawrence & Martin 2022, RAST) [Moderate] (PR):
  1. Next-quarter sales-guidance surprise.
  2. Analyst sales surprise.
  3. Annual Street EPS guidance surprise.
  4. Street EPS surprise.

  Thirteen surprise variables together explain only a single-digit share of announcement returns (adjusted R² ~2.8% → 7.7% [V-snip][SC]). Tell users that perfect knowledge of the numbers still leaves the sign of the move uncertain.
- **Guidance news dominates earnings news** at bundled announcements (Milian 2018) [Moderate]. The penalty for a guide-down exceeds the reward for a beat (Rees & Twedt 2010, WP) [Weak].
- **Variance shares** [K][SC]: management forecasts ~55% of the accounting-explained share of quarterly return variance, analyst forecasts ~22%, earnings releases ~16% (Beyer, Cohen, Lys & Walther 2010).
- **The call.** Q&A carries more information than the presentation (Matsumoto, Pronk & Roelofsen 2011) [Moderate].
- **Analysis order:** guide vs consensus → revenue → FY guide → EPS → segment KPIs and call. Express each surprise as a % of consensus and in SD units of the stock's own surprise history.

### 4.2 Base rates and the real bar
- **S&P 500 Q3 2026** (FactSet, 6 Nov 2026, 88% reported) [V] (Pract):
  - EPS beat rate 84% (5-yr average 78%, 10-yr 77%).
  - Aggregate EPS surprise +2.7% (5-yr +7.5%), the smallest since Q4 2022.
  - Revenue beat rate 74% (5-yr 70%).
- **The expected beat is the benchmark.** A +3% EPS beat is roughly a non-event, or a disappointment. Compare it with the company's own beat history against its guide.
- **Walk-down.** Forecasts start optimistic and are walked down to beatable levels (Richardson, Teoh & Wysocki 2004; Matsumoto 2002) [Moderate].
- **Whispers** proxied market expectations better than First Call in a small tech-heavy sample (Bagnoli, Beneish & Watts 1999). Consensus is more accurate on broader samples, though whispers add information (Brown & Fernando 2011). Crowdsourced Estimize adds information to I/B/E/S (Jame et al. 2016). Overall [Contested]; vendor accuracy claims are [Lore].

### 4.3 PEAD status
- **Dead in large caps** [Moderate]: prices absorb the surprise on the announcement day, and large-stock PEAD has been "non-existent since 2006" (Martineau 2022, CFR).
- **The 2025 "PEAD is back" papers** (Dickerson-Julliard-Mueller; Hirshleifer-Peng-Wang 2025 RFS) rest on microcaps and nonstandard factor construction. Subrahmanyam 2025 (WP) finds t = 1.43 ex-microcaps for Feb 2001-Dec 2024. Overall [Contested], but not for mega-caps.
- **Skill rule:** treat the reaction-day close as the new anchor. Do not forecast single-stock drift in large caps; equitykit's next-5-day drift column is descriptive only.
- **Announcement premium:** Savor & Wilson 2016 find 9.9% annualized for scheduled announcers, ~4bp/day, which is negligible against event SDs of 4-10%. Barber et al. 2013 attribute it to attention [Contested]. Ignore it for a projection's centre.
- **Inattention:** Friday and busy-day announcements see slower absorption (DellaVigna & Pollet 2009; Hirshleifer, Lim & Teoh 2009) [Moderate], mostly in smaller names.

### 4.4 Revisions, targets, dispersion
- **Revisions.**
  - Returns drift after consensus revisions (Stickel 1991). Earnings momentum and price momentum each predict returns (Chan, Jegadeesh & Lakonishok 1996). Innovative revisions (away from consensus) and less-followed firms carry more information (Gleason & Lee 2003) [Moderate].
  - Revision breadth (N_up − N_down)/N over 30-90 days is a practitioner signal with no canonical definition. It needs point-in-time data (paid) (Pract).
- **Targets are optimistic point forecasts.**
  - 38% are met at 12 months and 64% at any time within them. Mean absolute error is 45%, and target-implied returns exceed realized by ~15pt (Bradshaw, Brown & Huang 2013; 2000-09) [Moderate].
  - Targets average 28% above price (Brav & Lehavy 2003).
  - Target revisions draw significant reactions, and the strength of the justification matters more than the valuation method (Asquith, Mikhail & Au 2005) [Moderate].
- **Recommendations.** Consensus-recommendation strategies earn >4%/yr gross but ~0 net of costs (Barber et al. 2001) [Moderate]. The change predicts better than the level (Jegadeesh et al. 2004).
- **Dispersion.** High EPS-forecast dispersion predicts lower returns, strongest in small stocks (Diether, Malloy & Scherbina 2002) [Moderate].
  - Targets herd (Welch 2000; Hong, Kubik & Solomon 2000), so their range usually understates uncertainty. When the target range is narrower than the option-implied 1-yr 80% band, the options are more honest.
- **How to quote a target.** Give the median and the distribution (min / p25 / median / p75 / max) and haircut the implied return by ~15pt. For example: "the median implies +18%; historically ~38% of targets are met at 12 months."

### 4.5 Earnings-day volatility: implied vs realized
Extraction formulas (straddle, event variance, two-expiry method) are in `options-volatility.md` §4 and §10. Here: the evidence and how to read the toolkit.

| Source | Sample | Finding | Grade |
|---|---|---|---|
| Gao, Xing & Zhang 2018 (JFQA) | All stocks, academic period | Pre-earnings straddles earned +3.34% on average, concentrated in small, illiquid names | [Moderate] (PR) |
| Dubinsky et al. 2019 (RFS) | Options panel | Option prices embed a time-varying earnings-jump component that predicts realized vol | [Moderate] (PR) |
| Alexiou, Goyal, Kostakis & Rompolis 2025 (RoF) | Options panel | Concave pre-earnings IV curves = bimodal density; larger subsequent moves, but lower straddle returns | [Moderate] (PR) [V-snip] |
| IVolatility (vendor) | S&P 500, Feb 2021-Feb 2026, 9,651 events | Median implied 4.14% vs realized 3.32%; long straddles won 22%, mean −18.5%; mean IV crush 15.6 vol pts; NVDA "overpriced" (−8.1% mean straddle) | [Weak] (Pract) [V]: circular, no costs |
| EarningsWatcher (vendor) | 28,898 US reports, 2023-Sep 2026 | Large caps 7.86% implied vs 6.78% close; 36.4% closed beyond, 56.3% beyond at the intraday peak; AI complex 8.77% vs 8.64%; overpricing grows with the size of the priced move | [Weak] (Pract) [V] |

- **Reconciliation** [Contested]: academic averages say slightly *under*-priced (small, illiquid names); 2021-26 large-cap vendor data say ~1pt *over*-priced at close-to-close, with large dispersion name by name (META, PLTR, NFLX historically cheap; NVDA, AAPL mildly rich). Use the name's own history, not a universal rule.
- **Benchmarks** [Computed]:

  | Implied quoted as | Fair P(\|move\| > implied), normal | Laplace (fat tails) | Compare with |
  |---|---|---|---|
  | Expected \|move\| (straddle/spot) | 42.5% | 36.8% | mean \|move\| (fair ratio ~1.0) |
  | 1 SD (= 1.25 × straddle) | 31.7% | 24.3% | SD or RMS of moves |

  Kurtosis proxy mean(r²)/mean(|r|)² = π/2 ≈ 1.57 under normality; higher means fat tails.
- **`equitykit.py earnings` reads.**
  - The reaction runs from the close before the information to the first close after it (AMC → next session), with the gap and next-5-day drift, raw and not market-adjusted.
  - It compares the mean |move| with the implied expected |move|: `--straddle/--spot`, or `--implied` as an E|move|. `--implied-is-sd` converts a 1-SD figure ×0.798.
  - It labels the result rich (< 0.85×), in line, or cheap (> 1.15×), and reports the exceedance rate against 42%/37%.
- **Before concluding "rich":**
  1. **Ask which convention the quoted move uses.** Vendors often quote straddle/spot but call it "±X%".
  2. **Strip base vol.** A straddle spanning several days includes ordinary diffusion. Event variance ≈ total − σ_base² × (non-event days). With 50% base vol and five non-event days this changes the answer materially (§8.5).
  3. **Look at what history lacks.** A new governance or regulatory overhang is uncertainty the past 8-25 releases do not contain.
  4. **Count costs and the intraday path.** Spreads and the 43-56% intraday-peak exceedance matter for stops and short gamma.
- **IV crush:** post-event front IV ≈ σ_base. A long straddle held through the event pays only if |move| > ~m_e + the lost base time value. Pre-event IV ramp trades are a different trade from holding through the jump.

### 4.6 Data
- **Free** [V]: EDGAR 8-K times and press releases (company guidance is primary and free), FactSet Earnings Insight aggregates, Yahoo (unofficial).
- **Paid** [K][SC]: consensus and revisions (I/B/E/S, FactSet, Capital IQ, Visible Alpha); historical options (OptionMetrics, ORATS, Cboe). Never sign up for or spend on a paid feed without the user's explicit go-ahead.
- **Archive point-in-time snapshots going forward.** Take daily consensus, the next date and the pre-event straddle, with retrieval timestamps. Back-filled consensus is look-ahead.

## 5. News triage
Prices move on genuinely new, fundamentals-related news within seconds to a day in large caps (Busse & Green 2002 [SC]; Boudoukh et al. 2019 [K][SC]) [Moderate]. Stale or reprinted news moves prices temporarily and reverses, mainly via retail trading (Tetlock 2011) [Moderate]. Drift after news is concentrated after *bad* news and in small, illiquid stocks (Chan 2003) [Moderate].

**LLM sentiment.**
- GPT-4 scores hit ~90% on the direction of the *initial* reaction, which is untradeable. Their drift prediction is strongest in small stocks and negative news, and returns decline as LLM adoption rises (Lopez-Lira & Tang, v6 Oct 2025, WP) [Moderate]. Ke, Kelly & Xiu (WP) find predictability concentrated in the first 1-2 days [SC].
- The skill's comparative advantage in mega-caps is classification, novelty detection and fact/narrative separation, not sentiment alpha. Strategy returns are in `strategy-playbook.md` §15.

**Source tiers** (Pract synthesis; no validated weighting exists)

| Tier | Sources | Treatment |
|---|---|---|
| T1 primary | SEC filings (8-K, 10-Q/K, proxy), company release / Ex. 99.1, call transcript, regulator or court documents, exchange notices | A fact once read in the document itself |
| T2 | Reuters, Bloomberg, Dow Jones/WSJ, FT, AP with named sourcing | Likely fact; confirm numbers against T1 when it appears |
| T3 | Trade press, sell-side summaries, "people familiar" reports | A probability, not a fact |
| T4 | Social media, blogs, aggregator or AI-written rewrites | Lead only; never an input |

**8-K items as a first-pass classifier** [K] (SEC Form 8-K instructions)

| Item | Event | Item | Event |
|---|---|---|---|
| 1.01 / 1.02 | Material agreement entered / terminated | 4.01 | Auditor change |
| 1.03 | Bankruptcy | **4.02** | Non-reliance on prior financials (restatement) |
| 2.01 | Completed acquisition or disposal | **5.02** | Officer or director departure or appointment |
| **2.02** | Results of operations (furnished, usually at release) | 5.07 | Shareholder vote |
| 2.03 | New direct financial obligation | 7.01 | Reg FD (often guidance) |
| 2.05 / 2.06 | Restructuring costs / material impairment | 8.01 / 9.01 | Other events / exhibits (99.1 = release) |

Restatements (4.02), guidance cuts and CEO or CFO exits are the high-information negative classes [K].

**Procedure**
1. **Timestamp and dedupe.** Find the first public time: the EDGAR `acceptanceDateTime` or the wire time.
   - Test novelty against the last ~10 stories on the firm, Tetlock-2011 style: text similarity, or the question "is there any fact not in prior coverage?".
   - A stale story gets no directional weight, and a mild contrarian flag if the price moved on it.
2. **Tier the source** (table). Until a T1 or T2 source confirms a T3/T4 claim, it changes variance, not the cash-flow model.
3. **Classify the event**: earnings or guidance; product; customer or contract (1.01/1.02); regulatory; legal; M&A or capital (2.01/2.03); management (5.02); accounting (4.01/4.02); analyst action; read-through; flow (index changes, lock-ups). Attach a prior |move| from the stock's own history of that class (`eventkit.py study` for dated events).
4. **Separate facts from narrative.**
   - Facts: numbers, dates, binding decisions, signed contracts, filed suits, rulings.
   - Narrative: "could/may", unnamed sources, move rationalizations ("fell on fears of...").
   - Facts update the model. Narrative updates variance and reversal risk (Tetlock 2007).
5. **Priced-in test.**
   - Abnormal return since the first timestamp: `ar = r − β·r_mkt` (or minus the sector ETF), in units of daily idiosyncratic σ.
   - Options: ΔATM IV for the affected expiries, Δ25-delta risk reversal, and option volume against its 20-day average.
   - Peers: did read-through names move?
   - If |ar| already matches the class-typical move and IV has repriced, call it priced. Residual edge exists only if the facts differ from the market's apparent reading.
   - A large move with no identifiable news: a reversal candidate in small caps (Chan 2003). In a mega-cap, assume information you have not found yet.
6. **Direction asymmetry.** Drift after bad news is better documented. In mega-caps, expect most incorporation within the day.
7. **Output**: class, novelty, tier, fact list, narrative list, reaction (ar in σ, ΔIV, Δskew), a "priced?" probability, and the projection update (centre shift, variance change, a new jump date).

**Rumor vs filing, the teaching pair (NVIDIA 2026)** [Strong for the filings]:
- **27 Jul 2026, T2 report.** WSJ, Bloomberg and Reuters reported talks on a **~$250bn** guarantee for OpenAI's 10-GW Ohio campus. NVDA fell ~4.5% that day per one report [Moderate].
- **17 Aug 2026, 8-K.** The definitive version was residual-value guarantees to SB Energy for ~4.25 GW, **"cumulatively capped at $105 billion"**.
  - They are triggered only by OpenAI insolvency or non-payment. OpenAI indemnifies NVIDIA, and the obligations end if OpenAI reaches a satisfactory credit rating.
  - They phase in from FY2029. Total maximum guarantee exposure is $108.5bn.
- **Lesson.** The press number was 2.4× the filed cap and described a contingent, phased, indemnified exposure as if it were funded. Model the filed terms.
- **The same applies to bear arithmetic.** A third party's "$165bn AI financing exposure" ≈ $108.5bn guarantees + $36bn cloud-service commitments + $20bn leases [Derived, unconfirmed]. Mostly contingent, not debt.

**Filings before headlines (12 Nov 2026)** [Strong, verified against EDGAR].
- NVIDIA filed an 8-K (Item 5.02) at **08:52 ET on 12 Nov 2026**. On 11 Nov the board had accepted Jensen Huang's resignation as President, CEO and director, effective immediately.
- CFO Colette Kress became interim CEO and remains CFO. Harvey C. Jones was appointed the first-ever board Chair. No reason was given.
- Web-search summaries that day still reported no resignation. The stock opened ~13% lower: the 8-K was BMO, so the open was the first tradable reaction.
- **Rule:** before analysing any stock, pull `data.sec.gov/submissions/CIK##########.json` and scan new 8-Ks and their `items` since the last snapshot.

## 6. Projection as a distribution

### 6.1 Formula sheet [K, standard]
```
Lognormal quantile:  S_q = S0·exp((μ − q − ½σ²)T + z_q·σ√T);   P(S_T > K) = N(d2), d2 = [ln(S0/K) + (μ − q − ½σ²)T]/(σ√T)
  risk-neutral μ = r;  physical (Pract) μ = r + β·ERP;  CRRA tilt p(S) ∝ q(S)·S^γ shifts the log-mean by γ·s², variance unchanged
Event-aware variance: Var(ln S_T/S0) = σ_base²·(T − n_E·τ) + Σ_k s_e,k²     (n_E prints in horizon; next = implied s_e, later = historical RMS)
Jump-diffusion MC:   ln S_T = ln S0 + (μ − ½σ_base²)T − Σ ln E[e^J_k] + σ_base√T·Z + Σ J_k
  J ~ N(0, s_e²) | bootstrap own past moves × s_e/RMS_hist | bimodal ±m + noise when the IV curve is concave
Skew tail:           P_Q(S_T < K) = N(−d2(σ(K))) + K√T·n(d2)·σ'(K)    (or Breeden-Litzenberger: q(K) = e^{rT}·∂²C/∂K²)
Physical vol:        σ_P ≈ σ_IV × k, k = the name's own median RV/IV ex-earnings (≈1 for single names); never apply the index VRP to the jump
Scenario mixture:    m = Σ p_i·m_i;  V = Σ p_i(s_i² + m_i²) − m²   → compare √V with IV; explain or widen if √V << IV
Vol cone:            RV_w for w ∈ {10,21,42,63,126,252}: min/p10/p25/p50/p75/p90/max, all-days and ex-earnings; overlay the IV term structure
```

### 6.2 Risk-neutral vs physical
- Option-implied vol is an informative but upward-biased forecast, and implied densities need a risk adjustment (Christoffersen, Jacobs & Chang 2013) [Moderate].
- Single-name options carry little variance premium, unlike index options (Driessen, Maenhout & Vilkov 2009; Bakshi & Kapadia 2003) [Moderate].
- Risk-transformed option densities forecast best at 2-4 weeks, and historical densities win at 1 day (Shackleton, Taylor & Yu 2010, index-level) [Moderate]. Blending transformed and historical densities is best (Liu et al. 2007).
- **No mega-cap-specific Q→P estimate exists.** Default to the market distribution, add a modest premium (β·ERP·T, e.g. ~0.5% over 30 days at β 1.5 and ERP 4.4%), and blend in the historical bootstrap beyond ~3 months.

### 6.3 Combination and calibration
- **Combine** (a) the option-derived distribution with (b) your scenario mixture, and optionally (c) a bootstrap. Use equal weights until there are ≥30 scored projections (Stock & Watson 2004: simple averages are hard to beat).
- **A linear pool of calibrated forecasts is over-dispersed.** Recalibrate it, e.g. with a beta-transformed pool (Ranjan & Gneiting 2010) [Strong].
- **Score every projection.**
  - Brier on binary statements, with the Murphy decomposition.
  - Band coverage (50% and 80%) with `z = (x − Np)/√(Np(1−p))`.
  - A PIT histogram, which should be uniform (Diebold, Gunther & Tay 1998).
  - Pinball loss per quantile, and CRPS.
  - Maximize sharpness subject to calibration (Gneiting et al. 2007) [Strong].
- **Over-confidence is the dominant failure.** Verbal mapping: "likely" ≈ 60-75%. Never use 95%+ language on direction beyond a few days.
- **Earnings dominate short horizons.** With 25% base vol and a 6-7% event SD, one print is ~40-50% of a 1-month horizon's variance [Computed], so a 1-month projection is mostly an earnings projection.

### 6.4 Why point targets fail: 1-year lognormal bands [Computed]
Arithmetic expected return +8%. Most CRSP stocks underperform T-bills over their lives, and 4% of firms created all net wealth (Bessembinder 2018) [Strong]. Single-stock outcomes are skewed.

| σ (1-yr) | q05 | q10 | q25 | median | q75 | q90 | q95 | P(loss) | P(within ±10% of median) |
|---|---|---|---|---|---|---|---|---|---|
| 20% | −23.8% | −18.1% | −7.5% | +5.9% | +21.1% | +36.8% | +47.1% | 38.8% | 38.4% |
| 30% | −37.0% | −29.7% | −15.7% | +3.2% | +26.4% | +51.7% | +69.1% | 45.8% | 26.2% |
| 40% | −48.4% | −40.3% | −23.9% | −0.3% | +30.6% | +66.5% | +92.5% | 50.3% | 19.8% |
| 50% | −58.1% | −49.8% | −32.0% | −4.7% | +33.5% | +80.9% | +116.9% | 53.8% | 15.9% |

**Output format:** horizon; q10/q25/q50/q75/q90 for "market-implied" and "our view"; P(up), P(> +X%), P(< −Y%); the next print with its implied move and share of horizon variance; the scenario table (probabilities, drivers); the calibration record (e.g. "our 80% bands covered 76% of 41 scored projections").

### 6.5 Reading `equitykit.py projection`
- **Market-implied column.** A zero-drift, risk-neutral lognormal, rescaled so that E[S_T] = spot exactly (martingale-exact). Its median sits below spot by ~σ²T/2: that is arithmetic, not bearishness. It includes any vol premium and no equity premium.
- **Vol inputs.**
  - `--iv` is the horizon vol. With `--base-iv`, the base IV drives the diffusion and `--iv` is unused, so pass the same number.
  - `--event-move` is a 1-SD jump. `--event-straddle` converts a straddle price at 1 SD ≈ 1.25 × straddle.
  - Only one jump is added. For horizons spanning several prints, fold the later ones into `--iv` with the event-aware variance formula.
  - `--iv-down/--iv-up` split the vol by side, a crude skew.
- **Scenario column.** `scenario,prob,price` at the horizon. Probabilities are normalized (percentages are accepted). Each scenario is smeared by `--scenario-vol` (default 0.6 × base IV, annualized, × √T).
- **Gap column** = P_yours(price > level) − P_market, in points. It, not the probability-weighted price, is the trade idea. A gap under ~5pt is noise given that the probabilities are judgments.
- **Where the edge shows up.** A tree whose mean ≈ spot can still differ in *shape* (fatter left tail, bimodality); that is an options question (§8 in `options-volatility.md`), not a stock question.

## 7. Semiconductor and AI-hardware drivers
Semis are cyclical, and their inventory cycles show late in the income statement. For AI accelerators the dominant cash-flow news is hyperscaler capex. For the macro and AI-capex backdrop see `market-context-2026.md` §8.

| Driver | Metric / source | Read |
|---|---|---|
| End demand | Hyperscaler capex guides and capex/CFO. 2026 (Oct 2026 calls, secondary trackers [V][SC]): MSFT ~$170bn (CY), GOOGL $195-205bn, AMZN ~$220bn, META $135-145bn; combined >$720bn; 2027 guided "significantly"/"meaningfully" higher. Also neocloud and sovereign financing | The forward demand read; definitions differ (cash vs incl. leases) [Contested] |
| Pricing power | GM and the GM guide | A guided dip during a ramp is normal; a dip outside one is a flag |
| Cycle tells | DIO, DSO, customer advances (`ContractWithCustomerLiability`), purchase/supply commitments | DSO up on "extended terms" = vendor-financing fingerprint |
| Supply | TSMC monthly revenue (~10th of each month [K]); CoWoS capacity; HBM supply and pricing; ODM monthly sales (Hon Hai, Quanta, Wistron) | Supply-constrained guides cap upside surprises; lead-time indices are [Lore] |
| Industry | WSTS/SIA monthly sales [K]; SEMI book-to-bill discontinued (2017 [SC]); ASML stopped quarterly bookings from 2026 [SC] | Book-to-bill now comes from commentary, backlog and RPO |
| Policy | Export rules (Oct 2022, Oct 2023, Apr 2025 H20 licence [K][SC]); PRC purchase restrictions; pending bills (GAIN AI, RASA) | Binary-ish; once guidance excludes a market, it is upside optionality |
| Concentration | Top-customer % of revenue and of AR; direct (ODM/OEM) vs indirect (hyperscaler) customers | Hyperscaler demand hides behind ODM lines |
| Cost of capital | Semis WACC 10.55%, β 1.52, stock SD 55.8% (Damodaran, Jan 2026) [V] | DCF default |

**Inventory-cycle checklist** (Pract). A downturn is suggested when several of these hold over 2+ quarters:
1. Inventory grows faster than revenue (DIO up).
2. DSO is up, or customer advances are down.
3. GM is guided down outside a known ramp.
4. Sequential growth decelerates while supply commitments keep rising.
5. Customers' next-year capex guides flatten.
6. Lead times shorten or memory spot prices fall.

**NVIDIA cycle history** [K][SC]:
- Calendar 2018: a crypto-driven gaming channel glut, then the Nov 2018 guide-down and a ~50% drawdown.
- Calendar 2022: a gaming correction, with the 8 Aug 2022 pre-announcement [V timestamp] and an inventory charge.

## 8. Worked example: NVDA as of 11-12 Nov 2026
*Illustrative method, not a recommendation. Every number is dated. Refresh before reuse. Sources: EDGAR companyfacts and filings [Strong]; Yahoo via `fetch.py prices` [Moderate]; third-party trackers as tagged.*

### 8.1 Snapshot
| Item | Value | Date | Source / type |
|---|---|---|---|
| Close | $173.73 | 11 Nov 2026 | Yahoo, `fetch.py prices` [V] |
| 12 Nov session | Open $150.99, low $148.80 (52-wk low), ~$165.2-165.5 midday | 12 Nov, intraday | Yahoo [V][Moderate] |
| Record close / 52-wk high | $239.24 (6 Oct) / $243.37 intraday | 2026 | Yahoo [Moderate] |
| YTD | −6.9% vs NDX +12.4% | to 11 Nov | [Derived] |
| Realized vol | 10d 65.0%, 20d 52.8%, 60d 42.9%; EWMA(0.94) 54.2%; 7-yr Yang-Zhang 50.7% | to 11 Nov | [Derived]; `tradekit vol` [Computed] |
| Q2 FY27 (qtr to 26 Jul; reported 26 Aug) | Revenue $96.2bn (+106% y/y, +17.9% q/q); Data Center $89.0bn (+117%); GM 75.0%; OM 66.2%; NI $59.7bn; GAAP EPS $2.46, non-GAAP $2.22 (incl. SBC) | 26 Aug 2026 | 10-Q, CFO commentary [Reported][Strong] |
| TTM (to 26 Jul) | Revenue $303.0bn; NI $192.9bn; EPS $7.91; FCF $127.0bn; SBC $7.24bn; buybacks $55.3bn; net cash $36.0bn; diluted shares 24.285bn | 26 Jul 2026 | `fetch.py fundamentals` [V] |
| Q3 FY27 guide | Revenue $108.0bn ±2%; GM 74.0% ±50bp; GAAP opex ~$9.2bn; no China DC compute | 26 Aug 2026 | [Guidance][Strong] |
| Guide track record | Beat the midpoint by +5.6%, +4.8%, +4.6%, +5.7% (Q3 FY26-Q2 FY27) | | [Derived][Strong] |
| Consensus | Q3 revenue ~$109.0bn, EPS $2.47 (two aggregators); Q4 revenue $123.9bn | ~early Nov | [Consensus] [Moderate]; Q4 [Weak, single-source] |
| Next print | **Tue 17 Nov 2026, ~1:20pm PT (AMC)**, call 2pm PT; first reaction 18 Nov; first monthly expiry after it 20 Nov | 12 Nov | 8-K Ex. 99.1 [Strong]; calendars showing 18, 19 or 25 Nov were wrong |
| Implied event move | ±10.8% (12 Nov), up from ±7.9% (3 Nov); convention unclear | 12 Nov | EarningsWatcher [Weak, single-source] |
| Multiples at $173.73 | Trailing GAAP P/E ~22.0x; ~17.6x on Q3 consensus EPS ×4; P/S ~13.8x trailing, ~9.7x on the guide annualized ($432bn); FCF yield ~3.0%; forward P/E ~14 (FactSet, ~5 Nov) | 11 Nov | [Derived]; FactSet [Moderate, single-source] |
| Targets | Pre-shock average $304.73 (late Aug); Citi $285→$225, Aletheia to Hold and $340 withdrawn (~9-12 Nov); range up to $515 | Aug-Nov 2026 | [Opinion] [Weak-Moderate]; stale |
| Leadership | Huang resigned as President, CEO and director (accepted 11 Nov, effective immediately); Kress interim CEO and still CFO; Harvey C. Jones first-ever Chair; no reason given; internal and external search | 8-K 5.02, 12 Nov 08:52 ET | [Strong, verified on EDGAR] |
| Context | 5 Nov −9.3% (AI-financing and post-midterm selloff); 8 Nov board investigation of the CEO (allegations, not findings); 9 Nov −4.3% | Nov 2026 | Press [Moderate] |

### 8.2 Fundamentals read and flags (Q2 FY27, 26 Jul 2026) [V-calc]
- **Strength.** Revenue doubled at a ~75% GM. DOL ≈ 1.17 (operating income +124% vs revenue +106% y/y); incremental OM 71%. ROIC ≈ 85% (rough) vs a ~10.5% WACC.
- **Deceleration.** Sequential growth ran 22% → 20% → 20% → 18%, and the guide implies ~12%. Fast, but the second derivative is negative.
- **Flags that fire** (≥2, so raise the bar and size down):
  - TTM CFO/NI 0.70 (Q2 alone 0.40).
  - DSO 45 → 60 days, "extended payment terms on large, multi-quarter agreements".
  - Inventory $25.8bn → $31.6bn (+22% q/q) ahead of Rubin.
  - GM guided −100bp, though a ramp quarter.
  - Non-operating gains: $15.9bn in Q1 and $7.8bn in Q2.
- **Off-ratio leverage.** Supply commitments rose $119bn → $279bn in one quarter (mostly memory). $25bn of new notes. $47.9bn of non-marketable stakes. Max guarantees of $108.5bn and $36bn of cloud-service commitments.
- **Concentration.** One direct customer was 16% of Q2 revenue; three were 16%/15%/13% in 1H FY27; five held ~70% of AR. Revenue by customer HQ: US $60.1bn, Taiwan $27.0bn, China incl. HK $7.9bn.
- **Inventory-cycle checklist** (§7): (1) partly, (2) yes, (3) ramp-explained, (4) mild, (5) no, since hyperscalers guide 2027 capex up. Net: early-warning flags with demand still guided up. The print that discriminates is 17 Nov (DSO, commitments, Q4 guide).

### 8.3 What is priced: reverse DCF [Computed]
`equitykit.py dcf --price 173.73 --shares 24.285e9 --fcf 127.01e9 --sbc 7.24e9 --net-cash 36.0e9 --wacc 0.105 --tg 0.03 --years 10 --fcf-margin 0.42 --growth 0.10 0.20 0.30 0.40`
- **Result.**
  - FCF − SBC base $119.8bn, a 2.84% yield.
  - Implied starting FCF growth **26.9%**, fading to 3% by year 10.
  - Implied FCF $318bn in year 5 and $472bn in year 10 (3.9× today), i.e. ~$1.1tn of revenue in year 10 at a 42% FCF margin.
  - TV is 57% of EV.
- **Sensitivity of implied growth** (tg 3% / 2.5%):
  - by WACC: 9% → 20.5% / 22.3%; 10% → 24.9% / 26.5%; 11% → 28.9% / 30.3%; 12% → 32.7% / 34.0%;
  - by price: at $165.49 → 25.6%; at the $239.24 record → 35.7%.
- **Forward grid** (value per share; WACC rows 9.5/10.5/11.5%; starting growth 10/20/30/40%): 106/156/228/329; 91/134/195/279; 80/117/169/240.
- **A NOPAT-based cross-check** from the research notes (revenue fade, 60% EBIT margin, RONIC 30%, 10.5%, at $165.31 on 12 Nov) implies **~20% first-year revenue growth**, TV 56%, and ~8 years of 20% growth (MIFP).
  - The FCF-based figure is higher because the working-capital build depresses the FCF base.
- **Read.** FY27 revenue is already guided to ≥ ~$394bn (+80%+ vs FY26 $215.9bn), so the price does not extrapolate the run-rate. The market is pricing a cyclical deceleration in FY28-30. The debate is the duration of hyperscaler capex and the margin path, not FY27. Valuation does not say what the stock does on 18 Nov.

### 8.4 Earnings history vs implied [Computed]
`equitykit.py earnings --prices nvda.csv --dates nvda_dates.csv --implied 0.108 --implied-is-sd`
- **History.** 25 releases (18 Nov 2020 - 26 Aug 2026, including the 8 Aug 2022 BMO pre-announcement):
  - mean |move| **6.1%**, median 5.2%, SD 8.0%, 13 up / 12 down;
  - largest +24.4% (24 May 2023 release) and −8.5% (26 Feb 2025 release);
  - the last five were −0.8%, −3.2%, −5.5%, −1.8%, +8.7%.
- **Raw comparison.** Reading 10.8% as 1 SD gives E|move| 8.6%. History is **0.70×** that, and 20% of past moves exceeded it, against a fair ~42% / ~37%. That is "rich vs its own history".
  - If 10.8% is actually straddle/spot, the ratio is 0.56× (12% exceedance).
- **Event-only** [Computed]: remove ~50% base vol over the 5 non-event trading days to the 20 Nov expiry.
  - 1-SD reading: event SD ≈ 8.2%, E|move| ≈ 6.5%, ratio ≈ **0.93×**, roughly in line.
  - Straddle reading: ≈ 11.6% / 9.2% / 0.66×.
  - At 45% or 55% base vol the 1-SD reading gives 0.87× or 1.02×.
- **Read.** Whether the event is rich depends on the quoting convention and the base vol, so get a live straddle and term structure first (`tradekit.py move`). The CEO change, the board investigation and the financing debate are **new uncertainty the 25-release history does not contain**, so "rich vs history" is weak evidence for selling this event. Vendor data label NVDA mildly overpriced in 2021-26 [Weak].

### 8.5 Scenario tree through `equitykit.py projection` [Computed; probabilities are illustrative judgments]
Assumptions: spot $173.73 (11 Nov), 30 calendar days (spans the 17 Nov print and the 8-9 Dec FOMC). **Base IV 50% is an assumption, not an observed IV** (EWMA realized 54%). The event 1 SD is 10.8%, which sits between the two event-only readings in §8.4.

| Scenario (tree.csv) | Driver | Prob | Price |
|---|---|---|---|
| bull_beat_guide124plus | ~5% beat, Q4 guide ≥ $124bn, DSO/commitments explained, continuity under the interim CEO | 30% | $205 |
| base_inline_overhang | In-line beat and guide; governance overhang persists | 40% | $175 |
| bear_guide_or_cash | Light guide, or cash conversion and commitments worsen | 22% | $145 |
| tail_governance | Adverse investigation or export-compliance findings; customer fallout | 8% | $120 |

`equitykit.py projection --spot 173.73 --days 30 --iv 0.50 --base-iv 0.50 --event-move 0.108 --scenarios tree.csv --levels 150 160 173.73 190 200`

| | 5th | 10th | 25th | median | 75th | 90th | 95th | mean |
|---|---|---|---|---|---|---|---|---|
| Market-implied | $128 (−26%) | $137 | $152 | $171 (−2%) | $193 | $215 | $229 (+32%) | $173.73 |
| Scenario tree | $121 (−30%) | $131 | $151 | $174 | $195 | $213 | $222 (+28%) | $173.15 |

P(price > level), market / tree / gap: $150 77%/76%/−1pt; $160 65%/67%/+2pt; $173.73 46%/50%/+4pt; $190 28%/30%/+3pt; $200 19%/20%/+1pt.

**Read.**
- **This tree has no material gap.** The largest is +4pt, mostly because the lognormal median sits below spot. It is not a directional idea.
- **Its only real difference is shape.** A fatter left tail (5th percentile $121 vs $128) and a thinner right tail. That points at a defined-risk structure or a smaller size, not at a stock call.
- **The 1-year market band** (`--days 365 --iv 0.45`, IV assumed): 5th $75, 25th $116, median $157, 75th $213, 95th $329. P(>$225) 21%, P(>$305) 7%, P(>$515) < 1%.
  - The pre-shock average target (~$305, +75%) had a ~7% risk-neutral probability at this vol, and Bradshaw's ~15pt optimism haircut applies on top. That is why point targets fail.

### 8.6 Signposts for 17 Nov (dated catalysts)
- **Signposts:** the Q4 guide vs ~$124bn; the GM guide vs 74%; the DSO and AR trend; supply commitments vs $279bn; new guarantees or cloud commitments; the equity-gain share of GAAP EPS; the China assumption; any wording on customer continuity after the CEO change.
- **Later catalysts:** a requested House briefing (18 Nov, status unknown); FOMC 8-9 Dec; hyperscaler 2027 capex guides (Jan-Feb 2027); the new Congress on export bills (Jan 2027); the permanent-CEO appointment and investigation findings (open-ended).

## 9. Failure modes / traps

- **Numbers drift from your own data.** Quote every price move, return and multiple from the data you fetched (recompute it), not from memory or a headline; if a press figure differs from your file, say which you used. (Test run, 12 Nov 2026: a 5 Nov move quoted as -8.9% while the fetched file showed -9.26%.)
- **Apples-to-oranges valuation.** Compare like with like: EV/EBIT with EV/EBIT, GAAP P/E with GAAP P/E, trailing with trailing, forward with forward, and state the basis of each number.
- **Stale or undated inputs:** pre-event targets, consensus without an as-of date, or "current" multiples from before a 20% move. Catch: every number needs a date.
- **Headline-first research:** trusting a web summary over EDGAR. Catch: pull submissions and new 8-K items first. Search indexes lagged the NVIDIA 5.02 filing by hours.
- **Rumor as fact:** modelling "$250bn" when the filing says "capped at $105bn". Catch: T3 claims change variance, not the model.
- **GAAP vs Street mismatch:** XBRL EPS against adjusted consensus; or old non-GAAP series after a definition change (NVIDIA now includes SBC). Catch: same basis, same definition.
- **Keying EDGAR on `fy`/`fp`,** double-counting comparatives, or using frames in backtests (look-ahead). Catch: key on (start, end) and keep the earliest `filed` for point-in-time.
- **Treating a quarterly FCF swing or a COGS charge as trend:** for example the 22% FCF margin or the 59-day DIO. Catch: use TTM and read the charge notes.
- **Ignoring non-operating gains in P/E:** NVIDIA's Q1 FY27 NI exceeded operating income. Catch: use EV/EBIT or operating EPS.
- **"Cheap, so it will go up next month":** valuation has almost no short-horizon timing power. Catch: tie the valuation view to the print that would revise expectations.
- **DCF theatre:** terminal growth above the risk-free rate, TV above 80% unflagged, SBC added back, no WACC grid. Catch: `equitykit dcf` with the grid, tg ≤ r_f, FCF − SBC.
- **Calling an ordinary beat good news** with a 78% base beat rate, or ignoring the guide. Catch: rank the guide surprise first.
- **Selling an event because it is "rich vs history"** when the quoted move is in the wrong convention, includes base vol, or the history lacks today's risk (a CEO exit). Catch: §4.5 checklist.
- **Using the wrong exceedance benchmark** (68% inside 1 SD) for a straddle-based move. Catch: ~42% / ~37% for the straddle; 32% / 24% for 1 SD.
- **Point targets and over-tight bands:** a scenario tree with √V well below IV. Catch: compare dispersion with IV; report the gap column; score past bands.
- **Forecasting PEAD in a mega-cap,** or trusting LLM sentiment alpha in liquid names. Catch: §4.3, §5.
- **Red flag → short:** DSO and inventory builds have benign explanations. Catch: size down and name the discriminating print.

## 10. Toolkit hooks
- `python scripts/fetch.py prices TICKER --years 7 --out px.csv`: daily OHLCV (Yahoo, unofficial; drops today's partial bar unless `--include-partial`).
- `python scripts/fetch.py fundamentals TICKER [--cik] [--quarters 8] [--out f.csv]`: SEC XBRL quarterly table and TTM (growth, GM/OM, FCF, FCF%, DIO, DSO, SBC, buybacks, diluted shares, net cash).
- `python scripts/fetch.py earnings-dates TICKER [--out d.csv]`: 8-K Item 2.02 dates with ET time and AMC/BMO/DMH timing. Past releases only.
- `python scripts/equitykit.py earnings --prices px.csv --dates d.csv [--straddle X --spot S | --implied 0.07 [--implied-is-sd]] [--show 16]`: reaction history and mean |move| vs implied, with the exceedance rate.
- `python scripts/equitykit.py dcf --price P --shares N --fcf F [--sbc S] [--net-cash C] [--wacc 0.105] [--tg 0.03] [--years 10] [--fcf-margin m] [--growth g1 g2 ...]`: reverse DCF, TV share, forward grid. The default WACC is 0.09; set it explicitly.
- `python scripts/equitykit.py projection --spot S --days D --iv IV [--base-iv B --event-move 0.08 | --event-straddle X] [--iv-down --iv-up] [--scenarios tree.csv] [--scenario-vol] [--levels ...] [--trading-days n] [--sims] [--seed]`: market vs scenario percentiles and P(> level) with the gap.
- `python scripts/tradekit.py move --S S --days D --straddle X` (1 SD = 1.25 × straddle); `move --S S --days D --event-vol IV1 --base-vol IV0` (event-day SD, calendar-day convention); `tradekit.py iv`, `bs`: option inputs.
- `python scripts/tradekit.py vol px.csv`: base-vol candidates. `techkit.py indicators px.csv`: trend and levels.
- `python scripts/eventkit.py study --assets NVDA=px.csv --events DATE=LABEL ... --horizons 1 5 21`: reaction to dated non-earnings events (e.g. 5.02s, policy). `eventkit.py scenarios --file moves.csv --pos NVDA=AMOUNT [--max-loss X]`: position P&L across a tree (CSV `scenario,prob,NVDA` with % moves, not prices) and the scale factor that caps the worst case.
- `python scripts/tradekit.py size ...`: size so that a 1-2 SD event gap fits the risk budget.

## 11. Key sources
- SEC EDGAR APIs, endpoints and fair access — https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- NVIDIA companyfacts (pulled 12 Nov 2026) — https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json
- NVIDIA 8-K Item 5.02, CEO transition (12 Nov 2026) — https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/nvda-20261111.htm
- NVIDIA 8-K, SB Energy guarantee (17 Aug 2026) — https://www.sec.gov/Archives/edgar/data/1045810/000104581026000069/nvda-20260817.htm
- NVIDIA Q2 FY27 CFO commentary — https://www.sec.gov/Archives/edgar/data/1045810/000104581026000073/q2fy27cfocommentary.htm
- Damodaran, cost of capital by industry (Jan 2026) and implied ERP — https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/wacc.html
- Koller, Goedhart & Wessels, *Valuation* 7th ed. (2020); Mauboussin & Rappaport, *Expectations Investing* (2021)
- Sloan 1996, *TAR* 71(3) — https://www.jstor.org/stable/248290; Green, Hand & Soliman 2011, *Mgmt Sci* — https://doi.org/10.1287/mnsc.1110.1338
- Novy-Marx 2013, *JFE* — https://doi.org/10.1016/j.jfineco.2013.01.003; Ball et al. 2016, *JFE* — https://doi.org/10.1016/j.jfineco.2016.03.002
- Beneish 1999, *FAJ* — https://doi.org/10.2469/faj.v55.n5.2296; Piotroski 2000, *JAR* — https://doi.org/10.2307/2672906
- Vuolteenaho 2002, *JF* — https://doi.org/10.1111/1540-6261.00418; La Porta et al. 1997, *JF* [SC DOI]; Chan, Karceski & Lakonishok 2003, *JF* — https://doi.org/10.1111/1540-6261.00540
- Liu, Nissim & Thomas 2002, *JAR* — https://doi.org/10.1111/1475-679X.00042
- Martineau 2022, *CFR* (PEAD) — https://ideas.repec.org/a/now/jnlcfr/104.00000122.html; Subrahmanyam 2025 brief — https://anderson-review.ucla.edu/is-post-earnings-announcement-drift-a-thing-again
- Hand, Laurion, Lawrence & Martin 2022, *RAST* — https://ideas.repec.org/a/spr/reaccs/v27y2022i4d10.1007_s11142-021-09597-6.html
- Bradshaw, Brown & Huang 2013, *RAST* — https://ideas.repec.org/a/spr/reaccs/v18y2013i4d10.1007_s11142-012-9216-5.html
- FactSet Earnings Insight, 6 Nov 2026 — https://insight.factset.com/sp-500-earnings-season-update-november-6-2026
- IVolatility earnings study (2021-26) — https://www.ivolatility.com/news/3147; EarningsWatcher implied vs actual (2023-26) — https://earnings-watcher.com/wiki/options-implied-move-vs-actual-earnings-study-2026
- Tetlock 2011, *RFS* (stale news) — https://ideas.repec.org/a/oup/rfinst/v24y2011i5p1481-1512.html; Lopez-Lira & Tang v6 — https://arxiv.org/abs/2304.07619
- Ranjan & Gneiting 2010, *JRSS-B*; Gneiting, Balabdaoui & Raftery 2007, *JRSS-B*; Shackleton, Taylor & Yu 2010, *JBF*
- Bessembinder 2018, *JFE* — https://ideas.repec.org/a/eee/jfinec/v129y2018i3p440-457.html
