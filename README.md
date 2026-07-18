# golden-ratio-dual-gate

Research and, eventually, execution for a SPY/TIP dual-trend-gate leveraged
portfolio, adapted from a strategy posted to r/LETFs.

## Status

Phase 1 (backtester) is underway — see `docs/roadmap.md`. Strategy spec,
sizing decision, and data-sourcing questions are settled; see `docs/` for
all of it, and `docs/research-notes.md` for what's still open (notably: the
backtest currently runs from 2019 onward, not the published 1988, pending
pre-inception proxy data for the SPY/TIP signal series itself).

### Running it

```sh
uv sync
uv run pytest                              # unit tests
uv run python -m golden_ratio_dual_gate    # fetch data, run the backtest, print the report
```

Optional: to extend the managed-futures leg's history back to 2000 (see
`src/golden_ratio_dual_gate/data/managed_futures.py`), download the SG
Trend Index by hand and save it as `data/external/sg_trend_index.csv`
(columns: `date,value`). Without it, that leg is bounded by DBMF's real
inception (May 2019).

## Docs

- [`docs/strategy.md`](docs/strategy.md) — the mechanics: signal, allocations, rebalancing
- [`docs/sizing-and-role.md`](docs/sizing-and-role.md) — how this fits into the broader portfolio
- [`docs/research-notes.md`](docs/research-notes.md) — critiques and open questions from
  the source discussion
- [`docs/roadmap.md`](docs/roadmap.md) — phased plan, including future Schwab integration

## Origin

Adapted from [this r/LETFs post](https://old.reddit.com/r/LETFs/comments/1upw0hu/17x_golden_ratio_inspired_portfolio_using_spy_tip/)
by u/confettofetti, itself building on Risk Parity Radio's Golden Ratio
Portfolio and u/ApolloDan's TIP-canary post.

## Contributing

The contributor guide — workflow, commit rules, tooling, credentials — lives in
`AGENTS.md` (composed from your agent-config rules; generate it if it isn't
present yet). Architecture decisions live in
[`docs/adr/`](docs/adr/README.md). This README is the human front door and
points at those homes rather than restating them.
