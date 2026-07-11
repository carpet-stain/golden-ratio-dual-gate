"""Performance metrics matching the published backtest's headline table
(docs/strategy.md): CAGR, max drawdown, longest drawdown, Sharpe, Sortino.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

TRADING_DAYS_PER_YEAR = 252


def cagr(returns: pd.Series) -> float:
    growth = (1 + returns).prod()
    years = len(returns) / TRADING_DAYS_PER_YEAR
    return growth ** (1 / years) - 1


def max_drawdown(returns: pd.Series) -> float:
    wealth = (1 + returns).cumprod()
    peak = wealth.cummax()
    drawdown = wealth / peak - 1
    return drawdown.min()


def longest_drawdown_years(returns: pd.Series) -> float:
    """Longest continuous stretch, in years, spent below a prior wealth
    peak. A drawdown still underwater at the end of the series counts
    through the last available date."""
    wealth = (1 + returns).cumprod()
    peak = wealth.cummax()
    underwater = wealth < peak

    longest_days = 0
    current_days = 0
    for is_underwater in underwater:
        current_days = current_days + 1 if is_underwater else 0
        longest_days = max(longest_days, current_days)

    return longest_days / TRADING_DAYS_PER_YEAR


def sharpe(returns: pd.Series, risk_free: pd.Series | float = 0.0) -> float:
    excess = returns - risk_free
    return excess.mean() / excess.std() * np.sqrt(TRADING_DAYS_PER_YEAR)


def sortino(returns: pd.Series, risk_free: pd.Series | float = 0.0) -> float:
    excess = returns - risk_free
    downside_std = excess[excess < 0].std()
    return excess.mean() / downside_std * np.sqrt(TRADING_DAYS_PER_YEAR)


def summary(returns: pd.Series, risk_free: pd.Series | float = 0.0) -> dict[str, float]:
    return {
        "CAGR": cagr(returns),
        "MDD": max_drawdown(returns),
        "Longest DD (yr)": longest_drawdown_years(returns),
        "Sharpe": sharpe(returns, risk_free),
        "Sortino": sortino(returns, risk_free),
    }
