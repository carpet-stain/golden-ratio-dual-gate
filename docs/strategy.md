# Strategy: SPY/TIP Dual-Gate Golden Ratio Portfolio

## Summary

Two-state portfolio that runs 3x leveraged S&P 500 exposure when a dual
trend/canary signal confirms risk-on, and de-levers into an unleveraged
five-asset risk-parity-style sleeve otherwise. Adapted from u/confettofetti's
[r/LETFs post](https://old.reddit.com/r/LETFs/comments/1upw0hu/17x_golden_ratio_inspired_portfolio_using_spy_tip/)
(2026-07-07), itself adapting Risk Parity Radio's Golden Ratio Portfolio and
a TIP-canary signal from u/ApolloDan.

## Signal

Two 200-day SMA trend filters, computed on adjusted-close (dividend-adjusted)
price series:

- **SPY filter**: SPY price vs. its 200-day SMA, ±0.5% band
- **TIP filter**: TIP price vs. its 200-day SMA, ±0.1% band — tightened from
  an initial ±0.5%. TIP's volatility is low enough that a 0.5% band is
  disproportionately wide relative to its own price movement; the tighter
  band doesn't change headline returns much but does increase trade
  frequency (~4/yr → ~6/yr).

**Regime:**

- **Risk-on** requires BOTH SPY and TIP above their (banded) 200 SMA.
- **Risk-off** triggers if EITHER SPY or TIP is below its (banded) 200 SMA.

These are logically equivalent (De Morgan's), but worth stating both — the
original post's allocation table initially read as AND-for-risk-off and had
to be corrected to OR-for-risk-off after a reader caught the ambiguity. See
`research-notes.md` for why this is a reminder to verify our own
implementation, not just trust the spec.

Signal executes with a 1-day delay: act the day after an SMA cross is
confirmed, not same-day.

## Allocations

**Risk-off sleeve** (equal-weight, all five held at all times regardless of
regime):

| Role               | Ticker (US) | Ticker (UK) | Weight |
| ------------------ | ----------- | ----------- | ------ |
| Large Cap Momentum | SPMO        | IUMF        | 20%    |
| Small Cap Value    | VBR         | USSC        | 20%    |
| Managed Futures    | DBMF        | DBMG        | 20%    |
| Gold               | GLD         | SGLN        | 20%    |
| LT Treasuries      | TLT         | IDGA        | 20%    |

**Risk-on allocation** (only when both filters confirm risk-on):

| Role               | Ticker (US) | Weight |
| ------------------ | ----------- | ------ |
| 3x S&P 500         | UPRO        | 50%    |
| Large Cap Momentum | SPMO        | 10%    |
| Small Cap Value    | VBR         | 10%    |
| Managed Futures    | DBMF        | 10%    |
| Gold               | GLD         | 10%    |
| LT Treasuries      | TLT         | 10%    |

Risk-on and risk-off share the same five diversifiers at different weights,
by design — a regime flip only trades the UPRO leg, which limits whipsaw
cost.

## Rebalancing

Quarterly, or immediately on a regime flip, whichever comes first. Author
reports monthly/yearly rebalancing doesn't materially change results.

## Rationale

- **SPY 200 SMA** — standard lagging trend filter (Meb Faber-style). Cuts
  drawdowns and volatility drag by de-levering once negative trend is
  confirmed.
- **TIP 200 SMA** — a "canary," a leading rather than lagging signal.
  Published basis: bond momentum tends to lead equity returns, and TIPS
  additionally embed inflation expectations (Keller's protective/canary
  asset allocation research). Intended to catch some selloffs before the
  lagging SPY filter would.
- **Shared risk-off sleeve on both sides** — when either filter is a false
  positive, the portfolio isn't sitting in cash, it's sitting in an
  already-reasonable unlevered risk-parity-style portfolio. Being wrong is
  cheap.

## Backtest (as published, 1989–now, Testfolio, 0.1% trading cost, 1-day

signal delay)

|          | CAGR  | MDD   | Longest DD | Sharpe | Sortino |
| -------- | ----- | ----- | ---------- | ------ | ------- |
| S&P 500  | 11.5% | 55.1% | 6.6yr      | 0.53   | 0.75    |
| Strategy | 17.2% | 36.6% | 3.2yr      | 0.75   | 1.05    |

~4-6 trades/year. See `research-notes.md` for why these headline numbers
should not be taken at face value.

## Source

- [Original r/LETFs post][letfs-post] — u/confettofetti
- [Risk Parity Radio: Golden Ratio Portfolio](https://www.riskparityradio.com/portfolios)
- [Portfolio Charts: Golden Ratio Portfolio](https://portfoliocharts.com/2025/03/15/beautiful-constants-and-the-golden-ratio-portfolio/)
- u/ApolloDan's ["Adding TIP as a canary filter"][apollodan-canary] post (the direct inspiration)

[letfs-post]: https://old.reddit.com/r/LETFs/comments/1upw0hu/17x_golden_ratio_inspired_portfolio_using_spy_tip/
[apollodan-canary]: https://www.reddit.com/r/LETFs/comments/1ucnaxs/adding_tip_as_a_canary_filter/
