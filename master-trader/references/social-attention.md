# Social Media Trends, Online Attention and Markets

*Read when: a user asks whether Reddit/WallStreetBets, X/Twitter, StockTwits, Telegram, TikTok/YouTube finfluencers, Google searches or Wikipedia views predict prices; wants to trade a "trending", meme or squeeze stock or coin; is building a buzz, attention or sentiment feature, filter or sizing rule; or asks whether to chase or fade a social-media spike or a pump.*

Tags: [Strong] replicated/consensus · [Moderate] peer-reviewed, limited replication · [Weak] thin, short sample, working paper or secondary · [Contested] credible sources disagree · [Lore] practitioner wisdom or our own inference, untested. (WP) = working-paper figure; (press) = figure seen only in press coverage. Effects are per one standard deviation (SD) of the signal unless stated; bp = basis points. Research current to Nov 2026.

**Contents:** 1 Core findings · 2 Attention → returns · 3 Lead or lag · 4 Attention → volume and volatility · 5 Sentiment → returns, by platform · 6 Finfluencers · 7 Trend dynamics: level, velocity, spread, early vs peak · 8 Meme-stock episodes and squeezes · 9 Crypto · 10 FX and macro · 11 Signal construction that holds up · 12 Pitfalls · 13 What this means for a learned attention filter · 14 Key sources

---

## 1. Core findings

- **Attention forecasts volume and volatility much better than direction.** Searches, message counts and tweet counts lead turnover and realized volatility in stocks, crypto and FX, even after controls for lagged volatility (Antweiler & Frank 2004; Andrei & Hasler 2015; Jiao, Veiga & Walther 2020; Shen, Urquhart & Wang 2019; Goddard, Kita & Wang 2015) [Strong].
- **Abnormal attention brings brief price pressure, then reversal,** concentrated in small, retail-held, hard-to-arbitrage names. The smaller third of the Russell 3000 earned ~11 bp/week for two weeks after a search surge, reversed within a year (Da, Engelberg & Gao 2011, WP figure) [Strong in-sample]. Whether that positive leg survived after publication is [Contested].
- **After publication, the negative leg held up better.** In S&P 500 stocks 2008-13, high search predicted lower next-week returns (Bijl et al. 2016). In 2012-21, StockTwits attention predicted −14 bp the next day per SD, and Google abnormal search was also negative (Cookson, Lu, Mullins & Niessner 2024). Robinhood herding into the day's most-bought stocks was followed by −4.7% over 20 days (Barber, Huang, Odean & Schwarz 2022) [Moderate]. For longs, treat a spike as reversal risk.
- **Tone and volume are different signals.** About two-thirds of firm-day attention is common across StockTwits, X and Seeking Alpha. Sentiment barely correlates across them (0.04-0.13). Sentiment predicts +2 to +8 bp the next day per SD; attention predicts a negative return (Cookson et al. 2024) [Moderate]. Average attention across sources, but never average sentiment.
- **Crowd signals die when the crowd arrives.** WallStreetBets due-diligence posts predicted returns before the January 2021 GameStop squeeze and not after (Bradley, Hanousek, Jame & Xiao 2024). StockTwits sentiment's 11 bp next-day edge went to about zero after GME, driven by new users (Cookson et al. 2024) [Moderate]. Published anomalies lose ~58% after publication (McLean & Pontiff 2016) [Strong].
- **Social trends lead price more often in micro/small caps and altcoins than in large caps or Bitcoin,** and much of that "lead" is promotion that reverses within days (Leung & Ton 2015; Renault 2017 WP; Xu & Livshits 2019; Li, Shin & Wang 2025) [Moderate]. In large caps and BTC, social activity mostly moves with volatility (Behrendt & Schmidt 2018; Shen et al. 2019) [Moderate].
- **Most finfluencers have negative skill, and the worst ones have the most followers.** On StockTwits, 56% are antiskilled (−2.3%/month) and 28% skilled (+2.6%/month); trading against them earned 1.2%/month out of sample (Kakhbod, Kazempour, Livdan & Schürhoff, WP) [Moderate].
- **Much attention is a reaction, not a cause.** Volatility and volume drive next-day Bitcoin searches (Urquhart 2018), and institutional (Bloomberg) attention leads retail (Google) attention (Ben-Rephael, Da & Israelsen 2017) [Moderate]. A spike the day after a big move is mostly already priced.
- **Best use is as a regime and risk overlay** (size, stop width, which side to favour), not as a stand-alone signal. Published return effects (2-14 bp/day, ~11 bp/week) are below small-cap round-trip costs; Bijl et al.'s strategy was profitable gross but not net [Moderate].

---

## 2. Attention → returns

| Study | Sample | Measure | Effect | Horizon | Grade |
|---|---|---|---|---|---|
| Da, Engelberg & Gao 2011 *JF* | Russell 3000, 2004-08, weekly | ASVI = log SVI_t − log median(SVI_t−1..t−8), ticker searches | Smaller third: high- minus low-ASVI ≈ +11 bp/week (≈5.7%/yr); nothing in large caps | +2 weeks, fully reversed within a year (WP) | [Strong] in-sample |
| Da et al. 2011, IPOs | 181 IPOs 2004-07 | name searches | Median SVI +80% in IPO week; big pre-IPO search jump ≈ +7% first-day return, then long-run underperformance | 1 day / 1 year | [Moderate] |
| Joseph, Wintoki & Zhang 2011 *IJF* | S&P 500, 2005-08 | ticker SVI | Predicts abnormal returns and volume; return sensitivity rises with difficulty of arbitrage | weeks | [Moderate] |
| Bijl, Kringhaug, Molnár & Sandvik 2016 *IRFA* | 431 S&P 500 firms, 2008-13 | company-name SVI | High search → low returns; strategy profitable before costs, not after | 1 week | [Moderate] |
| Kim, Lučivjanská, Molnár & Villa 2019 *FRL* | Oslo large caps | SVI | No return predictability; predicts volume and volatility | days-weeks | [Moderate] |
| Cookson et al. 2024 *JFE* | US, 2012-21, daily | Google ASVI; StockTwits/X/Seeking Alpha message counts | ASVI negative; StockTwits attention −14 bp/SD; X and SA attention not significant | next day | [Moderate] |
| Barber et al. 2022 *JF* | Robinhood, 2018-20 | jump in number of users holding (herding) | Top stocks bought each day −4.7% abnormal over 20 days (WP: −3% over 5 days, −6% for extreme herding) | 5-20 days | [Moderate] |
| Moat et al. 2013 *Sci Rep* | DJIA, Dec 2007-Apr 2012, weekly | Wikipedia views (DJIA firms, finance topics) | Rising views preceded index falls; page edits carried no signal | 1 week | [Weak] |

- **Mechanism:** individual investors are net buyers of attention-grabbing stocks (news, abnormal volume, extreme one-day returns). To buy, they must choose from thousands of names; to sell, only from what they own (Barber & Odean 2008) [Strong]. Retail attention is buy pressure, so prices rise first and give it back later.
- **Where it lives:** small, low-priced, retail-held, high idiosyncratic volatility, few analysts (Da 2011; Joseph 2011; Gu & Kurov 2020; Cookson 2024) [Moderate].
- **Momentum interaction:** weekly momentum earned ~2.45%/yr more among high-SVI stocks (Da 2011 WP) [Moderate]. Price momentum is stronger in high-volume (high-attention) stocks and up markets and reverses long-run. Earnings momentum (PEAD) is stronger in low-attention stocks, ~64 bp/month apart across volume quintiles (Hou, Peng & Xiong 2009 WP) [Moderate]. Unusually high volume ("visibility") predicts higher returns over the next month (Gervais, Kaniel & Mingelgrin 2001) [Strong].
- **Wikipedia and Google Trends critiques:** Preis, Moat & Stanley (2013) reported a 326% "debt"-keyword Trends strategy (2004-11), and Moat et al. (2013) a Wikipedia sibling. Challet & Bel Hadj Ayed (2013/14) found keywords picked with hindsight, some backtests using keywords from the future, random finance keywords doing no better than random illness keywords, and past returns predicting as well as Trends [Moderate critique]. Treat index-level Wikipedia/Trends timing as [Weak].
- **Decay:** since 2011 the sign is negative (Bijl; Cookson) or zero (Kim). The positive price-pressure leg is [Contested]; "high attention → weaker later returns" is the more robust reading [Moderate]. Haircut any published attention edge by at least half (McLean & Pontiff 2016) [Strong].
- **Costs:** ~11 bp/week of gross edge is smaller than a 20-100 bp small-cap round trip (math on published figures). This is a sizing overlay, not a trade.

---

## 3. Lead or lag

- **Stocks, weekly:** in a VAR, search volume (SVI) leads absolute abnormal returns and news. Lagged turnover and news predict *lower* SVI the next week (spikes mean-revert). Same-week extreme returns, turnover and news explain only ~2.8% of weekly SVI changes, so search spikes are not mere echoes of price at weekly frequency (Da 2011 WP) [Moderate].
- **Institutions first:** Bloomberg-terminal attention (AIA) reacts faster to major news and leads retail Google attention; drift after earnings and recommendation changes comes from news institutions ignored (Ben-Rephael et al. 2017) [Moderate]. Retail search is the late leg.
- **Earnings:** abnormal search rises ~2 weeks before announcements and peaks on the day. High pre-announcement search means more of the news is priced before the announcement, so the reaction is smaller (Drake, Roulstone & Thornock 2012) [Moderate]. Friday announcements get a 15% lower immediate response, a 70% higher delayed response and 8% lower volume (DellaVigna & Pollet 2009) [Strong]. Busy announcement days give weaker immediate price and volume reactions and stronger drift (Hirshleifer, Lim & Teoh 2009) [Strong]. Socially connected areas react more strongly at once, drift less and trade more for longer ("social churning"; Hirshleifer, Peng & Wang 2025) [Moderate].
- **Twitter:** across the 30 DJIA stocks over 15 months, correlation and Granger causality are low. At volume peaks (often earnings), sentiment polarity predicts the direction of a ~1-2% cumulative abnormal return over the following days (Ranco et al. 2015) [Weak]. Message activity correlates *negatively* with same-day returns (Antweiler & Frank 2004).
- **Crypto:** realized volatility and volume drive next-day Bitcoin search (Urquhart 2018). Information flows both ways for up to 6 days, larger from volatility to attention (Aslanidis, Bariviera & López 2022). Price → search → word of mouth → price forms a feedback loop (Garcia et al. 2014) [Moderate].
- **What share of spikes are reactions?** No paper gives a clean share. Working rule: a spike that follows a ≥2-ATR session or scheduled news is reactive and already priced; a spike on a flat price is the candidate leading signal [Lore].

**Where social trends lead price, by asset class**

| Asset | Lead on returns? | Evidence |
|---|---|---|
| US large caps, index ETFs | Rarely; coincident with volatility | Intraday Twitter info for DJIA stocks is statistically significant but economically negligible, with no out-of-sample gain (Behrendt & Schmidt 2018); X and SA attention not significant (Cookson 2024) [Moderate] |
| US small/micro caps | Often. Small caps: some persistent drift; micro caps: pump then reversal | StockTwits attention more informative for small and mid caps (Cookson 2024). ASX HotCopper: bullish small caps beat bearish over days to months with no reversal, no effect in large caps (Leung & Ton 2015). OTC tweet spikes → jump, then sharp reversal within ~1 week (Renault 2017 WP, reversal per secondary summary) [Moderate] |
| BTC, ETH | Attention → next-week returns to 2018; tweets → volume and volatility, not returns | Liu & Tsyvinski 2021; Shen et al. 2019 [Contested] |
| Altcoins | Yes, short-term, pump-shaped | Twitter activity predicts short-term returns of 181 altcoins over 71 days (Steinert & Herff 2018) [Weak]; Telegram pumps (§9) [Moderate] |
| FX majors | No direction; attention → volatility | Goddard et al. 2015 [Moderate] |

---

## 4. Attention → volume and volatility

- **Message boards:** 1.5M Yahoo! Finance and Raging Bull posts on 45 firms (2000): posting activity helps predict volatility; disagreement goes with higher volume; return effects are statistically significant but economically small and reverse the next day (Antweiler & Frank 2004) [Strong].
- **Theory plus evidence:** return variance and risk premia rise with attention and uncertainty. Data support the rising relationship; the predicted quadratic shape is mixed (Andrei & Hasler 2015) [Moderate].
- **Search volume:** searches for index names help forecast realized volatility out of sample (Dimpfl & Jank 2016). Norway: search predicts volume and volatility, not returns (Kim et al. 2019) [Moderate].
- **Social vs news:** news coverage predicts *lower* subsequent volatility and turnover; social-media coverage predicts *higher*, an "echo chamber" effect (Jiao, Veiga & Walther 2020) [Moderate]. Press reports ~+50% volatility and ~+25% volume for a month for the most-discussed stocks [Weak (press)].
- **Disagreement:** StockTwits disagreement predicts abnormal volume; 1 SD of overnight cross-group disagreement ≈ +3.8% abnormal volume (Cookson & Niessner 2020, WP figure) [Moderate]. Users mostly see like-minded posts (echo chambers; Cookson, Engelberg & Mullins 2023) [Moderate].
- **Crypto:** daily Bitcoin tweet counts predict next-day volume and realized volatility, not returns (Shen et al. 2019) [Moderate].
- **Market level:** a FEARS index built from household searches ("recession", "unemployment", "bankruptcy") predicts short-term return reversals, temporary rises in volatility, and fund flows out of equity into bond funds (Da, Engelberg & Gao 2015) [Strong].
- **Implication:** the attention → volatility link is the one to build on. ATR-based stops and sizing already absorb part of it; attention adds information beyond lagged volatility (Andrei & Hasler; Dimpfl & Jank) [Moderate].

---

## 5. Sentiment → returns, by platform

| Platform | Finding | Grade |
|---|---|---|
| X/Twitter | "Calm" mood predicted DJIA moves 2-6 days ahead with 87.6% directional accuracy on a short test (Bollen, Mao & Zeng 2011). The replication found the effect only in the original window; it vanished when the sample was extended to 2007, with no out-of-sample value (Lachanski & Pav 2017). The fund launched to trade it closed in 2012. | [Weak]: treat as [Lore] |
| X/Twitter | Bloomberg firm-level Twitter sentiment predicts next-day returns, more for firms with few analysts (Gu & Kurov 2020). Pre-earnings tweet opinion predicts earnings and announcement returns, more in weak information environments (Bartov, Faurel & Mohanram 2018). +2.2 bp/SD next day (Cookson 2024). | [Moderate] |
| StockTwits | First half-hour sentiment change predicts the last half-hour SPY return, driven by novices, i.e. noise trading (Renault 2017). After the May 2019 limit rose from 140 to 1,000 characters, long posts became more informative (+17.8 bp/SD vs short posts); professionals more informative (Cookson 2024). | [Moderate] |
| Seeking Alpha | 2005-12: +1 percentage point in the share of negative words → −0.38% (articles) and −0.19% (comments) subsequent abnormal returns; also predicts earnings surprises (Chen, De, Hu & Hwang 2014). Highest next-day sentiment loading, +7.8 bp/SD (Cookson 2024). Paid fake promotional articles existed; after the 2017 SEC exposure, readers discounted all articles and the volume response fell, mostly in small firms (Kogan, Moskowitz & Niessner 2023). | [Moderate] |
| Reddit / WallStreetBets | DD buy posts: +1.1% over 2 days, +2% over the next month, ~+5% over the quarter (WP); predictability eliminated after GME (Bradley et al. 2024). Reddit tone predicts retail flows, more when posters are influential; short sellers ride or burst accordingly (Hu, Jones, Li, Zhang & Zhang, WP). | [Moderate] / [Weak] |
| Retail order flow | Routine net retail buying → +10 bp the next week, half from persistence and liquidity provision (Boehmer, Jones, Zhang & Zhang 2021) [Strong]. Robinhood herding hurts liquidity: Robinhood outages lower order imbalance and volatility in high-retail-interest stocks (Eaton, Green, Roseman & Wu 2022) [Moderate]. Routine flow is mildly informed; herding spikes are not. | mixed |
| EU equities | Social-media sentiment has only a transitory effect on excess returns (ESMA 2024) | [Weak] |

- **Reading:** sentiment adds a few bp per day. It is strongest in small or less-covered names, in long-form posts, and before a theme goes viral. It is below retail costs except as a tilt [Moderate].

---

## 6. Finfluencers (X, StockTwits, YouTube, TikTok)

- **StockTwits, 29,000+ finfluencers:** 28% skilled (+2.6%/month abnormal), 16-17% unskilled, 56% antiskilled (−2.3%/month). Unskilled and antiskilled ones have more followers, post more and move retail trading more. Skilled ones are contrarian to returns, sentiment and news; antiskilled ones chase momentum. Trading against them earned 1.2%/month out of sample (Kakhbod et al., SFI WP 23-30) [Moderate].
- **YouTube:** an inverse strategy against video stock calls beat the S&P 500 by ~6.8%/yr but with a lower Sharpe (0.41 vs 0.65); high-conviction calls did better than low-conviction ones but still trailed the index (VideoConviction, Galarnyk et al. 2025, arXiv) [Weak]. A UNSW study built portfolios from finfluencer video transcripts; the median one trailed the S&P 500 by 43 points over a year [Weak (press)]. No clean peer-reviewed TikTok return study was found; TikTok audits by brokers and screeners are not research [Weak].
- **Model evidence:** social trading raises retail losses by ~5.1% while modestly improving market liquidity and efficiency (Bundesbank DP 29/2025) [Weak]. Influencers who link to "fanatics" create bubbles, momentum, volume bursts and reversal; volume and volatility die down faster than the price bubble (Pedersen 2022) [Moderate, theory].
- **Cases:** GME closed +74% (intraday +118%) on 13 May 2024 after Keith Gill's first X post since 2021, then fell ~39-40% on the 7 June 2024 livestream day, alongside a share sale [Strong, fact]. In July 2025, Opendoor ran up after a fund manager's X posts and Kohl's closed +38% on 22 Jul (intraday >100%) on short interest; both gave back double digits within days [Weak (press)]. The SEC charged eight Twitter/Discord influencers in a $100M pump-and-sell scheme (Dec 2022) [Strong, fact].
- **Use:** an influencer post is an attention spike with an antiskilled prior. Never chase it; size down or fade with defined risk. Signs of skill are contrarian, long-form, few-follower posts [Moderate].

---

## 7. Trend dynamics: level, velocity, spread, early vs peak

- **Evidence is thin.** No large study cleanly tests mention *velocity or acceleration* against *level* as return predictors. Say so, and log these as features before acting on them [Weak].
- **Level is mostly size.** High-SVI stocks are bigger (Da 2011); raw counts rank popularity and liquidity. The informative part is the change relative to the stock's own baseline, which is why every robust measure is abnormal (Da's ASVI, Niessner's daily ASVI, Barber's herding = jump in users) [Moderate].
- **Velocity at the extreme is bearish.** Barber et al.'s herding events are one-day jumps in holders, and they predict −4.7% over 20 days [Moderate]. Bitcoin search spikes preceded sharp price declines (Garcia et al. 2014) [Moderate].
- **Early vs peak:**
  - The same WallStreetBets due diligence was informative early (pre-2021) and not at peak virality (Bradley 2024).
  - Sentiment from new, hype-era users lost its information (Cookson 2024).
  - Reddit discussion spreads and fades like a contagion, which explains reversals and bubble shapes (Semenova & Winkler, WP).
  - Regime-switching "mementum" episodes (synchronized buying with social activity) carry positive returns while active (Costola, Iacopini & Santagiustina 2021).
  - Epidemic-style hidden Markov models on Reddit features flagged crypto bubbles (Phillips & Gorse 2017).
  - Grades: Bradley and Cookson [Moderate]; the rest [Weak].
- **Cross-platform spread marks the stage.** Attention is ~67% common across platforms (Cookson 2024), and retail search lags institutional attention (Ben-Rephael 2017). So a theme that starts in a niche (StockTwits, a subreddit, Telegram), spreads to X, Wikipedia and Google, then reaches TV and mainstream press is ageing. Wikipedia and Google spikes are late indicators [Lore built on Moderate pieces].
- **Synthesis:** early stage looks like z rising for 1-3 days, a single source or few, price not yet extended, little mainstream coverage; price pressure is positive [Lore, Moderate pieces]. Peak looks like z ≥ 2-3 on every source, influencer or celebrity posts, record volume and price several ATR above trend; subsequent returns are negative [Moderate].
- **Features worth logging:** Δz over 1-3 days; days since z first crossed 1; breadth (sources with z ≥ 1); late-minus-early (Wikipedia z minus Reddit z); 5-day return in ATR at the spike; short interest [Lore].

---

## 8. Meme-stock episodes and squeezes

- **GME, January 2021:** short interest above 100% of float; the price went from ~$17 to an intraday ~$483 (pre-split) on 28 Jan, when brokers restricted buying. The SEC staff report (Oct 2021) found buy-to-cover added pressure, but the weeks-long rally was sustained by positive sentiment, short covering was not the main driver, and there was no evidence of a gamma squeeze [Strong].
- **Mechanism:** coordinated retail trading discussed on Reddit, X and StockTwits drove the squeezes; bots played no role; market quality worsened for the stocks and their competitors (Allen, Haas, Nowak, Pirovano & Tengulov, *Management Science*) [Moderate].
- **Before / during / after:** before, few but informative posts (Bradley 2024). During, attention, volume and volatility explode, with halts, gaps and limit-up runs. After, signal informativeness collapses (Bradley; Cookson) and attention mean-reverts faster than price (Pedersen 2022) [Moderate]. Later echoes (2024 Gill, 2025 Opendoor/Kohl's) lasted days to weeks [Weak (press)].
- **Squeeze ingredients:** high short interest and days-to-cover, rising borrow fees, call buying and a social catalyst. Payoffs are convex both ways [Lore, consistent with the cases]. Short sellers increase positions after Robinhood herding (Barber 2022), and those positions earn on average [Moderate], but the right tail against a short is unbounded.
- **Ramp-and-dumps:** FINRA, Nasdaq and NYSE flagged small-cap IPOs, mostly foreign issuers, with abnormal post-IPO run-ups and concentrated allocations (FINRA RN 22-25). Promotion runs through WhatsApp, WeChat and Telegram "investment clubs"; the FBI issued an alert in July 2025, and the SEC chair warned about China-linked cases in February 2026 [Strong as a pattern]. A social spike in a sub-$300M recent IPO is a red flag, not a setup.

---

## 9. Crypto

- **Attention predicts returns, in-sample to 2018.** A 1 SD rise in "Bitcoin" Google searches → +1.84% to +2.50% next-week BTC return (figures differ across versions); a rising "Bitcoin hack"/"Bitcoin" search ratio predicts lower returns; Twitter counts also predict (Liu & Tsyvinski 2021) [Moderate]. Post-2018 and post-ETF evidence is weaker [Contested].
- **Bidirectional and bubble-shaped:** prices correlate 0.88 with Google Trends and 0.83 with Wikipedia views (log-log) in the 2013 bubble, with feedback in both directions (Kristoufek 2013). Information flows both ways for up to 6 days, and volatility → attention is the stronger leg (Aslanidis et al. 2022). Price → search → word of mouth → price loops, and search spikes come before crashes (Garcia et al. 2014) [Moderate].
- **Majors:** Bitcoin tweets → volume and realized volatility, not returns (Shen 2019) [Moderate]. **Altcoins:** social activity predicts short-term returns (Steinert & Herff 2018) [Weak].
- **Telegram pump-and-dumps:**
  - 412 pumps (Jun 2018-Feb 2019) from ~100 channels, ~2 pumps/day, ~$6M/month of artificial volume. Targets are predictable: small caps on minor exchanges (Xu & Livshits 2019) [Moderate].
  - Pumps cause brief spikes in price, volume and volatility, then a rapid collapse. Prices rise *before* the announced start, so insiders profit at participants' expense. Exchange policy experiments show pumps reduce liquidity and prices (Li, Shin & Wang 2025) [Strong].
  - 355+ pumps over 7 months on two exchanges; participation is a puzzle explained by gambling and overconfidence (Dhawan & Putniņš 2023) [Moderate].
- **Bots and wash activity:** in 2017, 71% of the authors of suspicious cashtag tweets were bots that promoted low-cap stocks by piggybacking on popular cashtags; 37% were suspended months later (Cresci et al. 2019) [Moderate]. Wash trading averages over 70% of reported volume on unregulated exchanges (Cong, Li, Tang & Yang 2023) [Strong]. Assume crypto mention counts and "social volume" carry farmed engagement.

---

## 10. FX and macro

- **Majors:** Google-search attention moves with, and predicts, FX volatility after macro controls; causality runs mainly from attention to volatility, and attention looks like a priced risk in the currency premium (Goddard, Kita & Wang 2015) [Moderate]. Lagged attention affects currency returns only briefly, at the first lag (Han, Xu & Yin 2018) [Weak]. **No social-attention direction signal for major pairs is worth trading.** Use it as an event and volatility flag [Moderate].
- **Retail FX social networks** amplify the disposition effect (Heimer 2016) [Moderate]. Broker "client sentiment" positioning as a contrarian gauge is [Lore].
- **Market-wide:** the FEARS index → next-day reversal, volatility and flows (Da 2015) [Strong]. Attention-grabbing market events (Dow records, front-page news) lead individuals to sell and predict lower market returns (Yuan 2015) [Moderate]. A Twitter-based Economic Uncertainty index tracks policy uncertainty daily (Baker, Bloom, Davis & Renault) [Moderate as a gauge]. These are regime gauges, not single-asset signals.

---

## 11. Signal construction that holds up

- **Abnormal, not raw:**
  - Da 2011: ASVI_t = log SVI_t − log median(previous 8 weeks).
  - Niessner/Cookson, daily: SVI_t / median(SVI over days t−56..t−35), then the log; this skips the last 5 weeks so a slow build still registers. Cookson also controls 10 daily lags of attention.
  - Medians resist the spikes they are meant to detect [Strong as practice].
- **Counts:** use log(1+x), which is heavy-tailed even after the log; prefer median/MAD z-scores, and set a minimum absolute count before a "spike" can fire (0 → 3 mentions is noise) (math).
- **z-scores vs levels:** a z-score against the asset's own history removes size and popularity; cross-sectional levels mostly rank market cap [Moderate].
- **Day-of-week:** Wikipedia views and finance chatter are weekday-heavy, so a Monday decision that reads Sunday's value sees low z. Use a 7-day sum, or compare each day to the same weekday [Lore (math)].
- **Publication times (look-ahead):**
  - Wikipedia per-article daily views load after the UTC day ends (nominally 00:00 UTC; in practice up to ~24 h). A blank means not loaded, not zero. Use `agent=user`.
  - Google Trends: website non-realtime data runs up to 36-72 h behind and is rescaled 0-100 on every request; the scale uses the window's maximum, which is future information inside a backtest. Concatenate overlapping windows (Cookson used 200-day pulls with a 1-day overlap). The Trends API alpha (Jul 2025) is consistently scaled, ~48 h lag, ~5 years of history, allowlist only.
  - Reddit, X and Bluesky counts are near-real-time but gated by API terms (§12).
- **Same-day vs next-day:** contemporaneous correlations are much stronger than predictive ones (Antweiler & Frank; Ranco; Behrendt & Schmidt). A backtest that lets day-t attention trade day t's close leaks [Strong].
- **Lag:** use the latest fully published day strictly before the decision. Return effects sit at days 1-10 (Cookson next day; Da two weeks; Barber 20 days); volatility effects last weeks (Jiao: about a month). A 2-3 day-old reading still informs volatility, much less direction [Moderate].
- **Long/short asymmetry:** retail attention buys (Barber & Odean), so spikes give upward pressure, then reversal. Longs at a spike buy the pressure late. Shorts at a spike have positive expected value on average (Barber 2022) but face squeezes, borrow recalls, halts and gaps. The two sides need separate treatment [Moderate].
- **Momentum and breakouts:** attention strengthens price momentum and its eventual reversal (Hou, Peng & Xiong; Da 2011), and the high-volume premium (Gervais 2001) favours visible breakouts. A rising z at a fresh breakout is participation; a spike after an extended run is late [Moderate pieces, Lore synthesis]. Drift and PEAD setups do better at *low* attention (DellaVigna & Pollet; Hirshleifer et al.) [Strong].
- **Costs and capacity:** the edges live in small caps with wide spreads and thin depth, so capacity is small. Run `tradekit.py impact` before believing any attention backtest [Moderate].

---

## 12. Pitfalls

- **Ticker and name ambiguity:** Da flagged ~7% of tickers as "noisy" (common words). Cashtags collide ($CAT, $F, $GE, $ALL, $ON, $IT, $SOL). Company names are words (Apple, Shell, Visa). Wikipedia pages move and redirect (Facebook → Meta), disambiguation pages split views, and page moves break histories.
- **Survivorship:** delisted, renamed and merged names lose their social history; studies built on today's index members overstate predictability.
- **Bots, pumps and paid promotion:**
  - Cashtag piggybacking bots (Cresci 2019); Telegram pumps (Xu & Livshits; Li, Shin & Wang); ramp-and-dumps (§8); fake Seeking Alpha articles (Kogan et al. 2023); paid TikTok/YouTube promotion.
  - Wikimedia reclassified traffic after bots evading detection inflated May-June 2025 views; human pageviews were then ~8% lower year on year (Diff, Oct 2025), and AI answers keep cutting traffic. Expect level breaks; z against a trailing window absorbs slow drift, not a step change.
- **Platform changes:**
  - Reddit: Pushshift cut off (2023), paid API ($0.24 per 1,000 calls, 2023), and since Nov 2025 new data-API access needs approval under the Responsible Builder Policy. Secondary sources report further 2026-27 limits, unverified.
  - X: free API ended 2023; pay-per-use is the default since Feb 2026, and legacy Basic plans were migrated from Jun 2026.
  - StockTwits' 2019 character-limit change and the 2020-21 user influx changed what its signal means (Cookson 2024).
  - Each change is a regime break in the series.
- **Multiple testing and keyword choice:** platform × measure × window × threshold × universe × horizon is a large grid. Bollen-style results did not replicate; Preis-style keywords were chosen with hindsight (Challet). Count trials and deflate (`quant-research-validation.md` §3-§4) [Strong].
- **Sentiment classification:** message boards lean bullish; sarcasm, emojis (🚀, 💎🙌) and irony defeat dictionaries. LLM labels help extraction, but models still mistake casual remarks for recommendations (VideoConviction) [Moderate].
- **Rescaled or revised data:** Google Trends re-samples on every request; Wikipedia backfills late days. Store values as they were known at the time, with the fetch timestamp.

---

## 13. What this means for a learned attention filter

Setup assumed: each shadow trade gets a label of normal, rising (z ≥ 1) or spike (z ≥ 2), where z is log(1+value) against the symbol's own trailing 90 days, averaged over sources. The system learns per category whether setups do better or worse at each level and scales size 0.5x-1.5x.

1. **Keep it a regime filter, not a signal.**
   - The strong link is attention → volatility and volume [Strong]; the return link is small, short and sign-unstable [Contested].
   - Expect most learned multipliers to sit near 1.0x. Treat a large learned effect as suspect until it holds out of sample [Moderate].
2. **Make it side-aware: yes.**
   - Prior evidence points opposite ways for the two sides: for longs, a spike means late, pressure-driven entry and reversal risk [Moderate]; for shorts, a spike has a positive mean but a fat right tail (squeezes, halts, borrow) [Moderate].
   - Pooling the sides cancels the effects and teaches nothing. Learn per category × side × level.
   - Hard rule: shorts at spike never scale above 1.0x, whatever the learner says, unless risk is defined (a long put or put spread) [Lore, from the §8 cases].
3. **Lag: strictly before the decision, as known then.**
   - Use the latest fully published day before the decision: Wikipedia's UTC day once loaded (treat blanks as missing), Reddit, Bluesky and X counts for the prior UTC day [Strong for the look-ahead principle].
   - Drop readings older than ~2-3 trading days for return use. A source that lags 30 days (some free crypto social-volume tiers) cannot feed a live filter; use it only for research.
   - Record the z the decision actually saw on the shadow trade; never recompute it later from backfilled data.
4. **Window and statistics:**
   - 90 calendar days (~62 sessions) is sensible: longer than Da's 8 weeks, and it covers a quarter. Keep the 30-day minimum.
   - Switch to median/MAD, and deseasonalize by weekday (7-day sums, or same-weekday baselines) [Lore (math)].
   - For sparse count sources, raise the SD floor from 0.05 to ~0.25-0.30 in log1p units, and require a minimum raw count (for example ≥5-10 mentions/day) before rising or spike can fire. Otherwise 0 → 3 mentions reads as a spike (math).
5. **Thresholds:**
   - z ≥ 1 and z ≥ 2 are fine as bucket edges. Under fat tails, expect ~10-15% of days at or above 1 and ~4-6% at or above 2 per source; check that on your data.
   - Spike buckets will be small: 5% of 300 trades is 15. Require ≥30 trades in a bucket before it can move size, and shrink toward 1.0x (empirical Bayes) [Strong, statistics].
   - Consider an **extreme** bucket at z ≥ 3, or the top 0.5% (Barber's herding tail): no new longs, as a fixed rule rather than a learned one [Moderate].
   - Consider a **quiet** bucket at z ≤ −1: drift and PEAD-style setups do better under inattention [Strong].
   - Averaging z across sources dilutes a single-platform spike. Also log the maximum z and the breadth (sources with z ≥ 1) [Lore].
6. **Horizons:**
   - Swing trades (≤30 sessions) sit right on the documented windows: pressure for 1-2 weeks, reversal by 20 days (Barber), Robinhood −4.7% over 20 days, volatility elevated for ~a month. Label at the signal date, as now [Moderate].
   - Expect the clearest effect in long swing setups in small caps and altcoins at spike (worse) [Moderate].
   - Day trades: a daily lagged z is a coarse "in play" marker that overlaps with relative volume. Outcomes measured in R already normalize for volatility, so the learned effect will be small. Use attention only to *reduce* size or skip gap-and-go longs at spike in micro caps, never to upsize [Moderate/Lore].
7. **Scaling range:**
   - Make 0.5x-1.5x asymmetric. Allow downsizing as soon as a bucket clears the ≥30-trade bar with a shrunk effect below 1.0x.
   - Allow upsizing only with ≥50 trades and t ≥ 2 after shrinkage, capped at 1.25x for rising and 1.0x for spike [Lore; estimation-error logic as in Kelly haircuts, `risk-sizing-execution.md` §2.3].
   - ATR sizing already cuts size when volatility jumps; do not count that twice.
8. **What to expect by asset class:**

| Class | Expected learned effect | Notes |
|---|---|---|
| US mega/large caps, index and sector ETFs | ~1.0x; spikes mean wider ranges, not direction | Wikipedia is the most useful source; Reddit and Bluesky mentions are noisy and always high for megacaps [Moderate] |
| US small/mid caps | Longs at spike worse (reversal within weeks); rising + fresh breakout maybe better | Exclude or hard-cap micro caps and recent small IPOs at spike: pump and ramp risk [Moderate] |
| Foreign exchange-listed stocks | Weak with English sources | Local attention lives in local-language Wikipedia and forums; Norway shows volume and volatility only [Moderate] |
| BTC, ETH | Mild: in-sample positive next week to 2018, now mostly volatility | Bidirectional; spikes after crashes are reactions [Contested] |
| Altcoins | Longs at spike clearly worse | Pumps, bots, wash engagement [Moderate] |
| FX majors, futures | ~1.0x; use as a volatility and event flag only | No direction evidence worth sizing on [Moderate] |

9. **Guard against fooling yourself.** Categories × sides × levels are trials. Report each learned multiplier with its standard error and trade count. Re-check after platform or API changes (Reddit 2023/2025, X 2026, Wikimedia bot reclassification 2025), and freeze learning across a known series break [Strong].
10. **Next tests, logged as features before they are used:**
    - Δz over 1-3 days (velocity), breadth, and Wikipedia-minus-Reddit z (late vs early).
    - A reaction flag: the prior session moved ≥2 ATR.
    - Price extension at the spike, and short interest for shorts.
    - Per-platform sentiment, kept separate and never averaged.
    - Promote any of these only if it beats the level bucket out of sample [Lore].

---

## 14. Key sources

- Da, Engelberg & Gao (2011), "In Search of Attention", *JF* 66(5): 1461-1499. WP: https://conference.nber.org/confer/2009/mms09/Da_Engelberg_Gao.pdf
- Da, Engelberg & Gao (2015), "The Sum of All FEARS", *RFS* 28(1): 1-32. https://www3.nd.edu/~pgao/papers/FEARS_20131007.pdf
- Barber & Odean (2008), "All That Glitters", *RFS* 21(2): 785-818. doi:10.1093/rfs/hhm079
- Barber, Huang, Odean & Schwarz (2022), "Attention-Induced Trading and Returns: Evidence from Robinhood Users", *JF* 77(6). SSRN 3715077
- Cookson, Lu, Mullins & Niessner (2024), "The Social Signal", *JFE*. https://runi.ac.il/media/bolmq0ci/the-social-signal.pdf
- Cookson & Niessner (2020), "Why Don't We Agree?", *JF* 75(1): 173-228. https://ideas.repec.org/a/bla/jfinan/v75y2020i1p173-228.html
- Cookson, Engelberg & Mullins (2023), "Echo Chambers", *RFS* 36(2)
- Bradley, Hanousek, Jame & Xiao (2024), "Place Your Bets?", *RFS* 37(5): 1409-1459. https://ideas.repec.org/a/oup/rfinst/v37y2024i5p1409-1459..html
- Chen, De, Hu & Hwang (2014), "Wisdom of Crowds", *RFS* 27(5): 1367-1403. doi:10.1093/rfs/hhu001
- Kogan, Moskowitz & Niessner (2023), "Social Media and Financial News Manipulation", *Review of Finance*
- Renault (2017), "Intraday Online Investor Sentiment and Return Patterns in the U.S. Stock Market", *JBF* 84: 25-40. https://econpapers.repec.org/RePEc:eee:jbfina:v:84:y:2017:i:c:p:25-40 ; Renault (2017 WP), "Market Manipulation and Suspicious Stock Recommendations on Social Media"
- Antweiler & Frank (2004), "Is All That Talk Just Noise?", *JF* 59(3): 1259-1294. https://wernerantweiler.ca/public/noise-a.pdf
- Andrei & Hasler (2015), "Investor Attention and Stock Market Volatility", *RFS* 28(1): 33-72
- Jiao, Veiga & Walther (2020), "Social Media, News Media and the Stock Market", *JEBO* 176: 63-90. doi:10.1016/j.jebo.2020.03.002
- Bollen, Mao & Zeng (2011), "Twitter Mood Predicts the Stock Market". https://arxiv.org/abs/1010.3003 ; Lachanski & Pav (2017), *Econ Journal Watch* 14(3): 302-345. https://econjwatch.org/articles/shy-of-the-character-limit-twitter-mood-predicts-the-stock-market-revisited
- Gu & Kurov (2020), "Informational Role of Social Media: Evidence from Twitter Sentiment", *JBF*; Bartov, Faurel & Mohanram (2018), *Accounting Review* 93(3)
- Behrendt & Schmidt (2018), "The Twitter Myth Revisited", *JBF* 96: 355-367
- Ranco et al. (2015), "The Effects of Twitter Sentiment on Stock Price Returns", *PLoS ONE*. doi:10.1371/journal.pone.0138441
- Moat et al. (2013), *Sci Rep* 3:1801. doi:10.1038/srep01801 ; Preis, Moat & Stanley (2013), *Sci Rep* 3:1684. doi:10.1038/srep01684
- Challet & Bel Hadj Ayed (2013/14). https://arxiv.org/abs/1307.4643 ; https://arxiv.org/abs/1403.1715
- Bijl et al. (2016), *IRFA* 45: 150-156. https://ideas.repec.org/a/eee/finana/v45y2016icp150-156.html ; Kim et al. (2019), *FRL* 28: 208-220. https://ideas.repec.org/a/eee/finlet/v28y2019icp208-220.html
- Joseph, Wintoki & Zhang (2011), *IJF* 27(4); Dimpfl & Jank (2016), *European Financial Management* 22(2); Drake, Roulstone & Thornock (2012), *JAR* 50(4)
- McLean & Pontiff (2016), "Does Academic Research Destroy Stock Return Predictability?", *JF* 71(1). doi:10.1111/jofi.12365
- DellaVigna & Pollet (2009), *JF* 64(2): 709-749. https://www.nber.org/papers/w11683 ; Hirshleifer, Lim & Teoh (2009), *JF* 64(5): 2289-2325
- Ben-Rephael, Da & Israelsen (2017), "It Depends on Where You Search", *RFS* 30(9): 3009-3047
- Hirshleifer, Peng & Wang (2025), "News Diffusion in Social Networks and Stock Market Reactions", *RFS* 38(3): 883-937. https://www.nber.org/papers/w30860
- Hou, Peng & Xiong (2009 WP), "A Tale of Two Anomalies". https://www.princeton.edu/~wxiong/papers/momentum.pdf ; Gervais, Kaniel & Mingelgrin (2001), *JF* 56(3)
- Boehmer, Jones, Zhang & Zhang (2021), "Tracking Retail Investor Activity", *JF* 76(5): 2249-2305 ; Eaton, Green, Roseman & Wu (2022), *JFE* 146(2): 502-528
- Leung & Ton (2015), *JBF* 55: 37-55. https://ideas.repec.org/a/eee/jbfina/v55y2015icp37-55.html
- Kakhbod, Kazempour, Livdan & Schürhoff, "Finfluencers", SFI WP 23-30. https://ideas.repec.org/p/chf/rpseri/rp2330.html
- Galarnyk et al. (2025), "VideoConviction". https://arxiv.org/abs/2507.08104 ; Russ (2025), Bundesbank DP 29/2025
- Pedersen (2022), "Game On: Social Networks and Markets", *JFE* 146(3): 1097-1119. doi:10.1016/j.jfineco.2022.05.002
- Semenova & Winkler, "Social Contagion and Asset Prices: Reddit's Self-Organised Bull Runs". https://arxiv.org/abs/2104.01847 ; Costola, Iacopini & Santagiustina (2021), *Economics Letters* 207: 110021
- Allen, Haas, Nowak, Pirovano & Tengulov, "Squeezing Shorts Through Social Media Platforms", *Management Science*. doi:10.1287/mnsc.2023.02887
- Hu, Jones, Li, Zhang & Zhang (WP), "The Rise of Reddit". https://www.abfer.org/media/abfer-events-2024/annual-conference/papers-investment/AC24P3076-The-Rise-of-Reddit-How-Social-Media-Affects-Belief-Formation-and-Price-Discovery.pdf
- SEC Staff, "Staff Report on Equity and Options Market Structure Conditions in Early 2021" (Oct 2021), sec.gov ; FINRA Regulatory Notice 22-25. https://www.finra.org/rules-guidance/notices/22-25
- Liu & Tsyvinski (2021), "Risks and Returns of Cryptocurrency", *RFS* 34(6): 2689-2727. https://www.nber.org/system/files/working_papers/w24877/w24877.pdf
- Kristoufek (2013), *Sci Rep* 3:3415. doi:10.1038/srep03415 ; Garcia et al. (2014), *J R Soc Interface*. https://arxiv.org/abs/1408.1494
- Urquhart (2018), *Economics Letters* 166: 40-44 ; Shen, Urquhart & Wang (2019), *Economics Letters* 174: 118-122 ; Aslanidis, Bariviera & López (2022), *FRL* 47
- Steinert & Herff (2018), *PLoS ONE*. doi:10.1371/journal.pone.0208119 ; Phillips & Gorse (2017), IEEE SSCI: 394-400
- Xu & Livshits (2019), USENIX Security. https://arxiv.org/abs/1811.10109 ; Li, Shin & Wang (2025), *JFQA* 60(8): 3622-3659. doi:10.1017/S0022109025000201 ; Dhawan & Putniņš (2023), *Review of Finance* 27(3): 935-975
- Cresci et al. (2019), "Cashtag Piggybacking", *ACM TWEB*. https://arxiv.org/abs/1804.04406 ; Cong, Li, Tang & Yang (2023), "Crypto Wash Trading", *Management Science*
- Goddard, Kita & Wang (2015), *JIFMIM* 38: 79-96 ; Han, Xu & Yin (2018), *Economic Modelling* 68: 644-660 ; Heimer (2016), *RFS* 29(11) ; Yuan (2015), *JFE* 116(3)
- ESMA (2024), "Social Media Sentiment Influence on EU Equity Prices". https://www.esma.europa.eu/sites/default/files/2024-04/ESMA50-524821-3157_Risk_Article_Social_Media_sentiment_influence_on_EU_equity_prices.pdf
- Data plumbing:
  - Wikimedia Analytics API (load timing): https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/documentation/troubleshooting.html
  - Wikimedia Diff, "New User Trends on Wikipedia" (17 Oct 2025): https://diff.wikimedia.org/2025/10/17/new-user-trends-on-wikipedia/
  - Google Trends API alpha (Jul 2025): https://developers.google.com/search/blog/2025/07/trends-api
  - Google Trends FAQ: https://support.google.com/trends/answer/4365533
  - X API pricing: https://docs.x.com/x-api/getting-started/pricing
  - Reddit Responsible Builder Policy, r/redditdev (Nov 2025)
