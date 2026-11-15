# Vendor accounts: margin, costs and money rules (US retail, Nov 2026)

*Read when: setting up or explaining a paper account in `paperkit.py` (its `VENDORS` table), comparing what an account
at Schwab, Interactive Brokers, Coinbase or OANDA would cost or allow, or checking a margin call. Researched
2026-11-14. [P] read on the primary page; [S] search snippet only (the vendor blocked automated reads); (U)
unconfirmed. Rates move: the base rates and fee holidays below are dated.*

**Contents:** 1 Rules every US account shares · 2 Schwab · 3 Interactive Brokers · 4 Coinbase · 5 OANDA ·
6 Not modelled · 7 Sources

## 1. Rules every US account shares

- **Reg T** (12 CFR 220): 50% initial on stock purchases. Shorts deposit 150% of value (the proceeds plus 50%). [P]
- **FINRA 4210**: 25% long maintenance. Shorts under $5: the greater of $2.50/share or 100%. Shorts at $5 and up:
  the greater of $5/share or 30%. $2,000 minimum equity for margin. [P]
- **Intraday margin** (FINRA 4210(d)(2), effective 4 Jun 2026): replaced the pattern-day-trader rule and its $25k
  minimum. Maintenance applies to intraday exposure, and a position flat by the close gets no Reg T initial call.
  Brokers may phase it in until 20 Oct 2027. [P]
- **Bought options**: paid in full when 9 months or less to expiry (75% beyond that). [P]
- **Fees on sales**: SEC Section 31 is $20.60 per $1M from 4 Apr 2026. FINRA TAF is $0.000195/share (max $9.79) and
  $0.00329/contract, **paused for trades from 1 Oct to 31 Dec 2026**. Options regulatory fees run about
  $0.012-0.022 per contract. [P]
- **SEC Rule 201**: after a 10% fall from the prior close, short sales are restricted that day and the next.
- **Retail forex** (NFA Financial Requirements §12): 2% security deposit for USD against GBP, CHF, CAD, JPY, EUR,
  AUD, NZD, SEK, NOK and DKK; 5% for other pairs. NFA 2-43(b) requires FIFO and forbids hedging. [P]
- **Leveraged or short crypto** for US retail must trade on a CFTC-registered exchange (CEA 2(c)(2)(D)). Spot crypto
  has no loan value. [P]

## 2. Schwab (`schwab`: margin, cash, ira)

| Item | Value |
|---|---|
| Trades via the Trader API | US-listed stocks/ETFs and options only, whole shares; no futures, forex or crypto [P] |
| Maintenance | 25% long ($3+), 100% under $3; shorts per FINRA (30% above $16.66, $5/share $5-16.66, 100% $2.50-4.99, $2.50/share below); leveraged ETFs 2x 50%, 3x 75% [P] |
| Intraday | Intraday Margin Buying Power from 13 Jul 2026: 25% on positions opened and closed the same day, day ends 8 pm ET, needs $2,000 [P] |
| Commissions | $0 online stocks/ETFs; $0.65 a contract; OTC $6.95 a trade [P] |
| Margin interest | Base 10.25% from 18 Sep 2026: under $25k 12.075%, $25-50k 11.575%, $50-100k 10.625%, $100-250k 10.325% + 0.25 (10.575%), $250-500k 10.325%; $500k+ unpublished; nothing under $100; 360-day year, daily [P] |
| Cash sweep | ~0.05% (U) |
| Borrow | None on easy-to-borrow (U); hard-to-borrow at the quoted rate / 360 [P] |
| Cash account | T+1. One freeride, or three good-faith violations in 12 months, means 90 days of settled cash only [P] |
| IRA | Limited margin: may spend unsettled proceeds; no shorts, borrowing or naked calls; options levels 0-2; $25,000 minimum (one source says $5,000) [P]/[S] |

## 3. Interactive Brokers (`ibkr`: margin, IBKR Pro)

| Item | Value |
|---|---|
| Margin | Reg T 50% / 25% long, 30% short (US); foreign shares held to Reg T, house rates unpublished (30% used) [S] |
| US commission (Fixed) | $0.005/share, $1 minimum, 1% of value maximum [S] |
| Foreign commission | London, Xetra, Paris, Amsterdam, Milan, Madrid 0.05% (min GBP/EUR 3); Tokyo 0.08% (min JPY 80); Hong Kong 0.08% (min HKD 18); about 0.03% more to convert dollars automatically [S] |
| Transaction taxes | UK SDRT 0.5% on buys; France FTT 0.4% (large caps); Italy FTT 0.2% (from 2026); Spain FTT 0.2%; Hong Kong stamp duty 0.1% plus levies (0.106%) each side; Japan, Germany, Netherlands none [P]/[S] |
| Margin interest | Benchmark 3.88% (10 Nov 2026) + 1.5% under $100k, + 1% to $1M, + 0.75% above; blended across tiers; 360-day year [S] |
| Credit interest | Benchmark − 0.5% on cash above $10k, scaled by NAV / $100k under $100k NAV [S] |
| Borrow | ~0.25%/yr on easy-to-borrow shorts (IBKR's own example) [S] |
| Shorting abroad | Needs a borrow; Hong Kong only for HKEX-designated names (U) |

## 4. Coinbase (`coinbase`: spot, perps)

| Item | Value |
|---|---|
| Spot (Advanced, US) | 0.50% maker / 0.90% taker below $10k of monthly volume (from 16 Sep 2026); no margin or shorts [S] |
| US perps and futures | Coinbase Financial Markets (FCM) on Coinbase Derivatives: perps and dated futures on BTC, ETH, SOL, XRP, BNB, ADA, DOGE, AVAX, LINK, LTC, BCH, DOT, XLM, HBAR; none on TRX [P] |
| Perp margin | Up to 10x intraday (10%); overnight higher (Coinbase's example: 20%); liquidation below the threshold, which the 4 pm step-up alone can trigger [S] |
| Perp fees | ~0.02-0.05% of notional, $0.15 minimum a contract [S] |
| Funding | Hourly, clamped (±0.10%/h), longs pay when positive; no published average (10%/yr assumed) [P]/(U) |

## 5. OANDA (`oanda`: fx)

| Item | Value |
|---|---|
| Margin | NFA 2% majors (OANDA: 3% on AUD/USD), 5% others [P] |
| Spreads (standard) | EUR/USD 1.4, USD/JPY 1.4, GBP/USD 2.0, AUD/USD 1.4, USD/CAD 2.2, USD/CHF 1.8, NZD/USD 1.7 pips; USD/MXN not published [P] |
| Financing | At 5 pm ET: tom-next differential ± a 1% admin fee, 365-day year, Wednesday ×3 [P] |
| Closeout | Everything closes when equity is down to half the margin used [P] |

## 6. Not modelled in paperkit

- The interest-rate differential in FX financing; only OANDA's fee is charged.
- Hard-to-borrow fees and locates.
- ADR custody fees.
- Wash sales and taxes on gains.
- Coinbase's 10% intraday perp margin: swing trades hold overnight.
- Concentration add-ons and house increases without notice.
- Schwab's 8 pm intraday cutoff: paperkit's day trades flatten at 15:55.

## 7. Sources

- FINRA Rule 4210: https://www.finra.org/rules-guidance/rulebooks/finra-rules/4210
- FINRA RN 26-10: https://www.finra.org/rules-guidance/notices/26-10
- Reg T: https://www.law.cornell.edu/cfr/text/12/220.12
- SEC fee advisory: https://www.sec.gov/rules-regulations/fee-rate-advisories/2026-2
- TAF holiday: https://www.finra.org/sites/default/files/2026-09/SR-FINRA-2026-021.pdf
- NFA retail forex: https://www.nfa.futures.org/rulebook/rules.aspx?RuleID=SECTION%2012&Section=7
- Schwab margin rates and requirements: https://www.schwab.com/margin/margin-rates-and-requirements
- Schwab intraday margin: https://www.schwab.com/learn/story/schwab-changes-rules-around-day-trading
- Schwab cash accounts: https://www.schwab.com/learn/story/avoid-these-violations-when-trading-cash
- Schwab IRA options: https://www.schwab.com/learn/story/trading-options-ira
- IBKR rates via Lynx: https://lynxbroker.com/info/ibkr-margin-rates
- Italian FTT: https://www.clearstream.com/clearstream-en/res-library/tax-announcements/c26002-4891282
- Coinbase Derivatives fee schedule: https://www.cftc.gov/filings/orgrules/rules08032613651.pdf
- Coinbase funding rule: https://www.cftc.gov/filings/ptc/ptc11052646192.pdf
- Coinbase market hours: https://docs.cdp.coinbase.com/derivatives/introduction/market-hours
- OANDA pricing: https://www.oanda.com/us-en/trading/our-pricing
- OANDA financing: https://www.oanda.com/us-en/trading/financing-fees
