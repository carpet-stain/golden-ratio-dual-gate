# Roadmap

Docs-first. No code until the strategy spec and sizing are settled (see
`strategy.md`, `sizing-and-role.md`) and the open data-sourcing questions
in `research-notes.md` have real answers, not just a plan to find them.

## Phase 1 — Backtester

- Rebuild the strategy from scratch, independent of Testfolio, so we can:
  - Re-run laurenthu's SPY-only vs. SPY+TIP decomposition ourselves.
  - Test the leverage-inversion sanity check.
  - Test the TLT-to-managed-futures swap idea from the TIP-ambiguity
    discussion.
  - Try the EDV variant.
- Settle the pre-inception data question (SPMO/DBMF history before
  2015/2019) before writing the data layer — this is a decision, not a
  detail to leave for later.
- All price series total-return / dividend-adjusted, no exceptions.

## Phase 2 — Signal generator

- Given current market data, output today's target allocation (risk-on vs.
  risk-off) and whether a rebalance/regime-flip trade is due.
- No order placement yet — a "tell me what to do" tool, checked by hand.

## Phase 3 — Schwab-connected execution

- Talk to Schwab's API for account/position data and, eventually, order
  placement.
- Deferred deliberately — not scoped in detail yet. Revisit once phases 1-2
  are proven out and the sizing decision has been live for a while.

## Explicitly out of scope for now

- Live/automated order execution without a human in the loop.
- Multi-strategy portfolio orchestration (this repo is one sleeve; how it
  nets against the rest of the portfolio is tracked in
  `sizing-and-role.md`, not built here).
