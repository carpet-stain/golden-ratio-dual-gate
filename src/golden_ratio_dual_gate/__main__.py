"""Fetch data, run the dual-gate backtest, and print the headline report.

Usage: python -m golden_ratio_dual_gate

Known limitation (not yet resolved -- see docs/research-notes.md): this
runs over whatever window real SPY/TIP signal data actually covers, which
is bounded by TIP's real inception (Dec 2003), not 1988. Reaching the
published backtest's full 1988-present window needs pre-inception proxy
data for the SPY/TIP *signal* series itself, on top of the SPMO/DBMF asset
proxies already handled below -- that's a separate open question.
"""
from __future__ import annotations

import sys

import pandas as pd

from .backtest import TICKERS, run_backtest
from .data.kenneth_french import fetch_momentum_proxy_returns
from .data.managed_futures import load_sg_trend_returns
from .data.prices import fetch_adjusted_close
from .data.splice import splice_returns
from .metrics import summary
from .reports import spy_only_vs_dual_gate
from .signals import compute_regime

REAL_TICKERS = [*TICKERS, "SPY", "TIP"]


def load_data() -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    prices = {ticker: fetch_adjusted_close(ticker) for ticker in REAL_TICKERS}
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
    return returns, prices["SPY"], prices["TIP"]


def main() -> None:
    returns, spy_price, tip_price = load_data()

    print(f"Sleeve data available from {returns.index.min().date()} onward.")
    print("(Not 1988 -- see the module docstring and docs/research-notes.md.)\n")

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
