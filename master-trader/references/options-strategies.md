# Options Strategies: The 11 Core Structures

*Read when: a user asks about, plans, or reviews one of the classic structures — long call, long put, covered call,
cash-secured put, protective put (or collar), bull call spread, bear put spread, iron condor, straddle, strangle,
calendar spread — or asks which of them fits a view, what it can lose, what account level it needs, or what the
evidence says about its returns. Researched 2026-11-14.*

Evidence tags: `[Strong]` `[Moderate]` `[Weak]` `[Contested]` `[Lore]`. Payoff formulas are *(identity)*. Worked
numbers come from `tradekit.py strategy` (S = 100, 30 days, IV 20%, r 4%, strikes 5% and 10% from spot, $0.65 a
contract; one structure = 1 contract per option leg, 100 shares per stock leg). Theory, the surface and the VRP live
in `options-volatility.md`; this file is the per-structure playbook.

## Contents
1. Core principles · 2. The 11 at a glance · 3. What the evidence says, by structure · 4. Long call · 5. Long put ·
6. Covered call · 7. Cash-secured put · 8. Protective put and collar · 9. Bull call spread · 10. Bear put spread ·
11. Iron condor · 12. Straddle · 13. Strangle · 14. Calendar spread · 15. Rules shared by all of them ·
16. Assignment, pin risk and dividends · 17. US account rules and costs · 18. Choosing among the 11 ·
Failure modes · Toolkit hooks · Key sources

## 1. Core principles
- **Every structure is a bundle of four bets: direction (Δ), realized vs implied vol (Γ against Θ), the IV level
  (vega) and time.** Name which one is the real bet before choosing. A structure that is right on direction can still
  lose on vega or theta.
- **At fair prices, probability of profit buys nothing.** A 70%-win iron condor and a 35%-win long call both expect
  about minus their costs when realized vol matches implied (`strategy` prints this). Win rate is set by where the
  strikes sit; the edge comes only from IV vs the realized vol you forecast, skew, events, or flows.
- **Sellers collect the volatility risk premium on most days and give it back in a few.** Index implied vol has
  exceeded later realized vol on about 84% of days (1996–2026, `options-volatility.md` §6) [Strong]. The short
  structures (covered call, cash-secured put, iron condor, short straddle or strangle) earn it; the long ones pay it.
  Size the sellers for the few days.
- **Buyers need a reason the market is under-pricing the move:** an event priced below its history, realized vol
  forecast above IV, cheap skew, or a hedge whose cost the book can afford. "I think it goes up" alone is a stock
  trade, not an option trade.
- **Defined risk is not low risk.** A credit spread's max loss is several times its credit and has a real
  probability (8% for the example iron condor). Size by the max loss, not the margin or the credit.
- **Mechanics decide outcomes at the edges:** early assignment before ex-dividend, pin risk at expiry, a spread that
  finishes between strikes and turns into 100 shares, spreads of 5-20% of premium on single-stock options. Plan the
  exit before the entry.

## 2. The 11 at a glance
Payoff at expiry per share *(identity)*; c = net premium per share (debit +, credit −). Greeks signs at entry,
spot at the money of the structure.

| Structure | Legs | Max gain | Max loss | Break-even(s) | Δ | Γ | Θ | Vega | Schwab level |
|---|---|---|---|---|---|---|---|---|---|
| Long call | +C(K) | unlimited | c | K + c | + | + | − | + | 1 |
| Long put | +P(K) | K − c | c | K − c | − | + | − | + | 1 |
| Covered call | +100 sh, −C(K) | K − S + c | S − c (stock to 0) | S − c | + (1 − Δc) | − | + | − | 0 |
| Cash-secured put | −P(K) + cash K | c | K − c | K − c | + | − | + | − | 0 (cash) |
| Protective put | +100 sh, +P(K) | unlimited | S − K + c | S + c | + (1 + Δp) | + | − | + | 0 |
| Bull call spread | +C(K1), −C(K2) | K2 − K1 − c | c | K1 + c | + | ± | ± | ± | 2 |
| Bear put spread | +P(K2), −P(K1) | K2 − K1 − c | c | K2 − c | − | ± | ± | ± | 2 |
| Iron condor (short) | +P(K1), −P(K2), −C(K3), +C(K4) | credit | wider wing − credit | K2 − credit, K3 + credit | ≈0 | − | + | − | 2 |
| Long straddle | +C(K), +P(K) | unlimited | c | K ± c | ≈0 | + | − | + | 1 (short: 3) |
| Long strangle | +P(K1), +C(K2) | unlimited | c | K1 − c, K2 + c | ≈0 | + | − | + | 1 (short: 3) |
| Calendar (long) | −C(K, near), +C(K, far) | at K at the near expiry (model) | ≈ debit | model | ≈0 | − | + | + | 2 |

Sold versions: a short straddle or strangle flips every sign and has unlimited loss; a bull put spread and bear call
spread are the credit verticals (same payoff shape as the debit ones at the same strikes, by parity).

**Worked numbers** (`strategy NAME --S 100 --days 30 --vol 0.20`; calendar 30/60 days):

| Structure | Strikes | Net premium | Max gain | Max loss | Break-even(s) | P(profit) | P(max loss) | Δ sh | Θ $/day | Vega $/pt |
|---|---|---|---|---|---|---|---|---|---|---|
| Long call | 100 | −245.78 | unlimited | −245.78 | 102.46 | 34.7% | 48.9% | +53 | −4.36 | +11.40 |
| Long put | 100 | −212.95 | +9,787 | −212.95 | 97.87 | 34.3% | 51.1% | −47 | −3.26 | +11.40 |
| Covered call | 105 | +70.36 call | +570.64 | −9,929 (to 0) | 99.29 | 56.1% | ~0% | +78 | +3.08 | −8.54 |
| Cash-secured put | 95 | +50.24 | +50.24 | −9,450 (to 0) | 94.50 | 84.6% | ~0% | +16 | +2.17 | −7.07 |
| Protective put | 95 | −51.54 put | unlimited | −551.54 | 100.52 | 47.5% | 18.0% | +84 | −2.17 | +7.07 |
| Bull call spread | 100/105 | −175.13 | +324.87 | −175.13 | 101.75 | 39.1% | 48.9% | +31 | −1.28 | +2.86 |
| Bear put spread | 95/100 | −162.72 | +337.28 | −162.72 | 98.37 | 37.6% | 51.2% | −30 | −1.09 | +4.32 |
| Iron condor | 90/95/105/110 | +99.71 | +99.71 | −400.29 | 94.00, 106.00 | 70.4% | 8.3% | −3 | +3.52 | −10.51 |
| Long straddle | 100 | −458.73 | unlimited | −458.73 | 95.41, 104.59 | 42.5% | ~0% | +7 | −7.62 | +22.79 |
| Long strangle | 95/105 | −123.48 | unlimited | −123.48 | 93.77, 106.23 | 27.8% | 61.7% | +6 | −5.25 | +15.61 |
| Calendar | 100 (30/60d) | −112.35 | +132.78 | −112.35 | 96.88, 103.92 | 46.0% | ~0% | +1 | +1.12 | +4.66 |
| Short straddle | 100 | +456.13 | +456.13 | unlimited | 95.44, 104.56 | 57.5% | — | −7 | +7.62 | −22.79 |
| Short strangle | 95/105 | +120.88 | +120.88 | unlimited | 93.79, 106.21 | 72.1% | — | −6 | +5.25 | −15.61 |

Odds are lognormal at the 20% IV with no drift beyond the rate; real-world odds differ with drift, skew and fat
tails. Every row expects about −$0.65 per contract (the commission) when realized vol is 20%; at a realized 16% the
iron condor expects +$39.90 and wins 80.7%, and at 25% the straddle expects +$114.56 (`--rv`).

## 3. What the evidence says, by structure
Numbers are mid-price or index returns before fees unless stated; Cboe owns its benchmark indexes and their history
before each launch date is back-tested. Details and sources are in each structure's section.

| Structure | What the data say | Grade |
|---|---|---|
| Long call | ITM and near-money index calls can earn the levered equity premium (samples disagree at the money); OTM calls lose: 5% OTM SPX −19% a month, single-stock calls >15% OTM −28% a month. Retail lost $2.1bn on mostly long short-dated options in 2019-21 | [Strong] |
| Long put | The most overpriced options: SPX ≈ −30% a month ATM, −54% to −60% 5-6% OTM. The insurance premium; whether it is "mispriced" is contested | [Strong] |
| Covered call | BXM 8.6% vs 11.2% a year (1986-Oct 2026) at two-thirds the vol, equal Sharpe; OTM calls keep more (BXMD 10.6%). Funds trail the market (JEPI 11.2% vs 17.3% since 2020) | [Strong] lower vol · [Moderate] returns |
| Cash-secured put | PUT beat the S&P to 2015 (10.1% vs 9.8%) but not since 2007 (7.1% vs 11.0%); two-thirds the vol, skew −2.1. Weekly and OTM variants did worse | [Moderate] |
| Protective put / collar | PPUT 7.9% vs 11.2%: ≈3.3 points a year of cost. Flat in the 2008 and 2020 crashes, no help in 2022's slow bear. Less efficient than holding less equity | [Moderate] |
| Bull call spread | The short OTM call is the worse-returning leg, so the spread sells what is overpriced; bull call spreads were the strongest directional setup after costs in one S&P study | [Moderate] |
| Bear put spread | The short OTM put is the richest leg (−54% vs −32% a month), so the spread loses far less than the outright put | [Moderate] |
| Iron condor | CNDR 7.1% a year in back-test, 1.1% live (2015-26) vs 2.2% T-bills; the iron butterfly −2.5% live, −53% drawdown. Costs cut short-strangle Sharpe from 1.83 to 0.16 | [Moderate] |
| Long straddle | Loses on average (zero-beta ATM S&P ≈ −3% a week). Conditional single-stock edges (IV below HV, upward term structure, days before earnings) shrink sharply at real fills | [Strong] |
| Strangle | Short: the VRP harvest, Sharpe 0.5-0.7 in a no-cost SPX backtest (2001-20), 0.16 after costs and margin (1985-2001). Long: the max loss is the most likely outcome | [Moderate] |
| Calendar | No large direct study. The variance premium sits in the front month, which the calendar sells; term-structure slope predicts straddle returns; measured calendar returns are small | [Weak-Moderate] |

**Base rates worth quoting carefully.**
- The common "10% exercised, 55-60% closed, 30-35% expire worthless" split traces to a 2002 CBOE web page with no
  period or method [Weak]; don't present it as data. A win rate is set by strike placement, not by skill.
- Retail: US retail lost $2.1bn net on options from Nov 2019 to Jun 2021, and paid $6.4bn in trading costs against
  the mid (Bryzgalova, Pavlova & Sikorskaya 2023) [Strong]; 93% of Indian individual F&O traders lost money in FY22-24
  (SEBI, Sep 2024) [Strong]; selling volatility was the best strategy for retail and institutions alike (Hu,
  Kirilova, Park & Ryu 2024) [Strong].
- Spreads are the hidden cost: average retail bid-ask 12.6% of premium (Bryzgalova et al.); SPX 10-11%
  volume-weighted in 2004 (Santa-Clara & Saretto); 5-20% on single-stock options (Bogousslavsky & Muravyev 2024)
  [Moderate].

## 4. Long call
**Legs:** buy one call. **View:** up, by more than the market implies, before expiry. **Regime:** IV low against
your realized-vol forecast (low IV percentile), no event premium you don't mean to pay. In equity indices the call
wing usually trades below ATM IV, so OTM calls are the cheaper wing.

| | |
|---|---|
| Payoff *(identity)* | Max gain unlimited · max loss = premium · break-even = K + premium |
| Example | 100 call 2.45 ($245.78 with commission) · break-even 102.46 (+2.5%) · P(profit) 34.7% · P(lose it all) 48.9% |
| Greeks now → halfway (spot flat) | Δ +53 → +52 shares · Γ +6.9 → +9.8 · Θ −$4.36 → −$5.94 a day · vega +$11.40 → +$8.07 a vol point |
| With IV | +5 vol points: +$57 at once; OTM call deltas rise toward 0.5, ITM deltas fall. An event's IV crush takes the vega back |

- **Strike and expiry.** Delta 0.50-0.70 for a directional view; 0.70-0.85 (in the money) as stock replacement with
  less theta and vega per share of exposure; far OTM calls are lottery tickets with the worst average returns (§3).
  Buy at least twice the time the move should take [Lore]: an ATM option's time value scales with √T, so the last 30
  days of a 90-day option burn √(30/90) = 58% of its time value *(identity)*.
- **Exit.** Take profit at the underlying's target, or sell half at +100% on the premium [Lore]. Stop on the
  underlying's invalidation level, or at −50% of premium [Lore]. Time stop: close or roll out with 21-30 days left
  unless the catalyst is inside that window. Roll *up* (sell the call, buy a higher strike) to bank gains.
- **Risks.** Theta and IV crush (a correct-direction trade loses when the move is slower or smaller than priced).
  Early exercise is never optimal for a call except just before an ex-dividend date (§16) — sell it instead.
- **Evidence.** A call is levered equity, so in-the-money and near-money index calls can earn positive average
  returns, but the samples disagree near the money. SPX calls struck 3-5% below to 3% above spot returned +1.3% to
  +1.7% a week, 1996-2023, and those 3-5% OTM −1.4% a week (Doshi, Jacobs & Sert, Jul 2026 WP) [Moderate]. On
  45-day SPX calls the monthly excess return falls from +2.5% (5% ITM) to −2.5% (ATM) and −19.4% (5% OTM),
  1988-2007 (Constantinides, Jackwerth & Savov 2013) [Strong]. Every study agrees that OTM calls lose.
  Single stocks are worse: calls more than 15% OTM averaged −28% a month, 1996-2005 (Ni 2008) [Moderate]; 7-day
  calls in the most lottery-like (high-skew) quintile −35% a week vs +1.4% in the lowest (Boyer & Vorkink 2014,
  WP numbers) [Strong]. US retail lost $2.1bn net on options from Nov 2019 to Jun 2021, mostly in long short-dated
  options with average spreads of 12.6% (Bryzgalova, Pavlova & Sikorskaya 2023) [Strong]; around earnings retail
  buyers lose 5-9%, 10-14% when the expected move is large (de Silva, Smith & So 2025) [Strong].
- **Account.** Schwab Level 1; cash account and IRA allowed; paid in full ($0.65 a contract each way, free online
  buy-to-close at $0.05 or less). Over 9 months to expiry, a margin account lends 25% of the cost (§17).

## 5. Long put
**Legs:** buy one put. **View:** down, fast, or a hedge. **Regime:** IV low and skew flat (puts are cheap only then);
spot-vol correlation helps a long put because IV rises as spot falls (long vanna).

| | |
|---|---|
| Payoff *(identity)* | Max gain = K − premium (stock to zero) · max loss = premium · break-even = K − premium |
| Example | 100 put 2.12 ($212.95) · break-even 97.87 (−2.1%) · P(profit) 34.3% · P(lose it all) 51.1% |
| Greeks now → halfway | Δ −47 → −48 · Γ +6.9 → +9.8 · Θ −$3.26 → −$4.84 a day · vega +$11.40 → +$8.07 |
| With IV | In a selloff IV and skew rise together, so the put gains on vega as well as delta |

- **Strike and expiry.** Same delta logic as the call. Under steep put skew an OTM put costs several vol points
  over ATM: buy the ATM put and sell a lower one (a bear put spread, §10) to give the rich wing back.
- **Exit.** Puts pay in short, violent moves: take profits into vol spikes (IV and skew mean-revert after the low).
  Stops and time stops as for calls.
- **Risks.** Deep ITM American puts can be exercised early when the interest on the strike exceeds their time value
  — more often at a 4% rate than at zero (§16). A put bought as a trade on a stock that is hard to borrow is priced
  off the borrow rate; check parity.
- **Evidence.** Index puts are the most overpriced options measured: 45-day SPX puts returned −32% a month ATM and
  −54% 5% OTM, 1988-2007 (Constantinides, Jackwerth & Savov 2013) [Strong]; S&P futures puts ≈ −30% ATM and ≈ −60%
  6% OTM a month held to expiry, 1987-2005 (Broadie, Chernov & Johannes 2009) [Strong]; weekly −6.2% ATM and −11.2%
  3-5% OTM, 1996-2023 (Doshi, Jacobs & Sert 2026 WP) [Moderate]. Whether this is a mispricing is [Contested]:
  Broadie et al. find the OTM losses consistent with Black-Scholes given sampling error, Bondarenko (2014) finds
  no model in his class explains them. The loss is the insurance premium: a long put needs a reason (a hedge, a
  dated catalyst, or IV unusually low) to be bought.
- **Account.** Schwab Level 1; cash account and IRA allowed; paid in full. Exercising a long put without the shares
  creates short stock, so Schwab exercises long puts only if it can lend the shares: sell the put instead (§17).

## 6. Covered call
**Legs:** own 100 shares, sell one call (usually OTM). **View:** flat to mildly up; willing to sell at the strike.
**Regime:** IV rich against forecast realized vol; no earnings inside expiry unless you want the stock called. It is
equity beta plus short volatility, not "income" (Israelov & Nielsen 2015, `options-volatility.md` §9).

| | |
|---|---|
| Payoff *(identity)* | Max gain = K − S + premium · max loss = S − premium (stock to zero) · break-even = S − premium |
| Example | 105 call 0.71 · max gain $570.64 · break-even 99.29 · P(profit) 56.1% · at −2 SD (88.53) it loses $1,076 like the stock |
| Greeks now → halfway | Δ +78 → +87 (the short call loses delta as time passes OTM) · Γ −5.2 · Θ +$3.08 → +$2.94 · vega −$8.54 → −$4.21 |
| With IV | IV +5 costs $45 at once and cuts delta to +73 |

- **Strike and expiry.** ATM (the BXM rule) collects the most premium and caps the most upside; 30-delta (BXMD) or
  2% OTM (BXY) keeps more of the equity premium. One month or less: theta per day is highest near expiry.
- **Exit and rolling.** Let it expire, or buy back once 50-80% of the premium is earned [Lore]. When the stock runs
  through the strike, roll *up and out for a net credit* or let the shares go; when it falls, rolling *down* locks in
  a capped recovery — sell the next call at a strike you'd be happy to sell at, not at the old cost.
- **Risks.** Full downside minus a small premium. Upside capped in exactly the rallies that make the year. Short
  ITM calls are assigned early the day before ex-dividend when the dividend exceeds their time value (§16).
- **Evidence.** BXM (S&P 500 plus a monthly ATM call) returned 8.6% a year from Jun 1986 to Oct 2026 against 11.2% for
  the S&P 500 total return, at 10.6% vs 15.2% vol, a −35.8% vs −50.9% max drawdown and the same Sharpe (0.55 vs
  0.56). Selling further out kept more of the equity premium: BXMD (30-delta) 10.6% a year, BXY (2% OTM) 10.3%
  (Cboe factsheets, 31 Oct 2026; back-tested before launch; Cboe owns the indexes) [Moderate]. The cost is the
  rallies: BXM −2.8% in 2020 (S&P +18.4%), +11.8% in 2023 (+26.3%); the cushion is partial: −11.4% in 2022
  (−18.1%), −28.7% in 2008 (−37.0%). Lower vol at roughly equal Sharpe replicates across Whaley 2002, Callan
  2006, Hill et al. 2006 and Israelov & Nielsen 2014 (BXM excess return 4.4% at 13.4% vol vs 5.4% at 18.5%,
  1986-2013) [Strong]. In Russell 2000 names 2% OTM calls edged the index (8.9% vs 8.1%, 1996-2011) but not with
  2-month calls (Kapadia & Szado, OIC-funded) [Moderate]. Covered-call funds trail the market: JEPI 11.2% a year
  vs the S&P 500's 17.3% since May 2020, SPYI 14.3% vs 18.0% since Aug 2022, QYLD 8.9% vs its own index 9.8% since
  Dec 2013 (issuer factsheets, Aug-Oct 2026) [Moderate]. Overlays sized to hit a yield target lost 3.1-4.7% a
  year, 2011-2023 (Israelov & Ndong 2023) [Weak, secondary].
- **Account.** Schwab Level 0; cash account and IRA allowed. Nothing is required on the call; on margin the stock
  takes 50% initial / 25% maintenance and counts at no more than the strike. Assignment costs $0 at Schwab (§17).

## 7. Cash-secured put
**Legs:** sell one put, hold cash equal to the strike × 100. **View:** flat to up; happy to buy at K − premium.
**Regime:** high IV percentile *and* a positive ex-ante VRP; steep put skew (you sell the rich wing); contango, no
backwardation. By put-call parity it is the same position as a covered call at the same strike.

| | |
|---|---|
| Payoff *(identity)* | Max gain = premium · max loss = K − premium (stock to zero) · break-even = K − premium |
| Example | 95 put 0.51 ($50.24 credit) · break-even 94.50 (−5.5%) · P(profit) 84.6% · at −2 SD it loses $597, twelve times the credit |
| Greeks now → halfway | Δ +16 → +9 · Γ −4.3 · Θ +$2.17 → +$2.14 · vega −$7.07 → −$3.36 |
| With IV | IV +5 costs $38 and raises delta to +21: the position gets longer as the market falls (vanna) |

- **Strike and expiry.** PUT index sells the ATM one-month put; practitioners sell 0.20-0.30 delta at 30-45 days
  [Lore]. Sell only strikes at which you want the stock. "The wheel" (put → assignment → covered call) is the same
  short-vol equity position throughout.
- **Exit and rolling.** Buy back at 50% of max profit [Weak, vendor]. If tested, roll down and out *for a credit* or
  take assignment; never roll for a debit to avoid owning the stock you said you wanted.
- **Risks.** The left tail, sized as if the stock gaps 20-30%. Early assignment on deep ITM puts. In a margin account
  the same put held without the cash is an uncovered put (§17).
- **Evidence.** PUT (monthly ATM puts on the S&P 500, T-bill collateral) beat the index from Jul 1986 to Dec 2015
  (10.1% vs 9.8% a year at two-thirds the vol; Bondarenko 2016, Cboe-sponsored) but not since: 7.1% vs 11.0% a
  year from Jan 2007 to Oct 2026, vol 10.7% vs 15.4%, max drawdown −32.7% vs −50.9%, Sharpe 0.52 vs 0.61 (Cboe
  factsheet) [Moderate]; about 9.6% vs 11.2% chained over 1986-2026. Its skew is −2.1 against −0.8 for the S&P
  (1986-2018) [Moderate]. Calendar years: −26.8% in 2008, −7.7% in 2022 (S&P −18.1%), +14.3%, +17.8%, +9.2% in
  2023-25 (S&P +26.3%, +25.0%, +17.9%). Intrayear falls: −37% in 2008-09, −29% in 2020, −16% in 2022, −15% in
  2025. Selling further out or more often did not help: PUTY (2% OTM) 6.9% a year since 1986; WPUT (weekly) 4.8%
  since 2006, despite collecting 37% a year of gross premium against PUT's 22% (2006-18) [Moderate]. On the
  Russell 2000, PUTR 5.5% vs 7.5% for the index since Aug 2018. PUT beat BXM by about 1.1% a year over 1986-2015
  because BXM holds stock through a four-hour expiry-morning gap (Israelov 2017) [Weak-Moderate]; the gap persists
  (7.2% vs 6.0%, 2007-2026). Put-write ETFs lag the index further (CXO, Dec 2025) [Weak].
- **Account.** Schwab Level 0 when secured: strike × 100 in cash or equivalents, with the premium counting toward it
  (a 95 put ties up $9,500 less the $51 credit). IRAs: listed at Level 0 in Schwab's application but "generally
  not allowed" per a 2025 Schwab article [Contested]. Without the cash on margin it is an uncovered put: Level 3,
  $5,000 equity, premium + max(20% of spot − OTM, 10% of strike) (§17).

## 8. Protective put and collar
**Legs:** own 100 shares, buy one put (a **collar** also sells an OTM call to pay for it). **View:** long-term
bullish, short-term worried, or a hedge through an event. **Regime:** buy when IV is low and skew flat; under steep
skew, a put spread or a collar is the cheaper hedge.

| | |
|---|---|
| Payoff *(identity)* | Max gain unlimited (collar: K_call − S + net) · max loss = S − K_put + premium · break-even = S + premium |
| Example | 95 put 0.51 ($51.54) · worst case −$551.54 (−5.5%) · P(profit) 47.5%. Collar 95/105: max gain $519, max loss $481, a net credit of $19 |
| Greeks now → halfway | Δ +84 → +91 · Γ +4.3 · Θ −$2.17 · vega +$7.07 |
| Cost of carry | A 5% OTM one-month put at 20% IV costs 0.51% of the stock: rolled monthly ≈ 6.2% a year; a one-year 95 put ≈ 4.0% (floor not reset). Put skew makes real OTM puts dearer |

- **Strike and expiry.** 5% OTM monthly (the PPUT rule) is expensive; longer expiries cost less per day (theta
  ∝ 1/√T) but reset the floor less often. A put spread (buy 95, sell 85) cuts the cost and keeps the protection that
  matters most for a 5-15% drop.
- **Exit.** A hedge's job is to be sold into the spike: monetize part of it when IV jumps, then re-strike. Holding it
  to expiry turns a vol hedge into pure decay.
- **Risks.** The steady cost. Israelov (2019) finds protective puts cut drawdowns less efficiently than simply
  holding less equity, because they pay the VRP (`options-volatility.md` §9) [Moderate].
- **Evidence.** PPUT (S&P 500 plus a monthly 5% OTM put) returned 7.9% a year from Jun 1986 to Oct 2026 against 11.2%:
  about 3.3 points a year of net hedge cost (2.9 since 2007), for 12.3% vs 15.2% vol and a −38.9% vs −50.9% max
  drawdown (computed from Cboe's index history; verified Nov 2026) [Moderate]. That net cost is the ≈6% a year of
  premium (Cost of carry, above) less what the puts paid back. It works in crashes and fails in slow
  bears: +0.2% in 4Q 2008 (S&P −21.9%), 0.0% in 1Q 2020 (−19.6%), but −13.1% in 2Q 2022 (−16.1%) and −19.8% for
  2022 (−18.1%). The CLL collar (quarterly 95 put, monthly 110 call) lost −5.9%, −5.0% and −6.7% in those three
  quarters (Cboe) but earned 3.2% a year in excess of cash vs 7.3% for the S&P, Sharpe 0.30 vs 0.47, 1986-2014
  (Israelov & Klein 2016) [Moderate]. In ten single stocks, 2003-2013, plain stock beat both the protective put
  and the collar on all four measures (Hemler & Miller 2015, OIC-funded) [Moderate]. Per unit of return given up,
  holding less equity cut drawdowns more (Israelov 2019) [Moderate].
- **Account.** Schwab Level 0; cash account and IRA allowed; put paid in full. Margin maintenance: the lesser of 10%
  of the strike plus the OTM amount, or the stock's requirement; a collar, the lesser of 10% of the put strike plus
  its OTM amount, or 25% of the call strike (§17).

## 9. Bull call spread
**Legs:** buy a call at K1, sell a call at K2 > K1, same expiry. **View:** moderately up, to about K2, by expiry.
**Regime:** works when IV is middling or high (the short call refunds part of the vega). In equity indices the
short OTM call has the lower IV, yet OTM calls are still the worse-returning leg (§3), so the spread sells what
is overpriced in return terms.

| | |
|---|---|
| Payoff *(identity)* | Max gain = K2 − K1 − debit · max loss = debit · break-even = K1 + debit |
| Example | 100/105 for 1.74 ($175.13) · max gain $324.87 (1.85 : 1) · break-even 101.75 · P(profit) 39.1% · P(max loss) 48.9% |
| Greeks now → halfway | Δ +31 → +40 · Γ +1.7 → +4.7 · Θ −$1.28 → −$2.99 · vega +$2.86 (a quarter of the lone call's) |
| With time and IV | With spot between the strikes the spread converges to its payoff late, so most of the gain comes in the last third. IV up pushes the value toward half the width: it helps an OTM spread and hurts an ITM one |

- **Strike and expiry.** Buy ATM or slightly ITM, sell at the target. A debit of 30-50% of the width is the usual
  zone [Lore]. Expiry beyond the date the target should be reached.
- **Exit.** Take 50-75% of max value [Lore]; the last part comes slowly and carries pin risk at K2. Stop on the
  underlying's invalidation level.
- **Risks.** If spot finishes between the strikes, the long call is auto-exercised into 100 shares per contract
  that the account must carry over the weekend — close it before the bell (§16). Early assignment of the short call
  before ex-dividend leaves you short stock owing the dividend.
- **Evidence.** Index calls lose more the further OTM they are (45-day SPX: −2.5% a month ATM, −19.4% 5% OTM;
  Constantinides et al. 2013) [Strong], so the short OTM leg sells the worse-returning option even though its IV is
  lower (inference from those tables, not a direct spread test) [Moderate]. McKeon (2016) finds S&P bull call spreads
  that sell an OTM call the strongest directional option setups, keeping strong average returns after costs and doing
  better held to expiry than closed early [Moderate, abstract only].
- **Account.** Schwab Level 2: margin account, or an IRA with limited margin (Schwab says $5,000 for IRA spreads; a 2019
  form said $25,000). Not in a plain cash account (American-style equity spreads, Reg T). The debit is paid in
  full; 2 contracts × $0.65 each way (§17).

## 10. Bear put spread
**Legs:** buy a put at K2, sell a put at K1 < K2, same expiry. **View:** moderately down, to about K1. **Regime:** the
skew-efficient bearish trade: under steep put skew the short lower strike carries more IV than the long one, so you
sell what is rich (`options-volatility.md` §8).

| | |
|---|---|
| Payoff *(identity)* | Max gain = K2 − K1 − debit · max loss = debit · break-even = K2 − debit |
| Example | 100/95 for 1.61 ($162.72) · max gain $337.28 (2.07 : 1) · break-even 98.37 · P(profit) 37.6%. With skew (95 put at 24.4%, 100 at 21.6%, `--px 0.85,2.30`): debit $146.30, max gain $353.70 (2.42 : 1) |
| Greeks now → halfway | Δ −30 → −38 · Γ +2.6 → +5.7 · Θ −$1.09 → −$2.71 · vega +$4.32 |
| With IV | As for the call spread; in a crash IV rises most at the short lower strike, which caps the spread's mark-to-market |

- **Strike and expiry, exit.** As for the bull call spread, mirrored. `scanner.py scan --puts` proposes one from the
  listed chain for bearish candidates (long put near the entry, short put near the target).
- **Risks.** Between the strikes at expiry the long put exercises into a short stock position (borrow, margin,
  squeeze risk). Deep ITM short puts can be assigned early.
- **Evidence.** OTM index puts are richer than ATM ones (−54% vs −32% a month at 0.95 and 1.00 moneyness, 1988-2007;
  Constantinides et al. 2013) [Strong], so the short lower strike gives back the most overpriced leg and the spread
  loses far less than the outright put (inference, not a direct spread backtest) [Moderate]. The skew premium is
  over 40% of the slope of the S&P IV curve and is largely the same bet as the variance premium (Kozhan, Neuberger
  & Schneider 2013) [Strong].
- **Account.** Schwab Level 2, as for the bull call spread. If the long put is exercised the account goes short the
  shares, which needs margin and a borrow (§17).

## 11. Iron condor
**Legs:** buy put K1, sell put K2, sell call K3, buy call K4 (K1 < K2 < K3 < K4), same expiry: a bull put spread plus
a bear call spread. **View:** range-bound to expiry. **Regime:** IV rich against forecast realized vol, contango, no
event inside expiry; avoid when VIX/VIX3M > 1. In equities the put side pays more (skew): many traders set the put
short further out or take more credit there.

| | |
|---|---|
| Payoff *(identity)* | Max gain = credit · max loss = wider wing − credit · break-evens = K2 − credit, K3 + credit |
| Example | 90/95/105/110 for 1.02 ($99.71 net) · max loss $400.29 (risk 4 to make 1) · break-evens 94.00, 106.00 · P(profit) 70.4% · **P(max loss) 8.3%** |
| Greeks now → halfway | Δ −3 · Γ −6.4 → −8.2 · Θ +$3.52 → +$4.52 · vega −$10.51 → −$6.75 |
| With time and IV | Theta and short gamma both grow as expiry nears with spot inside: the late days pay most and can lose fastest. IV +5 costs $49 at once at spot 100 |

- **Strike and expiry.** Short strikes near 15-20 delta (about 1 SD), wings 5-10% or a few strikes wide, 30-45 days
  [Lore/vendor]. A credit of about a third of the wing width is a common floor [Lore]; check the break-even win rate
  with `tradekit.py expectancy`.
- **Exit.** Take 50% of max profit, or close at 21 days to expiry, whichever first [Weak, vendor]. Loss rule: close at
  1.5-2× the credit or when a short strike is touched [Lore]. Rolling the untested side closer adds credit *and*
  risk.
- **Risks.** A gap through a wing; four legs of commissions and spreads (eight fills round trip); early assignment of
  a short leg; pin risk at a short strike on expiry Friday.
- **Evidence.** Cboe's CNDR (monthly S&P iron condor, short legs near 0.20 delta, wings near 0.05) earned 7.1% a year in
  its back-test (1986-Jul 2015) and 1.1% a year live (Aug 2015-Oct 2026), below T-bills at 2.2%, with a −19.0%
  drawdown from Feb 2010 to Jun 2020. BFLY, the iron butterfly (short ATM, 5% wings), earned −2.5% a year live and
  fell −53.4% from Dec 2009 to Jun 2024, deeper than the S&P's worst (computed from Cboe's index history; Cboe
  owns both indexes) [Moderate]. The 2015 launch release put CNDR's short legs at 0.15 delta, the methodology at
  0.20. Short strangles' gross Sharpe of 1.83 fell to 0.16 after costs and margin calls (Santa-Clara & Saretto
  2009) [Strong]. Vendor win rates near 85% (SPY 45-day condors closed at 50% of max profit, 2007-2017) say
  nothing about returns [Weak]. Of the 11, this popular structure has the weakest out-of-sample record.
- **Account.** Schwab Level 2 (margined as a complex spread; IRA allowed by inference). Requirement: the lesser of the
  legs' naked requirements or the max loss (the wider wing), credit applied; all four legs in one expiry. IBKR: the
  put-side width, 102% of max loss on some spreads (§17).

## 12. Straddle
**Legs:** buy a call and a put at the same strike (ATM), same expiry. **View:** a big move, direction unknown.
**Regime:** your realized-vol forecast above IV, or an event priced below the name's history; low IV percentile.
**Short straddle:** the pure VRP harvest with unlimited risk.

| | |
|---|---|
| Payoff *(identity)* | Long: max gain unlimited · max loss = debit at S = K · break-evens = K ± debit (straddle ≈ the expected absolute move) |
| Example | 4.57 ($458.73) · break-evens 95.41 / 104.59 (±4.6%) · P(profit) 42.5%. At a realized 25%: expected +$114.56 |
| Greeks now → halfway | Δ +7 · Γ +13.9 → +19.6 · Θ −$7.62 → −$10.78 · vega +$22.79 → +$16.14 |
| Short version | Credit $456.13 · FINRA margin ≈ $2,457 · loses $691-725 at ±2 SD at expiry |

- **Entry.** Earnings: buy 3-5 days before the announcement (the pre-event ramp; Gao, Xing & Zhang) and decide in
  advance whether to sell before the print or hold through the crush (`options-volatility.md` §10). Compare the
  implied move with the name's last 8-12 absolute moves (`equitykit.py earnings`).
- **Exit and management.** Gamma-scalp: re-hedge delta at fixed moves to bank realized vol. Close when the move
  exceeds the break-even or the catalyst passes. A long straddle held through a quiet fortnight is theta paid for
  nothing; set a time stop.
- **Risks.** IV crush after the event; realized vol below implied (the usual outcome, §3). Short straddle: a gap
  loses several times the credit; buy wings (an iron butterfly) to define it.
- **Evidence.** Long straddles lose on average: zero-beta ATM S&P straddles about −3% a week (Coval & Shumway 2001)
  [Strong]; ATM S&P straddles about −13% a month, 1987-2001 (Driessen & Maenhout, WP) [Moderate]. In single
  stocks the edge is conditional: long straddles where historical vol exceeds IV and short where it is below
  earned 15% a month gross but 5.3% at half the quoted spread, 1996-2005 (Goyal & Saretto 2009, WP numbers)
  [Strong paper, Moderate numbers]; long where the IV term structure slopes steeply up and short where it is flat
  or inverted earned 27% a month gross, 12% net, 1996-2007 (Vasquez 2017, WP numbers) [Strong paper, Moderate
  numbers]. Earnings straddles bought 3
  days before averaged +3.3% to the announcement (Gao, Xing & Zhang 2018) [Moderate]; retail buyers around
  earnings still lose 5-14%, mostly to spreads and overpaying (de Silva, Smith & So 2025) [Strong]. Among
  retail and institutions alike, selling volatility was the best-performing strategy (Hu, Kirilova, Park & Ryu
  2024) [Strong].
- **Account.** Long: Schwab Level 1, cash account and IRA allowed, paid in full. Short: Level 3, margin only, $5,000
  equity, the higher leg's naked requirement plus the other leg's premium; not in an IRA or an IBKR cash account
  (§17).

## 13. Strangle
**Legs:** buy an OTM put (K1) and an OTM call (K2), same expiry. **View:** a very big move. Cheaper than the straddle,
needs a larger move, and has more vega convexity (volga). **Short strangle:** the classic premium-seller's trade.

| | |
|---|---|
| Payoff *(identity)* | Long: max loss = debit (spot between strikes) · break-evens = K1 − debit, K2 + debit |
| Example | 95/105 for 1.22 ($123.48) · break-evens 93.77 / 106.23 (±6.2%) · P(profit) 27.8% · **P(max loss) 61.7%** |
| Greeks now → halfway | Δ +6 · Γ +9.5 → +9.2 · Θ −$5.25 → −$5.08 · vega +$15.61 → +$7.57 (OTM vega decays fastest) |
| Short version | Credit $120.88 · FINRA margin ≈ $1,622 · P(profit) 72.1% · loses $526-575 at ±2 SD, 4.4-4.8× the credit |

- **Short strangle rules (practitioner):** 16-delta strikes (about 1 SD), 45 days, close at 50% of max profit or at
  21 days, size so a 3-SD move costs no more than a few percent of equity [Weak, vendor]. Undefined risk belongs only
  in a margin account that survives a 20% gap: otherwise use the iron condor.
- **Risks.** Short: unlimited loss, margin that expands in the selloff (the requirement is recomputed on the new
  spot), early assignment on the ITM side. Long: the most common outcome is the max loss.
- **Evidence.** Short near-term OTM S&P strangles had a gross Sharpe of 1.83 that fell to 0.16 after transaction costs
  and margin calls, 1985-2001 (Santa-Clara & Saretto 2009) [Strong]. An independent SPX backtest of 16-delta
  strangles, 2001-May 2020, no costs: 45 days in, out at 50% profit or 21 days, 4.4% a year at 8.6% vol (Sharpe
  0.52); 30 days in, out at 5 days, 5.5% at 8.2% (Sharpe 0.67), so managing winners did not add risk-adjusted
  value (Blom, SteadyOptions 2022) [Weak-Moderate]. The vendor view (tastylive, SPY since 2005, 1-SD 45-day
  strangles): 82% winners held to expiry, 90% managed at 50%, 95% at 25%; closing at 21 days roughly halved the
  median loss relative to premium [Weak, vendor; partly snippets]. Win rates near 82% against a ~70% delta-implied
  probability are the VRP showing up as OTM options finishing in the money less often than priced [Weak]. Long
  strangles carry the long-OTM-option evidence of §4-§5: the worst average returns.
- **Account.** As for the straddle: long at Level 1 (IRA allowed), short at Level 3 with the higher leg's naked
  requirement plus the other premium, $5,000 minimum, not in an IRA (§17).

## 14. Calendar spread
**Legs:** sell a near-term option, buy a longer-term option at the same strike (calls or puts). **View:** spot near
the strike at the near expiry. **Regime:** front IV rich against back IV (an event in the front month, a term
structure kink); hurt by a big move, by a falling back-month IV, and by front IV rising further against the back
after entry. Long vega, short gamma.

| | |
|---|---|
| Payoff | Not an identity: the far leg is still alive at the near expiry. Max gain at K at the near expiry; max loss ≈ the debit if spot runs far either way |
| Example | 100 calls 30/60 days for 1.11 ($112.35) · max gain $132.78 at 100 · break-evens 96.88 / 103.92 · P(profit) 46.0%. Puts with front IV 25% and back 21% (`--kind put --ivs 0.25,0.21`): debit $38.70, max gain $185 |
| Greeks now → halfway | Δ +1 · Γ −2.1 → −4.2 · Θ +$1.12 → +$2.28 · vega +$4.66 → +$5.86 |
| With IV | Back-month IV +5 is a gain (the long leg has the larger vega); a front-month IV spike that fades also helps. A big spot move kills both |

- **Strike and expiry.** ATM for neutral; an OTM call calendar is mildly bullish, an OTM put calendar mildly bearish.
  Front 20-45 days, back one or two cycles later. An earnings calendar sells the expiry that holds the event against
  a later one, so the front's IV crush is larger than the back's.
- **Exit.** Close before the near expiry (pin, assignment and gamma all peak then); take 20-30% of the debit [Lore];
  close if spot leaves the break-evens.
- **Risks.** If the short front leg is assigned, the long back leg still covers it, but don't exercise the long (it
  forfeits time value): buy or sell the shares, or close the whole spread. The reverse calendar (long front, short
  back) leaves a naked short after the front expires.
- **Evidence.** No large study of plain calendar returns exists. On S&P futures options, long calendars were "less
  impressive" than other structures except a 10% OTM call calendar at +20% a month (Sharpe 0.17), 1985-2001
  (Santa-Clara & Saretto 2004 WP) [Moderate]. The variance premium sits in the front month: hedging news about
  future variance (one quarter to 14 years) was costless on average, 1996-2014, and only short-lived realized
  variance is priced (Dew-Becker, Giglio, Le & Rodriguez 2017) [Strong], which supports selling the front and
  owning the back. The VIX term-structure slope predicts returns on straddles, variance swaps and VIX futures
  (Johnson 2017) [Strong]; single-stock straddles with flat or inverted term structures earn less (Vasquez 2017),
  so a calendar's short front leg fits those names. Calendars were most profitable when the term structure was
  inverted (Campasano & Linn 2017, summary only) [Weak]; an SPY call calendar returned −0.09% a year, +0.58% with
  a term-structure filter (ORATS 2019) [Weak]. Earnings IV rises into the report and drops discontinuously after
  it (Dubinsky, Johannes, Kaeck & Seeger 2019) [Strong]; no academic study of earnings calendars was found.
- **Account.** Schwab Level 2; margin or IRA limited margin (equity and ETF calendars; none on cash-settled indexes).
  The long must expire on or after the short to count as a spread; pay the debit. Schwab picks how legs pair and may
  not pick the cheapest (U). After the front leg expires, the back leg is a plain long option (§17).

## 15. Rules shared by all of them
**Strikes by delta.** |Δ| is roughly the risk-neutral chance of finishing in the money: 50 ATM, 30 a modest OTM
strike, 16 about 1 SD, 5 a far wing. Quote strikes in delta or in SD of the move to expiry, not in dollars, so a rule
travels across names and vol levels (`move` gives the SD).

**Expiry by the bet.** Short-dated options are gamma (realized-vol) trades, long-dated ones vega (IV) trades
(`options-volatility.md` §2). Sellers cluster at 30-45 days, where theta is large but gamma not yet extreme
[Lore/vendor]. Buyers buy more time than the thesis needs: time value ∝ √T, so the final week of a 30-day ATM
option holds √(7/30) = 48% of its time value *(identity)*.

**Profit-taking and stops.**
- Credit structures: close at 50% of max profit; the remaining half needs the full gamma risk of expiry week to
  collect [Weak, vendor backtests].
- Debit structures: exit at the underlying's target; a spread's last 20-25% of value arrives slowly and carries pin
  risk.
- Stops belong on the underlying's invalidation level where possible. Option marks are noisy and spreads widen in
  stress, so premium stops (−50% of a debit; 2× a credit) trigger on quotes [Lore].
- Time stops: close long premium with about 21-30 days left unless the catalyst is inside; close short premium before
  expiry week unless the plan is to take assignment.

**Rolling is a close plus a new trade.** Judge the new position on its own merits, today's IV and today's thesis.
Roll credit structures for a net credit or not at all; rolling out in time to avoid booking a loss adds duration and
risk to a losing trade. Write the roll rule down before entry.

**Liquidity and orders.** Enter multi-leg structures as one net-price limit order (the complex order book), starting
near the mid. Check the bid-ask as a share of the premium on every leg: on a four-leg condor collecting $1.00, legs
quoted $0.05 wide cost about $0.10 to cross each way, a fifth of the credit for a round trip.

**Sizing.** Defined risk: size from the max loss (`tradekit.py size --equity E --risk 1 --entry <max loss per share>
--stop 0 --multiplier 100`). Undefined risk (short straddle, strangle, naked put on margin): size from a stress loss
— a 20-30% single-stock gap or a 10% index day with IV doubling — and the margin on that day, not today's margin
(`options-volatility.md` §12).

## 16. Assignment, pin risk and dividends
US equity and ETF options are American and physically settled; SPX, XSP, NDX and RUT are European and cash-settled
(no early assignment, no shares) [Strong, exchange rules].

- **Calls before ex-dividend.** Exercising a call just before the ex-date is rational when the dividend exceeds the
  call's remaining time value (about the same-strike put's value). Short ITM calls (covered calls, the short legs of
  call spreads, condors and calendars) are at high risk of assignment the day before; the short leg of a spread then
  leaves you short stock that owes the dividend. Close or roll them first. Expect professionals to exercise: from
  1996 to 2006 holders failed to exercise more than half the calls they should have before ex-dates, leaving over
  $491M that arbitrageurs captured — by being the ones who exercised (Pool, Stoll & Whaley 2008) [Strong].
- **Deep ITM puts.** Early exercise pays when the interest on the strike exceeds the put's time value, so short deep
  ITM puts get assigned early — more often at today's ~4% rates than at zero rates. From 1996 to 2008, 3.7% of puts
  outstanding were left unexercised when they should have been exercised (Barraclough & Whaley 2012) [Strong]; early
  exercise also pays when it cuts short-sale, funding or trading costs (Jensen & Pedersen 2016) [Strong].
- **Exercise by exception.** OCC exercises options $0.01 or more in the money at expiry unless the holder says
  otherwise (OCC Rule 805; $0.05 before Jun 2008; brokers may use their own threshold) [P]. A vertical that finishes
  between its strikes becomes 100 shares per contract (long for a bull call spread, short for a bear put spread) with
  no hedge; in a small account that is a margin call on Monday.
- **Pin risk.** Holders decide until 5:30 pm ET on expiry day (1.5 hours after an early close), and firms can submit
  contrary instructions until 7:30 pm ET, so after-hours news can turn an OTM short into an assignment (FINRA Rule
  2360(b)(23); RN 10-36) [P]. A short strike near the closing price leaves you unsure whether you will be assigned.
  Close short legs within about 1% of spot before the bell. Once a leg is assigned it must be honoured whatever the
  rest of the spread does (FINRA, 2020) [P].
- **Expiries multiply.** Weeklies were 52% of US option volume from Feb 2024 to Feb 2025 (OCC data in
  SR-CBOE-2026-007), and that filing added Monday and Wednesday expiries for large single stocks and ETFs in 2026
  [P]: more expiry days means more pin and assignment events per month.
- **Spreads and assignment.** If a short leg is assigned early, the long leg still caps the loss; respond by trading
  the shares or closing the spread, not by exercising the long (that throws away its time value).

## 17. US account rules and costs
Checked 2026-11-14. [P] read on the primary page; [Pa] primary document read through an archived copy; [S] snippet
or secondary; (U) unconfirmed. Brokers can set stricter house rules at any time. Account-wide rules (Reg T, intraday
margin, fees on sales) are in `vendors.md`.

**Schwab option approval levels** (Schwab options application APP20247, 12/24 [Pa]; Schwab Learn, Jul 2023 [P])

| Level | Adds | Account | Among the 11 |
|---|---|---|---|
| 0 Covered | Covered calls, cash-secured equity puts, protective puts, collars (covered puts need margin, not in IRAs) | Cash, IRA or margin | Covered call, cash-secured put, protective put, collar |
| 1 Long | Long calls and puts, long straddles, strangles and combinations | Any | Long call, long put, long straddle, long strangle |
| 2 Spreads | Verticals, calendars, diagonals, condors, butterflies, boxes, ratio spreads heavy on the long side | Margin (added automatically) or IRA limited margin | Bull call and bear put spreads, iron condor (margined as a complex spread; level inferred, U), calendar |
| 3 Uncovered | Naked calls and puts, short straddles, strangles and combinations, uncovered ratios | Margin only; $5,000 equity before selling uncovered options | Short straddle, short strangle, a put sold without the cash |

No level chosen means Level 0 without margin; custodial and ESA accounts stay at Level 0 [Pa]. No $25,000 minimum
for Level 3 was found. An old (2011) Schwab help page put cash-secured puts at Level 1; the 2024 application says 0.

**Schwab IRA.** Levels 0-2 only, with "limited margin": spreads and trading on unsettled proceeds, but no
borrowing, no naked options, no short straddles or strangles, no short stock [Pa]/[P].
- The account must hold cash for any exercise on the last day before expiry; Schwab may close positions without
  notice [Pa].
- No spreads on American-style cash-settled index options and no calendars on cash-settled indexes; equity and ETF
  calendars look allowed (inferred) [Pa].
- Minimum for IRA spreads: $5,000 in the 2024 application and on the live margin page; $25,000 in the 2019 IRA
  supplement [Pa]/[P]. Use $5,000, but confirm.
- A 2025 Schwab Learn article says short puts are "generally not allowed" in IRAs, while the application lists
  cash-secured puts at Level 0 for IRAs [Contested]: confirm per account.

**What each structure ties up** (Schwab margin page [P], FINRA 4210 [P]; equity options)

| Structure | Requirement |
|---|---|
| Long call, put, straddle, strangle | Paid in full (75% loan value beyond 9 months to expiry, in margin). Schwab's minimum: the lesser of $2,000 or 100% of the cost |
| Covered call | Stock paid by settlement, or margined at 50% initial / 25% maintenance; nothing on the call. For margin the stock counts at no more than the strike (FINRA (f)(2)(H)(v)) |
| Cash-secured put | Strike × 100 in cash, money funds, bank deposits or Treasuries under a year; the premium counts toward it. Schwab's example: a 134 put needs $13,400 = $110 credit + $13,290 cash [P] |
| Protective put | Maintenance is the lesser of 10% of the strike plus the out-of-the-money amount, or the stock's requirement |
| Collar | The lesser of 10% of the put strike plus the put's out-of-the-money amount, or 25% of the call strike |
| Debit vertical (bull call, bear put) | The debit, in full |
| Credit vertical | Strike width × 100; the credit received can be applied (FINRA (f)(2)(H)(i)) |
| Iron condor, butterfly | The lesser of the legs' naked requirements or the max loss (the wider side's width); all legs one expiry |
| Calendar, diagonal | The long must expire on or after the short to count as a spread; pay the debit. Schwab chooses the pairing and may not pick the cheapest (U) |
| Uncovered equity option | Greatest of: premium + 20% of the underlying − the out-of-the-money amount; premium + 10% of the underlying (calls) or of the strike (puts); $100 a contract. Broad indexes 15%; 2x leveraged ETFs 30-40%, 3x 45-60%. $5,000 minimum equity |
| Short straddle or strangle | The higher leg's naked requirement plus the other leg's premium; $5,000 minimum |

- **Cash accounts** (Reg T §220.8, FINRA 4210(f)(2)(N)) [P]: long options, covered calls (stock paid in full) and
  cash-secured puts. Spreads are allowed only in European cash-settled index options expiring together, with the max
  loss in cash; American-style equity spreads need margin or an IRA's limited margin. Cboe's margin page lists
  two-leg spreads for cash accounts without that restriction [Contested]. IBKR applies the European-only rule, and
  an American put spread in an IBKR cash account needs the full short strike [P].
- **Interactive Brokers** [P]: uncovered options need $2,000 of net liquidation value; naked and straddle
  requirements follow FINRA; verticals need the width; iron condors the put-side width (equal wings assumed, U);
  short straddles and strangles are not allowed in cash or IRA accounts; some spreads need 102% of max loss.
- **Intraday margin** (FINRA 4210(d)(2), from 4 Jun 2026, transition to 20 Oct 2027) [P]: legs of a spread sent as
  one order may be treated as executed together, and an assignment with its same-day liquidation as simultaneous.
  Schwab stopped flagging pattern day traders on 8 Jun 2026 [P].

**Costs** (Schwab pricing guide, Apr 2026 [P]; IBKR commissions page [P])
- Schwab: $0.65 a contract online (+$5 automated phone, +$25 broker-assisted); every contract in every leg pays;
  online buy-to-close at $0.05 or less is free; exercise and assignment cost $0. A borrow fee can apply when
  assignment or exercise leaves short stock. No 2026 option-fee change found.
- IBKR Pro (up to 10,000 contracts a month): $0.65 a contract at premiums of $0.10 or more, $0.50 at $0.05-0.10,
  $0.25 below $0.05; lower tiers to $0.15 at volume; $1 minimum per order, per leg of a combo. Plus exchange fees,
  OCC $0.025, the options regulatory fee, CAT $0.0003 a contract and the SEC fee on sales. No exercise or assignment
  commission. IBKR Lite: $0.65 on the first 1,000 US contracts a month.
- Regulatory: FINRA TAF on option sales is paused 1 Oct-31 Dec 2026; the options regulatory fee is about
  $0.012-0.022 a contract (`vendors.md`).
- **Cost drag:** the example iron condor pays 4 × $0.65 = $2.60 to open and the same to close, $5.20 on a $102
  credit (5% of max profit) before the bid-ask, which usually costs more.

**Exercise and assignment timing**
- Holders have until 5:30 pm ET on expiry day to decide; firms may submit contrary advice until 7:30 pm ET (FINRA
  Rule 2360(b)(23)) [Pa]. Schwab's own cut-off is 5:00 pm ET for equity options (4:00 pm for index options on other
  days) [Pa].
- Schwab may sell a long ITM option before the close, tell OCC not to exercise it, or exercise it; long puts are
  exercised only if Schwab can lend the shares [Pa].
- OCC assigns overnight, before the next open; the writer may hear one or more days later and can no longer close
  the position once assigned. A call exercised before the ex-date gets the dividend even if the writer learns after
  it (OCC risk disclosure, Jun 2024) [Pa].
- Cboe C1 won approval (28 May 2026) for a 4:00-4:15 pm ET session in about 20 single-stock option classes, meant to
  reduce contrary-exercise risk; whether it launched on 13 Jul 2026 is (U).

## 18. Choosing among the 11
Start from the view on direction, volatility and time (`options-volatility.md` §8 has the full matrix), then pick the
cheapest structure that is right if you're right and survivable if you're wrong.

| View | IV low (cheap vs forecast RV, low IVP) | IV high (rich vs forecast RV, steep skew) |
|---|---|---|
| Strongly up | Long call | Bull call spread (sells back vega) |
| Up, slowly, or own it anyway | Long call or the stock | Cash-secured put (to buy); covered call (if held) |
| Down, fast | Long put | Bear put spread (sells the rich lower strike) |
| Hedge a long stock | Protective put | Collar or put spread; or hold less stock |
| Range-bound | Calendar (if front IV ≥ back) or stay out | Iron condor; short strangle only with margin that survives a gap |
| Big move, direction unknown | Long straddle (event) or strangle (bigger move) | Usually pass: the move is priced. If it is over-priced against history, a defined-risk short (iron butterfly) |
| IV to rise, spot quiet | Calendar or long back-month options | — |

**Cross-checks before choosing.** (1) The implied move against the move you need (`move`); (2) events inside expiry;
(3) skew percentile: steep skew favours selling puts and buying put spreads, flat skew favours buying puts; (4) term
structure: an inversion means stress, so no new short premium; (5) the account level and margin (§17); (6) the max
loss as a share of equity.

## Failure modes / traps
- **Choosing by win rate.** A 70-85% win rate is the strike placement, not an edge; check the break-even win rate
  (`expectancy`) and the expected P&L at your realized-vol forecast (`strategy --rv`).
- **"Income" framing** for covered calls, cash-secured puts and condors: they are short volatility with equity-like
  or worse left tails.
- **Buying far OTM calls and puts as lottery tickets.** They carry the worst average returns among options and the
  widest relative spreads.
- **Holding long premium through the last weeks** without a catalyst: the decay accelerates as √T shrinks.
- **Holding a spread into the close on expiry day** with spot between the strikes, or near a short strike.
- **Ignoring ex-dividend dates** on short calls and early assignment on deep ITM short puts.
- **Rolling losers for debits,** or further out in time, to avoid booking the loss.
- **Sizing short strangles or naked puts on today's margin.** The requirement is recomputed on the stressed spot,
  in the selloff.
- **Iron condors through earnings** or inside a backwardated term structure.
- **Long straddles judged on direction.** Attribute the P&L: realized vs implied (gamma vs theta) and the IV change
  (vega).
- **Mid-price backtests.** For four-leg structures and single-stock options, the spread is often the whole result.

## Toolkit hooks
- `python scripts/tradekit.py strategy NAME --S 100 --days 30 --vol 0.20` prices any of the 11 presets
  (`long-call`, `long-put`, `covered-call`, `cash-secured-put`, `protective-put`, `bull-call-spread`,
  `bear-put-spread`, `iron-condor`, `straddle`, `strangle`, `calendar`): the legs and their prices; position Greeks
  now, at IV +5 points and halfway to expiry; net premium with commissions; max gain and loss; break-evens; P(profit)
  and P(max loss); expected P&L over cash; Schwab level; cash or FINRA margin; P&L at expiry by price; and a spot
  (±1/±2 SD) × time × IV scenario grid.
  - `--strikes 90,95,105,110` (lowest first) or `--otm 0.05` sets strikes; defaults are spot and spot × (1 ± k·otm).
  - `--px` (market prices, one per option leg, in the printed order) backs out each leg's IV so the Greeks match
    the chain; `--ivs` sets IVs directly (skew). `--rv 0.16` sets the realized-vol forecast for the odds and the
    expected P&L: the edge test.
  - `--short` sells the structure (short straddle or strangle, long iron condor, credit verticals);
    `--kind put --far-days 60` for a put calendar; `--qty`, `--fee`, `--q` for dividends.
  - `custom --leg "+100 stock" --leg "+1 put 95" --leg "-1 call 105"` builds anything else (a collar here);
    `--leg` takes `days=`, `iv=` and `px=` per leg.
  - Later-expiry legs are valued with Black-Scholes at their IV and never below intrinsic (American exercise).
    Odds are lognormal: no skew, no fat tails.
- `bs`, `iv`, `move` for single legs, implied vol from prices and the implied move; `vol FILE` for the realized-vol
  forecast behind `--rv`; `size` and `expectancy` for sizing and the break-even win rate.
- `scanner.py scan --puts` proposes a long put and a bear put spread from the listed chain for bearish candidates;
  `paperkit.py order SYM --put/--call --strike --expiry` paper-trades bought calls and puts (spreads, short options
  and the other structures are not modelled in paperkit).
- `equitykit.py earnings` gives a name's earnings-move history against today's implied move (straddle and
  strangle entries).

## Key sources
Index data and rules (checked 2026-11-14):
- Cboe index factsheets (31 Oct 2026) —
  https://cdn.cboe.com/resources/indices/factsheet/CboeGlobalIndices_BXM-Index.pdf (same pattern for BXMD, BXY, PUT,
  PUTY, PUTR); daily history CSVs — https://cdn-api.cboe.com/api/global/us_indices/daily_prices/CNDR_History.csv (same
  pattern; PPUT, CNDR, BFLY, WPUT, CMBO, CLLZ statistics computed from them); methodologies —
  https://cdn.cboe.com/api/global/us_indices/governance/CNDR_Methodology.pdf
- Cboe crisis-quarter returns for PPUT and CLL — https://www.cboe.com/us/indices/index-protection/
- Bondarenko (2019, Cboe-sponsored), put-writing 1986-2018 —
  https://www.cboe.com/insights/posts/white-paper-shows-volatility-risk-premium-facilitated-higher-risk-adjusted-returns-for-put-index
- Callan (2006) BXM study — https://cdn.cboe.com/resources/education/research_publications/Callan_CBOE.pdf
- Hill, Balasubramanian, Gregory & Tierens (2006) FAJ 62(5): covered index writing —
  https://prd-web.optionseducation.org/getmedia/da1042f9-5e5c-4806-bb4c-50d4d9a11d1d/finding-alpha-via-covered-index-writing.pdf
- Kapadia & Szado (2007, 2011 update): Russell 2000 buy-writes —
  https://www.optionseducation.org/getmedia/8cd47e98-89f5-432a-8905-ba0c805eaa62/oic-buy-write-strategy-full.pdf
- Israelov & Nielsen (2014) FAJ: covered calls, one fact and eight myths —
  https://www.aqr.com/-/media/AQR/Documents/Insights/Journal-Article/FAJ-Covered-Call-Strategies-One-Fact-and-Eight-Myths.pdf
- Israelov & Klein (2016) JAI: collars; Israelov (2017) SSRN: PutWrite vs BuyWrite; Israelov (2019) JAI: pathetic
  protection
- Fund factsheets: JEPI —
  https://am.jpmorgan.com/content/dam/jpm-am-aem/americas/us/en/literature/fact-sheet/etfs/FS-JEPI.PDF ; QYLD —
  https://assets.globalxetfs.com/funds/documents/qyld/Fact-Sheet_QYLD.pdf ; SPYI — https://neosfunds.com/spyi/

Option returns:
- Constantinides, Jackwerth & Savov (2013) RAPS 3(1): the puzzle of index option returns —
  https://kops.uni-konstanz.de/server/api/core/bitstreams/d9eb4523-5c7e-45ad-9f79-7365493dd758/content
- Broadie, Chernov & Johannes (2009) RFS 22(11): understanding index option returns —
  https://researchonline.lse.ac.uk/id/eprint/32229
- Bondarenko (2014) QJF 4(3): why are put options so expensive? —
  https://ideas.repec.org/a/wsi/qjfxxx/v04y2014i03ns2010139214500153.html
- Doshi, Jacobs & Sert (WP, Jul 2026): SPX option returns 1996-2023 —
  https://www.bauer.uh.edu/hdoshi/docs/DJS_OptionReturns_July21.pdf
- Coval & Shumway (2001) JF 56(3); Ni (2008) SSRN: stock option returns; Boyer & Vorkink (2014) JF 69(4) —
  https://ideas.repec.org/a/bla/jfinan/v69y2014i4p1485-1527.html
- Goyal & Saretto (2009) JFE 94(2); Cao & Han (2013) JFE 108(1); Vasquez (2017) JFQA 52(6)
- Kozhan, Neuberger & Schneider (2013) RFS 26(9): the skew risk premium —
  https://econpapers.repec.org/RePEc:oup:rfinst:v:26:y:2013:i:9:p:2174-2203
- McKeon (2016) J. Asset Management 17(6): S&P option strategies —
  https://ideas.repec.org/a/pal/assmgt/v17y2016i6d10.1057_jam.2016.6.html
- Santa-Clara & Saretto (2009) JFM 12(3): option strategies, good deals and margin calls —
  https://escholarship.org/content/qt0499w44p/qt0499w44p_noSplash_a53c67820225e4ebff79454eb60c5447.pdf
- Johnson (2017) JFQA 52(6): VIX term structure — https://ideas.repec.org/a/cup/jfinqa/v52y2017i06p2461-2490_00.html ;
  Dew-Becker, Giglio, Le & Rodriguez (2017) JFE 123(2) —
  https://econpapers.repec.org/RePEc:eee:jfinec:v:123:y:2017:i:2:p:225-250 ; Dubinsky, Johannes, Kaeck & Seeger (2019)
  RFS 32(2): earnings uncertainty
- Gao, Xing & Zhang (2018) JFQA 53(6): earnings straddles (see `options-volatility.md`)

Retail outcomes and management:
- Bryzgalova, Pavlova & Sikorskaya (2023) JF 78(6): retail options trading —
  https://lbsresearch.london.edu/id/eprint/2827/
- de Silva, Smith & So (2025) Review of Finance: losing is optional —
  https://www.gsb.stanford.edu/faculty-research/working-papers/losing-optional-retail-option-trading-expected-announcement
- Hu, Kirilova, Park & Ryu (2024) Management Science 70(7) —
  https://econpapers.repec.org/RePEc:inm:ormnsc:v:70:y:2024:i:7:p:4742-4761
- SEBI (23 Sep 2024): F&O trader outcomes FY22-24 —
  https://www.sebi.gov.in/media-and-notifications/press-releases/sep-2024/updated-sebi-study-reveals-93-of-individual-traders-incurred-losses-in-equity-fando-between-fy22-and-fy24-aggregate-losses-exceed-1-8-lakh-crores-over-three-years_86906.html
- tastylive (2016): managing strangles at 50% —
  https://www.tastylive.com/news-insights/why-manage-at-50-not-25-for-short-strangles ; Blom (2022) SteadyOptions:
  managing winners —
  https://steadyoptions.com/articles/does-%E2%80%9Cmanaging-winners%E2%80%9D-add-value-to-short-strangles-r618

Exercise and assignment:
- Pool, Stoll & Whaley (2008) JFM 11(1): failure to exercise calls; Barraclough & Whaley (2012) JF 67(4): early
  exercise of puts; Jensen & Pedersen (2016) JFE 121(2) —
  https://econpapers.repec.org/RePEc:eee:jfinec:v:121:y:2016:i:2:p:278-299
- OIC exercise FAQ (OCC Rule 805, $0.01) — https://www.optionseducation.org/referencelibrary/faq/options-exercise ;
  FINRA RN 10-36 (contrary advice to 7:30 pm) — https://www.finra.org/rules-guidance/notices/10-36 ;
  FINRA on assignment — https://www.finra.org/investors/insights/trading-options-understanding-assignment
- SR-CBOE-2026-007 (Monday/Wednesday expiries, weekly volume share) —
  https://cdn.cboe.com/resources/regulation/rule_filings/approved/2026/SR-CBOE-2026-007.pdf

Account rules:
- Schwab margin rates and requirements — https://www.schwab.com/margin/margin-rates-and-requirements ; options and
  margin application (APP20247, 12/24) — https://www.schwab.com/public/file/P-1038697 ; IRA spreads supplement
  (APP40015) —
  https://www.schwab.com/resource/supplemental-application-and-agreement-limited-margin-and-trading-option-spreads-your-ira
  ; options in an IRA — https://www.schwab.com/learn/story/trading-options-ira ; pricing guide (Apr 2026) —
  https://www.schwab.com/legal/schwab-pricing-guide-for-individual-investors
- FINRA Rule 4210 — https://www.finra.org/rules-guidance/rulebooks/finra-rules/4210 ; Rule 2360 —
  https://www.finra.org/rules-guidance/rulebooks/finra-rules/2360 ; Reg T —
  https://www.ecfr.gov/current/title-12/part-220
- Cboe strategy-based margin — https://www.cboe.com/markets/us/options/margin/strategy-based-margin
- IBKR option commissions — https://www.interactivebrokers.com/en/pricing/commissions-options.php?re=amer
- Cboe C1 extended hours (28 May 2026) —
  https://ir.cboe.com/news/news-details/2026/Cboe-Receives-SEC-Approval-to-Offer-Extended-Trading-Hours-for-Select-Multi-Listed-Single-Stock-Options/default.aspx
