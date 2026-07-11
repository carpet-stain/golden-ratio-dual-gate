"""SG Trend Index loader for the DBMF leg's pre-inception (before May 2019)
proxy history.

No stable, freely-downloadable URL was found for this index (see
docs/research-notes.md #2) -- it's published on Societe Generale's Prime
Services Indices page as an interactive page, not a stable file. Rather
than scrape a page layout that can change without notice, this expects a
CSV dropped in by hand:

  1. Download the SG Trend Index (daily, since 2000) from
     https://wholesale.banking.societegenerale.com/en/prime-services-indices/
  2. Save it as data/external/sg_trend_index.csv with two columns:
     date,value -- where value is the index level, not a return.

If the file isn't there, callers get an empty series and 1988-2000 (and, if
the file is never provided, all the way to DBMF's real May 2019 inception)
stays an explicit, unmodeled gap for the managed-futures leg -- per the
"stay fully free" decision in docs/research-notes.md, this is not silently
backfilled with something else.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DEFAULT_PATH = Path("data/external/sg_trend_index.csv")


def load_sg_trend_returns(path: Path = DEFAULT_PATH) -> pd.Series:
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found -- see the module docstring in "
            "data/managed_futures.py for how to obtain it by hand. There is "
            "no automated source for this index."
        )
    frame = pd.read_csv(path, parse_dates=["date"]).set_index("date").sort_index()
    returns = frame["value"].pct_change().dropna()
    returns.name = "MF_PROXY"
    return returns
