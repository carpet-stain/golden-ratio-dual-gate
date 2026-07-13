"""Kenneth French daily factor data, used to build a long-only momentum-tilt
proxy for the SPMO leg before its real inception (Oct 2015).

Free, CSV, back to 1926. See docs/research-notes.md #2 for why this exists:
neither SPMO nor the S&P 500 Momentum Index it tracks has usable history
that far back, and a paid data license doesn't close the gap either.
"""

from __future__ import annotations

import io
import re
import zipfile

import pandas as pd
import requests

_MOMENTUM_URL = (
    "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_daily_CSV.zip"
)
_FACTORS_URL = (
    "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
    "F-F_Research_Data_Factors_daily_CSV.zip"
)

# How much of the long-short momentum factor's return a long-only,
# market-cap-relative momentum tilt (like SPMO) plausibly captures. There is
# no single settled value for this -- it's a documented modeling assumption,
# not a derived constant. Flagged in docs/research-notes.md for
# sensitivity-testing once the backtester is running end to end.
MOMENTUM_TILT_LOADING = 0.5

_DATE_ROW = re.compile(r"^\d{8},")


def _download_ff_zip(url: str) -> str:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    archive = zipfile.ZipFile(io.BytesIO(response.content))
    name = archive.namelist()[0]
    return archive.read(name).decode("latin-1")


def _parse_ff_csv(text: str) -> pd.DataFrame:
    """Ken French's daily-factor CSVs share one layout: several lines of
    prose, a header row, YYYYMMDD-keyed data rows, then a blank line and a
    copyright footer. Keep only the header and the data rows."""
    lines = text.splitlines()
    data_start = next(i for i, line in enumerate(lines) if _DATE_ROW.match(line))
    header = [c.strip() for c in lines[data_start - 1].split(",")]
    header[0] = "date"
    rows = [line.split(",") for line in lines[data_start:] if _DATE_ROW.match(line)]
    frame = pd.DataFrame(rows, columns=header)
    frame["date"] = pd.to_datetime(frame["date"], format="%Y%m%d")
    frame = frame.set_index("date")
    return frame.apply(pd.to_numeric, errors="coerce") / 100.0


def fetch_momentum_proxy_returns() -> pd.Series:
    """Daily total-return series for a synthetic long-only momentum-tilted
    large-cap proxy: risk-free rate + market return + a scaled momentum
    factor loading. Stands in for SPMO before its Oct 2015 inception."""
    momentum = _parse_ff_csv(_download_ff_zip(_MOMENTUM_URL))["Mom"]
    factors = _parse_ff_csv(_download_ff_zip(_FACTORS_URL))
    combined = factors.join(momentum, how="inner")
    proxy_return = combined["RF"] + combined["Mkt-RF"] + MOMENTUM_TILT_LOADING * combined["Mom"]
    proxy_return.name = "SPMO_PROXY"
    return proxy_return
