# Research Notes

Findings and open questions from the source r/LETFs discussion, plus
anything we learn building this out. A living log, not a final verdict —
update as we backtest and, in later phases, collect live behavior.

## Validated

- **laurenthu independently rebuilt the strategy** outside Testfolio (real
  UPRO from 2009, a synthetic 3x SPY series with modeled financing
  pre-2009) and reproduced comparable — slightly better — numbers.
  Reasonable evidence the published backtest isn't a Testfolio-specific
  artifact.
- **laurenthu also built it on bestfolio.app** using real fund data back to
  2008: ~18.9% CAGR, ~-37% MDD. Consistent with the original numbers.

## Concerns to carry into implementation

### 1. The TIP filter's edge is thin and concentrated (laurenthu's decomposition)

- SPY-filter alone: ~19% CAGR, 1.07 Sortino.
- SPY + TIP filter: ~22% CAGR, 1.27 Sortino, same MDD.
- Almost all of that incremental edge comes from three years — 2015, 2018,
  2022 (rate-shock-driven equity selloffs) — each worth ~15-20pts of
  relative outperformance.
- Cost case: 2013 taper tantrum. TIP fell below its 200 SMA while SPY kept
  climbing (+32% year), forcing an unneeded de-lever, costing ~27pts that
  year alone.
- **Read**: TIP is a specific bet on catching rate-shock-driven selloffs,
  not a general early-crash detector. Real, but narrower and noisier than
  "17% CAGR" suggests.
- **Open question**: is a shorter sample (post-2000, or post-2003 when the
  IEF-extended TIP history starts) more honest than 1988-present for
  evaluating this specific edge? Re-run the SPY-only vs. SPY+TIP
  decomposition ourselves once the backtester exists — don't take the
  published split on faith.

### 2. Pre-inception backfill risk for SPMO and DBMF (Separate-Ad-9633)

- SPMO inception: 2015. DBMF inception: 2019. Testfolio's
  SPMOSIM/DBMFSIM backfills stand in for the ~25-45 years before that.
- Flagged as implausibly good pre-2000 (SPMOSIM 1972-2000 Sharpe 0.73 vs.
  SPY 0.47) — momentum factor is real, but a live fund's frictions
  (financing cost, tracking error, capacity limits) weren't present in the
  backfill.
- Post-2000 numbers look sound.
- **Open question for us**: how do we source pre-inception history? Options:
  (a) truncate the backtest to real fund inception — too short to be
  useful for CAGR/drawdown stats; (b) build our own simple factor proxies
  (momentum factor returns, a published trend-following/managed-futures
  index) with caveats stated explicitly; (c) use a backfilled ticker
  (Testfolio-style) with the limitation flagged in every report we
  generate. Leaning toward (b), or a clearly-labeled (c) — not (a). Decide
  before writing the backtester's data layer.
- Related, separately flagged: AQR's published managed-futures backtests
  show a similar pattern — strong backtest Sharpe, then a real "lost
  decade" for the actual live fund (AQMIX) through the 2010s. A reminder
  that DBMF's own live track record (inception 2019) is short and doesn't
  yet span a full regime cycle.

**Decision (2026-07-11):** stay fully free, no paid data licenses. Resolved
differently per leg:

- **SPMO (momentum)**: neither the ETF (launched Oct 2015) nor the S&P 500
  Momentum Index it tracks (launched Nov 2014) reaches back to 1988. S&P's
  own hypothetical back-tested numbers only go to Dec 1994, and the
  downloadable series requires a paid S&P Capital IQ license anyway — so
  paying wouldn't even close the gap. Instead, build a synthetic long-only
  momentum-tilted proxy from Ken French's data library (Market factor +
  Mom factor, free, CSV, back to 1927, standard academic construction) for
  the full 1988-present window, switching to real SPMO returns from Oct
  2015 onward.

  The proxy's `MOMENTUM_TILT_LOADING = 0.5` (`data/kenneth_french.py`) is a
  modeling assumption, not a derived constant: it stands for how much of
  the long-short momentum factor's return a long-only, market-cap-relative
  momentum tilt (like SPMO) plausibly captures. There is no single settled
  value — sensitivity-test it once the backtester runs end to end.

- **DBMF (managed futures)**: DBi has no long backtest of its own — its
  replication index only has a track record back to Dec 2015. No free
  source reaches 1988. Free options top out at SG Trend Index (free,
  published by Société Générale, live since 2000). Barclay BTOP50 (1987,
  nearly the full window) and Barclay CTA Index (1980) would close the gap
  but require a $150/yr subscription — ruled out to stay fully free.

  **Correction (2026-07-11, while building phase 1):** the "SG Trend Index
  is free, published, since 2000" claim above was wrong in the way that
  matters. Checked the actual page directly — it only shows an interactive
  MTD/YTD summary figure, not a downloadable historical series. Full daily
  history requires either SG's licensed Markets Analytics platform or
  contacting their Capital Consulting team — same access tier as the
  Barclay indices, not actually free. Checked several long-history
  managed-futures mutual funds too (MLMIX, ASFYX, QMHIX) — none reach
  earlier than 2010-2016. **Practical result: staying fully free means the
  managed-futures leg is bounded by DBMF's real inception (May 2019), not
  2000 as originally assumed.** That's a materially shorter usable window
  than the "stay fully free" decision was made expecting. Revisit the
  $150/yr paid option now that the real free/paid tradeoff is clearer, or
  accept 2019-present as the honest window for anything depending on the
  managed-futures leg.

  Either way, don't quietly extrapolate or backfill the missing window to
  make the series look more complete than it is — exclude it from
  MF-dependent comparisons, or flag it clearly as lower-confidence in
  every report the backtester produces.

  **Decision (2026-07-11):** accept 2019-present as the honest window for
  now rather than pay for BTOP50/Barclay CTA. Revisit paying for it later
  if the shorter window turns out to be a real limitation once we're
  further into using this — noted here so it isn't forgotten as an
  available option, not treated as permanently closed.

### 2b. SPY and TIP themselves don't reach 1988 either (found while building phase 1)

- Not something the original thread raised, but surfaced immediately when
  building the data layer: **SPY (ETF since Jan 1993) and TIP (ETF since
  Dec 2003) don't cover the published 1988-present window on their own.**
  The original post's backtest handled this for TIP by extending its
  _signal_ history with IEF pre-inception (mentioned in passing in
  `strategy.md`'s source), but IEF itself only goes back to 2002 -- it
  doesn't reach 1988 either. Reaching SPY/TIP's full window would need
  index-level or synthetic proxy data for the _signal_ series itself, on
  top of the SPMO/DBMF asset-leg proxies already resolved above.
  **Resolved (2026-07-11)**, more easily than expected:

- **SPY signal**: `^SP500TR` (S&P 500 Total Return Index, via yfinance) has
  real daily history back to **1988-01-04** -- the strategy's own published
  start date, exactly. Dividend-inclusive, no construction needed. Used
  directly for the whole window; no splice with the SPY ETF required.
- **TIP signal**: no single free series reaches 1988, but three real
  series chain cleanly: **VUSTX** (Vanguard Long-Term Treasury fund, real
  NAV history since 1986-05-19) → **IEF** (real, since 2002-07-30) → real
  **TIP** (since 2003-12-05). This mirrors the original post's own move of
  substituting a nominal treasury proxy before TIP existed (they used IEF;
  this extends the same idea one step further back with VUSTX). VUSTX is
  long-duration (~17yr) versus TIP's intermediate ~7-8yr duration -- a real,
  documented duration mismatch for the 1988-2002 segment specifically, not
  a like-for-like substitute. Treat regime signals from that period with
  that caveat in mind.
- See `src/golden_ratio_dual_gate/data/signal_history.py`.

This closes the signal-side gap independent of the SPMO/DBMF asset-leg
proxies (#2 above). The backtest's _actual_ remaining bound is now the
managed-futures asset leg specifically (DBMF's real inception, absent a
paid subscription) -- not the signal series.

### 3. Dividend adjustment is mandatory (ApolloDan)

- Un-adjusted price history makes TIP's 200 SMA break (false signals)
  almost monthly, since TIP's price return is small relative to its
  distribution yield.
- **Action**: every price series in the backtester must be total-return /
  adjusted-close. No exceptions, no "just for now" raw-price shortcuts.

### 4. TIP signal ambiguity vs. the TLT allocation (Separate-Ad-9633)

- TIP-below-SMA fires on inflation-scare regimes (2006, 2013, 2016, 2022)
  AND on deflation/liquidity-scare regimes (GFC, 2014-15, 2018) — different
  economic stories, same signal.
- If you fully trust "TIP fell because of inflation risk," holding TLT
  (nominal long treasuries) in the risk-off sleeve at the same time is
  arguably self-defeating — nominal long bonds do poorly exactly when
  inflation is the driver.
- Author's own proposed mitigation (untested in the post): replace the
  extra 10% risk-off-only TLT weight with more managed futures instead of
  removing it outright, so the bond allocation doesn't grow specifically
  when bond momentum is negative.
- **Open question**: worth backtesting this variant once the engine exists.
  Not assumed correct — just worth checking.

### 5. Leverage-direction sanity check (howevertheory98968's question, already answered in-thread)

- Inverting the schedule (lever up below the SMA to buy cheap, de-lever
  above it) makes the strategy worse than the sum of its parts, per the
  author's linked Testfolio runs. Mechanism: volatility is structurally
  higher below the SMA, which is what hurts a daily-reset 3x product most;
  and avoiding deep drawdowns shortens recovery time, which is most of
  where the CAGR improvement comes from — not a risk/return tradeoff, a
  genuine asymmetry.
- Not an open question, but worth re-confirming ourselves once the
  backtester exists, as a sanity check on data/timing correctness: if our
  from-scratch backtester says leverage-inverted is _better_, something is
  wired backwards.

### 6. The AND/OR bug

- The original post's table initially read as AND-for-risk-off; a
  commenter (RottenGrapeJuice) caught it, author corrected to
  OR-for-risk-off / AND-for-risk-on.
- Not a flaw in the final logic (documented correctly in `strategy.md`),
  but a reminder this is a promising research-stage idea, not something
  battle-tested elsewhere. Verify our own implementation against a few
  manually-checked historical regime dates before trusting the
  backtester's output.

## Explicitly rejected by the original author

- **Stacking a second, independent trend filter** (e.g. a leveraged HAA
  overlay) on top of this one. When two independently-computed signals
  disagree, you're forced into an arbitrary tiebreak exactly when it's most
  costly to be wrong. Keep this a single self-contained dual-gate system;
  if we want more tactical strategies, run them as separate, genuinely
  uncorrelated sleeves rather than combining signals inside one.

## Ideas floated but not built (yet)

- **EDV variant** of the treasury leg (manlymatt83 / laurenthu): more
  crash convexity in equity-driven selloffs, but EDV's own duration
  (~24yr) makes it vulnerable in rate-shock crashes — exactly the scenario
  the TIP filter is best at catching. Net effect unclear without testing.
- **Real yield as an alternative signal to TIP price** (Separate-Ad-9633's
  suggestion; author hadn't researched it as of the thread). Worth a look
  if we want a cleaner-than-TIP-price inflation/duration signal.
