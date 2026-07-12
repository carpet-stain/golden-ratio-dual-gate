"""Extended price-level history for the dual-gate signal itself (SPY and
TIP), reaching back toward the strategy's published 1988 start rather than
being bounded by SPY's real 1993 or TIP's real 2003 inception.

See docs/research-notes.md #2b -- a separate gap from the SPMO/DBMF
asset-leg proxies, found while building phase 1.
"""

from __future__ import annotations

import pandas as pd

from .prices import fetch_adjusted_close
from .splice import splice_returns


def fetch_spy_signal_price() -> pd.Series:
    """S&P 500 Total Return Index (^SP500TR) -- a real, dividend-inclusive
    index with daily history back to 1988-01-04, the strategy's own
    published start date. Used directly for the whole window; no splice
    with the SPY ETF is needed, since ^SP500TR already covers the full
    range continuously and is arguably a cleaner trend signal than the ETF
    (no ETF tracking error or liquidity effects to worry about)."""
    return fetch_adjusted_close("^SP500TR")


def fetch_tip_signal_price() -> pd.Series:
    """Synthetic TIP-signal price level, chaining three real return series
    and reconstructing a price index from them:

      VUSTX (Vanguard Long-Term Treasury fund, since 1986-05-19)
        -> IEF (iShares 7-10yr Treasury, real, since 2002-07-30)
        -> TIP (real, since 2003-12-05)

    This mirrors the original post's own approach of substituting a
    nominal treasury proxy before TIP existed (they used IEF; this extends
    the same idea one step further back with VUSTX). VUSTX is long-duration
    (~17yr) versus TIP's intermediate ~7-8yr duration -- a real, documented
    duration mismatch for the 1988-2002 segment specifically, not a
    like-for-like substitute. Treat regime signals from that period with
    that in mind.
    """
    vustx_returns = fetch_adjusted_close("VUSTX").pct_change().dropna()
    ief_returns = fetch_adjusted_close("IEF").pct_change().dropna()
    tip_returns = fetch_adjusted_close("TIP").pct_change().dropna()

    combined = splice_returns(vustx_returns, ief_returns, "intermediate_proxy")
    combined = splice_returns(combined, tip_returns, "TIP_SIGNAL")

    price = 100.0 * (1 + combined).cumprod()
    price.name = "TIP_SIGNAL"
    return price
