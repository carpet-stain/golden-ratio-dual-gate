"""Real ticker price history via yfinance."""

from __future__ import annotations

from typing import cast

import pandas as pd
import yfinance as yf


def fetch_adjusted_close(
    ticker: str, start: str | None = None, end: str | None = None
) -> pd.Series:
    """Daily adjusted-close price series for `ticker`, indexed by date.

    `auto_adjust=True` folds dividends/splits into the price directly -- the
    dividend-adjustment ApolloDan's warning requires (docs/research-notes.md
    #3). Never disable auto_adjust to "simplify" this.

    Passes `period="max"` when `start`/`end` aren't given -- yfinance's own
    default period is one month, not the full history, and silently
    returning a month of data instead of decades is exactly the kind of
    quiet gap this project is trying not to have.
    """
    period = None if (start or end) else "max"
    data = yf.download(
        ticker,
        start=start,
        end=end,
        period=period,  # pyright: ignore[reportArgumentType] -- yfinance ships no type
        # stub; inferred `str` type is a stub artifact, `None` is a real dispatch branch
        auto_adjust=True,
        progress=False,
    )
    if data is None or data.empty:
        raise ValueError(f"no data returned for {ticker}")
    close = data["Close"]
    if isinstance(close, pd.DataFrame):
        close = cast(pd.DataFrame, close).iloc[:, 0]
    close = close.dropna()
    close.name = ticker
    return close
