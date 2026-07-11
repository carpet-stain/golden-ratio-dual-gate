"""Portfolio backtest engine: applies the dual-gate regime to the sleeve's
target weights, rebalancing quarterly or immediately on a regime flip, with
a trading cost charged on realized turnover. See docs/strategy.md.
"""
from __future__ import annotations

import pandas as pd

RISK_ON_WEIGHTS = {
    "UPRO": 0.50,
    "SPMO": 0.10,
    "VBR": 0.10,
    "DBMF": 0.10,
    "GLD": 0.10,
    "TLT": 0.10,
}
RISK_OFF_WEIGHTS = {
    "UPRO": 0.00,
    "SPMO": 0.20,
    "VBR": 0.20,
    "DBMF": 0.20,
    "GLD": 0.20,
    "TLT": 0.20,
}
TICKERS = list(RISK_ON_WEIGHTS)
TRADING_COST = 0.001  # 0.1% of traded notional, matching the published backtest


def target_weights(risk_on: bool) -> dict[str, float]:
    return RISK_ON_WEIGHTS if risk_on else RISK_OFF_WEIGHTS


def _quarter_end_dates(index: pd.DatetimeIndex) -> set[pd.Timestamp]:
    """Last available trading date in each calendar quarter present in
    `index` -- the fixed rebalance schedule, on top of regime-flip
    rebalances."""
    by_quarter = pd.Series(index, index=index.to_period("Q"))
    return set(by_quarter.groupby(level=0).max())


def run_backtest(returns: pd.DataFrame, regime: pd.Series) -> pd.Series:
    """`returns`: daily return frame with columns backtest.TICKERS.
    `regime`: daily bool series (True=risk-on), already signal-delayed.

    Returns the daily portfolio return series, net of trading costs.
    """
    idx = returns.index.intersection(regime.index)
    if len(idx) == 0:
        raise ValueError("no overlapping dates between returns and regime")
    returns = returns.loc[idx, TICKERS]
    regime = regime.loc[idx]
    quarter_marks = _quarter_end_dates(idx)

    weights = pd.Series(target_weights(regime.iloc[0]), index=TICKERS)
    prev_regime = regime.iloc[0]
    portfolio_returns = []

    for date in idx:
        day_regime = regime.loc[date]
        if (date in quarter_marks) or (day_regime != prev_regime):
            new_weights = pd.Series(target_weights(day_regime), index=TICKERS)
            cost = (new_weights - weights).abs().sum() * TRADING_COST
            weights = new_weights
        else:
            cost = 0.0

        day_returns = returns.loc[date]
        portfolio_return = (weights * day_returns).sum() - cost
        portfolio_returns.append(portfolio_return)

        drifted = weights * (1 + day_returns)
        weights = drifted / drifted.sum()
        prev_regime = day_regime

    return pd.Series(portfolio_returns, index=idx, name="portfolio")
