# Sizing & Role in Portfolio

## Current portfolio (context)

| Ticker | Weight | Role |
|---|---|---|
| AVUV | 30% | US Small Cap Value |
| RSST | 20% | US equity (S&P) + managed-futures overlay, ~100%/100% notional each |
| RSSB | 20% | Global equity + US Treasury futures (2-30yr), ~100%/100% notional each |
| AVDV | 10% | Intl Small Cap Value |
| AVEE | 10% | EM Equity |
| AVNV | 10% | Intl (developed + EM) Value |

Decomposed: ~100% equity-beta notional + ~20% managed-futures notional (via
RSST) + ~20% Treasury-futures notional (via RSSB, blended 2-30yr duration)
≈ **~140% gross notional**. All-equity factor tilts, heavy small/value
weighting, no gold, no momentum, no dynamic de-lever mechanism.

## What the dual-gate sleeve is genuinely additive on

- **Gold** — zero overlap with current holdings.
- **Large-cap momentum (SPMO)** — genuinely new factor, and a useful
  complement to the existing heavy value tilt (momentum and value are
  typically uncorrelated-to-negatively-correlated).
- **The trend-timed leverage mechanism itself** — nothing in the current
  book scales exposure dynamically. This is the real point of adding it.

## What's largely redundant in role (not instrument)

- **Managed futures (DBMF)** — RSST already provides a MF overlay.
- **LT Treasuries (TLT)** — RSSB already provides blended 2-30yr
  Treasury-futures duration, though not identical to TLT's pure long
  duration specifically.

Net: the honest diversification benefit is narrower than "five new
uncorrelated assets" — closer to "gold + momentum + a dynamic leverage
dial," layered on exposure the book substantially already carries via the
MF/Treasury legs.

## Decision (2026-07-11)

- **Funding**: mixed — a partial carve-out to establish a starting
  position, then grown via new contributions (DCA) rather than continuing
  to trim existing sleeves indefinitely.
- **Target size**: 15-25% of total investable portfolio.
- **Rationale for the band**: the published 17% CAGR headline is
  optimistic — see `research-notes.md` for why (thin/concentrated
  TIP-filter edge, pre-2000 SPMOSIM/DBMFSIM backfill risk). At 15-25%, a
  full backtested-MDD event in the sleeve (~37%, before real-world LETF
  slippage) costs roughly 5.5-9.25 points of the total portfolio —
  material, but bounded, and proportionate to treating this as "a second
  real return driver," not "the new core."
- **Not yet decided**: exact carve-out source/amount, and exact target
  within the 15-25% band. Revisit once the backtester exists and we can
  see real rolling-drawdown numbers instead of headline stats.

## Open questions for later

- Does the carve-out come specifically from RSST/RSSB (since their
  MF/Treasury legs are the most redundant with the new sleeve), or
  proportionally from everything?
- Should this be actively rebalanced against the rest of the portfolio
  (i.e. the total book gets rebalanced back to a 15-25% sleeve / 75-85%
  static-book split), or does it float?
