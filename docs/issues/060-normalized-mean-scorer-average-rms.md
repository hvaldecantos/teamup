# Issue 060: `MeanAverageDifferenceScorer` and `MeanRMSDifferenceScorer`

**Type**: AFK
**Status**: open

## What to build

Extend `scorer.py` with two additional concrete subclasses of `NormalizedMeanScorer`:

- `MeanAverageDifferenceScorer` — overrides `_combine()` to return the arithmetic mean of per-attribute differences: `sum(differences) / len(differences)`.
- `MeanRMSDifferenceScorer` — overrides `_combine()` to return the root mean square: `(sum(d ** 2 for d in differences) / len(differences)) ** 0.5`.

Both classes are thin wrappers; all normalization and orchestration logic lives in the base class from Issue #050.

Tests go in `tests/test_scorer.py`. For each subclass: verify it instantiates as a `Scorer`, and verify correct scores on a known multi-attribute partition where the expected value can be hand-computed from the average and RMS formulas respectively. Convenience subclass tests mirror the structure already established for `MeanMaxDifferenceScorer`.

No changes to `NormalizedMeanScorer`, `MeanMaxDifferenceScorer`, `Partitioner`, `PartitionerBuilder`, `Entity`, `Partition`, or `MaxDifferenceScorer`.

## Acceptance criteria

- [ ] `MeanAverageDifferenceScorer` overrides `_combine()` to return `sum(differences) / len(differences)`
- [ ] `MeanRMSDifferenceScorer` overrides `_combine()` to return `(sum(d ** 2 for d in differences) / len(differences)) ** 0.5`
- [ ] Both subclasses are `Scorer` instances
- [ ] Tests in `tests/test_scorer.py` verify correct scores for known distributions using average and RMS formulas
- [ ] No logic duplicated from `NormalizedMeanScorer` base class

## Blocked by

- Issue #050 (abstract `NormalizedMeanScorer` base class and `MeanMaxDifferenceScorer`)
