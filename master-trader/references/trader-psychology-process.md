# Trader Psychology, Process and Coaching

*Read when: a trader asks why they keep losing, whether their edge or track record is real, or how to size up; describes tilt, revenge trading, freezing, cutting winners or holding losers; wants a trade plan, review or journal template, or drawdown and stop-trading rules; quotes Market Wizards lore; or asks to be coached.*

**Contents:** Core principles · 1 Base rates · 2 Biases · 3 Debiasing that works · 4 Physiology, emotion, tilt · 5 Elite-trader practices (lore) · 6 Process vs outcome · 7 Edge and sample size · 8 R, expectancy, SQN · 9 Sizing, scaling, pyramiding · 10 Drawdown and stop-trading rules · 11 Pre-trade plan template · 12 Post-trade review template · 13 Journal schema · 14 Diagnosing a struggling trader · 15 Coaching conversation · Where TA fits · Failure modes · Toolkit hooks · Key sources

## Core principles

- **Start from the base rate.** In the best-documented datasets, about 1–3% of persistent day traders become durably profitable. Treat a new trader's results as noise until their sample says otherwise. Use this to calibrate: say it once, then turn to the levers the trader controls.
- **Structure beats willpower.** Pre-committed exits reduced the disposition effect in experiments, and reminders did nothing (Fischbacher et al. 2017). Advise rules, resting orders and if-then plans. Do not advise "be more disciplined".
- **Grade decisions separately from outcomes.** Judge any single trade on its process. Judge a setup on mean R with a confidence interval over a large sample. A good process that wins nothing on 20 trades is not yet a broken process.
- **Sample size is the main constraint.** Thirty trades cannot tell a 40% win rate from a 60% one. A +0.25R edge takes about 90 trades to reach t≈2. Most "lessons" traders draw from a few trades are noise.
- **Every edge needs a counterparty.** Ask who is on the other side of the trade and why they are willing to be there (Mauboussin). If the trader cannot answer, treat the setup as an experiment, not as an edge.
- **Prior P&L changes the next decision.** Morning losses and gains measurably shift afternoon risk-taking, even among professionals. Write the rules in advance so they bind at exactly those moments.
- **The trader's state is a risk factor.** Sleep loss, stress hormones and emotional intensity bias risk-taking. When the trader's state is poor, cut size. Pushing through is not a strategy.
- **Diagnose before you counsel.** Many problems that look psychological are really problems of a lost edge or poor sizing (Steenbarger). Read the journal first.
- **Elite-trader wisdom is hypothesis, not proof.** Market Wizards themes come from survivors. They are useful because they match the experimental bias evidence, not because the interviews prove anything.

## 1. Base rates: calibrate, don't lecture

| Population (period) | Finding | Tag | Source |
|---|---|---|---|
| US discount-broker households (1991–96) | The most active traders earned 11.4%/yr against a market return of 17.9%. Average turnover was about 75%/yr | [Strong] | Barber & Odean 2000 |
| Same population | Stocks bought underperformed stocks sold by ~3.3pp over the next year, before costs | [Strong] | Odean 1999 |
| Brazil mini-index futures day traders who persisted ≥300 days (2013–15) | 97% lost money. 0.4% earned more than a bank teller (~US$54/day). No evidence of learning | [Moderate] full population, one study | Chague, De-Losso & Giovannetti WP |
| Taiwan day traders (1992–2006, complete exchange data) | <1% are predictably profitable net of fees. Prior-year top performers show some persistence | [Strong] | Barber, Lee, Liu & Odean 2014 |
| Taiwan individual investors | Trading losses ≈ 2.2% of GDP, a ~3.8pp/yr penalty. Institutions captured the losses | [Strong] | Barber et al. 2009 |
| US retail options (Nov 2019–Jun 2021) | The aggregate retail portfolio lost ~$2.1B, assuming a 10-day hold. Most of the loss came from indirect costs (~$6.4B, measured as trade price vs midquote). About half of retail volume was in weeklies, with a 12.6% quoted spread (6.6% effective) | [Moderate] | Bryzgalova, Pavlova & Sikorskaya 2023, verified in the JF text. The widely quoted $1.14B/$4.13B figures come from an earlier draft |
| Retail options around earnings | Retail traders lose 5–9% on average, and 10–14% around high-expected-volatility announcements. They overpay relative to realized volatility | [Moderate] | de Silva, Smith & So 2025 |
| Robinhood users' herding | The day's most-bought stocks earned an average 20-day abnormal return of −4.7% | [Moderate] | Barber, Huang, Odean & Schwarz 2022, verified in the abstract |
| EU retail CFD accounts (national regulator analyses, 2018) | 74–89% of accounts lose money. Average loss per client was €1,600–€29,000. This led to leverage caps, a 50% margin close-out rule and negative-balance protection | [Strong] | ESMA 2018 |
| India, individual equity F&O traders | FY22–24: 93% of ~11.3M traders lost money, with an average loss of ~₹2 lakh. More than 75% of loss-makers kept trading. FY24: 91.1% lost. FY25: 91% lost. FY26: 87.7% lost, ₹91,685 crore in aggregate | [Strong] to FY24 (SEBI primary). FY25–26 [Moderate]: press reports of SEBI's Jul 2025 and Aug 2026 studies, primary not fetched | SEBI 2024; press 2025–26 |
| Finnish investors | Performance improves with experience, but much of the apparent "learning" is poor traders quitting | [Strong] | Seru, Shumway & Stoffman 2010 |
| Professionals (CBOT floor traders, prop day traders) | They also hold losers longer than winners | [Moderate] | Locke & Mann 2005; Garvey & Murphy 2004 |

Counterpoints [Moderate]: aggregate retail order imbalance predicts returns over the following weeks (Kelley & Tetlock 2013; Boehmer et al. 2021). The aggregate Robinhood crowd portfolio also did reasonably well (Welch 2022). Individual traders' losses come from their costs, timing, instrument choice and concentration, so the crowd's direction can be right while the individuals still lose.

How to use these numbers:
1. State the prior once, with its source and period. Then move straight to what the trader controls.
2. Point out that most of the losses come from controllable sources: spreads and costs, overtrading, lottery-like instruments (weeklies, buying event volatility), leverage, and holding losers.
3. Point out that persistence despite losses is the norm. Self-assessment does not correct itself, so quit and size-down criteria must be written in advance (§10).
4. Skill exists and persists in a small minority. Whether *this* trader has it is a sample-size question (§7). It cannot be answered by how they feel about their trading.

## 2. Biases with measured trading impact

| Bias | Evidence | How it shows in a journal | Countermeasure |
|---|---|---|---|
| Disposition effect | [Strong] Investors realized 14.8% of paper gains against 9.8% of paper losses, and the winners they sold beat the losers they held by ~3.4pp over the next year (Odean 1998). Professionals show it too. Experience removes the reluctance to realize losses but cuts premature gain-taking by only ~37% (Feng & Seasholes 2005) | Average loss worse than −1R. Losers held longer than winners. Realized R on winners below planned R | Resting stop and target at entry. Hide the entry price. Ask "would I open this here, at this size, today?" |
| Loss aversion, myopic loss aversion | [Strong] λ ≈ 2.25 (Tversky & Kahneman 1992). [Moderate] CBOT pros showed more myopic loss aversion than students (Haigh & List 2005) | Valid setups skipped after losses. Targets too small | Portfolio framing (§3). Check P&L less often (swing and position traders) |
| Break-even seeking vs house money | [Moderate] CBOT locals with morning losses were ~15–16% more likely to take above-average afternoon risk, and other traders profited against them (Coval & Shumway 2005). [Contested] on direction: Frino et al. 2008 and Liu et al. 2010 find *more* risk after gains. The robust finding is that prior intraday P&L moves risk-taking either way | Size or trade frequency rises after a red morning, or after a green one | Daily loss limit. No intraday size increases. Size fixed from equity at the session open |
| Overconfidence, overtrading | [Strong] Men traded 45% more than women and lost 2.65pp/yr to trading against 1.72pp (Barber & Odean 2001). Sensation-seeking predicts turnover (Grinblatt & Keloharju 2009). Better-than-average beliefs drive volume (Glaser & Weber 2007) | High trade count. Trades outside the playbook. Costs a large share of gross P&L | Cap on trades per day. Playbook-only rule. Track expectancy on off-plan trades |
| Illusion of control | [Moderate] Among 107 bank traders, a higher illusion of control went with worse manager ratings and lower pay (Fenton-O'Creevy et al. 2003) | Tinkering with live trades. "I can manage it" | Exits defined before entry. Outside view |
| Anchoring | [Strong] as a general heuristic (Tversky & Kahneman 1974). In markets, investors anchor on the 52-week high (George & Hwang 2004) | Stops at breakeven or entry for no reason. Waiting to "get back to" a price | Judge on current merits. Hide the purchase price |
| Extrapolation, recency | [Strong] Expected returns extrapolate recent returns and correlate negatively with realized returns (Greenwood & Shleifer 2014) | Chasing after streaks. Rules rewritten after 3–5 trades | Base rates. A minimum-N rule before any rule change |
| Confirmation bias | [Moderate] Investors with stronger confirmation bias were more overconfident, traded more and earned less (Park et al. 2013) | Only supporting evidence in the notes. No invalidation level written | Write the invalidation first. Premortem |
| Sunk cost, narrative fallacy | [Lore] for trading. Established in general psychology (Arkes & Blumer 1985), but no trading-specific causal study | Averaging down. The thesis rewritten after entry | No adds to losers. Thesis frozen at entry |

## 3. Debiasing techniques that have evidence

| Technique | Evidence | Implement as |
|---|---|---|
| Pre-commitment orders | [Moderate] Stop-loss and take-gain orders cut the disposition effect, mainly by increasing realized losses. A reminder alone had no effect (Fischbacher, Hoffmann & Schudy 2017, lab) | Stop and target sent as resting OCO orders at entry. The stop may move only in the trade's favor |
| Hide the purchase price | [Moderate] Lower salience of the purchase price cut the disposition effect by ~25% (Frydman & Rangel 2014, lab) | Hide the cost-basis and open-P&L columns. Manage from the chart and the plan levels |
| "Think like a trader" (portfolio frame) | [Moderate] Reduced behavioral loss aversion and physiological arousal to losses (Sokol-Hessner et al. 2009) | Before a session, say "this trade is one of the next 100". Review R statistics in aggregate, never single trades |
| If-then plans | [Strong] for goal attainment in general: d ≈ 0.65 across 94 studies (Gollwitzer & Sheeran 2006). Not tested on trading P&L | "If price closes below X, I exit." "If I hit −2R today, I stop." Written before the session |
| Premortem | [Moderate] Prospective hindsight raised the generation of correct reasons by ~30% (Mitchell, Russo & Pennington 1989). Klein 2007 turned it into a method | Before new or large positions, ask "it lost 2R; why?" and list 3 reasons |
| Outside view | [Moderate] Reference-class base rates counter inside-view optimism (Kahneman & Lovallo 1993) | Every plan quotes the setup's logged N, win rate and mean R |
| Less frequent feedback (long horizons only) | [Moderate] Less frequent feedback reduced myopic loss aversion and raised acceptance of positive-EV risk (Gneezy & Potters 1997) | Swing and position traders review P&L daily or weekly, not tick by tick. Intraday traders need the opposite: hard limits |
| Checklists | [Strong] in surgery: deaths fell from 1.5% to 0.8% and complications from 11.0% to 7.0% (Haynes et al. 2009). [Lore] for trading | A short pre-trade checklist (§11) to catch omissions |
| Decision hygiene | [Moderate] Score components independently before forming a holistic view (Kahneman, Sibony & Sunstein 2021) | Score trend, catalyst, positioning, R:R and liquidity separately, each 1–5, then decide |
| Calibration scoring | [Strong] Training and teaming improved forecast accuracy, and a short training module added ~10% (Mellers et al. 2014; Tetlock & Gardner 2015) | Log P(thesis right) on each trade and compute a monthly Brier score (§13) |

Caveat [Weak]: no field study shows that journaling or checklists causally improve trading P&L. The templates below are evidence-informed syntheses, not validated instruments.

## 4. Physiology, emotion and tilt

| Finding | Tag | Coaching use |
|---|---|---|
| On a London floor, morning testosterone was higher on above-average-profit days. Cortisol rose with P&L variance and market volatility (Coates & Herbert 2008, n=17 over 8 days; correlational) | [Weak] | After a hot streak, expect more appetite for risk, so keep size on the rule |
| Experimentally raising cortisol for 8 days made people more risk-averse (Kandasamy et al. 2014) | [Moderate] | After volatile stretches, expect under-risking and missed A-setups. That pattern is a state effect, not a lost edge |
| Professional traders showed physiological responses to volatility and reversals, and less experienced traders responded more (Lo & Repin 2002, n=10) | [Weak] | Arousal is normal. Plan for it; do not try to eliminate it |
| Among 80 day-traders, more intense emotional reactions to gains *and* losses went with worse performance. There was no distinct "trader personality" (Lo, Repin & Steenbarger 2005; self-selected sample) | [Weak] | Track emotional intensity next to R. Skill may be learnable |
| Higher-performing bank traders regulated emotion; they did not suppress it (Fenton-O'Creevy et al. 2011, n=118). Reappraisal beats suppression (Gross & John 2003) | [Moderate] / [Strong] | Notice it, label it, treat it as data (Shull's framing). Then follow the pre-committed rule |
| One night without sleep shifted choices toward gain-seeking and lowered sensitivity to losses (Venkatraman et al. 2011) | [Moderate] | After a short night: smaller size, A-setups only, no new strategies |
| Brain activation before a choice biased risk-taking and risk-seeking mistakes (Kuhnen & Knutson 2005) | [Moderate] | Supports cooling-off pauses before re-entry |
| A lower 2D:4D digit ratio predicted HFT profitability and survival (Coates, Gurnell & Rustichini 2009, n=44) | [Weak] | Not actionable. Do not use it in coaching |

**Tilt** (a poker term for emotion-driven play after losses) is documented qualitatively in poker: players lose control after bad beats or perceived unfairness (Palomäki et al. 2013) [Moderate, qualitative]. The trading version is revenge trading, which matches the break-even evidence in §2.
- *Signs:* trades come faster than the setup frequency, size rises after a loss, the trader enters without a written stop, re-enters the same name right after a stop-out, or says "the market owes me".
- *Circuit breaker (pre-committed):* 2 consecutive rule-breaking trades, or the daily loss limit → flat, platform closed, 15+ min away, review written before any further trade. Daily limit hit → done for the day. The cool-off length is a convention [Lore].
- *Re-entry test:* "Is this in the playbook, and would I take it at this size if I were flat and green today?"

**Expertise limits.** Intuition is trustworthy only where cues are valid and feedback is fast and clear, and stock picking is cited as a low-validity domain (Kahneman & Klein 2009) [Moderate]. Deliberate practice explains under 1% of performance variance in professions, against ~26% in games (Macnamara et al. 2014) [Strong]. So trust "feel" only in narrow, high-repetition setups that the trader has logged. Specialization beats breadth.

**Practitioner frameworks [Lore]** (no controlled trial shows they improve P&L): Steenbarger treats trading as performance. He asks what the trader does when trading *well* and has them do more of it, uses daily report cards, and observes that many "psych" problems are really edge or sizing problems. Shull treats emotions as information to read in context, not noise to suppress.

## 5. Elite-trader practices: anecdotal, survivor-selected, paraphrased

These are interview and book accounts of people chosen *because* they succeeded. All quotes are paraphrased from memory of the texts, so check them before quoting verbatim. Present them as practitioner versions of evidence-based debiasing.

| Trader | Practice (paraphrased) [Lore] | Evidence-based analogue | Coaching use / danger |
|---|---|---|---|
| Druckenmiller (via Soros) | What counts is how much you make when right and lose when wrong, not how often you are right. When conviction is very high, size very large. Reportedly no losing year at Duquesne 1981–2010 (press and Mallaby 2010, not audited), but he also tells of costly errors such as buying tech near the March 2000 top | Payoff asymmetry. Expectancy beats hit rate | **The most dangerous lesson for novices.** Allow conviction sizing only when logged calibration shows high-confidence trades have higher mean R, and keep it capped by a max risk per idea |
| Soros | Reflexivity: biased views change fundamentals, which feed back into prices. Kept a real-time diary of hypotheses as falsifiable bets (*Alchemy of Finance* 1987). Commonly attributed, not verified: "invest first, investigate later", meaning probe small and add on confirmation | Premortem. Calibration logging. Pyramiding on confirmation | Make every thesis falsifiable, with a written invalidation |
| Paul Tudor Jones | Defense first. Cut size when trading poorly. "Losers average losers." Exits anything below its 200-day MA. Targets ~5:1 (Schwager 1989; Robbins 2014) | Drawdown-contingent sizing (Grossman & Zhou). Disposition countermeasure | At 5:1 the breakeven win rate is 1/(1+5) ≈ 16.7% before costs. Treat 5:1 and the 200DMA as illustrations, not parameters |
| Ed Seykota | The elements of good trading are cutting losses, cutting losses and cutting losses. Results reflect what the trader unconsciously wants | Disposition effect | Ask what the trader is actually optimizing (action? being right? P&L?) |
| Jesse Livermore | The big money came from sitting through trends. Pyramid only after confirmation. Never average down. Wait for pivotal points. He went broke several times despite knowing his rules (historical record) | Time-series momentum gives a rationale for adding to winners | Knowing the rules is not the same as following them. That gap is why rules must be mechanical |
| Schwager's themes (1989–2020) | No holy grail. The method must fit the trader's temperament. Risk management matters more than entries. Trade only a verifiable edge, with patience. Size down or stop in drawdowns. Think independently and be willing to reverse. A few high-conviction trades drive the results | Each maps to a bias finding (§2) | Frame these as hypotheses to test in the trader's own journal |
| Desk process | SMB PlayBook: context, technicals, tape, intuition, entry, exits, and the reason to size up, plus recorded reviews and "one good trade" at a time (Bellafiore 2010, 2013). Avoid "resulting" (Duke 2018) | Checklists. Process grading | These become the templates in §11–13 |

## 6. Process vs outcome

| | Good outcome | Bad outcome |
|---|---|---|
| **Good process** | Earned. Repeat it | Variance. Repeat it. Do not change rules on it |
| **Bad process** | **Dumb luck: the most dangerous quadrant.** It reinforces rule-breaking. Flag it hard | Deserved. Fix the process, not the trader's self-worth |

Procedure to grade one trade (outcome hidden or ignored):
1. Was it a playbook setup, with the plan written *before* entry?
2. Was the size within the risk rule and the tier rule? Were the stop and target placed as orders?
3. Were the exits taken per plan? List every deviation.
4. What was knowable at entry? Strip out hindsight; Duke's test is "what did I know, and when?"
5. Assign a process grade (rubric in §12). Only then look at the R.

Anti-resulting rules: no rule change because of a single trade. Change setup rules only at the scheduled weekly or monthly review, and only when the confidence interval supports it (§7).

## 7. Sources of edge and sample-size math

| Edge source (Mauboussin 2019) [Lore framework] | Who is on the other side | Example from the notes |
|---|---|---|
| Behavioral | Traders acting on biases | Fading the afternoon break-even trades of traders with losing mornings (Coval & Shumway 2005). Anchoring at the 52-week high (George & Hwang 2004) |
| Analytical | People with the same information who weigh it worse | Better synthesis of public data |
| Informational | People who are slower or less informed (legally) | Faster or better legal data |
| Technical/structural | Forced or non-economic traders | Index rebalances, liquidity needs. SOES bandits exploited slow quote updates, and the edge vanished when the market structure changed (Harris & Schultz 1998) |

Edges cost money to find and they decay: markets cannot be fully informationally efficient when information is costly (Grossman & Stiglitz 1980), and edges adapt away (Lo 2004 AMH). FX technical-rule profits faded after the 1980s (Neely et al. 2009) [Strong]. Treat any widely taught setup as already arbitraged until the trader's own data shows otherwise.

```
R            = (exit − entry) × size × side / initial risk (entry→stop × size)
expectancy E = mean(R);  SD = stdev(R)   (compute SD from the actual R list)
t            = E / SD × √N                 (this IS Tharp's SQN)
N for t = z  = (z × SD / E)²
win-rate SE  = √(p(1−p)/n);  95% CI ≈ ±1.96 × SE
Sharpe t     ≈ SR_annual × √years           (Lo 2002; serial correlation shifts SEs)
```

| Win rate p = 0.5 | 95% CI | | Edge (SD 1.2R) | N for t=2 | N for t=3 |
|---|---|---|---|---|---|
| n = 30 | ±18pp | | E = +0.25R | ~92 | ~207 |
| n = 100 | ±10pp | | E = +0.10R | ~576 | ~1,296 |
| n = 400 | ±5pp | | Sharpe 1.0 / 0.5 | ~4 yrs / ~16 yrs to t≈2 | |

[Strong, arithmetic.] Fat-tailed setups (low win rate, high R:R) need more trades.
- **Multiple testing** [Moderate]: a new factor needs t > 3, not 2 (Harvey, Liu & Zhu 2016). Ask how many setup variants were tried, and deflate for them (DSR; Bailey & López de Prado 2014). With enough trials, high in-sample Sharpes appear by chance (Bailey et al. 2014).
- **Validation standard** (synthesis): a setup counts as validated only after a pre-registered forward sample, roughly 100+ trades for a moderate edge, judged on mean R with a CI and not on win rate or $ P&L. Expect live expectancy to come in below journaled or backtested expectancy.
- Learning is slow and partly survivorship (Seru et al. 2010; Barber et al. 2020) [Strong], so self-assessment from small samples is unreliable.

## 8. R-multiples, expectancy, SQN

- **1R** = the initial dollar risk (entry to stop × size), fixed at entry. Record every outcome in R. Moving the stop does not change 1R.
- **Expectancy** = mean R per trade = p·W̄ − (1−p)·L̄. Breakeven win rate = L̄/(W̄+L̄). **Profit factor** = gross wins / gross losses.
- **SQN** (Tharp) = √N × mean(R)/SD(R). It is a t-statistic, so read it like one (<2: not distinguishable from luck). It grows with √N, so compare SQNs only at similar N [Lore metric, Strong arithmetic].
- A two-point model (one average win, one average loss) **understates SD** when wins vary. Compute SD from the trader's actual R list.
- Healthy signatures: average loss close to −1.0R (much worse means stops are slipping or being moved); MFE capture (realized R ÷ MFE in R on winners) stable or rising; outcomes after a loss look like outcomes after a win.
- Tharp's claim that sizing drives most of the variation in results [Lore] matches the math: the same expectancy at a different risk % gives very different drawdown paths (run `ruin`).

## 9. Sizing, scaling and pyramiding

- **Default risk per trade: 0.25–1% of equity** [Lore: practitioner norm, no study sets the optimum]. New or unvalidated setups get the bottom of that range.
- **Kelly** [Strong, math]: f* = edge/odds. Growth at fraction k of Kelly is g = (2k − k²)·g*, so half-Kelly earns ~75% of the maximum growth at half the volatility. Betting above 2× Kelly gives negative growth. Edge estimates are noisy, so stay at or below half-Kelly of a *haircut* edge.
- **Size tiers.** A, B and C tiers (for example 1×, 0.5× and 0.25× of base risk) are assigned by each setup's logged mean R and N. **Conviction sizing** (Druckenmiller) unlocks only when the trader's high-confidence trades show higher mean R in their own log, never as a feeling, and always under a max-risk-per-idea cap.
- **Pyramiding**: add only to confirmed winners, never to losers (PTJ, Livermore [Lore]). The disposition evidence makes averaging down a known failure mode. Time-series momentum gives an indirect rationale for adding into trends [Moderate, indirect]. Documented protocol (Turtles, Faith 2007) [Lore]: 1N = 20-day ATR; size each unit so 1N = 1% of equity; stop at 2N; add a unit every ½N of favorable move; at most 4 units per market. No evidence compares pyramiding with fixed sizing for discretionary traders [gap].
- Coaching default [Lore]: after each add, move the stop so that total open risk does not exceed the risk approved at the initial plan.
- **Stop placement**: put the stop at the thesis-invalidation level, not just beyond an obvious round number or swing level. Stops cluster there and get run (Osler 2003) [Moderate]. If the right stop is wide, cut the size; do not tighten the stop.

## 10. Drawdown and stop-trading rules

Recovery math [Strong]: a loss of x needs a gain of x/(1−x) to recover. Losing 10% needs +11.1%, losing 20% needs +25%, and losing 50% needs +100%. Under a drawdown constraint, the optimal policy cuts exposure as wealth nears the floor (Grossman & Zhou 1993) [Strong, theory]. That is the formal version of PTJ's "size down when trading poorly".

Default ladder. The numbers are conventions [Lore]; no study sets them. Write it before trading and adjust it to the setup with `ruin`.

| Trigger | Action |
|---|---|
| Daily loss reaches ~2–3R | Flat. Done for the day. Write a review before the next session |
| Red morning or green morning | No intraday size increase in either case (break-even and house-money evidence, §2) |
| Weekly loss limit (set in advance, e.g. ~2× the daily limit) | Rest of the week at half size, A-setups only |
| Drawdown of 5–10% from the equity peak | Halve size until a new high or until N plan-compliant trades |
| Deeper pre-set threshold | Full stop. Full journal review: is the edge gone, or is execution the problem? Restart at minimum size |
| Pre-registered setup sample done, CI of mean R below 0 | Retire or rework the setup. Do not "give it more time" without writing a new N |

Benchmark: multi-manager platforms reportedly cut a PM's capital at ~5% loss and terminate at ~7.5% (press-reported, not verified) [Weak]. Calibrate the thresholds: with a +0.26R edge (45% win rate, 1.8:1) at 1% risk, the toolkit Monte Carlo gives a 55% chance of a ≥10% drawdown within 250 trades, and a ~2% chance of a ≥20% drawdown. So a −10% "halve size" rule will trigger even when the edge is real, which is intended. A −20% hit at that risk is strong evidence that something has changed (this assumes iid two-outcome trades; streaky or fat-tailed results make deep drawdowns more likely).

Restart protocol: minimum size, A-setups only, and a written plan for every trade. Return to normal size after a pre-set number of trades with ≥90% plan adherence. Adherence is the gate, not P&L (convention).

## 11. Pre-trade plan template

Fill it in and timestamp it before entry. A missing field means no trade, or minimum size as an experiment.

```
1  SETUP ID      playbook name/version ___   (none -> EXPERIMENT, minimum size)
2  THESIS        one sentence ___
   EDGE SOURCE   behavioral / analytical / informational / structural
   OTHER SIDE    who takes the other side, and why ___
3  CATALYST      why now ___   event? is implied vol already pricing it? (retail overpays)
4  INVALIDATION  price/event that proves me wrong ___ -> STOP ___ as resting order
                 (not just beyond an obvious round number / swing level)
5  TARGETS       T1 ___ T2 ___   TIME STOP: out if ___ by ___
   R:R           ___ : 1   breakeven win rate = 1/(1+R:R) = ___
6  SIZE          1R = $___ = ___% equity   tier A/B/C because ___ (setup log)
   ADDS          only if ___ confirms; new stop ___; total open risk <= ___R
7  SCENARIOS     bull __% (+__R) | base __% (__R) | bear __% (−__R)  -> EV ___R
   PREMORTEM     "Two weeks on, this lost 2R. Why?"  1) ___ 2) ___ 3) ___
8  BASE RATE     this setup: N ___ win ___% mean ___R (95% CI ___ to ___)
9  STATE         sleep ___h  stress 1-5 ___  today ___R  week ___R  limits ___/___
                 Trying to win back a loss?  Y -> no trade
10 IF-THEN       If ___ then I ___.  If ___ then I ___.  If news ___ then reassess.
   CONFIDENCE    P(thesis right) = ___%  (scored monthly, Brier)
```
Intraday short form (one line, before every trade): `setup | stop (order placed?) | target | 1R $ | today vs limit | state OK?`

## 12. Post-trade review template

Do it the same day. Grade the process before looking at the $ P&L.

```
OUTCOME      ___R   MAE ___R   MFE ___R   exit: stop / target / time / thesis broken / discretion
PLAN FOLLOWED  Y/N   deviations: entry | size | stop moved | early exit | add | no plan | other ___
PROCESS GRADE  A-F (rubric)              QUADRANT  good/good | good/bad | bad/good | bad/bad
KNOWABLE?    what I knew at entry vs what I learned after ___
STATE        emotion label ___  intensity 1-5 ___  did it change an action? Y/N
THESIS       stated P ___%   thesis right? Y/N
TAKE AGAIN?  same setup, info, price, size: Y/N
LESSON       one line, tagged to setup ID. Rule changes only at weekly review.
```
Process rubric. **A**: playbook setup, written plan, size per rule, exits per plan. **B**: a minor deviation that did not change the risk (entry slippage). **C**: a deviation that changed the R (early exit, late chase). **D**: a broken risk rule (stop moved away, oversize, no stop order). **F**: an off-playbook trade with no plan, a revenge trade, or a loss-limit breach.

## 13. Trading journal schema

| Field | Values | Why |
|---|---|---|
| trade_id, open_ts, close_ts | id, timestamps | Hold time, time-of-day effects |
| instrument, side, timeframe | text | Slice by market |
| setup_id, setup_version | playbook key | Expectancy by setup. Variant count for deflation |
| plan_written_before | Y/N | Gate for process grading |
| thesis, edge_source, catalyst | text, enum | Edge audit (§7) |
| entry, stop_initial, target, exit | prices | R math. Stop-drift check |
| size, risk_usd (1R), risk_pct | numbers | Sizing-rule compliance |
| exit_reason | stop/target/time/thesis/discretion | Early-exit and stop-moving patterns |
| r_multiple, fees_slippage_usd | number | Net expectancy. Costs as % of gross |
| mae_r, mfe_r | number | Stop quality. Exit efficiency |
| confidence_p | 0–1 | Calibration (Brier) |
| rule_flags | stop_order_placed, size_ok, exits_per_plan, no_add_to_loser | Adherence rate |
| process_grade, quadrant | A–F, enum | Process vs outcome |
| sleep_h, stress_1to5, emotion_label, intensity_1to5 | numbers, text | State-conditioned expectancy |
| day_pnl_r_at_entry, consec_losses_before, trade_no_today | numbers | Tilt and break-even detection |
| notes, screenshot | text, link | Playbook building |

**Compute weekly:** N; win rate; average win and loss in R; expectancy; SD; t (SQN) by setup; adherence %; expectancy on-plan vs off-plan; costs ÷ gross P&L; largest loss in R; loss-limit breaches; mean R and size *after a loss* vs *after a win*; trades per day.
**Compute monthly:** rolling 50- and 100-trade expectancy with 95% CI; drawdown from peak in R and %; Brier score = mean((p − outcome)²) plus calibration buckets (do 70% calls win ~70%?); expectancy by sleep, stress and emotion-intensity bucket; MFE capture; expectancy by confidence tier (the gate for conviction sizing); playbook rebalance (more of the best setups, Steenbarger).
**Quarterly:** promote or retire setups against their pre-registered N; record the variants tried; run a full `perf` report.

## 14. Diagnosing a struggling trader

| Symptom | Likely cause | Intervention | Metric to track |
|---|---|---|---|
| High win rate, net loser; a few big losses | Disposition effect; stops moved or missing | Resting stop at entry; a stop can only tighten | Average loss (target ≈ −1.0R); % of losses worse than −1.2R |
| Winners cut far below plan | Loss aversion on gains; P&L salience | Resting targets; hide open P&L; pre-set partial-exit rule | Realized vs planned R on winners; MFE capture |
| Worse trades and bigger size after a red morning | Break-even seeking, tilt | Daily limit 2–3R; cool-off after 2 losses; no intraday size increases | Mean R and size of trades after a loss vs after a win |
| Size creeps up during a hot streak | House money, overconfidence | Size set only from equity and tier; tier caps | Risk_pct vs rule; R of trades after a 3-win streak |
| Many trades, flat or negative expectancy | Overtrading, sensation-seeking, no filter | Playbook-only; max trades per day; tag off-plan trades | Off-plan expectancy; costs ÷ gross; trades per day |
| Freezes, misses A-setups after a drawdown | Stress-driven risk aversion, fear | Cut size until pulling the trigger is easy; if-then entries as conditional orders | % of qualifying setups taken |
| Good process, still losing | Small sample, edge decay, regime change | Compute the CI before acting; check setups for decay; no rule changes before pre-set N | Rolling mean R with CI; t |
| Bad process, making money | Luck; reinforcement of rule-breaking | Grade process; size down until adherence recovers | Adherence % vs P&L; grade distribution |
| Big losses on options and events | Lottery preference, overpaying IV, spreads | Compare implied move with typical move; avoid wide-spread weeklies; size the premium as 1R | Spread paid as % of premium; R on event trades |
| Erratic day-to-day results | State effects (sleep, stress) | State check; size by state | Expectancy by sleep and stress bucket |
| Can't say what the edge is | No edge | Define setups with a counterparty; experiment at minimum size | % of trades with a setup_id; N per setup |
| Strategy-hopping | Resulting, recency | Commit to one setup for a pre-registered N | Variants tried; trades per setup |
| Adds to losing positions | Sunk cost, break-even seeking | Hard rule: no adds below the plan; adds only on confirmation | Count of adds to losers (target 0) |
| "My stop always gets hunted" | Stops just beyond obvious levels | Stop at invalidation, away from clusters; smaller size | % of stop-outs that reverse within a few bars |
| Knows the rules, breaks them under pressure | The knowing-doing gap (Livermore) | Automate: resting orders, platform loss lock, written if-thens | Rule-flag adherence per trade |

## 15. Coaching conversation

**Stance:** be curious, start from the data, and stay specific. Describe behavior ("the last 12 losers averaged −1.7R"), not character ("you lack discipline"). The trader's own rules are the yardstick.

Questions to ask, roughly in this order:
1. What are you trying to achieve, over what period, with what capital, and at what risk per trade?
2. Show me your last 50–100 trades in R. What is the N per setup?
3. What is your edge, and who is on the other side? Why are they willing to be there?
4. How many setups or variants have you tried, and how many did you drop?
5. Which of your rules did you break most often last month? What was happening each time?
6. What do your best weeks look like? (Steenbarger: find what works and do more of it.)
7. What do you do right after a loss? After a big win?
8. What is your stop-trading rule, and have you ever kept trading past it?
9. How are sleep, stress and life outside trading right now?

How to deliver hard truths without moralizing:
1. **Ask permission:** "Want the blunt read of the numbers?"
2. **Lead with their data, then the base rate.** For example: "92 trades, +0.04R, CI roughly −0.2 to +0.3. That can't be told apart from zero yet. For context, in the Brazil and Taiwan full-population studies about 1–3% of persistent day traders were durably profitable."
3. **Turn it into something controllable:** "Your on-plan trades average +0.3R. Your off-plan trades average −0.6R. The edge you have is getting buried."
4. **Prescribe one experiment** with a metric and a date: "Next 40 trades: playbook only, stop orders at entry, daily limit −2R. We judge it on adherence first and R second."
5. **Give probabilities, not verdicts.** Say "the evidence so far suggests", not "you're not a trader".
6. **Avoid** "discipline", "greed", "gambling", "just stop", shaming, and repeating the base-rate lecture once it has been said.

When to recommend sizing down or stopping: the pre-set drawdown or limit has been breached; the CI of mean R is below zero after the pre-registered N; adherence is below the gate; or the trader cannot write a plan for most of their trades. If the trader describes borrowing to trade, hiding losses, or real distress, step out of coaching mode. Suggest pausing trading and talking to a professional, such as a clinician or a gambling-support service.

## Where TA fits

Simple trend and momentum rules, 52-week-high proximity and round-number order clustering have the best support. Even these are modest, sensitive to costs, and decayed after publication. Most named patterns, candlesticks, Fibonacci levels and Elliott Wave have weak, null or no rigorous support. Patterns that carry *information* (Lo, Mamaysky & Wang 2000) do not by themselves make *money*. Use TA for timing, stop placement and reading positioning. For the evidence, see `technical-analysis.md`.

## Failure modes / traps

- **Judging on <50 trades,** or on win rate, or on $ P&L instead of R. Compute the CI before saying anything about edge.
- **Resulting:** praising a bad-process winner, or rewriting rules after one loss.
- **Unlogged variants:** "I tested a few versions" is data snooping. Get a count and deflate for it.
- **Conviction sizing without calibration data:** the most common route to a blow-up for traders who copy Druckenmiller.
- **Stops placed by pain tolerance or round numbers** instead of thesis invalidation. Then widened or moved after entry.
- **Averaging down** described as "scaling in".
- **Loss limits that exist only in the trader's head,** or limits reset intraday. Check whether they are enforced by the platform.
- **Lecture-style debiasing:** reminders don't work. Give the trader structure.
- **Treating psychology as the problem** when the journal shows no edge, or a risk-per-trade far above 1%.
- **Ignoring state:** sleep, illness, life stress and prior-day P&L not logged at all.
- **Options traders measuring wins by premium,** not by R and spread paid. Buying event volatility without comparing the implied and typical move.
- **Prop "funded trader" pass-rate claims** taken at face value. They come from vendor marketing, with no independent audit [Weak].

## Toolkit hooks

- `python scripts/tradekit.py expectancy --p 0.45 --win 1.8 --loss 1 --trades 60`: expectancy, breakeven win rate, trades needed for t=2 and t=3, and the current t (≈SQN). This uses a two-point SD; for a real journal, prefer `perf`.
- `python scripts/tradekit.py perf journal.csv --col R --percent --ppy <trades/yr>`: feed the R column with `--percent` (treats 1R as 1% of equity). Gives hit rate, payoff, profit factor, max DD, skew and kurtosis, lag-1 autocorrelation (a heuristic for streak dependence and tilt), PSR, and MinTRL. Add `--trials K --var-sr V` for DSR when variants were tried.
- `python scripts/tradekit.py ruin --p 0.45 --b 1.8 --risk 1 --trades 250 --limit 10`: how often a drawdown rule fires by chance. Use it to set the ladder in §10.
- `python scripts/tradekit.py drawdown --loss 10 20 50`: recovery math.
- `python scripts/tradekit.py size --equity 50000 --risk 0.5 --entry 100 --stop 96`: shares for 1R. For a Turtle-style N stop, use `--atr 2.1 --atr-mult 2`.
- `python scripts/tradekit.py kelly --p 0.45 --b 1.8`: full, half and quarter Kelly. Haircut p before using it.
- `python scripts/tradekit.py sharpe --sr 1.0 --n 504 --trials 10 --var-sr 0.25`: when a trader quotes a Sharpe, gives the SE, PSR, DSR and minimum track record. `--kurt` is raw kurtosis (normal = 3).

## Key sources

- Barber & Odean 2000, "Trading Is Hazardous to Your Wealth," *JF* 55(2); Odean 1998, *JF* 53(5); Odean 1999, *AER* 89(5)
- Barber, Lee, Liu & Odean 2014, *J. Financial Markets* 18 — https://ideas.repec.org/a/eee/finmar/v18y2014icp1-24.html
- Chague, De-Losso & Giovannetti, "Day Trading for a Living?" — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3423101
- Bryzgalova, Pavlova & Sikorskaya 2023, *JF* 78(6) — https://lbsresearch.london.edu/id/eprint/2827
- Barber, Huang, Odean & Schwarz 2022, *JF* 77(6) — https://ideas.repec.org/a/bla/jfinan/v77y2022i6p3141-3190.html
- de Silva, Smith & So 2025, "Losing is Optional," *Review of Finance* — https://www.gsb.stanford.edu/faculty-research/publications/losing-optional-retail-option-trading-expected-announcement
- SEBI F&O study, Sept 2024 — https://www.sebi.gov.in/media-and-notifications/press-releases/sep-2024/updated-sebi-study-reveals-93-of-individual-traders-incurred-losses-in-equity-fando-between-fy22-and-fy24-aggregate-losses-exceed-1-8-lakh-crores-over-three-years_86906.html ; FY26 (press) — https://www.moneylife.in/article/retail-fo-traders-lose-rs91685-crore-in-fy26-despite-sebi-curbs-average-loss-hits-rs117-lakh-govt/81318.html
- ESMA 2018 CFD/binary product intervention — https://www.esma.europa.eu/node/84933
- Coval & Shumway 2005, *JF* 60(1) — https://ideas.repec.org/a/bla/jfinan/v60y2005i1p1-34.html
- Fischbacher, Hoffmann & Schudy 2017, *RFS* 30(6) — https://econpapers.repec.org/RePEc:oup:rfinst:v:30:y:2017:i:6:p:2110-2129.
- Frydman & Rangel 2014, *JEBO* 107; Gollwitzer & Sheeran 2006, *AESP* 38; Mitchell, Russo & Pennington 1989, *JBDM* 2(1)
- Coates & Herbert 2008, *PNAS* 105(16) — https://pmc.ncbi.nlm.nih.gov/articles/PMC2329689
- Lo, Repin & Steenbarger 2005, *AER P&P* 95(2) — https://ideas.repec.org/p/nbr/nberwo/11243.html ; Lo & Repin 2002, *J. Cognitive Neuroscience* 14(3)
- Kahneman & Klein 2009, *American Psychologist* 64(6); Macnamara, Hambrick & Oswald 2014, *Psych. Science* 25(8)
- Schwager, *Market Wizards* series (1989–2020); Mallaby 2010, *More Money Than God*; Lefèvre 1923, *Reminiscences of a Stock Operator* [Lore]
- Mauboussin 2019, "Who Is on the Other Side?"; Tharp 2007, *Trade Your Way to Financial Freedom*; Faith 2007, *Way of the Turtle*
- Duke 2018, *Thinking in Bets*; Bellafiore 2010/2013, *One Good Trade* / *The PlayBook*; Steenbarger 2009, *The Daily Trading Coach*
- Harvey, Liu & Zhu 2016, *RFS* 29(1); Bailey & López de Prado 2014, *JPM* 40(5); Lo 2002, *FAJ* 58(4)
- Kelly 1956, *BSTJ* 35(4); Thorp 2006; Grossman & Zhou 1993, *Mathematical Finance* 3(3)
