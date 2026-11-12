---
tags: [master-trader]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

ok so I finally found a winner. I backtested an RSI + moving average crossover system on BTC daily candles from 2021 to 2024 and optimized it — tried about 200 different combos of RSI length, oversold level and MA lengths. The best one has a Sharpe of 2.1, 4 years of daily data (crypto trades every day so ~1460 bars), skew around -0.8 and kurtosis around 7. Max drawdown in the backtest was only 18%. I want to go live with 3x leverage on perps next week. Is this real? What would you do? Write your verdict to verdict.md.
