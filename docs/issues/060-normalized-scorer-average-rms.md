# Issue 060: `NormalizedAverageDifferenceScorer` and `NormalizedRMSDifferenceScorer`

**Type**: AFK
**Status**: open

## What to build

Extend `scorer.py` with two additional concrete subclasses of `NormalizedScorer`:

- `NormalizedAverageDifferenceScorer` — overrides `_combine()` to return the arithmetic mean of per-attribute differences: `sum(differences) / len(differences)`.
- `NormalizedRMSDifferenceScorer` — overrides `_combine()` to return the root mean square: `(sum(d ** 2 for d in differences) / len(differences)) ** 0.5`.

Both classes are thin wrappers; all normalization and orchestration logic lives in the base class from Issue #055.

Tests go in `tests/test_scorer.py`. For each subclass: verify it instantiates as a `Scorer`, and verify correct scores on a known multi-attribute partition where the expected value can be hand-computed from the average and RMS formulas respectively. Convenience subclass tests mirror the structure already established for `NormalizedMaxDifferenceScorer`.

No changes to `NormalizedScorer`, `NormalizedMaxDifferenceScorer`, `Partitioner`, `PartitionerBuilder`, `Entity`, `Partition`, or `MaxDifferenceScorer`.

## Acceptance criteria

- [ ] `NormalizedAverageDifferenceScorer` overrides `_combine()` to return `sum(differences) / len(differences)`
- [ ] `NormalizedRMSDifferenceScorer` overrides `_combine()` to return `(sum(d ** 2 for d in differences) / len(differences)) ** 0.5`
- [ ] Both subclasses are `Scorer` instances
- [ ] Tests in `tests/test_scorer.py` verify correct scores for known distributions using average and RMS formulas
- [ ] No logic duplicated from `NormalizedScorer` base class

## Blocked by

- Issue #055 (rename to `NormalizedScorer` and switch normalized aggregation to sums)
