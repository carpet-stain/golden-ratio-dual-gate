"""Metrics tests -- hand-computable synthetic series so a correct
implementation can be verified by arithmetic, not just plausibility.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from golden_ratio_dual_gate import metrics

TRADING_DAYS = metrics.TRADING_DAYS_PER_YEAR


def test_cagr_of_a_constant_daily_return_over_one_year():
    daily = 0.0004
    returns = pd.Series([daily] * TRADING_DAYS)
    expected = (1 + daily) ** TRADING_DAYS - 1
    assert metrics.cagr(returns) == pytest.approx(expected, rel=1e-9)


def test_max_drawdown_on_a_simple_peak_and_trough():
    returns = pd.Series([0.10, -0.20, 0.0, 0.0])
    wealth = (1 + returns).cumprod()
    expected = wealth.iloc[1] / wealth.iloc[0] - 1
    assert metrics.max_drawdown(returns) == pytest.approx(expected)
    assert metrics.max_drawdown(returns) < 0


def test_longest_drawdown_counts_the_full_underwater_stretch():
    # Peak on day 0; underwater for exactly 3 days (days 1-3); recovered on
    # day 4.
    returns = pd.Series([0.10, -0.05, -0.01, 0.0, 0.20, 0.0])
    assert metrics.longest_drawdown_years(returns) == pytest.approx(3 / TRADING_DAYS)


def test_sharpe_is_zero_for_a_zero_mean_series():
    returns = pd.Series([0.01, -0.01, 0.01, -0.01])
    assert metrics.sharpe(returns) == pytest.approx(0.0)


def test_sortino_matches_hand_computed_downside_deviation():
    returns = pd.Series([0.02, -0.01, 0.03, -0.02])
    downside_std = pd.Series([-0.01, -0.02]).std()
    expected = returns.mean() / downside_std * np.sqrt(TRADING_DAYS)
    assert metrics.sortino(returns) == pytest.approx(expected)
