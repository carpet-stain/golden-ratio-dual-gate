"""Diagnostics called for in docs/research-notes.md: reproduce laurenthu's
SPY-only vs. SPY+TIP decomposition ourselves rather than take the published
thread's split on faith, and a leverage-inversion sanity check against the
author's own finding (research-notes.md #5).
"""

from __future__ import annotations

from typing import cast

import pandas as pd

from . import metrics
from .backtest import run_backtest
from .signals import SIGNAL_DELAY_DAYS, SPY_BAND, SPY_SMA_WINDOW, _above_band, compute_regime


def spy_only_regime(spy_price: pd.Series) -> pd.Series:
    """Risk-on defined by the SPY trend filter alone, dropping the TIP
    canary -- for comparison against the full dual-gate regime."""
    spy_above = _above_band(spy_price, SPY_SMA_WINDOW, SPY_BAND)
    return spy_above.shift(SIGNAL_DELAY_DAYS).dropna().astype(bool)


def leverage_inverted_regime(regime: pd.Series) -> pd.Series:
    """Flips risk-on/risk-off: levers up below the SMA, de-levers above it.
    A sanity check only (research-notes.md #5) -- our backtester should
    show this performing worse than the real strategy, matching the
    original author's finding. If it instead shows leverage-inverted
    beating the real schedule, something in our signal or timing logic is
    wired backwards."""
    return ~regime


def spy_only_vs_dual_gate(
    returns: pd.DataFrame, spy_price: pd.Series, tip_price: pd.Series
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Reproduces laurenthu's decomposition: how much of the dual-gate
    strategy's edge over a plain SPY-trend filter is real, and which years
    it comes from."""
    spy_regime = spy_only_regime(spy_price)
    dual_regime = compute_regime(spy_price, tip_price)

    spy_only_returns = run_backtest(returns, spy_regime)
    dual_gate_returns = run_backtest(returns, dual_regime)

    headline = pd.DataFrame(
        {
            "SPY-filter only": metrics.summary(spy_only_returns),
            "SPY+TIP dual-gate": metrics.summary(dual_gate_returns),
        }
    ).T

    def _yearly(r: pd.Series) -> pd.Series:
        return r.groupby(pd.DatetimeIndex(r.index).year).apply(
            lambda x: cast(float, (1 + x).prod()) - 1
        )

    yearly = pd.DataFrame(
        {
            "SPY-filter only": _yearly(spy_only_returns),
            "SPY+TIP dual-gate": _yearly(dual_gate_returns),
        }
    )
    yearly["dual-gate edge"] = yearly["SPY+TIP dual-gate"] - yearly["SPY-filter only"]

    return headline, yearly
