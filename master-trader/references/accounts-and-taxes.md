# Accounts and taxes: account types, IRAs, minimums and 2026 US tax on trading

*Read when: explaining how a user's accounts differ (cash, margin, IRA, Roth, SEP, SIMPLE, 401(k), HSA, UTMA, 529,
Coverdell, Trump account), what an account at Schwab, Interactive Brokers, Coinbase or OANDA needs or allows, or
computing 2026 federal and state tax on gains, dividends, futures, forex and crypto, estimated payments, or a family's
savings goals. These are rules and parameters for an app to implement, not personal tax advice. Researched 2026-11-14
for a US-resident individual. [P] read on the primary page (IRS, statute, regulator, vendor); [S] secondary source or
search snippet; (U) unconfirmed. Where interpretation matters: [Strong] statute, regulation or ruling on point;
[Moderate] mainstream practice without direct authority; [Weak] thin; [Contested] practitioners split.*

**Contents:** 1 Account types · 2 IRAs and other retirement accounts · 3 Trading inside an IRA, by vendor · 4 Account
minimums by vendor and trade type · 5 2026 federal parameters · 6 How each instrument is taxed · 7 Trader tax status
and §475(f) · 8 State taxes · 9 Estimated taxes · 10 Children and family goals · 11 How to compute it · 12 Sources

## 1. Account types

| Account | Who can fund it | Tax on activity inside | Trading limits |
|---|---|---|---|
| Taxable cash | anyone | gains, dividends, interest taxed each year | T+1 settlement; no shorts; long options, covered calls, cash-secured puts |
| Taxable margin | anyone with $2,000 equity | same as cash | Reg T 50% initial, 25% maintenance; shorts; spreads; interest on debits |
| Traditional / rollover IRA | anyone with earned income (no age limit since 2020) | none until withdrawn | no borrowing; "limited margin" only (§3) |
| Roth IRA | earned income, MAGI under the limit | none; qualified withdrawals tax-free | as IRA |
| SEP / SIMPLE IRA | employer, incl. a self-employed owner | none until withdrawn | as IRA |
| 401(k) / 403(b) / 457 | payroll | none until withdrawn | plan fund menu, sometimes a brokerage window |
| HSA | anyone covered by an HSA-eligible health plan | none; medical withdrawals tax-free | custodian's menu |
| Futures (Schwab, IBKR, Coinbase Financial Markets) | anyone approved | §1256 60/40, marked to market | CFTC segregation; not SIPC |
| Retail forex (OANDA) | anyone | §988 ordinary by default | NFA 2%/5% deposits (50:1 / 20:1); not SIPC |
| Crypto spot (Coinbase) | anyone | property, capital gain/loss | no margin or shorts for US retail spot; not SIPC |

- **Cash account.** T+1 settlement (SEC Rule 15c6-1, since 28 May 2024). A *good-faith violation* is buying with
  unsettled proceeds and selling before that purchase is paid for with settled cash. *Freeriding* (paying for a purchase
  only with the proceeds of selling it) triggers a 90-day settled-cash freeze (Reg T §220.8(c)). Schwab freezes after one
  freeride or three GFVs in 12 months [P, `vendors.md` §2].
- **Margin account.** Reg T 50% initial; FINRA 4210 25% maintenance (houses use 30%+); $2,000 minimum. Shorts need a
  locate/borrow (Reg SHO) and a 150% deposit. Intraday margin replaced the pattern-day-trader rule on 4 Jun 2026; brokers
  may phase it in until 20 Oct 2027 (`vendors.md` §1) [P].
- **Shares on loan pay ordinary income.** Margin shares (or fully-paid-lending shares) lent out over a record date pay a
  "substitute payment in lieu of dividends": ordinary income on a 1099-MISC, not a qualified dividend [Strong].
- **Ownership.** Individual; joint (JTWROS: at death the survivor's basis steps up on the decedent's half, or on the whole
  in community-property states, §1014(b)(6)) [Strong]; trust; custodial (UTMA, §10); entity.
- **Protection.** SIPC covers securities and cash at a broker-dealer to $500k ($250k cash). It does not cover futures,
  forex, crypto or commodities [Strong].

## 2. IRAs and other retirement accounts

2026 limits (Notice 2025-67; IR-2025-111; Rev. Proc. 2025-19 for HSAs) [P]:

| Item | 2026 |
|---|---|
| IRA contribution (traditional + Roth combined) | $7,500; +$1,100 catch-up at 50+ (first indexed year) = $8,600; capped at earned income; due 15 Apr 2027 |
| Traditional IRA deduction phase-out (MAGI), if covered by a workplace plan | single/HoH $81,000-91,000; MFJ $129,000-149,000; MFJ with only the spouse covered $242,000-252,000; MFS $0-10,000; nobody covered: no limit |
| Roth contribution phase-out (MAGI) | single/HoH $153,000-168,000; MFJ $242,000-252,000; MFS $0-10,000 |
| 401(k)/403(b)/457/TSP deferral | $24,500; 50+ +$8,000; age 60-63 +$11,250; total additions (§415(c)) $72,000; pay counted to $360,000; catch-ups must be Roth if 2025 FICA wages > $150,000 |
| SIMPLE IRA | $17,000 ($18,100 in "applicable" small-employer plans); 50+ +$4,000 ($3,850); 60-63 +$5,250 |
| SEP-IRA | employer only: 25% of pay (≈20% of net self-employment earnings), max $72,000; pay counted to $360,000; eligibility pay $800 |
| HSA | $4,400 self-only / $8,750 family; 55+ +$1,000 |
| Saver's credit AGI ceiling | MFJ $80,500; HoH $60,375; others $40,250 |

- **Phase-out arithmetic** (Pub 590-A): allowed = limit × (end − MAGI) / (end − start), rounded up to $10, minimum $200
  if MAGI is below the end of the range [Strong].
- **Who.** Traditional: anyone with compensation, or a spouse's on a joint return (spousal IRA). Roth: compensation and
  MAGI below the range. SEP: the employer funds it for all eligible employees. SIMPLE: employers with ≤100 employees;
  deferrals plus a 3% match or 2% nonelective. Rollover IRA: a traditional IRA holding plan money, same rules; keep it
  separate if it may go back into a 401(k), which clears the pro-rata problem below.
- **Tax.** Traditional: deductible contribution (inside the phase-out), deferred growth, withdrawals taxed as ordinary
  income, pro rata with any nondeductible basis (Form 8606). Roth: after-tax in, tax-free growth and qualified
  withdrawals. Inside either: no capital-gains rates, no wash-sale benefit, no deductible losses. IRA withdrawals are not
  net investment income but raise MAGI, which can push other investment income into the NIIT [Strong].
- **10% additional tax** (§72(t)) on the taxable part before 59½. IRA exceptions: death, disability, substantially equal
  periodic payments, medical costs above 7.5% of AGI, health insurance while unemployed, higher education, first home
  ($10,000 lifetime), birth or adoption ($5,000), terminal illness, federally declared disaster ($22,000), emergency
  ($1,000 a year), domestic abuse ($10,500 in 2026), IRS levy, reservists. Plan-only: leaving the employer at 55+, QDRO.
  SIMPLE IRA withdrawals in the first two years of participation: 25% (§72(t)(6)) [P].
- **Roth ordering** (§408A(d)(4)): contributions come out first, always tax- and penalty-free; then conversions, oldest
  first and taxable part first; then earnings. **Five-year rules:** (1) earnings are tax-free only after 5 tax years from
  1 Jan of the year of the first Roth IRA contribution or conversion *and* at 59½, death, disability or a first home;
  (2) each conversion has its own 5-year clock for the 10% penalty if under 59½ [Strong].
- **RMDs.** Start at 73 (born 1951-59) or 75 (born 1960+); the first by 1 Apr of the next year. A missed RMD costs 25%,
  10% if fixed within two years. No lifetime RMDs from Roth IRAs or, since 2024, Roth 401(k)s. Most non-spouse heirs
  must empty an inherited IRA within 10 years, with annual RMDs if the owner had started them [P].
- **Conversions.** Traditional, SEP or SIMPLE (after two years) to Roth, with no income limit. The pre-tax amount is
  ordinary income that year: watch brackets, the NIIT, Medicare IRMAA (two-year lookback), the senior deduction phase-out.
  Recharacterizing a conversion has been banned since 2018.
- **Backdoor Roth.** Nondeductible traditional contribution, then convert. Pro-rata rule (§408(d)(2)): taxable share =
  pre-tax balance ÷ total of all traditional, rollover, SEP and SIMPLE IRAs on 31 Dec of the conversion year (plus that
  year's distributions). 401(k) balances don't count. The two steps are widely used and acknowledged in the 2017
  conference report; the IRS hasn't challenged them [Moderate].
- **Rollovers.** Trustee-to-trustee: unlimited. 60-day indirect IRA rollovers: one per 12 months across all IRAs. Plan
  distributions paid to you withhold 20%. Excess contributions: 6% a year until removed (§4973).
- **401(k) and HSA, briefly.** 401(k): plan menu, loans possible, no IRA-style trading. HSA: deductible in, tax-free out
  for medical; non-medical before 65 = income tax + 20%; after 65 just income tax. California and New Jersey tax HSAs (U).

## 3. Trading inside an IRA, by vendor

- **No borrowing** [Strong]. Pledging an IRA deems the pledged part distributed (§408(e)(4)), and lending between you and
  your IRA is a prohibited transaction. "IRA margin" is therefore *limited margin*: trade on unsettled proceeds (no GFVs),
  carry spreads and futures margin, but no debit balance and no short stock.
- **Prohibited transactions** (§4975) [Strong]: any dealing between the IRA and you or a disqualified person (spouse,
  ancestors, descendants and their spouses, fiduciaries): selling it property, borrowing from it, guaranteeing its debt,
  using its assets personally. The whole IRA is treated as distributed on 1 Jan of that year (§408(e)(2)).
- **Collectibles** (§408(m)): art, gems, most coins and metals bought by the IRA count as distributions; certain bullion
  held by the trustee is excepted. Metal ETFs such as GLD are allowed (IRS letter rulings) [Moderate].
- **UBTI** (§§511-514): an IRA with over $1,000 of unrelated business taxable income files Form 990-T and pays trust rates
  (37% above $16,000 in 2026). Sources: MLP units, true margin debt (debt-financed income), some K-1 partnerships.
  Dividends, interest, capital gains and gains on options and futures are excluded (§512(b)(5)) [Strong]. Commodity-pool
  ETPs (USO, UNG) earn mostly futures gains and interest, so usually no UBTI [Moderate]. Flag MLPs and K-1 ETPs in IRAs.
- **Losses don't count.** Trades inside an IRA create no gain or loss for the owner; only distributions are taxed.
  Miscellaneous itemized deductions are gone permanently (OBBBA made §67(g) permanent), so even closing every IRA below
  its nondeductible basis gives no deduction [Strong]. Foreign tax withheld in an IRA can't be credited; Canada exempts
  IRAs by treaty, with a form for Roths (U).
- **Crypto in an IRA.** Spot bitcoin/ether ETPs (IBIT, FBTC, ETHA...) are securities that any brokerage IRA can hold.
  Coins themselves need a self-directed IRA custodian (Alto, iTrustCapital, Kingdom Trust), several running on Coinbase
  custody or trading [S]. Crypto is not a designated collectible [Moderate].

| | Schwab | IBKR | Coinbase | OANDA |
|---|---|---|---|---|
| IRAs | traditional, Roth, rollover, SEP (all futures-eligible [S]); SIMPLE, inherited, custodial (U) | traditional, Roth, rollover, SEP, inherited (U) | none of its own | none |
| Margin | limited margin: unsettled proceeds, no borrowing; $25,000 equity for limited margin/spreads [P] | "IRA margin": no short stock, no debit in any currency [S] | — | — |
| Options | levels 0-2 only: 0 covered (covered calls, protective puts, collars); 1 long (+ cash-secured puts per Schwab's table; another Schwab page puts them at 0); 2 spreads, needs limited margin. No uncovered [S] | covered, cash-secured puts, long, spreads; no naked calls (U) | — | — |
| Short stock | no | no | — | — |
| Futures | yes in traditional, Roth, rollover, SEP: $25,000 net liquidation value, margin and spread approval, 125% of initial margin, no intraday futures margin [S] | yes; IRA futures margin may be ≥2× the non-IRA overnight rate [S] | — | — |
| Forex | not offered in IRAs (U) | conversions only, no borrowed currency [S] | — | — |
| Crypto | ETPs yes; Schwab Crypto spot BTC/ETH (phased rollout from 12 May 2026, linked account, 0.75%): IRA eligibility (U) | ETPs yes; spot crypto in IRAs (U) | taxable accounts only; partners offer crypto IRAs on its rails [S] | — |

## 4. Account minimums by vendor and trade type

| Vendor | Trade type | Minimum (2026) | Source |
|---|---|---|---|
| All | Margin (any broker-dealer) | $2,000 equity (FINRA 4210(b)) | [P] FINRA 4210 |
| All | Day trading, old rule | $25,000 equity to make 4+ day trades in 5 days; brokers not yet on intraday margin may keep it until 20 Oct 2027 | [P] FINRA RN 26-10 |
| All | Day trading, new rule | intraday margin from 4 Jun 2026: maintenance on intraday exposure, $2,000 margin minimum, no $25,000 | [P] FINRA RN 26-10 |
| Schwab | Open a brokerage account | $0 | [S] |
| Schwab | Margin and short stock | margin approval + $2,000; shorts also need a borrow (HTB fee) | [P] Schwab margin page |
| Schwab | Options level 0 (covered) / 1 (long, cash-secured puts) | no dollar minimum; cash account OK; approval by experience | [S] Schwab option levels |
| Schwab | Options level 2 (spreads) | margin account ($2,000); in an IRA, limited margin at $25,000 (one Schwab source: $5,000) | [P]/[S] |
| Schwab | Options level 3 (uncovered) | margin account; no published dollar minimum (U); not in IRAs | [S] |
| Schwab | Portfolio margin | $125,000 initial (Schwab PM page, thinkorswim manual), maintain $100,000 (PM request form lists $100,000); level 3 options and margin | [S] |
| Schwab | Futures | margin + options level 2 approval; US$1,500 per Schwab's international FAQ, US figure (U); IRA $25,000 | [S] |
| Schwab | Forex | margin approval first; not for Ohio or Arizona residents; minimum (U) | [S] |
| Schwab | Intraday margin | Intraday Margin Buying Power from 13 Jul 2026, needs $2,000 | [P] `vendors.md` §2 |
| Schwab | Order size via Trader API | whole shares only | [P] `vendors.md` §2 |
| Schwab | Tax-aware long-short (RIA strategies) | $1M Reg T / $3M portfolio margin (June 2026 report) | [S] |
| IBKR | Open an account (cash) | $0 | [S] |
| IBKR | Margin / short stock | $2,000 (or equivalent) for Reg T margin; shorts need a borrow | [S] IBKR margin page |
| IBKR | Options | permissions by experience; spreads and naked need a margin account; IRAs: covered, long, spreads | (U) |
| IBKR | Portfolio margin | $110,000 to open, $100,000 to keep (below it: margin-reducing trades only, or a surcharge); option approval | [S] IBKR KB |
| IBKR | Day trading | PDT ($25,000) still applied in its KB; intraday-margin go-live date not confirmed; PDT never applied to portfolio margin | [S]/(U) |
| IBKR | Order size | odd lots fine; fractional shares on eligible US stocks/ETFs | [S] |
| Coinbase | Spot order size | per-market notional minimum (e.g. $1 on DOGE-USD; others like 0.0001 BTC); no margin | [S] Coinbase docs |
| Coinbase | US futures / perpetual-style (Coinbase Financial Markets) | 1 contract: nano BTC 0.01 BTC (BIT monthly, BIP 5-year perp-style); nano ETH perp 0.10 ETH; no published account minimum (U); intraday up to 10x | [P] Coinbase contract specs |
| OANDA | Open an account | $0 (Standard); Elite Trader $10,000 and $10M monthly volume | [S] |
| OANDA | Trade size | 1 unit of base currency; 2% / 5% NFA deposit | [S]/[P] |

## 5. 2026 federal parameters

**Ordinary brackets: upper end of each bracket, taxable income** (Rev. Proc. 2025-32 §4.01) [P]

| Rate | Single | MFJ / surviving spouse | MFS | HoH |
|---|---|---|---|---|
| 10% | 12,400 | 24,800 | 12,400 | 17,700 |
| 12% | 50,400 | 100,800 | 50,400 | 67,450 |
| 22% | 105,700 | 211,400 | 105,700 | 105,700 |
| 24% | 201,775 | 403,550 | 201,775 | 201,750 |
| 32% | 256,225 | 512,450 | 256,225 | 256,200 |
| 35% | 640,600 | 768,700 | 384,350 | 640,600 |
| 37% | above | above | above | above |

Trusts (IRA UBTI): 10% to 3,300; 24% to 11,700; 35% to 16,000; 37% above.

**Long-term capital gains and qualified dividends: top of each band** (§1(h), §1(j)(5); Rev. Proc. 2025-32 §4.03) [P]

| Rate | Single | MFJ | MFS | HoH | Trusts |
|---|---|---|---|---|---|
| 0% | 49,450 | 98,900 | 49,450 | 66,200 | 3,300 |
| 15% | 545,500 | 613,700 | 306,850 | 579,600 | 16,250 |
| 20% | above | above | above | above | above |

Also: collectibles, including grantor-trust metal ETFs like GLD and SLV, max 28%; unrecaptured §1250 gain max 25%.

| Parameter | 2026 | Source |
|---|---|---|
| Standard deduction | single/MFS $16,100; MFJ $32,200; HoH $24,150; +$1,650 each 65+/blind ($2,050 unmarried) | [P] RP 2025-32 |
| Senior deduction (2025-28) | $6,000 per person 65+, any filer; reduced 6% of MAGI above $75,000 ($150,000 MFJ) | [S] OBBBA §70103 |
| NIIT (§1411) | 3.8% × min(net investment income, MAGI − threshold); thresholds $200,000 single/HoH, $250,000 MFJ, $125,000 MFS; not indexed | [Strong] |
| Capital loss limit | $3,000 a year against ordinary income ($1,500 MFS); rest carries forward indefinitely, keeping ST/LT character (§§1211(b), 1212(b)); dies with the taxpayer | [Strong] |
| AMT | exemption $90,100 single, $140,200 MFJ, $70,100 MFS; phases out 50¢/$ above $500,000 / $1,000,000; 28% above AMTI $244,500 | [P] |
| SALT deduction cap | $40,400, cut by 30% of MAGI above $505,000 to a $10,000 floor; back to $10,000 in 2030 | [S] |
| Kiddie tax | child's first $1,350 of unearned income untaxed, next $1,350 at the child's rate, above $2,700 at the parents' rate | [P] |
| Gift exclusion / estate exemption | $19,000 per recipient / $15,000,000 | [P] |
| Child tax credit | $2,200 per child under 17, up to $1,700 refundable; phases out $50 per $1,000 of MAGI above $200,000 ($400,000 MFJ) | [P]/[Strong] |
| Underpayment interest | 7% (Q4 2026; 6% in Q2); set quarterly at the federal short-term rate + 3 | [P] |

**One Big Beautiful Bill Act** (Pub. L. 119-21, 4 Jul 2025) as it applies to 2026:
- *Made permanent:* the 10-37% rate structure, the larger standard deduction, the AMT exemption (phase-out reset to
  $500k/$1M at 50%), the ban on miscellaneous itemized deductions (§67(g): investment fees and expenses not deductible
  for investors), the 20% §199A deduction (REIT dividends: 37% × 0.8 = 29.6% top), a $15M estate exemption [P].
- *New from 2026:* itemized deductions trimmed for 37%-bracket filers so each dollar saves at most 35¢ (§68), which also
  hits investment interest [S]; $1,000/$2,000 charitable deduction for non-itemizers and a 0.5%-of-AGI floor for
  itemizers; 529 K-12 limit $20,000; Trump accounts (§10); 1099-NEC/MISC threshold $2,000 [P]; 1099-K threshold back
  to $20,000 and 200 transactions (U).
- *2025-2028 only:* the senior deduction, tips and overtime deductions, car-loan interest; SALT cap $40,000 (2025) rising
  1% a year to 2029 [S].
- *Unchanged:* capital-gains rates, the NIIT (still not indexed), the $3,000 loss limit, wash sales (still not crypto),
  §1256, §475, §988.
- *Opportunity zones:* gains deferred into QOFs under the old rules are recognized on 31 Dec 2026 (§1400Z-2(b)); the new
  rolling regime starts 1 Jan 2027 [Moderate]. *QSBS* (§1202) for stock issued after 4 Jul 2025: 50/75/100% exclusion
  after 3/4/5 years, $15M cap [S].

## 6. How each instrument is taxed

**Holding period and netting.** The period starts the day after the trade date and is long-term if the sale is *more
than* one year later: bought 10 Mar 2026 → long-term from 11 Mar 2027. Trade date, not settlement, sets the tax year for
gains and losses (a 31 Dec trade counts in December) [Strong]. Net short-term against short-term and long-term against
long-term, then net the two. A net short-term gain is ordinary income; a net long-term gain gets 0/15/20%. Inherited
property is long-term at once with a stepped-up basis (§1014); gifts carry the donor's basis and holding period.

**Stocks and ETFs.** Basis = price + fees. Lot choice: specific identification, communicated to the broker by settlement
(standing orders count), else FIFO (Reg. §1.1012-1(c)); mutual funds may use average cost. Brokers report covered lots
on 1099-B, applying wash sales only within the same account and CUSIP. Grantor-trust ETPs (GLD: collectible 28%; IBIT:
treated as owning bitcoin) look through to the asset [Moderate]. Partnership ETPs (USO, UNG) issue K-1s and pass through
§1256 60/40 [Strong].

**Dividends.** Qualified (0/15/20%) if from a US or qualified foreign corporation (treaty country or US-listed) and held
more than 60 days in the 121-day window starting 60 days before the ex-date (preferred: 90 of 181) [Strong]. Ordinary:
REITs (less the 20% §199A deduction), money-market and bond funds, short-holding dividends, substitute payments, PFICs.

**Wash sales (§1091)** [Strong unless noted]:
- A loss is disallowed if you (or your spouse, or your IRA/Roth) acquire substantially identical stock or securities, or
  a contract or option to acquire them, within 30 days before or after the sale (a 61-day window).
- The disallowed loss is added to the replacement's basis (§1091(d)), and the replacement's holding period includes the
  sold lot's (§1223(3)). Partial matches disallow pro rata, by share count.
- **IRA or Roth buys within the window: the loss is gone for good**, with no basis added inside the IRA (Rev. Rul.
  2008-5).
- "Substantially identical" is undefined. Same stock or same fund in another share class: yes. Options on the same stock
  (bought calls; sold deep in-the-money puts) can trigger it. Two ETFs on different indexes: generally not. Two funds on
  the same index from different issuers: [Contested].
- Applies to short-sale closings (§1091(e)). Doesn't apply to gains, §1256 contracts or spot forex [Moderate], or to crypto
  (below). Dividend reinvestment triggers small wash sales. A December loss with a January rebuy is disallowed in December.

**Short sales (§1233).** Gain or loss is recognized when the short is closed, and its character comes from the shares
delivered, so usually short-term. If you held substantially identical shares for one year or less when shorting (or buy
them while the short is open): gain on closing is short-term, and those shares' holding period restarts at the close
(§1233(b)). If you held them over a year: a loss on the short is long-term (§1233(d)). Shorting against an appreciated
long is a constructive sale (§1259): gain is recognized at once. Payments in lieu of dividends: added to basis if the
short is open 45 days or less (§263(h)), else investment interest [Strong].

**Bought options.** Capital assets with their own holding period. Sold: gain or loss. Expired: treated as sold for $0 on
the expiry date (§1234(a)). Exercised: premium joins the stock's basis (call) or cuts the amount realized (put); the
stock's holding period starts the day after exercise. **Written options:** premium is taxed when closed or expired, as
short-term gain, whatever the holding time (§1234(b)); on assignment it adjusts the stock's sale price or basis.
Straddles (§1092) defer losses to the extent of unrecognized gain in the offsetting position; covered calls that are
in-the-money beyond the "qualified covered call" limits can suspend the stock's holding period [Strong].

**§1256 contracts** (regulated futures, options on futures, broad-based index options such as SPX, XSP, NDX, RUT and VIX;
not SPY/QQQ/IBIT options, which are equity options) [Strong]: marked to market at 31 Dec; every gain or loss is 60%
long-term and 40% short-term regardless of holding period; Form 6781. A net §1256 loss can be carried back three years
against §1256 gains (§1212(c)).

**Coinbase's US futures.** The nano and perpetual-style (5-year expiry, hourly funding) futures trade on Coinbase
Derivatives, a CFTC designated contract market, so they are regulated futures contracts under §1256(g)(1): 60/40 and
year-end marking [Moderate]. In late May 2026 the CFTC classified true perpetuals listed on a DCM as futures, starting
with Kalshi's BTCPERP, which "strongly supports" §1256 treatment (Cahill) [Moderate]. Funding payments are unsettled:
folded into the year-end mark, or ordinary income/expense like notional principal contract payments (and an individual
can't deduct net investment expense) [Contested]. Perpetuals reached via Coinbase Financial Markets on Deribit are
"foreign futures"; §1256 needs an IRS-recognized qualified board or exchange, and none is known for Deribit (U).
Coinbase's 1099-B format for futures is (U). Offshore perpetual swaps are not §1256.

**Spot forex (OANDA).** §988: gains and losses on retail rolling spot are ordinary income or loss by default, with no
$3,000 cap and no wash-sale rule; usually reported as other income on Schedule 1 [Moderate]. The §988(a)(1)(B) capital
election covers forwards, futures and options that are capital assets and not in a straddle, and must be identified in
your records on the day of the trade. Whether rolling spot counts as a forward is [Contested]. Treating OANDA spot as a
§1256 "foreign currency contract" (§1256(g)(2), interbank market) is not the common view [Weak]. OANDA issues no gain or
loss form, only annual statements and a 1099-INT for interest over $600 [S]. CME FX futures are §1256.

**Crypto (spot)** [Strong unless noted]:
- Property (Notice 2014-21): every sale, swap into another coin or stablecoin, or purchase paid in crypto is a disposal;
  over one year is long-term. Staking and rewards are ordinary income when you gain control (Rev. Rul. 2023-14).
- **Wash-sale rule: does not apply to crypto in 2026.** §1091 covers stock and securities only. H.R. 10357 (Digital
  Asset Tax Certainty Act) would extend it to traded digital assets sold after 14 Sep 2026; Ways and Means passed it
  38-5 on 16 Sep 2026; no floor vote as of mid-Nov [S]. Build the check and keep it off until enacted. Economic-substance
  risk for instant rebuys [Weak]. Straddle rules can reach offsetting crypto positions [Moderate].
- **Basis per wallet/account from 1 Jan 2025** (Reg. §1.1012-1(j)): no universal pool. Units at a broker: specific
  identification by instruction or standing order to the broker, else FIFO within that account. Notice 2025-7's relief
  (identify in your own records) ended 31 Dec 2025 [P]. Rev. Proc. 2024-28 governed the one-time allocation of old basis.
- **Form 1099-DA:** gross proceeds for 2025 sales; cost basis also for "covered" units acquired from 1 Jan 2026 in the same
  account (forms in early 2027). Coins transferred in or bought earlier are noncovered: the app must supply basis [S].

**Foreign stocks.** Foreign tax withheld on dividends (treaty rate usually 15%; reclaim any excess from that country) is
creditable on Form 1116, or without the form up to $300 ($600 MFJ) of passive 1099-reported tax. Hold more than 15 days
in the 31-day window around the ex-date (§901(k)) [Strong]. Foreign-currency cash at IBKR: conversion gains and losses
are §988 ordinary [Strong]. **PFIC risk:** foreign-domiciled funds and ETFs (UCITS, London- or Frankfurt-listed) are
PFICs: default excess-distribution tax at top rates plus interest, Form 8621 each year, or a mark-to-market election
(ordinary). Avoid them in taxable accounts; inside an IRA the 8621 is generally not required [Moderate].

**Margin interest** (§163(d)). Investment interest is deductible only if you itemize, up to net investment income
(interest, ordinary dividends, net short-term gain; qualified dividends and long-term gains only if you elect ordinary
rates on Form 4952, line 4g); the excess carries forward indefinitely. Interest on margin spent on personal items is
nondeductible (tracing, Reg. §1.163-8T) [Strong]. With the 2026 standard deduction and the §68 haircut it often saves
nothing. Traders with trader tax status deduct it on Schedule C.

**Interest on cash.** Sweep, money-market and broker credit interest are ordinary income (1099-INT/DIV) and NII.
Treasury interest is exempt from state tax, and Treasury money funds pass that through in part [Strong].

## 7. Trader tax status and §475(f)

- **Trader tax status** (case law, not statute): trading that is substantial, frequent, regular and continuous, aiming at
  short-term swings (Chen 2004, Holsinger 2008, Endicott 2013, Poppe 2015) [Moderate]. Practitioner rules of thumb: trades
  on ~75% of market days, hundreds of trades a year, average hold under a month [Lore]. Benefit: expenses (data,
  software, equipment, home office, margin interest) on Schedule C. No self-employment tax. Gains stay capital.
- **§475(f) mark-to-market** (traders only): every open position is marked at 31 Dec; gains and losses are ordinary (Form
  4797); no wash sales and no $3,000 cap, so large losses offset wages. Cost: long-term rates are gone on trading
  positions; investments must be identified and segregated the day they're bought. Election deadline: the original due
  date of the *prior* year's return (15 Apr 2026 for 2026), then Form 3115 with the election-year return; new taxpayers
  within 2 months and 15 days of starting. Securities and commodities elections are separate; electing for commodities
  gives up 60/40. Revocation follows similar timing, with a 5-year wait to re-elect (U) [Strong on deadline].
- **When it matters:** a year with large net trading losses; heavy wash sales across accounts; big trading expenses. Not
  for buy-and-hold or for winners who would get 60/40 or long-term rates.

## 8. State taxes

2026 top rates on ordinary income (most tax capital gains as ordinary income). Tax Foundation's Jan 2026 table,
updated for the 2026 cuts and the Georgia, Massachusetts and Washington pages [S unless noted]. Local taxes are extra
(NYC 3.876%, Maryland counties ~2.25-3.3%, some Ohio, Pennsylvania, Michigan and Kentucky cities, Portland area).

| State | Top % | Capital-gain notes | State | Top % | Capital-gain notes |
|---|---|---|---|---|---|
| AL | 5.0 | | MT | 5.65 | lower LTCG rates (3.0/4.1) (U) |
| AK | none | | NE | 4.55 | |
| AZ | 2.5 flat | 25% LTCG subtraction, assets bought after 2011 | NV | none | |
| AR | 3.7 | cut retro to 1 Jan 2026; 50% LTCG exclusion; gains over $10M exempt | NH | none | interest and dividends tax repealed 2025 |
| CA | 13.3 | 12.3 + 1% over $1M; gains ordinary | NJ | 10.75 | over $1M |
| CO | 4.4 flat | | NM | 5.9 | capital-gain deduction narrowed in 2025 (U) |
| CT | 6.99 | | NY | 10.9 | over $25M; + NYC |
| DE | 6.6 | | NC | 3.99 flat | |
| DC | 10.75 | over $1M | ND | 2.5 | 40% LTCG exclusion |
| FL | none | | OH | 2.75 flat | above $26,050 |
| GA | 4.99 flat | HB 463, retro to 1 Jan 2026 | OK | 4.5 | |
| HI | 11.0 | LTCG capped at 7.25% | OR | 9.9 | + local |
| ID | 5.3 flat | | PA | 3.07 flat | + local |
| IL | 4.95 flat | | RI | 5.99 | |
| IN | 2.95 flat | + county | SC | 5.21 | cut from 6.0 retro to 1 Jan 2026; 44% LTCG exclusion |
| IA | 3.8 flat | | SD | none | |
| KS | 5.58 | | TN | none | |
| KY | 3.5 flat | + local | TX | none | |
| LA | 3.0 flat | | UT | 4.45 flat | |
| ME | 7.15 | | VT | 8.75 | partial LTCG exclusion (U) |
| MD | 6.5 | + county; +2% on net capital gain if federal AGI > $350,000 | VA | 5.75 | |
| MA | 5.0 / 9.0 | +4% surtax over $1,107,750 [P]; short-term gains 8.5% (+4%) [P] | WA | none on wages | 7% on LTCG above the deduction ($278,000 for 2025; 2026 unpublished), 9.9% over $1M [P/S] |
| MI | 4.25 flat | + city | WV | 4.58 | |
| MN | 9.85 | +1% on net investment income over $1M | WI | 7.65 | 30% LTCG exclusion |
| MS | 4.0 flat | above $10,000 | WY | none | |
| MO | 4.7 | capital gains fully subtracted from 2025 | | | |

- **No income tax on wages:** AK, FL, NV, NH, SD, TN, TX, WA, WY. Washington's capital-gains excise tax exempts real
  estate and retirement accounts. Washington also enacted a 9.9% tax on income over $1M in Mar 2026, starting 2028 (U);
  the repeal initiative I-645 failed on 3 Nov 2026, and litigation is expected [S].
- States generally don't tax trades inside IRAs. They differ on IRA distributions, 529 deductions and HSAs (CA, NJ).
  State tax is federally deductible only if you itemize, under the SALT cap.

## 9. Estimated taxes

- **Federal safe harbors** (§6654) [Strong]: no penalty if withholding plus timely estimates cover the lesser of 90% of
  2026 tax or 100% of 2025 tax (110% if 2025 AGI > $150,000, $75,000 MFS), or if less than $1,000 is owed. Due dates for
  2026: 15 Apr, 15 Jun, 15 Sep 2026 and 15 Jan 2027 (25% each).
- **Lumpy gains:** the annualized-income method (Form 2210 Schedule AI) bases each installment on income to that date, so
  a Q4 gain needs only a Q4 payment. Withholding counts as paid evenly through the year, so extra W-4 withholding in
  December fixes earlier shortfalls.
- **Penalty** = interest on each late installment at the underpayment rate (7% in Q4 2026), not a flat fine. NIIT and
  self-employment tax count toward the required payments.
- **States** mostly mirror this. California wants 30%/40%/0%/30% installments, 110% of prior-year tax above $150,000 AGI,
  and no prior-year safe harbor at $1M+ AGI (U). Washington allows capital-gains prepayment from 2026 [P].

## 10. Children and family goals

| Vehicle | Contributions | Tax | Investing | FAFSA (dependent student) |
|---|---|---|---|---|
| 529 plan | after-tax; any donor; gift-tax annual exclusion | growth tax-free; qualified withdrawals tax-free | plan's portfolio menu; change at most twice a year | parent asset (≤5.64%) if parent- or student-owned; grandparent-owned not reported |
| Coverdell ESA | $2,000/yr per child, all donors combined; donor MAGI phase-out $95,000-110,000 single, $190,000-220,000 MFJ (not indexed); until 18 | like 529; must be used by 30 | self-directed brokerage possible (stocks, ETFs, funds) | parent asset |
| UTMA/UGMA | irrevocable gift; annual exclusion | child's income; kiddie tax | brokerage: stocks, ETFs, funds | student asset (20%) |
| Custodial Roth IRA | ≤ child's earned income, max $7,500 | Roth | IRA rules (§3) | retirement assets not reported |
| Trump account (§530A) | $5,000/yr from 4 Jul 2026; employer up to $2,500 inside it; government/charity and pilot money outside the cap | deferred; traditional-IRA rules from 18 | US equity index funds only | unsettled [Contested] |

- **529** (§529; Pub 970) [P/S]. 2026 gift exclusion $19,000 per donor per child; the 5-year election (§529(c)(2)(B), Form
  709) front-loads $95,000 ($190,000 per couple), with a pro-rata clawback into the estate if the donor dies within five
  years. Qualified: college tuition, fees, books, equipment, computers, room and board if at least half-time;
  apprenticeships; $10,000 lifetime of student loans; K-12 up to $10,000 a year through 2025 and **$20,000 from 2026**,
  now covering curriculum, books, online materials, tutoring, test fees, dual enrollment and therapies for disabled
  students (distributions after 4 Jul 2025); recognized postsecondary credential programs (OBBBA). Non-qualified: earnings
  taxed as ordinary income + 10% (waived for scholarships, death, disability, service academies). No double-dipping with
  the American Opportunity or Lifetime Learning credit. **States:** about 35 plus DC give a deduction or credit, mostly
  for the home-state plan only, and some recapture it on rollovers out; several don't conform to the OBBBA K-12 and
  credential expansions, making those withdrawals state-taxable [S]. **Trading:** investment changes at most twice per
  calendar year plus on a beneficiary change (§529(b)(4)); no single stocks, options or margin. The app can model a 529
  but not trade it.
- **529 → Roth IRA** (SECURE 2.0 §126, from 2024): into the *beneficiary's* Roth; the 529 must be open 15+ years;
  contributions from the last 5 years and their earnings excluded; each year ≤ the Roth limit ($7,500 in 2026) less other
  IRA contributions, and ≤ the beneficiary's earned income; no Roth income limit; $35,000 lifetime per beneficiary.
  Whether a beneficiary change restarts the 15-year clock: no IRS guidance (U).
- **UTMA/UGMA.** The money is the child's: custodians must invest prudently for the child, and the child takes control
  at the state's age, 18-21, some up to 25 (U by state). Unearned income in 2026: the first $1,350 untaxed, the next
  $1,350 at the child's rates, above $2,700 at the parents' top rate (Form 8615), for children under 19, or under 24 if
  full-time students. Parents can report it on their own return if the child's gross income is $1,350-13,500 (Form 8814)
  [P]. Harvest gains up to the 0% band. Moving it into a custodial 529 needs a sale first (realizes gains) and makes it a
  parent asset.
- **Custodial Roth IRA.** Needs the child's own earned income (W-2, or documented self-employment such as babysitting;
  reasonable wages from a parent's business). A parent may gift the cash. Contributions come back tax- and penalty-free.
- **Trump accounts** (§530A, §6434; Notice 2025-68; proposed regs May 2026) [P/S]. Who: US citizens under 18 with an SSN;
  open via Form 4547 or trumpaccounts.gov. **$1,000 pilot deposit** from Treasury for citizens born 2025-2028 (needs the
  election). Contributions from 4 Jul 2026: $5,000 a year (2026-27, then indexed) from parents, relatives and others, no
  deduction; employer contributions up to $2,500 per employee (§128, excluded from the employee's pay) count toward the
  $5,000; pilot, government, 501(c)(3) and rollover money doesn't. Investments: mutual funds or ETFs tracking a
  broad US equity index (S&P 500-type), no sector indexes, no leverage, total fees ≤ 0.10%; cash only in transit. No
  withdrawals before the year the child turns 18; from then on traditional-IRA rules apply (10% penalty before 59½ with
  the usual exceptions, Roth conversions allowed, no IRA aggregation). Basis: family contributions are after-tax basis;
  pilot, employer and government money and all earnings are taxed when withdrawn. Gifts qualify for the annual exclusion
  (Rev. Proc. 2026-25 relief for gift-tax reporting) [S]. FAFSA: Education hasn't ruled; aid experts expect 20%
  student-asset treatment, others argue IRA-like exclusion [Contested].
- **Child tax credit 2026:** $2,200 per child under 17 with an SSN, up to $1,700 refundable, $500 for other dependents;
  phases out above $200,000 / $400,000 MFJ; OBBBA requires an SSN for at least one parent [P/S].

**Inputs a goals planner needs:** filing status and state; parents' ages and incomes; each child's birth date (sets the
pilot, kiddie-tax and Trump-account eligibility and the college start year); each goal (type, amount in today's dollars,
date or child's age, years of spending: 4 for college); balances by account and owner; monthly saving capacity and
employer contributions; expected nominal return and volatility per account (glide path for age-based 529s); CPI and
education-inflation assumptions; expected aid and scholarships; the state 529 deduction and plan.

**Projection math** (monthly compounding, deposits at month end; i = (1 + r)^(1/12) − 1; m = months):
```
FV_lump    = PV * (1 + i)**m
FV_deposit = PMT * ((1 + i)**m - 1) / i              # x (1 + i) if deposits at month start
target_nom = target_today * (1 + g)**years           # g = goal inflation (CPI, or education inflation)
PMT_needed = (target_nom - PV * (1 + i)**m) * i / ((1 + i)**m - 1)    # floor at 0
college    = sum(cost_today * (1 + g)**(t_k - now) for t_k in attendance_years)   # nominal need per year;
             # to fund by enrollment, discount years 2-4 back to enrollment at the post-enrollment return
real_r     = (1 + r) / (1 + cpi) - 1                 # or work in real terms with real_r and today's dollars
```
After-tax returns: 529, Roth and Trump accounts compound untaxed when used as intended; UTMA/taxable compound at r less
dividend tax drag; a non-qualified 529 withdrawal loses (ordinary rate + 10%) on earnings. Show a range (e.g. 10th/50th/
90th percentile from return volatility), not one number.

**Education cost inputs** (College Board, Trends in College Pricing 2026) [P]: 2026-27 average published tuition and
fees: public four-year in-state $12,290 (+2.9%), out-of-state $32,730 (+3.5%), private nonprofit four-year $46,350
(+3.7%), public two-year $4,210 (+2.4%). Add housing and food (≈$13,000-16,000 in 2025-26, figures differ by source)
(U). Inflation-adjusted published tuition at public colleges is below its level of a decade ago [S]; the 2026-27
increases were 2.4-3.7% nominal. Default education inflation: 3-4% a year (CPI + ~1), a convention, not a forecast
[Weak]; show a 2-6% sensitivity.

## 11. How to compute it

**Federal tax on a year** (Qualified Dividends and Capital Gain Tax Worksheet logic):
```
ST, LT  = net short-term, net long-term gains (after loss carryforwards; §1256: 40% ST / 60% LT;
          §988 forex goes to ordinary, not here; collectibles/§1250 LT are taxed at min(ordinary rate, 28%/25%)
          and stacked below the 0/15/20 gains; omitted here)
net_cg  = ST + LT
cap_ded = max(net_cg, -3000 if status != "MFS" else -1500)       # loss limited; rest carries forward
pref    = max(0, min(LT, net_cg)) + qualified_dividends           # net LT gain over net ST loss + QD
AGI     = wages + other_ordinary + interest + nonqualified_dividends + qualified_dividends + cap_ded + forex_988
TI      = max(0, AGI - deduction)    # deduction = max(standard (+65+/blind), itemized after §68), + senior deduction
pref    = min(pref, TI); ord = TI - pref
tax     = brackets(ord, status)
        + 0.15 * overlap([ord, ord+pref], [T0, T15)) + 0.20 * overlap([ord, ord+pref], [T15, inf))
tax     = min(tax, brackets(TI, status))                           # worksheet takes the lower
niit    = 0.038 * max(0, min(NII, MAGI - NIIT_threshold[status]))  # NII: interest, dividends, net gains, §1256, crypto, forex
total   = tax + niit + amt_if_any - credits + state_tax(...)
```
- **Incremental tax on trading** = total(base + trading) − total(base), where base = the user's other income. This
  captures bracket creep, LTCG stacking (gains sit on top of ordinary income, so the 0% band fills from below),
  the NIIT, and phase-outs that gains push through: senior deduction (6%), IRA deductibility and Roth eligibility (MAGI),
  child tax credit, SALT cap above $505,000, ACA premium credits, IRMAA two years later. Report the marginal rate on the
  next $1,000 of ST and LT gain separately.
- **State:** apply the state's rate schedule to its taxable income with the §8 adjustments (exclusions, MA short-term
  rate, MD/MN surtaxes, WA's separate tax on LTCG, MO's exemption). If itemizing, the state tax feeds back into federal
  itemized deductions under the SALT cap.
- **Tax if sold today:** per lot, gain = (price − wash-adjusted basis) × qty; long-term if today > LT date (below). Add
  to year-to-date realized results, run the incremental formula, and show the tax and the after-tax proceeds by account.
  Losses: harvest value = loss × marginal rate, capped by the $3,000 rule once net gains are gone; carryforward
  otherwise. IRA/Roth lots: no tax on sale, $0 harvest value.
- **Days to long-term:** `lt_date = same month/day next year + 1 day` (29 Feb → treat 1 Mar as the anniversary, so 2 Mar
  is long-term [Moderate]); `days_left = lt_date − today`. Tack holding periods for wash-sale replacements, gifts; inherited
  = long-term now; §1233(b) restarts and §1092 straddles suspend the clock; exercised options start fresh.
- **Wash sales across accounts:** gather every trade in all of the household's accounts (both spouses' taxable, IRA, Roth,
  401(k) brokerage windows). For each loss sale in a taxable account, find buys of the same symbol (CUSIP, plus a
  user-maintained map of substantially identical tickers, plus bought calls) from sale − 30 to sale + 30 days, excluding
  the lot sold and shares already used as replacements; match FIFO by share count; disallowed = loss × matched/sold.
  Replacement in a taxable account: add to its basis and tack the holding period (it may itself wash later: chain).
  Replacement in an IRA/Roth: loss permanently lost. Skip §1256, spot forex, crypto (flag H.R. 10357, which would reach
  sales after 14 Sep 2026) and §475 traders. Reconcile against 1099-B code W, which covers only within-account matches.
- **After-tax value of $1 of pre-tax earnings saved for n years at return r** (t_now = marginal rate today, t_ret = rate on
  withdrawal, both federal + state):
  ```
  traditional = (1 + r)**n * (1 - t_ret)                       # deductible contribution
  roth        = (1 - t_now) * (1 + r)**n                         # Roth wins iff t_now < t_ret
  nondeduct   = (1 - t_now) * (1 + ((1 + r)**n - 1) * (1 - t_ret))   # basis back tax-free, earnings ordinary
  taxable     = after-tax FV of (1 - t_now) with yield y taxed yearly at t_div, growth g = r - y deferred:
                FV = (1 - t_now) * (1 + g + y*(1 - t_div))**n; basis grows with reinvested after-tax dividends;
                value = FV - t_ltcg_total * (FV - basis)   # 0 at death (step-up); active trading: r*(1 - t_ord) each year
  hsa (medical) = (1 + r)**n
  ```
  Subtract 10% for early withdrawals (traditional; Roth earnings only). A maxed Roth shelters more because its limit is
  in after-tax dollars. Use the app's own marginal-rate function for t_now and t_ret, not the bracket rate.
- **Estimated tax:** required_annual = min(0.90 × projected 2026 tax, 1.00 or 1.10 × 2025 tax); installment due =
  required_annual × {25, 50, 75, 100}% − withholding and payments to date. With Schedule AI, base each installment on
  annualized year-to-date gains; recompute after each realized trade.

## 12. Sources

- Rev. Proc. 2025-32 (2026 brackets, LTCG, standard deduction, AMT, kiddie, gifts, CTC): https://www.irs.gov/pub/irs-drop/rp-25-32.pdf
- Notice 2025-67 (2026 retirement limits): https://www.irs.gov/pub/irs-drop/n-25-67.pdf
- IR-2025-111 (IRA and Roth phase-outs): https://www.irs.gov/newsroom/401k-limit-increases-to-24500-for-2026-ira-limit-increases-to-7500
- Rev. Proc. 2025-19 (HSA 2026): https://www.irs.gov/pub/irs-drop/rp-25-19.pdf
- Pub 550 (investment income), Pub 590-A, Pub 590-B, Pub 544, Pub 970: https://www.irs.gov/publications/p550,
  https://www.irs.gov/publications/p590a, https://www.irs.gov/publications/p590b, https://www.irs.gov/publications/p544,
  https://www.irs.gov/publications/p970
- Rev. Rul. 2008-5 (IRA wash sales): https://www.irs.gov/pub/irs-drop/rr-08-05.pdf
- Notice 2025-7 (crypto lot identification relief): https://www.irs.gov/pub/irs-drop/n-25-07.pdf
- Notice 2025-68 (Trump accounts): https://www.irs.gov/pub/irs-drop/n-25-68.pdf ; BDO summary:
  https://www.bdo.com/insights/tax/irs-issues-initial-guidance-on-obbbas-trump-accounts-for-us-children
- IRC (§§1, 72, 408, 408A, 529, 530, 530A, 1091, 1211-1212, 1233-1234, 1256, 1259, 1411, 475, 988, 4975, 6654):
  https://www.law.cornell.edu/uscode/text/26
- IRS Q4 2026 interest rates: https://www.irs.gov/newsroom/interest-rates-remain-the-same-for-the-fourth-quarter-of-2026
- OBBBA summaries: https://www.kitces.com/blog/obbba-one-big-beautiful-bill-act-tax-planning-salt-cap-senior-deduction-qbi-deduction-tax-cut-and-jobs-act-tcja-amt-trump-accounts/ ;
  529 changes: https://www.jpmorgan.com/insights/wealth-planning/education-planning/new-529-plan-rules-2026
- Crypto perpetuals and §1256 (Cahill, 2 Jun 2026): https://static.cahill.com/docs/CahillNXT%20Alert%20-%20True%20Perpetuals%20Come%20Onshore%206.2.26.pdf
- Digital Asset Tax Certainty Act: https://www.forvismazars.us/forsights/2026/09/ways-means-approves-digital-asset-tax-certainty-act ;
  https://taxnews.ey.com/news/2026-1972-ways-and-means-approves-digital-assets-tax-bill
- Schwab: futures FAQ https://www.schwab.com/futures/faqs ; IRA limited margin agreement
  https://www.schwab.com/resource/supplemental-application-and-agreement-for-margin-and-option-spreads-in-ira ; option
  levels https://help.streetsmart.schwab.com/pro/4.36/Content/Option_Approval_Levels.htm ; portfolio margin
  https://www.schwab.com/margin/portfolio-margin ; Schwab Crypto https://www.theblock.co/news/business/2026-05-13-charles-schwab-spot-btc-eth-401069
- IBKR: IRA margin https://ibkb.interactivebrokers.com/node/2187 ; trading permissions https://ibkb.interactivebrokers.com/node/188 ;
  risk-based margin https://ibkb.interactivebrokers.com/article/3560
- Coinbase perp-style contract specs: https://help.coinbase.com/derivatives/perpetual-style-futures/contract-specifications ;
  order size limits: https://www.coinbase.com/blog/upcoming-changes-to-order-size-limits
- OANDA tax forms: https://help.oanda.com/us/en/faqs/tax-filing-and-forms.htm
- FINRA 4210 and RN 26-10: https://www.finra.org/rules-guidance/rulebooks/finra-rules/4210 ; https://www.finra.org/rules-guidance/notices/26-10
- State rates: https://taxfoundation.org/data/all/state/state-income-tax-rates-2026/ ; 2026 cuts:
  https://taxfoundation.org/blog/arkansas-income-tax-cut-rates/ ; Georgia HB 463:
  https://www.paylocity.com/resources/tax-compliance/alerts/georgia-reduces-individual-income-tax-rates-for-2026/ ;
  Massachusetts DOR https://www.mass.gov/info-details/tax-rates ; Washington DOR
  https://dor.wa.gov/taxes-rates/other-taxes/capital-gains-tax ; I-645 result
  https://www.axios.com/local/seattle/2026/11/06/washington-i-645-election-results-millionaires-tax-repeal-2026
- College Board Trends in College Pricing 2026: https://research.collegeboard.org/trends/college-pricing/highlights
- Trump accounts and FAFSA: https://edsource.org/2026/trump-accounts-financial-aid-uncertainty/769041
