"""Splice tests -- confirm the real series takes over cleanly from its
first date, with no overlap blending.
"""

from __future__ import annotations

import pandas as pd

from golden_ratio_dual_gate.data.splice import splice_returns


def test_real_series_takes_over_from_its_first_date():
    dates_proxy = pd.bdate_range("2000-01-01", periods=10)
    dates_real = pd.bdate_range("2000-01-08", periods=5)  # overlaps the tail of proxy
    proxy = pd.Series([0.01] * 10, index=dates_proxy)
    real = pd.Series([0.02] * 5, index=dates_real)

    spliced = splice_returns(proxy, real, "TICKER")

    cutover = dates_real.min()
    assert (spliced.loc[: cutover - pd.Timedelta(days=1)] == 0.01).all()
    assert (spliced.loc[cutover:] == 0.02).all()
    assert spliced.name == "TICKER"


def test_empty_real_series_falls_back_to_proxy_entirely():
    dates_proxy = pd.bdate_range("2000-01-01", periods=10)
    proxy = pd.Series([0.01] * 10, index=dates_proxy)
    real = pd.Series(dtype=float)

    spliced = splice_returns(proxy, real, "TICKER")

    assert (spliced == 0.01).all()
    assert spliced.name == "TICKER"


def test_empty_proxy_falls_back_to_real_entirely():
    # "No manual CSV" managed-futures case (docs/research-notes.md #2): an
    # empty, non-datetime proxy must not crash the index comparison.
    dates_real = pd.bdate_range("2019-05-01", periods=5)
    proxy = pd.Series(dtype=float)
    real = pd.Series([0.02] * 5, index=dates_real)

    spliced = splice_returns(proxy, real, "TICKER")

    assert (spliced == 0.02).all()
    assert spliced.name == "TICKER"
