"""Combine pre-inception proxy return series with real ticker returns."""

from __future__ import annotations

import pandas as pd


def splice_returns(proxy: pd.Series, real: pd.Series, ticker: str) -> pd.Series:
    """Use `proxy` returns before the real ticker's first date, `real`
    returns from its first date onward. No overlap blending -- the real
    series simply takes over from its first available date, so results
    never depend on how the two series compare during a transition window.
    """
    if real.empty:
        return proxy.rename(ticker)
    if proxy.empty:
        return real.rename(ticker)
    cutover = real.index.min()
    spliced = pd.concat([proxy[proxy.index < cutover], real])
    spliced.name = ticker
    return spliced.sort_index()
