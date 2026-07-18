# AGENTS.md

Precedence: this repo's own docs win over the generic files referenced below (a personal
global rules tree, not committed here).

## Git Workflow

> Concrete realization of **git.md** (and **github.md**, which folds in here — it defines no
> section of its own) for this repo.

### Commits — Conventional Commits

[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/): `type(scope): description`,
imperative lowercase subject ≤50 chars (hard limit 72); `type` ∈ feat/fix/docs/style/refactor/perf/
test/build/ci/chore; `scope` ∈ `data`, `docs`, `src`, `tests`. Breaking change: `type!:` or a
`BREAKING CHANGE:` footer. Blank line, then a body wrapped at 72 explaining _what_ and _why_, never
_how_. `Co-authored-by:` per human contributor; never AI attribution. One logical change per
commit; propose the split before committing.

### Version Control Discipline

- Don't commit or push on your own initiative — show what changed, get approval, commit only that.
- Commit freely on the working branch; `main` stays clean (one squashed commit per merged change,
  not its iteration history).
- Rebase onto latest `main` before merging.
- Never rewrite history you don't own. The only sanctioned force-push is your own just-squashed
  branch, and it aborts if the remote moved. If the remote moved unexpectedly, stop and inspect
  before anything destructive — realign, don't overwrite.

### Branch & PR model — short-lived feature branches + protected main, rebase-merged

> Note: this repo's history to date is entirely direct commits to `main` (no branches, no PRs).
> This section documents the target workflow going forward, per user decision.

1. Fetch and check `origin/main` before branching — a stale base means painful divergence later.
   Branch off it per change; the branch is single-use and short-lived.
2. Commit freely on the feature branch — WIP commits needn't follow the commit style, since only
   the final squashed commit reaches `main`.
3. One logical change per PR. Never bundle unrelated changes to save a round trip.
4. When ready and tested, squash the branch to exactly one Conventional Commit
   (`git reset --soft origin/main && git commit`), then PR → `main`. CI gates on the PR being
   exactly one commit with a Conventional-Commit subject — the two checks rebase-merge relies on,
   since GitHub won't rewrite the message the way squash-merge would.
5. Once green, **rebase-merge**: your single commit lands on `main` verbatim, and the branch
   auto-deletes. No branch reuse or reset step needed — the next change starts a fresh branch off
   `main`.
6. `main` stays releasable, never committed to directly. Merge method is rebase-merge only,
   enforced by GitHub branch protection/rulesets (github.md) — not yet configured; enable before
   relying on this as a hard gate.

### Working iteratively when you can't self-verify

For changes the agent can't confirm alone (e.g. report/chart output that needs eyeballing):
commit locally as checkpoints but hold off push/PR until confirmed — each round-trip is real
overhead for something unvalidated. Once confirmed, squash to one commit for the final state and
push → PR → merge once. Squash before any PR (`git reset --soft origin/main && git commit`) — a
twenty-WIP PR is hard to review. Directly-verifiable work (syntax, dry run, CLI) skips this.

### Shift-left tooling and credential scope

No CI workflow exists yet (`.github/workflows` is empty), so there's nothing to mirror from CI —
the closest local equivalent is `ruff check .` and `python3 -m pytest`; run both before every
commit. `gh` is available — scope it to a fine-grained PAT (contents/PRs/actions read-write, no
Administration) for routine work, elevating explicitly only for the one action that needs admin
(github.md).

### Releases

No version scheme or release automation is set up. `pyproject.toml` carries `version = "0.1.0"`
but nothing cuts tagged releases from it yet — this section doesn't apply until that changes.

---

## What this repo is

<!-- TODO: one paragraph — what problem this backtester/research repo solves, for a reader who
     hasn't read README.md. Seed: README.md already covers the origin (r/LETFs SPY/TIP dual-gate
     strategy) and current phase (Phase 1 backtester, see docs/roadmap.md). -->

## Philosophy

<!-- TODO: any non-obvious principles specific to this repo (e.g. "docs-first, no code until the
     spec is settled" — see docs/roadmap.md's stated approach) that a contributor should know
     before proposing changes. -->

## Structure & conventions

- `src/golden_ratio_dual_gate/` — package code: `signals.py`, `backtest.py`, `metrics.py`,
  `reports.py`, `data/` (per-source fetchers: `prices.py`, `kenneth_french.py`,
  `managed_futures.py`, `signal_history.py`, `splice.py`), `__main__.py` (CLI entry point).
- `tests/` — pytest, one file per module under test.
- `docs/` — strategy spec, sizing rationale, research notes, roadmap. Read before structural
  changes; supersede explicitly rather than letting code and docs drift (per docs/roadmap.md's
  docs-first stance).
- `data/external/` — hand-downloaded data the package can't fetch itself (e.g. SG Trend Index
  CSV; see README.md).

<!-- TODO: name a real exemplar file and a real anti-pattern file for the data/-fetcher pattern
     (one function per source, returning a pd.Series) once more than one convention emerges. -->

## How to verify changes

- `python3 -m pytest` — unit tests (`tests/`).
- `ruff check .` — lint, per `[tool.ruff]` in `pyproject.toml` (line-length 100).
- `python3 -m golden_ratio_dual_gate` — end-to-end: fetches data, runs the backtest, prints the
  headline report. Useful for eyeballing output after a `signals.py`/`backtest.py`/`reports.py`
  change.

<!-- TODO: anything else worth checking before calling a change done (e.g. a specific report
     field or metric to sanity-check by hand). -->
