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

- **Small cap value (VBR)** — AVUV already provides this (30% of the
  current book). Missed in the first pass at this doc; corrected here.
- **Managed futures (DBMF)** — RSST already provides a MF overlay.
- **LT Treasuries (TLT)** — RSSB already provides blended 2-30yr
  Treasury-futures duration, though not identical to TLT's pure long
  duration specifically.

So three of the sleeve's five risk-off components overlap in role with
existing holdings (Small Value, MF, Treasuries) — only Gold and Large Cap
Momentum are genuinely new. Net: the honest diversification benefit is
narrower than "five new uncorrelated assets" — closer to "gold + momentum
+ a dynamic leverage dial," layered on exposure the book substantially
already carries via the AVUV/RSST/RSSB legs.

## Decision (2026-07-11)

- **Funding**: mixed — a partial carve-out now to establish a real
  starting position, then grown toward the top of the target band via new
  contributions (DCA) rather than continuing to trim existing holdings.
- **Target size**: 15-25% of total investable portfolio. Carve out to the
  **low end (~15%) now**; the rest of the band is filled by DCA over time.
- **Carve-out source**: AVUV + RSST + RSSB, proportional to their current
  weight (30/20/20 → 43%/29%/29% of the carve-out amount). AVDV, AVEE,
  AVNV are left untouched — they're the only positions with zero overlap
  with the new sleeve.

  Concretely, a 15%-of-portfolio carve-out looks like:

  | Ticker | Before | Trim | After |
  |---|---|---|---|
  | AVUV | 30% | -6.4% | 23.6% |
  | RSST | 20% | -4.3% | 15.7% |
  | RSSB | 20% | -4.3% | 15.7% |
  | AVDV | 10% | — | 10% |
  | AVEE | 10% | — | 10% |
  | AVNV | 10% | — | 10% |
  | golden-ratio-dual-gate | 0% | +15% | 15% |

- **Rationale for the band**: the published 17% CAGR headline is
  optimistic — see `research-notes.md` for why (thin/concentrated
  TIP-filter edge, pre-2000 SPMOSIM/DBMFSIM backfill risk). At 15-25%, a
  full backtested-MDD event in the sleeve (~37%, before real-world LETF
  slippage) costs roughly 5.5-9.25 points of the total portfolio —
  material, but bounded, and proportionate to treating this as "a second
  real return driver," not "the new core."
- **Not yet decided**: the exact eventual target within 15-25%, and
  whether growth toward it comes purely from new contributions or a second
  smaller carve-out later. Revisit once the backtester exists and there
  are real rolling-drawdown numbers instead of headline stats to size
  against.

## Open questions for later

- Should this sleeve be actively rebalanced against the rest of the
  portfolio (i.e. the total book gets rebalanced back to a target
  sleeve / static-book split on a schedule), or does it float and only get
  topped up via new contributions?
