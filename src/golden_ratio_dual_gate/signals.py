"""SPY/TIP dual-gate signal: 200-day SMA trend filters with bands and a
1-day execution delay. See docs/strategy.md for the spec this implements.

docs/research-notes.md #6 records that the original post's own allocation
table got the AND/OR direction backwards on first draft. Treat that as a
standing reminder to verify this module against hand-checked scenarios
(see tests/test_signals.py) rather than trust it by construction.
"""
from __future__ import annotations

import pandas as pd

SPY_SMA_WINDOW = 200
SPY_BAND = 0.005  # +/- 0.5%
TIP_SMA_WINDOW = 200
TIP_BAND = 0.001  # +/- 0.1%, tightened from an initial 0.5% (see docs/strategy.md)
SIGNAL_DELAY_DAYS = 1


def _above_band(price: pd.Series, window: int, band: float) -> pd.Series:
    """True once price closes more than `band` above its SMA, False once it
    closes more than `band` below. Holds its last confirmed state while
    price sits inside the band -- that's what the band is for: it stops
    single-day noise around the SMA line from flipping the regime."""
    sma = price.rolling(window).mean()
    upper = sma * (1 + band)
    lower = sma * (1 - band)
    state = pd.Series(index=price.index, dtype="boolean")
    state[price > upper] = True
    state[price < lower] = False
    return state.ffill()


def compute_regime(spy_price: pd.Series, tip_price: pd.Series) -> pd.Series:
    """True = risk-on, False = risk-off, delayed by SIGNAL_DELAY_DAYS to
    reflect a 1-day-late execution.

    Risk-on requires BOTH SPY and TIP confirmed above their banded 200 SMA.
    Risk-off triggers if EITHER is confirmed below. These are logically
    equivalent (De Morgan's) but both are spelled out in docs/strategy.md
    because the original post's table read as AND-for-risk-off on first
    draft and had to be corrected.
    """
    spy_above = _above_band(spy_price, SPY_SMA_WINDOW, SPY_BAND)
    tip_above = _above_band(tip_price, TIP_SMA_WINDOW, TIP_BAND)
    combined = pd.concat([spy_above, tip_above], axis=1).dropna()
    risk_on = combined.iloc[:, 0] & combined.iloc[:, 1]
    return risk_on.shift(SIGNAL_DELAY_DAYS).dropna().astype(bool)
