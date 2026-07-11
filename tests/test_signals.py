"""Signal logic tests -- exercise the exact AND/OR distinction the original
post got backwards on first draft (docs/research-notes.md #6), so a broken
regime implementation fails loudly here rather than silently in a backtest.
"""
from __future__ import annotations

import pandas as pd

from golden_ratio_dual_gate.signals import compute_regime

SEED_DAYS = 210  # long enough to fill the 200-day SMA window


def _series(values: list[float]) -> pd.Series:
    dates = pd.bdate_range(start="2020-01-01", periods=len(values))
    return pd.Series(values, index=dates, dtype=float)


def test_risk_on_requires_both_filters_confirmed_above():
    spy = _series([100.0] * SEED_DAYS + [110.0] * 10)  # clears its 0.5% band
    tip = _series([100.0] * SEED_DAYS + [102.0] * 10)  # clears its 0.1% band
    regime = compute_regime(spy, tip)
    assert regime.tail(5).all()


def test_risk_off_if_tip_confirms_below_even_though_spy_confirms_above():
    spy = _series([100.0] * SEED_DAYS + [110.0] * 10)  # SPY alone: risk-on
    tip = _series([100.0] * SEED_DAYS + [98.0] * 10)  # TIP confirms below its band
    regime = compute_regime(spy, tip)
    # OR-for-risk-off: TIP alone confirming below must force risk-off
    # overall, regardless of SPY. This is exactly the direction the
    # original post's table got backwards (AND instead of OR).
    assert not regime.tail(5).any()


def test_risk_off_if_spy_confirms_below_even_though_tip_confirms_above():
    spy = _series([100.0] * SEED_DAYS + [90.0] * 10)  # SPY confirms below
    tip = _series([100.0] * SEED_DAYS + [102.0] * 10)  # TIP alone: risk-on
    regime = compute_regime(spy, tip)
    assert not regime.tail(5).any()


def test_small_moves_inside_the_band_do_not_flip_the_regime():
    tip = _series([100.0] * SEED_DAYS + [100.2] * 30)  # confirms above once, holds
    spy = _series([100.0] * SEED_DAYS + [110.0] * 20 + [110.3] * 10)  # break, then wobble
    regime = compute_regime(spy, tip)
    assert regime.tail(5).all()


def test_signal_is_delayed_by_one_trading_day():
    tip = _series([100.0] * SEED_DAYS + [100.2] * 10)  # confirmed above throughout
    spy = _series([100.0] * SEED_DAYS + [90.0] * 10)  # confirms below on day SEED_DAYS
    regime = compute_regime(spy, tip)

    break_date = spy.index[SEED_DAYS]
    next_date = spy.index[SEED_DAYS + 1]

    # Too early for a delayed value to exist yet for the break date itself.
    assert break_date not in regime.index
    # The break is reflected starting one trading day later.
    assert regime.loc[next_date] == False  # noqa: E712
