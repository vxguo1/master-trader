# Order Flow Strategy: Data, Signals, Setups, Crypto Flow, Market Making and Testing

*Read when: a user trades or builds tools from footprint, delta/CVD, DOM, tape, heat maps or L1/L2/L3 data (futures, equities, FX, crypto; seconds to days); asks whether order flow "predicts"; wants rules for absorption, imbalances, delta divergence, failed auctions, sweeps or icebergs; compares spot vs perp CVD, OI, funding or liquidation maps; asks about OFI, queue imbalance, microprice, VPIN, deep-LOB models, FX customer flow, options flow or "unusual options"/dark-pool alert services; is thinking about market making; or needs an order-flow backtest, fill model, cost or sample-size check reviewed.*

**Tags.** Grade: **[Strong]** replicated / out-of-sample · **[Moderate]** peer-reviewed with limited replication · **[Weak]** thin, in-sample or vendor · **[Contested]** credible sources disagree · **[Lore]** practitioner convention with no rigorous test. Class: **PR** peer-reviewed · **WP** working paper/preprint · **DOC** exchange or API documentation · **VEN** vendor/platform docs or marketing · **PL** practitioner lore. Verification: **V** fetched from the cited URL in the Nov 2026 research pass · **K** from the literature with a full citation, not fetched · **SC** spot-check this number before quoting it. "Inference" = reasoning from cited evidence, not a finding.

**Depth elsewhere (point there, do not repeat):** `price-action.md` §7 has the CKS OFI formula, the DOM/T&S/footprint tool table, data quality by market (CME tag 5797, equity signing accuracy 76–81%, off-exchange 50.6% of US volume in 2025, crypto wash trading) and spoofing law; §6 has value area/POC/LVN/80% rule; §9 has the setup template. `market-forces-flows.md` §3 has Kyle λ, the square-root law, the VPIN brief and BJZZ retail flow; §4 gamma regimes; §12 crypto perps, funding and the Oct 2025 cascade. Sizing: `risk-sizing-execution.md`. Deflated Sharpe and multiple testing: `quant-research-validation.md`.

**Contents:** 1 Core principles · 2 What order flow can and cannot do · 3 Data foundations · 4 Signals with evidence · 5 Footprint definitions · 6 Setup playbook · 7 Crypto order flow · 8 Market making and liquidity provision · 9 Testing order-flow strategies · 10 Review checklist and failure modes · 11 Toolkit hooks · 12 Key sources

---

## 1. Core principles

- **Order flow explains far better than it predicts.** Net flow relative to depth explains most same-interval price change [Strong · PR]; forecasting power decays within ticks to minutes. *Why:* a footprint chart shows the explanation after the fact, which feels like prediction.
- **Delta is only the aggressive half of order flow.** Footprint delta and CVD are trade imbalance; they omit limit adds and cancels, which is why CKS found trade imbalance explains price worse than OFI [Strong · PR]. *Why:* many "hidden seller" divergence stories are passive book activity (§2).
- **Location first, flow second.** Use order flow as a trigger at levels marked before the session, never as a free-standing forecast. *Why:* no footprint setup has outcome evidence; the level part (stop and take-profit clustering, Osler) does have mechanism support.
- **Latency and cost set your horizon.** Latency races are decided in microseconds; retail sees data tens of ms late and pays about 1.3 ES ticks per round trip. *Why:* a signal whose expected move is under 1–2 ticks is negative EV for retail.
- **Sign conventions silently corrupt CVD.** Coinbase reports the maker side; Kraken WS v2 and Binance (`m`) encode the taker; Databento `A` means a seller aggressed. *Why:* one flipped feed inverts every delta-based signal built on it.
- **Executed volume beats displayed size.** Resting orders can vanish in milliseconds, and spoofing is real and illegal. *Why:* treat DOM walls as hypotheses until they trade.
- **Persistence is real but bounded.** Metaorder splitting makes aggressive flow persist; liquidity adjusts and impact decays (propagator). *Why:* continuation trades target small, fast moves and exit when aggression stops; reversal trades wait for it to stop.
- **Slow predictive flow is mostly private.** Days-to-weeks evidence uses signed, participant-level, mostly non-public data (bank customer FX, CBOE opening volume). *Why:* retail "smart money flow" scanners are degraded proxies with no peer-reviewed support.
- **Test at the granularity you trade.** Footprint rules need tick trades with true aggressor side; limit-order rules need MBO plus queue and latency models. *Why:* bar-level and fill-at-touch backtests overstate order-flow strategies.

---

## 2. What order flow can and cannot do

| Horizon | What the evidence shows | Grade | Who can use it |
|---|---|---|---|
| Same interval | Equities: OFI explains most of 10-s mid changes, mean R² ≈ 65% (CKS 2014) [SC]; adding deeper levels improves fit (MLOFI, integrated OFI). FX: daily interdealer flow R² > 50% (Evans-Lyons 2002) | [Strong · PR] | Explanation, impact models; not a trade signal |
| Next tick to seconds | Queue imbalance predicts the next mid move; micro-price; DeepLOB labels 10–100 events ahead; lagged cross-asset OFI decays rapidly | [Moderate · WP/PR] | Market makers, execution algos; retail only as an execution filter |
| Minutes | Lagged NYSE imbalance window ~30 min (1996) → ~5 min (CRS 2005), probably shorter now (inference); order-sign persistence from splitting | [Moderate · PR] | Retail trigger at a level, holding minutes to hours |
| Hours | Continuation after stop clusters trigger at levels, significant for hours, not days (Osler 2005, FX) | [Moderate · PR] | Level-break follow-through |
| Days–weeks | Bank customer FX flow forecasts 1 day–1 month OOS; CBOE signed opening option volume: > 40 bp next day, > 1% next week; retail imbalance predicts weeks (BJZZ) | [Moderate · PR] | Owners of the data; retail gets degraded proxies |

**The key correction to footprint lore (inference from CKS):**
- A rising price with flat or negative delta is **not** proof of "hidden selling". Bids can be added at higher prices and offers cancelled, so price lifts with little aggression. Only MBP/MBO data show this.
- The mirror case also holds: a falling price with positive delta can be offers stepping down while bids are pulled.
- Before accepting a divergence read:
  1. Check whether the book moved (bids stepping up, offers pulled) on L1/L2.
  2. If L1 quotes exist, compare OFI with delta over the same window (`flowkit.py ofi`). OFI aligned with price while delta disagrees means a passive-driven move, not a reversal signal.
  3. Act only at a planned level, and only after confirmation (card B, §6).
- Crypto caveat [Weak · PR · K · SC]: on BitMEX XBTUSD, trade-flow imbalance explained contemporaneous price better than book OFI (Silantyev 2019), attributed to noisy book updates. Measure the ranking per venue rather than assuming it.

**Realistic retail use (inference from the cost and latency evidence, §3 and §8):**
- Hold for minutes to hours, with targets several ticks to points away, set by structure (VWAP, value area, prior-day levels).
- Use order flow for (a) a go/no-go decision at the level, (b) a stop beyond the flow-defined invalidation, and (c) a time stop, because impact decays.
- Use book signals only to improve execution, e.g. do not join a bid when queue imbalance is strongly negative.

**Slower horizons: how participant flow enters an order-flow plan** (detail in `market-forces-flows.md` §5–§8):
1. Weekly/daily bias from positioning extremes, calendar and rebalance flows, ETF flow streaks.
2. Daily regime: gamma sign, vol level, scheduled events.
3. Intraday location: value, VWAP, prior-day levels.
4. Order-flow trigger (§6).
5. Exit by structure or time.

ETF creations lag secondary-market demand, and creation/redemption activity *negatively* predicts subsequent returns (Brown, Davies & Ringgenberg 2021) [Moderate · PR · K · SC magnitude]. Read creation streaks as reversal risk, not as confirmation.

---

## 3. Data foundations

### Data levels (Databento schema vocabulary) [V · DOC]

| Level | Schema | Contains | Enables | Cannot do |
|---|---|---|---|---|
| L0 | OHLCV | Bars | Approximate profile and VWAP | Delta, footprint |
| Trades | Trades | Every print, with side if the source has it | Footprint, delta, CVD, tape speed, sweeps | Adds/cancels, so OFI is impossible |
| L1 | MBP-1; **TBBO** (each trade plus the BBO just before it); BBO sampled at 1 s / 1 min | Top of book (plus trades) | Best-level OFI, queue imbalance, weighted mid, Lee-Ready signing | Deep-book OFI, queue position |
| L2 | MBP-10 | Aggregated depth, top 10 levels | MLOFI/integrated OFI, depth imbalance, stacking/pulling | Which order cancelled; reliable icebergs |
| L3 | MBO | Every order add/modify/cancel/fill by order ID | Queue position, iceberg refills, spoof-pattern recognition, honest limit-fill backtests | Hidden size before it trades |

Other schemas: Imbalance (auction imbalance), Statistics (OI, settlement), Status (halts, auctions). Records carry `ts_event` (matching-engine time) and `ts_recv` (capture time), which lets you model feed latency [K].

### Aggressor flags vs inference
- **CME** gives a true aggressor in the MDP 3.0 Trade Summary (`price-action.md` §7). That summary groups all fills of one aggressing order per price level in a match event, so a CME footprint "trade" is usually one aggressor event. Platforms that re-split prints into fills inflate trade counts [K · SC].
- **No flag** (equities, OTC, older data) [K · PR]: **tick rule** +1 on an uptick, −1 on a downtick, zero tick carries the last non-zero sign; **quote rule** +1 above the midquote, −1 below; **Lee-Ready (1991)** = quote rule, tick rule at the midpoint. Use the prevailing quote with **no lag** on modern timestamps (the 5-second lag was for 1980s data; timestamp handling matters, Holden & Jacobsen 2014).
- **BVC:** V^B = V·Z(ΔP/σ_ΔP) (Easley, López de Prado & O'Hara 2016) [Contested]. Against near-perfect CME labels, BVC underperformed the tick rule (a result usually attributed to Andersen & Bondarenko 2015; Chakrabarty, Pascual & Shkilko 2015 used equity data).
- **Retail flag in TAQ:** BJZZ catches only about a third of retail trades and mis-signs a material share. Barber et al. (2024, *JF* 79(4)) propose a midpoint refinement [Moderate · PR · K · SC: ~35% identified, ~28% mis-signed].

### Side-sign normalization (aggressor = +1 when a buyer lifted the offer)

| Venue / feed | Raw field | Meaning | Map to aggressor | Tag |
|---|---|---|---|---|
| CME MDP 3.0 | AggressorSide (tag 5797) | 1 = buy, 2 = sell, 0 = none (implied trades; first trade after a Velocity Logic re-open) | 1 → +1, 2 → −1, 0 → exclude | [V · DOC] |
| Databento, action `T` (trade) | `side` | `B` = buyer aggressed, `A` = seller aggressed, `N` = none | B → +1, A → −1, N → exclude | [V · DOC] |
| Databento, action `F` (fill) and Add/Modify/Cancel | `side` | Side of the **resting** order | Never use as aggressor | [V · DOC] |
| Databento `side = N` on trades | — | Source gives no side; auction open/close; trades vs non-displayed or implied orders; off-exchange | Exclude or sign by Lee-Ready, and flag it | [V · DOC] |
| Databento MBP datasets | — | No Fill records; Trade side reportedly always `N` on datasets sourced from top-of-book feeds | Check before building CVD | [V · DOC · SC] |
| Coinbase Exchange matches | `side` | **Maker** side: a `sell` match is an up-tick (buyer aggressed) | sell → +1, buy → −1 | [V · DOC] |
| Kraken WS v2 trade | `side`, `ord_type` | **Taker** side and taker order type | buy → +1 | [V · DOC] |
| Kraken REST Trades | `b`/`s` (4th field) | Not defined on the REST page | Treated as taker (consistent with WS v2); confirm on the same trade IDs | [V · DOC] + inference |
| Binance spot aggTrades | `m` | "Buyer is maker"; one aggTrade ≈ one taker order at one price | m = true → −1, false → +1 | [V · DOC] (sign by inference) |
| Bybit, OKX public trades | side | Taker side | buy → +1 | [K · SC] |
| Tardis.dev, Kaiko, Amberdata | side | Usually normalized to aggressor | Verify each feed | [K] |
| US equities (no flag) | — | — | Lee-Ready on TBBO; tick-rule fallback | [K · PR] |

**flowkit input rule.** By default (`--side-convention aggressor`) `flowkit.py delta|profile` accepts only unambiguous aggressor labels: `buy`/`sell`, `b`/`s`, `1`/`-1` — which is what `fetch.py trades` writes. Letters such as `A`/`B`/`ask`/`bid` mean opposite things in different feeds, so for raw vendor files pass the convention explicitly: `--side-convention databento` (A = sell aggressor, B = buy aggressor, N = none), `cme` (MDP3 1 = buy, 2 = sell), `maker` (raw Coinbase maker side, inverted), `buyer-maker` (Binance `m`/isBuyerMaker: true = sell aggressor), `at-quote` (vendor "traded at ask/bid"). If most side values don't fit the chosen convention the script stops with an error instead of guessing; rows with no side (`N`, blank) fall back to the tick rule with a warning. All five conventions were checked to give identical delta on the same tape.

### Off-exchange, hidden and side-less prints
- About half of US equity volume prints off-exchange (FINRA TRF; 50.6% FY2025, `price-action.md` §7). These prints carry no side and are reported after execution, within about 10 s [SC]. A single-exchange equity footprint misses about half the tape.
- Large "dark pool block" prints are often pre-arranged trades, VWAP or risk-trade completions, or late reports with special condition codes [K]. They are not directional by default.
- Hidden and iceberg liquidity reveals itself only when it trades. It is partly inferable from public data (Frey & Sandås; `price-action.md` §7) [Weak · WP].
- **Spot FX** has no consolidated tape. Use CME FX futures (6E, 6J …) as the observable order-flow proxy [PL].

### Data-quality checklist (ask before trusting any footprint)
1. **Dropped messages.** The Coinbase matches channel can drop messages: repair gaps using the heartbeat's last trade ID plus REST. `level2` (authenticated) guarantees delivery; `level2_batch` (unauthenticated) batches every 50 ms; `full`/`level3` give L3 [V · DOC].
2. **Gateway aggregation.** Whether a Rithmic/CQG/other retail connection delivers every Trade Summary message or aggregated/throttled ticks varies by gateway and platform. This is the biggest hidden source of footprint mismatch between platforms [K · SC].
3. **Liquidation feeds are sampled.** Binance USDⓈ-M `<symbol>@forceOrder` pushes only the latest liquidation per symbol per 1000 ms, so totals built from it are lower bounds [K · DOC · SC].
4. **Historical vs live.** Exchange-complete history and a throttled live feed give different footprints. Paper-trade on the live feed before trusting a backtest.
5. **Session boundary.** Reset CVD at the exchange session (CME 17:00 CT [K · SC]; NT8 `CumulativeDelta` resets at the session break [V · VEN]). Pick one crypto day boundary and keep it.

### Latency realities [K · PR · SC numbers]
- **Budish, Cramton & Shim (2015):** ES–SPY correlation breaks down at millisecond horizons; the median ES–SPY arbitrage duration fell from ~97 ms (2005) to ~7 ms (2011).
- **Aquilina, Budish & O'Neill (2022, LSE message data):** latency-arbitrage races occur about once a minute per FTSE 100 stock, are decided in microseconds (modal ~5–10 µs), involve ~20% of volume, and impose a "latency tax" of ~0.4 bp of volume.
- **Physical floor, Aurora → New Jersey:** ~4 ms one-way by microwave vs ~6.5 ms by fiber. Retail round trips run tens of ms plus platform rendering.

### Platforms (vendor capabilities change; [VEN], spot-check specifics; docs as fetched Nov 2026)

| Platform / source | Shows | Documented specifics | Tag |
|---|---|---|---|
| Sierra Chart Numbers Bars | Footprint bid×ask per price; delta = ask − bid volume | Diagonal compare: bid volume at a price vs ask volume one level higher. Minimum-volume compare threshold default **0**; percent-compare thresholds 0.25/0.50/0.75. The 3:1 = 300% ratio appears only as an illustration, not a default. Stacked imbalances need a separate study (Volume at Price Threshold Alert V2) | [V · VEN] |
| NinjaTrader 8 Order Flow+ | Volumetric bars: `BarDelta`, `CumulativeDelta` (session reset), `MaxSeenDelta`/`MinSeenDelta`, `DeltaSh`/`DeltaSl`, total buy/sell volume, `Trades`, per-price ask/bid/delta | The default imbalance ratio is not on the fetched page; recalled as 1.5 | [V · VEN]; ratio [SC] |
| Bookmap | Heat map of historical *displayed* liquidity, volume bubbles, CME MBO views | Iceberg/stop-run add-ons have no published accuracy | [K · VEN] |
| ATAS | Cluster/footprint, Smart DOM, Big Trades, cluster search | Claims to rebuild aggressor orders from prints | [K · VEN · SC] |
| Jigsaw Daytradr | DOM, "reconstructed tape" (merges one aggressor's prints), summary and depth-and-sales | — | [K · VEN] |
| Quantower | Multi-broker footprint/cluster, DOM Surface, volume analysis | — | [K · VEN] |
| Rithmic / CQG | FCM gateways beneath most retail futures platforms; Rithmic common for unbundled ticks and CME MBO | Tick aggregation varies (checklist item 2) | [K · SC] |
| Databento | Normalized historical/live feeds (CME `GLBX.MDP3`, equity MBO/ITCH-type) | Schemas above | [V · DOC] |

**Data hierarchy for order-flow work:**
1. CME futures: MBO, aggressor-flagged trades, a single venue.
2. Regulated or major crypto venues: explicit side, but conventions differ; normalize and aggregate.
3. Nasdaq/NYSE single-venue MBO plus TAQ with inferred sign; half the volume is off-exchange.
4. Spot FX: proxy via CME FX futures.

---

## 4. Signals with evidence

| Signal | Definition | Horizon | Evidence | Practical use |
|---|---|---|---|---|
| OFI, best level | Σ e_n (formula in `price-action.md` §7); ΔP_k = α + β·OFI_k, β ≈ c/average depth | Contemporaneous | [Strong · PR · V in prior notes] | Diagnose passive vs aggressive moves |
| Multi-level OFI (MLOFI) | e_n applied at levels 1..M; linear fit | Contemporaneous | [Moderate · WP · V]: out-of-sample fit improves with **each** added level, 6 liquid Nasdaq stocks (Xu, Gould & Howison 2019) | Needs MBP-10 |
| Integrated OFI | Depth-normalize each level's OFI (M = 10), weight by first PC: OFI^I = w₁ᵀ·ofi/‖w₁‖₁ [K · SC] | Contemporaneous; lagged cross-asset terms short-lived | [Moderate · WP · V] (Cont, Cucuringu & Zhang; *Quant. Finance* 2023 [SC]) | Research and cross-asset execution |
| Deep OFI | Deep nets on OFI features beat nets on raw book states | A few mid-price changes | [Moderate · PR · K · SC] (Kolm, Turiel & Westray 2023) | Not retail |
| Queue imbalance | I = (q^B − q^A)/(q^B + q^A); P(up) = 1/(1 + e^−(x₀ + x₁·I)) | Next mid move | [Moderate · WP · V]: significant in all 10 Nasdaq stocks; large gain for **large-tick**, moderate for small-tick (Gould & Bonart; *MML* 2016 [K · SC]) | Execution filter on large-tick books |
| Weighted mid | P_w = I_w·P^A + (1 − I_w)·P^B, I_w = q^B/(q^B + q^A) | Next tick | [K]; noisy and can overshoot | Rough fair value |
| Micro-price | P_micro = M + g(I, S): expected mid after many future mid changes, estimated by a Markov chain over (imbalance bucket, spread) states; ~10 buckets, spreads 1–2 ticks, symmetrized data [SC] | Several mid changes | [Moderate · PR · K] (Stoikov 2018) | Limit-order fair value |
| Order-sign long memory | Sign ACF ~ τ^−α, α ≈ 0.6 (H ≈ 0.7), LSE | Persistence over many trades | Stylized fact [Strong; Lillo & Farmer V · WP; Bouchaud et al. 2004, Tóth et al. 2015 K · PR] | Explains continuation; plan exits |
| Tape speed | Trades per second; short durations ⇒ larger impact, faster quote updating | Event level | [Moderate · PR · K] (Dufour & Engle 2000; ACD, Hawkes models) | "Pay attention" cue |
| VPIN | Σ\|V^S − V^B\|/(n·V) over n = 50 volume buckets, V = ADV/50, BVC on 1-min bars [SC]; alerts at CDF > 0.9 [SC] | Volatility, not direction | [Contested · PR · K] | Never a crash alarm |
| DeepLOB-type models | CNN + LSTM on top 10 levels; FI-2010 benchmark; labels k = 10–100 events [SC] | Seconds | [Moderate · PR · V] in-sample; LOBCAST: all 15 models drop significantly on new data [Moderate · WP · V] | Treat "AI order-book" products as unproven |
| FX customer flow | Bank end-user signed flow | 1 day–1 month | [Moderate · PR · K] | Data is private |
| Options opening flow | Buyer-initiated *opening* volume P/C | 1 day–1 week | [Moderate · PR · V], non-public data | Use open/close datasets |
| Retail UOA / sweep / dark-pool alerts | Vendor-inferred side and "size" | — | **No evidence** (none found, which is not the same as negative evidence) | Context only |

**OFI family notes.**
- CKS setup: Δt = 10 s, β re-estimated over 30-minute windows, 50 S&P 500 stocks, NYSE TAQ, April 2010 [K · SC]. Trade imbalance alone explained much less.
- Cross-impact: once multi-level OFI is integrated, cross-asset terms add **no** contemporaneous power. Lagged cross-asset OFI helps forecasts only at short horizons, and the effect decays rapidly [V · WP].
- Microstructure models agree that the forecastable component lives at the horizon of a few book events. Net-of-cost OOS evidence for non-colocated traders: **none found**.

**Queue imbalance and tick size.**
- The signal is strong where the spread is usually one tick and queues are long (large-tick: ES, many low-priced stocks). It is weak where price moves through thin, frequently changing queues (small-tick: BTC at $0.01, high-priced stocks). The mechanism here is inference; the large/small-tick difference is the finding.
- Practical rule: for small-tick books, read depth **within N bps** rather than top-N levels. A live BTC snapshot in this session showed a top-of-book bid of 0.00014 BTC, which is dust.

**Persistence vs efficiency (propagator).**
```
p_t = Σ_{t'<t} G(t − t')·ε_{t'} + noise,   G(ℓ) ~ ℓ^(−β),   diffusive prices need β ≈ (1 − γ)/2
```
γ is the sign-autocorrelation exponent. Impact decays, offsetting predictable flow [Moderate · PR · K] (Bouchaud, Gefen, Potters & Wyart 2004). Sign persistence comes mainly from **splitting, not herding** (Tóth et al. 2015). Prices stay efficient because liquidity and trade size adjust anti-correlated to flow (Lillo-Farmer). Trading rule: stacked aggressive flow tends to continue for a while, so take small, fast continuation targets and exit when aggression stops.

**VPIN (extends `market-forces-flows.md` §3).**
- Easley, López de Prado & O'Hara (2012, *RFS* 25(5)) report predictive power for toxicity-induced volatility.
- Andersen & Bondarenko (2014, *JFM* 17) attribute that power to classification and volume-clock choices and to VPIN's mechanical link with trading intensity. Controlling for volume and volatility removes most of it, and in their replication VPIN did not peak *before* the flash crash [SC].
- In crypto, Roll, Kyle λ, Amihud and VPIN measures helped predict volatility (Easley, O'Hara, Yang & Zhang 2024) [Weak · WP · K · SC].

**FX order flow.**
- Evans & Lyons (2002, *JPE* 110(1)) [Strong · PR · V]: daily order flow gives R² > 50% vs macro models whose R² rarely reaches 10%; $1bn of net dollar purchases moves DM/$ by about 1 pfennig. Detail [K · SC]: interdealer D2000-1 data, May–Aug 1996; R² ≈ 0.64 DM/$, ≈ 0.45 ¥/$. **It explains, it does not predict:** the "forecast" uses contemporaneous flow.
- What predicts: bank **customer** flow. Citibank end-user flow beat a random walk OOS at 1-day to 1-month horizons (Evans & Lyons 2005, *AER* 95(2)) [Moderate · PR · K].
- Who is informed: **financial** customers (asset managers, hedge funds) predict returns; corporate and private flow carries little information (Menkhoff, Sarno, Schmeling & Schrimpf 2016, *JF* 71(2)) [Moderate · PR · K · SC].
- Public-ish data: CLS hourly settlement-based flow by counterparty type is sold via vendors [K · SC].
- Retail proxies: CME FX futures flow and positioning.

**Equity order imbalance.** Daily imbalances are strongly autocorrelated (splitting) (Chordia & Subrahmanyam 2004, *JFE* 72(3)) [Moderate · PR · K · SC]. Lagged imbalance predicts returns positively on its own but negatively once current imbalance is controlled for. Simple daily strategies were profitable in 1988–1998 NYSE data. The horizon has since shrunk to minutes (CRS 2005).

**Options order flow.**
- Pan & Poteshman (2006, *RFS* 19(3)) [Moderate · PR · V]: put-call ratios from **buyer-initiated opening** volume (a unique CBOE dataset) predict stock returns; low-P/C stocks beat high-P/C by **> 40 bp next day** and **> 1% over the next week**, risk-adjusted. The source is **non-public information**; the effect is stronger with more informed traders and higher-leverage options. Ratios from *publicly observable* volume showed little predictability [K · SC]. Persistence after the 1990–2001 sample is unchecked.
- Related [K · PR]: signed "positive"/"negative" option volume is informative (Easley, O'Hara & Srinivas 1998); delta-weighted option order imbalance predicts stock returns (Hu 2014); high option-to-stock volume predicts *lower* returns, low-minus-high ~1.47%/month (Johnson & So 2012) [SC], traced to *opening* trades (Ge, Lin & Pearson 2016); option imbalance moves *option* prices via market-maker inventory risk (Muravyev 2016); abnormal directional volume before M&A announcements (Augustin, Brenner & Subrahmanyam 2019) is largely illegal insider activity that cannot be identified ex ante.

**Retail "unusual options activity", sweep scanners and dark-pool print services: no peer-reviewed test found.** Mechanical noise [K]: OPRA prints carry no aggressor side (vendors infer it against the NBBO); opening vs closing is unknown intraday (OCC open interest updates next morning); multi-leg, hedge and roll trades print as single legs; an ISO "sweep" signals urgency to execute across venues, not information; TRF prints have no side and are reported after the fact.

**Coaching rule:** the signal with evidence is *opening, signed, by investor class*. Prefer exchange open/close datasets (Cboe/ISE/Nasdaq) over real-time sweep feeds, and still expect a decayed effect.

---

## 5. Footprint definitions (precise)

```
Delta(bar)          = ask-traded volume − bid-traded volume = buyer-aggressor − seller-aggressor volume
CVD                 = running Σ delta, reset at the session boundary
Buy imbalance at P  : AskVol(P) ≥ R · BidVol(P − 1 tick)      (diagonal, Sierra Chart convention)
Sell imbalance at P : BidVol(P) ≥ R · AskVol(P + 1 tick)
Stacked imbalance   : ≥ 3 consecutive price levels with same-direction imbalances
Unfinished auction  : both bid and ask volume > 0 at the bar/session extreme (e.g. 12×35 at the high);
                      "finished" = ~0 on the aggressor side at the extreme (0×35 at the high)
Exhaustion print    : very small volume at the extreme after a run (aggressors stopped)
Absorption          : aggressive volume at/near one price ≥ 2–3× the median per-price volume of the last
                      20 bars, with ≤ 1–2 ticks of progress within ~30–120 s  ("effort without result")
Delta divergence    : price higher high while bar delta or CVD makes a lower high (mirror for lows)
Iceberg signature   : repeated executions at one price exceeding the displayed size there
Sweep               : one aggressor event clearing ≥ 3 price levels (or ≥ k× average trade size)
Tape burst          : trades/s ≥ 3× the trailing 5-minute median
Initiative/responsive (Dalton): buying above value or selling below value = initiative;
                      buying below value or selling above value = responsive
```
The definitions follow vendor docs (Sierra, NT8) where they exist [V · VEN]; the thresholds are [PL].

**Why diagonal (inference):** with a one-tick spread, buyers lifting the offer at P trade against sellers hitting the bid at P − 1, so those are the volumes competing at the same moment.

| Parameter | Convention | Status |
|---|---|---|
| Imbalance ratio R | **3.0 ("300%") is the most-cited convention**, range 1.5–4.0 | [PL]. Not a platform default: Sierra only illustrates 3:1 [V]; NT8 default recalled as 1.5 [SC] |
| Minimum volume on the larger side | Instrument-scaled: often 10–30 contracts for ES/NQ 1-tick rows; higher for coarser rows | [PL]; Sierra default 0 [V] |
| Stack count | ≥ 3 levels | [PL] |
| Absorption | Volume ≥ 2.5× median per-price volume (20 bars), net progress ≤ 2 ticks within 60 s | [PL] test default |
| Proximity to level | Within ~1–4 ticks (ES/NQ) | [PL] |

Every parameter is a trial: sweeping R (1.5–4), stack (2–5), minimum volume and bar type is multiple testing (§9).

---

## 6. Setup playbook (rule cards)

None of these setups has peer-reviewed evidence of profitability net of costs [Lore · PL]. Parts of their mechanisms are supported: flow beyond depth moves price (CKS); splitting makes aggression persist (Lillo-Farmer); impact is transient (propagator); stops cluster just beyond levels and cascade when hit (Osler, `price-action.md` §2); fast tape carries more information (Dufour-Engle). The cards are codified conventions for coaching and testing, not proof of edge.

**Before every session, mark locations:** prior-day high/low/close and overnight high/low; VAH/VAL, POC, single prints/LVNs; VWAP with 1σ/2σ bands and anchored VWAPs; the opening range and round numbers. Take triggers only within ~1–4 ticks of a level. Stand aside midday and in the seconds after scheduled data, because depth is withdrawn then (`market-forces-flows.md` §3).

**A. Absorption reversal at a level (responsive).** Mechanism: propagator decay; CKS (deep passive side).
- *Trigger:* at the level, aggressive volume ≥ 2–3× the median per-price volume of the last 20 bars, and price fails to trade > 1–2 ticks through within ~30–120 s. Then the first opposite imbalance or delta flip, e.g. bar delta turns positive after a selling-absorption bar.
- *Entry:* limit at or just inside the absorbed price, or a stop 1 tick beyond the trigger bar.
- *Stop:* 1–3 ticks beyond the absorption extreme. A true defender should not let price trade there again.
- *Targets:* T1 at VWAP or POC (1–1.5R); T2 at the opposite value-area edge.
- *Manage:* scratch if there is no follow-through in ~2–5 min (impact has decayed).
- *Fails when:* the absorber is an iceberg that completes (it becomes a breakout; flip to C or G); "absorption" was offers pulled and re-posted (spoof-like); news hits.

**B. Delta divergence or exhaustion at the extreme.** The most over-fitted footprint pattern in education material [PL].
- *Trigger:* a new high or low **at a level**, with bar delta or CVD not confirming, plus an exhaustion print or finished auction at the extreme. *Confirmation:* an opposite stacked imbalance or a break of the trigger bar's low (high).
- *Entry:* on confirmation only. *Stop:* beyond the extreme + 1–2 ticks. *Target:* VWAP, POC, or the impulse origin.
- *Passive-activity caveat:* divergence persists through passive-driven trends, because delta omits limit adds and cancels (§2). Check the book or OFI before reading divergence as hidden opposition.
- *Fails when:* divergence is common and cheap, so without location plus confirmation it is noise.

**C. Stacked-imbalance continuation (initiative).** Mechanism: splitting persistence; CKS impact through thin depth.
- *Trigger:* a break through a level (IB high, ON high, VAH) with **≥ 3 stacked buy imbalances at R ≥ 3.0**, the minimum-volume filter passed, positive bar delta, and CVD at a session high.
- *Entry:* on the first pullback **into the stacked zone**, not on the breakout bar. *Stop:* lowest imbalance price of the stack − 1–2 ticks.
- *Target:* next LVN/HVN boundary, prior swing, or measured move. Trail behind each new stacked zone.
- *Fails when:* the breakout meets a responsive seller and the zone is fully retraced (trapped longs fuel card D); or the market is in a positive-gamma, mean-reverting regime (`market-forces-flows.md` §4).

**D. Failed auction / trapped traders.** Mechanism: stop clustering and cascades (Osler) [Moderate · PR]; the setup itself is untested.
- *Trigger:* heavy aggressive buying or stacked buy imbalances at or above a level (e.g. above the prior-day high), then price returns **inside** the level within 1–3 five-minute bars and trades through the imbalance zone.
- *Entry:* on the re-entry, or on a retest of the zone from below. *Stop:* above the trap high.
- *Target:* the opposite side of value or the POC. Expect acceleration as trapped buyers' stops trigger.
- *Fails when:* acceptance builds back above the level (time and volume), in which case the move was initiative.

**E. Unfinished auction ("unfinished business") revisit.** [Lore]; "revisited more often than chance" is untested.
- *Use:* a session high or low printed as an unfinished auction is a **magnet target** for other trades, not a stand-alone entry.
- *Test it:* compare the revisit rate with a matched control of other extremes (§9). `flowkit.py delta` flags unfinished auctions at swing extremes.

**F. LVN rejection vs acceptance; POC migration (AMT + flow).** AMT lore (`price-action.md` §6); consistent with CKS depth logic.
- *Read:* price entering an LVN tends to traverse it fast (thin depth).
- *Entry:* a rejection *at* the LVN edge with absorption is a responsive entry, with the stop beyond the absorption extreme and the next HVN/POC as target.
- *Bias flip:* acceptance (time and volume building inside the LVN) flips the bias. A POC migrating in the trend direction during the day confirms initiative.

**G. Initiative breakout from value (synthesis of C + F + Dalton).**
- *Location:* the prior value-area edge or IB extreme. *Trigger:* trade outside value with initiative activity (buying above value: stacked buy imbalances, CVD making session highs).
- *Acceptance:* time and volume build outside value, and the developing POC migrates outward.
- *Entry:* a pullback to the VAH/breakout level that holds, with responsive buying or absorption of selling at the edge. *Stop:* back inside value, beyond the stack low + 1–2 ticks.
- *Target:* next LVN/HVN or prior swing; trail behind new stacks.
- *Fails when:* price returns inside value and is accepted there. That is card D's setup, and the rotation logic of the 80% rule applies (`price-action.md` §6; its 80% figure is lore).

**H. Sweep and reclaim of a level.** Mechanism: stop-cascade (Osler); otherwise lore. This is the same mechanism as the liquidity sweep / spring / UTAD in `price-action.md` §8.
- *Trigger:* a sweep (one aggressor event clearing ≥ 3 levels, or ≥ k× average trade size) runs **into stops beyond a level**. Use the next 10–30 s to decide:
  - *Follow:* new aggressive flow arrives within seconds in the sweep direction.
  - *Fade/reclaim:* the sweep prints at the extreme with no follow-up, responsive absorption appears, and price trades back inside the level.
- *Entry (reclaim):* on the return inside the level. *Stop:* beyond the sweep extreme. *Target:* POC or the opposite side of value (as in D).
- *Never* engineer a sweep with non-bona-fide orders; that is manipulation.

**I. Iceberg reload at a level.** Hidden depth is partly detectable, and icebergs impose adverse selection on displayed orders (Frey & Sandås) [Weak · WP]. Vendor iceberg detectors have no published accuracy.
- *Trigger:* repeated executions at one price exceed its displayed size, and the displayed size refreshes after each hit (MBP-10 plus trades at minimum; MBO preferred). It is a variant of A.
- *Entry:* fade toward the defended side once the aggressor fails to progress. *Stop:* 1–3 ticks beyond the iceberg price. *Target:* as A.
- *Flip:* when the reload stops and price trades through, the iceberg is exhausted; treat it as a breakout (C).
- *Fails when:* the iceberg is an execution algo that finishes; or a throttled/aggregated feed fakes the refill pattern. How CME MBO represents iceberg refills (same order ID vs a new ID) was not verified.

**J. DOM stacking/pulling and tape speed: context filters, not entries.**
- Displayed size that holds **and gets hit** is information. Size that vanishes as price approaches is not, and a repeated pattern may be spoofing (recognize it; never imitate it; law in `price-action.md` §7).
- A tape burst at a level (trades/s ≥ 3× the trailing median) marks the decision point. Act only after the burst resolves [Moderate · PR · K mechanism, Dufour-Engle].

**Rules that follow from the evidence:**
- Put the stop at the price that invalidates the flow story (beyond the absorption or stack extreme), not at a fixed dollar amount.
- Target the next liquidity reference.
- Use time stops, because impact decays.
- Log every signal with objective rules and test it (§9) before sizing up.

---

## 7. Crypto order flow

Crypto offers unusually rich *public* flow data: explicit side, perp OI, funding and liquidations. Four warnings: sides differ by venue (§3 table); unregulated-venue volume is mostly wash trading: of 29 exchanges studied (regulated and unregulated), it averaged > 70% on the unregulated ones and was absent on regulated ones (Cong et al. 2023) [Moderate · PR]; liquidity is fragmented, with large cross-border deviations such as the Korean premium (`market-forces-flows.md` §12); liquidation feeds are sampled (§3).

**Spot vs perp CVD [Lore · PL]; plausible from leverage mechanics, untested in peer review.**
- Build normalized CVD separately for (a) **spot** on regulated or major venues (Coinbase, Kraken, Binance spot; US spot ETF flows are the slow channel) and (b) **perps** (Binance, Bybit, OKX, Hyperliquid, CME futures).
- *Spot-led up-move:* spot CVD rising; perp CVD, funding and OI flat or OI down. Lore reads this as "real demand".
- *Perp-led up-move:* perp CVD up, OI up, funding rising, spot CVD flat or down. This is leverage-driven and vulnerable to a long flush.

**OI/price matrix [Lore · PL; standard futures lore]:**

| Price | OI | Read |
|---|---|---|
| Up | Up | New longs; flush fuel if funding is elevated |
| Up | Down | Short covering; weaker continuation |
| Down | Up | New shorts; squeeze fuel if funding is negative |
| Down | Down | Long liquidation/capitulation; exhaustion once OI stabilizes |

**Liquidation heatmaps** (CoinGlass, Hyblock, Kingfisher-type) [Weak · VEN · K] are **model estimates**. They infer liquidation clusters from OI changes at each price and assumed leverage tiers (e.g. 10×/25×/50×/100×) and maintenance margins. True liquidation prices depend on unobserved entries, margin mode and added collateral. Treat a cluster as a hypothesis about where forced flow *could* occur. Require live liquidation prints plus aggressive flow to confirm it, and never assume a cluster "must" be swept.

**What is predictive vs narrative:**

| Claim | Status |
|---|---|
| Post-cascade exhaustion (OI collapse + negative funding) | Best-supported use; mechanism [Moderate], no peer-reviewed return test |
| Extreme funding / OI as risk amplifiers | Risk gauge, not alpha (`market-forces-flows.md` §12) |
| Derivatives lead spot in price discovery on offshore perps | [Moderate · PR · K] (Alexander, Choi, Park & Sohn 2020, BitMEX) |
| Microstructure measures predict crypto volatility | [Weak · WP · K · SC] (Easley et al. 2024) |
| Spot-led vs perp-led classification | [Lore]; plausible, untested |
| Heatmap clusters as targets | [Weak · VEN]; narrative until prints confirm |
| Single-venue CVD on an unregulated exchange | Ignore |

**Session effect (inference from CKS depth logic):** weekend and off-hours books are thinner, so the same flow moves price more; size down. The 10 Oct 2025 cascade (> $19bn liquidated; OI −$19.2bn in 40 minutes) is in `market-forces-flows.md` §12.

---

## 8. Market making and liquidity provision

Professional liquidity provision is an inventory and adverse-selection control problem [V · PR] (Avellaneda & Stoikov 2008, paper text checked).
```
Mid:               dS = σ dW            (no drift view; maximize expected exponential utility of terminal P&L)
Reservation price: r(s, q, t) = s − q·γ·σ²·(T − t)      long q > 0 → quotes shade down to shed inventory
Fill intensity:    λ(δ) = A·e^(−k·δ)                     δ = quote distance from mid
Total spread:      δ^a + δ^b = γ·σ²·(T − t) + (2/γ)·ln(1 + γ/k)   centred on r, not the mid; independent of q
Paper values:      s = 100, T = 1, σ = 2, dt = 0.005, q0 = 0, γ = 0.1 (also 0.01), k = 1.5, A = 140; 1,000 runs
Check (γ = 0.1):   0.4·(T − t) + 20·ln(1.0667) = 1.69 at t = 0 → 1.29 at T; time-average 1.49 = paper's spread
```

| Strategy (γ = 0.1) | Profit | Std(profit) | Std(final q) |
|---|---|---|---|
| Inventory-skewed | 65.0 | 6.6 | 2.9 |
| Symmetric around mid | 68.4 | 12.7 | 8.4 |

At γ = 0.01, profit is 68.6 vs 68.8 and std 8.7 vs 12.8. Inventory skewing roughly halves P&L dispersion for a small loss in mean. Choose dt small enough that multiple fills per step are unlikely, but larger than the typical tick time.

**Extensions [K · PR]:** closed-form quotes with inventory limits, the standard practical form (Guéant, Lehalle & Fernandez-Tapia 2013); skewing or cancelling quotes on volume imbalance to cut adverse selection (Cartea, Donnelly & Jaimungal 2018; textbook Cartea, Jaimungal & Penalva 2015); queue imbalance tells a resting order when to stay or cancel, and that value falls with latency (Lehalle & Mounjid 2017); front-of-queue positions are worth a meaningful fraction of the spread in large-tick assets (Moallemi & Yuan 2017) [WP · SC].

**Why retail cannot compete at HFT horizons:**
1. On FIFO books, queue priority goes to the fastest; retail limit orders join the back.
2. Retail limit fills are adversely selected: you get filled when informed or faster flow runs through you.
3. Rebates and fee tiers favour registered market makers.
4. Signal half-lives (ticks to seconds) are shorter than retail latency plus decision time.

**Cost arithmetic (ES contract specs [K]; fees [SC], not verified Nov 2026):**
- **ES:** tick = 0.25 pt = $12.50. Fees run ~$3–5 per round trip (~0.3 tick), plus ~1 tick of spread/slippage for market in and out, so **≈ 1.3 ticks all-in**.
- **MES:** tick value $1.25 with fees ~$1–1.5 per round trip, so fees alone are ~0.8–1.2 ticks, roughly 3× heavier per tick than ES.
- A seconds-horizon signal worth < 1 tick is negative EV.

**What to take from market making (inference from the models above):**
- **Adverse selection is measurable.** Record markouts: the mid-price change at +1 s, +10 s and +60 s after each fill, signed in the trade direction. Persistently negative short markouts on limit fills mean you are providing liquidity to informed flow.
- **Easy fills are the suspect ones.** A limit entry that fills instantly while the queue imbalance is against you is the adverse-selection case. Don't join a bid when queue imbalance is strongly negative.
- **Inventory changes your fair exit price.** A market maker shades quotes to shed risk as inventory and remaining time grow. For a directional trader, the analogue is to plan exits into liquidity at targets and to cut size into thin books (weekends, midday, post-release).

---

## 9. Testing order-flow strategies

**Data required by setup type:**

| Setup type | Minimum data | Notes |
|---|---|---|
| Footprint / CVD / imbalance rules | Tick trades with **true** aggressor (CME; normalized crypto) or TBBO + Lee-Ready (equities) | Rebuild bars from raw prints with the **same aggregation as the live platform** (per-aggressor event vs per-fill); session-reset CVD |
| DOM pulling/stacking, OFI, queue imbalance | MBP-10 (OFI, MLOFI) or MBO (adds/cancels/modifies by order; iceberg refills) | MBP cannot say *which* order cancelled |
| Any limit-order entry | MBO + queue-position model + latency | Without these, the P&L is fiction |

**Fill and latency rules for honest backtests:**
1. **Market/stop orders:** fill at the opposite best after latency L (e.g. 20–100 ms retail [SC]), walk the book for size, and add slippage in fast-tape events.
2. **Limit orders, conservative:** fill only when price trades **through** your limit.
3. **Limit orders, queue-based (MBO):** join the back of the queue at t + L. Your position improves only as trades print at your price and as orders ahead of you cancel (known exactly by order ID). Fill when the queue ahead is zero and a trade hits your price.
4. **MBP only:** allocate cancels probabilistically. A cancel is attributed to the queue ahead of you with probability f(front)/(f(front) + f(back)), with f(x) = xⁿ, n = 2–3, or log forms. Trades always consume the queue ahead first. The risk-averse variant advances you on trades only [K · SC].
5. **Always record markouts.** Limit-fill backtests that ignore adverse selection overstate P&L.

**hftbacktest approach** [V · VEN] (open source; probability queue-model tutorial): queue models `SquareProbQueueModel` via `power_prob_queue_model(2)`, `LogProbQueueModel2`, `PowerProbQueueModel3(3)`; `no_partial_fill_exchange()`; order latency **replayed from recorded live latency** (`intp_order_latency`); maker-rebate fee model (−0.005% maker, 0.07% taker). The queue model is chosen by **comparing backtest with live fills**, which is the right standard for any limit-order strategy.

**Hindsight and look-ahead illusions:** labelling "absorption", "trapped traders" or "divergence" after the outcome (fix: causal rules on data up to decision time); bar-close information used inside the bar, such as a completed stack or final bar delta (fix: event/tick time, or enter at the next bar's open); education screenshots as survivorship samples (demand every-signal, full-session logs); historical vs live data drift (paper-trade on the live feed); parameter mining over R, stack count, minimum volume and bar type (count trials and deflate, `quant-research-validation.md`).

**Event-study recipe:**
1. Define the event causally, e.g. ≥ 3 stacked buy imbalances at R ≥ 3.0 with minimum volume V_min, within X ticks of a pre-marked level.
2. Measure the forward mid change in ticks at +10 s, +1 m, +5 m and +30 m, signed in the trade direction.
3. Compare with a **matched control**: random timestamps at the same level, time of day and volatility decile.
4. Report mean, median, hit rate, MFE/MAE distributions and **net-of-cost** expectancy per trade.
5. **Cluster standard errors by day**, because events within a day are dependent; the effective n is smaller than the event count.

**Break-even and sample size (math):**
```
Break-even win rate      p* = (S + c) / (T + S)          T target, S stop, c round-trip cost, all in ticks
  T=8, S=6, c=1.3   →    p* = 7.3/14 = 52.1%
  T=4, S=6, c=1.3   →    p* = 7.3/10 = 73.0%             small targets are punished by fixed costs
Win-rate edge δ over p0  n ≈ ((z_α + z_β)·sqrt(p0(1−p0)) / δ)²
  p0=0.5, δ=0.05, 80% power: two-sided (1.96+0.84) → 784 trades; one-sided (1.645+0.84) → 618 trades
Expectancy in R          n ≈ ((z_α + z_β)·σ_R / μ_R)²;   σ_R = 1.2R, μ_R = 0.1R → ≈ 1,129 trades
```
A discretionary setup firing 1–3 times a day needs years of data, or tick replay of many sessions, before sizing up. `tradekit.py expectancy` reports trades for t = 2/3, which is a detection threshold at about 50% power. For 80% power, use the 2.8σ/μ form above.

**Analytics defaults (conventions to expose as arguments, not optimal values):**

| Signal | Default | Basis |
|---|---|---|
| OFI | Δt = 10 s; β refit over 30 min | CKS |
| MLOFI / integrated OFI | M = 5–10 levels; first-PC weights on depth-normalized OFI | Xu et al.; Cont-Cucuringu-Zhang [SC] |
| Queue imbalance | Logistic fit, reported by spread state | Gould-Bonart |
| Micro-price | 10 imbalance buckets, spreads 1–2 ticks, symmetrized | Stoikov [SC] |
| VPIN | n = 50, V = ADV/50, BVC on 1-min bars, trailing σ_ΔP; always cite the Andersen-Bondarenko critique | Easley-López de Prado-O'Hara [Contested] |
| Footprint | R = 3.0, V_min instrument-scaled (ES ~20), stack ≥ 3, session-reset CVD | [PL] |
| Tape speed / markouts | ≥ 3× trailing 5-min median trades/s; markouts at +1 s, +10 s, +60 s | [PL] |
| A-S simulator | γ = 0.1, k = 1.5, A = 140, σ = 2, T = 1, dt = 0.005 | Paper values |

---

## 10. Review checklist and failure modes

**When a user brings an order-flow plan, ask in this order:**
1. Which market, feed and gateway? Is the aggressor side true or inferred, and how was it normalized (§3 table)?
2. Is the location defined before the session, and is the trigger an objective, causal rule?
3. Is the stop at the flow invalidation, with a target at the next liquidity reference and a time stop?
4. What are the costs in ticks, and what is p* = (S + c)/(T + S)? Does the claimed hit rate clear it?
5. How many independent signals has it been tested on, out of sample, with how many parameter variants tried?
6. For limit entries: are there queue and latency models, and markouts?

**Traps to catch:**
- **Delta divergence read as hidden selling** without checking the book. It may be passive adds and cancels (§2).
- **Sign-flipped CVD** from raw Coinbase maker sides or raw Databento `A`/`B` fed to tools expecting buy/sell.
- **Unregulated-venue crypto volume** or single-exchange equity footprints treated like CME data.
- **Footprint mismatch between platforms** blamed on the market when the cause is gateway aggregation or print re-splitting.
- **"300% is the setting"**: it is a convention, not a platform default (Sierra's compare threshold defaults to 0).
- **Trading DOM walls at face value.** Did the size *execute*? Repeated pull-as-price-approaches is a spoofing pattern to recognize and avoid, never to copy.
- **Seconds-horizon signals** (queue imbalance, microprice, OFI) traded stand-alone by a retail trader paying ≥ 1 tick per round trip.
- **Holding swing trades on intraday delta.** The evidence horizon is minutes to hours.
- **VPIN as a crash alarm; DeepLOB or "AI order-book" claims** without out-of-sample, net-of-cost evidence (LOBCAST drop).
- **UOA, sweep or dark-pool alerts as signals.** No evidence; side inferred, open/close unknown, block prints often pre-arranged.
- **Liquidation heatmaps as certainties**; liquidation totals as complete (sampled feeds).
- **Limit-order backtests filled at touch**, or entries using bar-close footprint data inside the bar.
- **20–50-trade samples, or galleries of winners.** Run `tradekit.py expectancy` and quote the t-stat.
- **Any request to spoof, layer, or place orders to move price or trigger stops.** Refuse the technique; explain recognition and the law (CEA §4c(a)(5)(C), `price-action.md` §7).

---

## 11. Toolkit hooks

Run these instead of mental math. Script paths are relative to the skill directory; call each script by its absolute path from a working folder. The outputs below were checked this session.

- **Free crypto tape with true aggressor side:** `python scripts/fetch.py trades BTC --exchange kraken --minutes 60` (or `--exchange coinbase`; defaults kraken, 60 min, `--max 50000`, output `BTC_trades.csv` or `--out`). It writes `time,price,size,side` with side = **aggressor** `buy`/`sell` and prints the buy-aggressor share. The script normalizes both venues: Coinbase `side` is inverted from the maker side; Kraken REST `b`/`s` is treated as the taker side, consistent with Kraken's WS v2 docs (the REST page does not define it). Rows sort by time, then exchange sequence, so a sweep is never re-ordered by price. Both are single **spot** venues; perp CVD needs another source.
- **L2 snapshot:** `python scripts/fetch.py book BTC` (default `--exchange coinbase`, `--depth 100`) writes `side,price,size`; then `python scripts/flowkit.py book BTC_book.csv --wall 5` gives spread, size-weighted mid (not Stoikov's micro-price), depth imbalance (top 1/5/10/20 and within 10/25/50 bps) and resting orders ≥ 5× median, with a spoofing caveat. On small-tick BTC read the bps rows, not top-1/top-5; raise `--depth` if all bps windows read the same.
- **Footprint, delta, CVD:** `python scripts/flowkit.py delta TRADES.csv --bar 1m --tick 0.25`.
  - Defaults: `--bar 5m` (also `30s`, `500t`, `100v`), `--ratio 3`, `--stack 3`, `--lookback 10`, `--min-vol 0.5` (fraction of median bar volume ÷ the number of price levels in the bar), `--show 12`, `--events 15`; `--out bars.csv` writes OHLCV + delta + CVD for techkit. Auto row size = median bar range / 12, rounded: pass `--tick` for futures (ES 0.25). Imbalances are diagonal (ask at P vs bid at P − 1 tick).
  - Flags are bar-level simplifications of §5. *Absorption:* bar volume ≥ 2× lookback average, range ≤ 0.6× average, |delta| ≥ 20% of volume, close against the delta. *Divergence:* new lookback-bar extreme with opposite bar delta *or* CVD below its value at the prior extreme (loose; fires often). *Unfinished auction:* both sides ≥ 0.25× median level volume at a swing extreme. The Summary prints "DIVERGENT (passive side winning)" when net delta and price disagree.
  - **Missing or partial side column → tick-rule fallback with a printed WARNING.** Feed only literal aggressor `buy`/`sell` (§3 flowkit input rule).
- **Volume profile and VWAP:** `python scripts/flowkit.py profile FILE` (`--bins 40`, `--tick`, `--anchor YYYY-MM-DD` for bars, `--last N`, `--show`) gives POC, 70% value area, HVN/LVN and VWAP ±1/2σ; exact from a trades CSV, approximate from OHLCV bars. Use it to mark §6 locations.
- **OFI and queue imbalance:** `python scripts/flowkit.py ofi QUOTES.csv --window 50` needs `time,bid,bid_size,ask,ask_size`, at least 4× window updates, and uses **event** windows (quote updates), not seconds. It reports the CKS impact slope, contemporaneous vs **next-window predictive R²** (the gap is the explain-vs-predict point), last queue imbalance as bid share (0.5 = neutral; I = 2·share − 1), the weighted-mid "microprice" (not Stoikov's Markov micro-price) and the queue-imbalance hit rate. fetch.py does not record quote streams; the user needs their own L1 capture.
- **Expectancy from ticks:** convert with win R = (T − c)/S, loss R = (S + c)/S. `python scripts/tradekit.py expectancy --p 0.57 --win 1.117 --loss 1.217 --trades 200` (T = 8, S = 6, c = 1.3) gives break-even 52.1%, +0.113R, σ 1.16R, 416/935 trades for t = 2/3, t = 1.39 at 200 trades. A 4-tick target (`--win 0.45`) gives break-even 73.0%.
- **Size from the flow stop:** `python scripts/tradekit.py size --equity 50000 --risk 0.5 --entry 5000 --stop 4998.5 --multiplier 50 --target 5002` gives 3 ES contracts, $225 at risk, 1.33R, and a 15× notional warning.
- **Drawdown risk of a scalp profile:** `python scripts/tradekit.py ruin --p 0.57 --b 0.918 --risk 0.5 --trades 500 --limit 10` gives P(drawdown ≥ 10%) ≈ 10% and a median max drawdown of 6.4%.
- **Pipeline:** `fetch.py trades` → `flowkit.py profile` (levels) → `flowkit.py delta --out` (events) → log the signals → `tradekit.py expectancy` / `ruin`.
- **Not in the toolkit:** MBO/queue-position backtesting, VPIN, MLOFI/integrated OFI, Stoikov's micro-price, cross-venue CVD aggregation, perp OI/funding/liquidation feeds. Say so and do these outside the toolkit (hftbacktest for queue fills).

---

## 12. Key sources

- Cont, Kukanov & Stoikov 2014, "The Price Impact of Order Book Events," *J. Fin. Econometrics* 12(1) — https://arxiv.org/abs/1011.6402
- Xu, Gould & Howison 2019, multi-level OFI [WP] — https://arxiv.org/abs/1907.06230 ; Cont, Cucuringu & Zhang, integrated OFI and cross-impact [WP] — https://arxiv.org/abs/2112.13213
- Gould & Bonart, queue imbalance [WP; *MML* 2016] — https://arxiv.org/abs/1512.03492 ; Stoikov 2018, "The Micro-Price," *Quant. Finance* 18(12) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2970694
- Lillo & Farmer 2004, long memory of order flow — https://arxiv.org/abs/cond-mat/0311053 ; Tóth, Palit, Lillo & Farmer 2015, *JEDC* 51; Bouchaud, Gefen, Potters & Wyart 2004, *Quant. Finance* 4(2) (propagator)
- Dufour & Engle 2000, "Time and the Price Impact of a Trade," *J. Finance* 55(6)
- Easley, López de Prado & O'Hara 2012, VPIN, *RFS* 25(5); Andersen & Bondarenko 2014, *J. Financial Markets* 17 (critique)
- Zhang, Zohren & Roberts 2019, DeepLOB, *IEEE TSP* 67(11) — https://arxiv.org/abs/1808.03668 ; Prata et al. 2023, LOBCAST [WP] — https://arxiv.org/abs/2308.01915
- Evans & Lyons 2002, "Order Flow and Exchange Rate Dynamics," *JPE* 110(1) — https://www.nber.org/papers/w7317 ; Evans & Lyons 2005, *AER* 95(2); Menkhoff et al. 2016, *J. Finance* 71(2)
- Pan & Poteshman 2006, "The Information in Option Volume for Future Stock Prices," *RFS* 19(3) — https://www.nber.org/papers/w10925
- Avellaneda & Stoikov 2008, "High-Frequency Trading in a Limit Order Book," *Quant. Finance* 8(3) — https://www.math.nyu.edu/~avellane/HighFrequencyTrading.pdf
- Aquilina, Budish & O'Neill 2022, latency arms race, *QJE* 137(1); Budish, Cramton & Shim 2015, *QJE* 130(4)
- Lee & Ready 1991, *J. Finance* 46(2); Barber, Huang, Jorion, Odean & Schwarz 2024, retail flow in TAQ, *J. Finance* 79(4)
- Sierra Chart Numbers Bars [VEN] — https://www.sierrachart.com/index.php?page=doc/NumbersBars.php ; NinjaTrader 8 Volumetric Bars [VEN] — https://static.ninjatrader.com/support/helpGuides/nt8/order_flow_volumetric_bars2.htm
- Databento schemas and side/action enums [DOC] — https://databento.com/docs/schemas-and-data-formats ; https://databento.com/docs/standards-and-conventions/common-fields-enums-types
- Coinbase Exchange WebSocket channels [DOC] — https://docs.cdp.coinbase.com/exchange/websocket-feed/channels ; Kraken WS v2 trade [DOC] — https://docs.kraken.com/api/docs/websocket-v2/trade ; Binance spot market data [DOC] — https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints
- hftbacktest probability queue models [VEN] — https://hftbacktest.readthedocs.io/en/latest/tutorials/Probability%20Queue%20Models.html
- Alexander, Choi, Park & Sohn 2020, BitMEX price discovery, *J. Futures Markets* 40(1); Cong, Li, Tang & Yang 2023, crypto wash trading, *Management Science* — https://nber.org/papers/w30783
