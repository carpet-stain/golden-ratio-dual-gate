"""Fetch data, run the dual-gate backtest, and print the headline report.

Usage: python -m golden_ratio_dual_gate

The SPY/TIP signal itself now reaches back to 1988 (see
data/signal_history.py, docs/research-notes.md #2b). The remaining bound
on the backtest window is the managed-futures asset leg: without a
manually-supplied SG Trend Index CSV (data/managed_futures.py), it's
bounded by DBMF's real inception (May 2019), not 1988 or even 2000 -- see
docs/research-notes.md #2 for why "stay fully free" turned out to deliver
less than first assumed there.
"""

from __future__ import annotations

import sys

import pandas as pd

from .backtest import TICKERS, run_backtest
from .data.kenneth_french import fetch_momentum_proxy_returns
from .data.managed_futures import load_sg_trend_returns
from .data.prices import fetch_adjusted_close
from .data.signal_history import fetch_spy_signal_price, fetch_tip_signal_price
from .data.splice import splice_returns
from .metrics import summary
from .reports import spy_only_vs_dual_gate
from .signals import compute_regime


def load_data() -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    prices = {ticker: fetch_adjusted_close(ticker) for ticker in TICKERS}
    asset_returns = {ticker: prices[ticker].pct_change().dropna() for ticker in TICKERS}

    asset_returns["SPMO"] = splice_returns(
        fetch_momentum_proxy_returns(), asset_returns["SPMO"], "SPMO"
    )

    try:
        mf_proxy = load_sg_trend_returns()
    except FileNotFoundError as exc:
        print(f"warning: {exc}", file=sys.stderr)
        mf_proxy = pd.Series(dtype=float)
    asset_returns["DBMF"] = splice_returns(mf_proxy, asset_returns["DBMF"], "DBMF")

    returns = pd.DataFrame(asset_returns)[TICKERS].dropna()

    spy_price = fetch_spy_signal_price()
    tip_price = fetch_tip_signal_price()
    return returns, spy_price, tip_price


def main() -> None:
    returns, spy_price, tip_price = load_data()

    print(f"SPY/TIP signal available from {tip_price.index.min().date()} onward.")
    print(
        f"Sleeve asset data (the actual binding constraint) available from "
        f"{returns.index.min().date()} onward -- see docs/research-notes.md #2.\n"
    )

    regime = compute_regime(spy_price, tip_price)
    portfolio_returns = run_backtest(returns, regime)

    print("Headline metrics (full dual-gate strategy):")
    print(pd.Series(summary(portfolio_returns)).to_string())

    print("\nSPY-only vs. SPY+TIP dual-gate decomposition:")
    headline, yearly = spy_only_vs_dual_gate(returns, spy_price, tip_price)
    print(headline.to_string())
    print("\nYear-by-year dual-gate edge over SPY-only filter:")
    print(yearly.to_string())


if __name__ == "__main__":
    main()
