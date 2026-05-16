# Issue 050: Abstract `NormalizedMeanScorer` base class and `MeanMaxDifferenceScorer`

**Type**: AFK
**Status**: open

## What to build

Add an abstract `NormalizedMeanScorer` base class to `scorer.py` alongside `MaxDifferenceScorer`. The class implements the `Scorer` interface and defines a two-phase scoring algorithm:

1. A protected `_normalize(groups, attributes)` method that computes global min/max per attribute across all entities in all groups and returns normalized values in `[0, 1]`. Zero-variance attributes (all entities share the same value) produce `0.0` for all normalized values.
2. An abstract `_combine(differences)` template method that subclasses override to turn a list of per-attribute `max_group_mean − min_group_mean` values into a single score.
3. A concrete `score(groups, attributes)` method that orchestrates `_normalize()` → per-attribute group means → per-attribute differences → `_combine()`. Raises `ValueError` on empty groups, empty attributes, or any empty group — matching the contract of `MaxDifferenceScorer`.

Implement `MeanMaxDifferenceScorer(NormalizedMeanScorer)` as the first concrete subclass, overriding `_combine()` to return `max(differences)`. This subclass is the conservative default and is used to exercise the full algorithm in tests.

All tests go in `tests/test_scorer.py`. Use `MeanMaxDifferenceScorer` as the concrete class for all algorithm-level tests: balanced groups (score 0), full-range unbalanced groups (score 1.0), multiple entities per group, multiple attributes, zero-variance attributes, three or more groups, floating-point values, and all error cases. Add an instantiation test confirming `MeanMaxDifferenceScorer` satisfies the `Scorer` interface.

No changes to `Partitioner`, `PartitionerBuilder`, `Entity`, `Partition`, or `MaxDifferenceScorer`.

## Acceptance criteria

- [ ] `NormalizedMeanScorer` is abstract and cannot be instantiated directly
- [ ] `_normalize()` computes global min/max across all groups; zero-variance attributes yield `0.0`
- [ ] `_combine()` is abstract; `NormalizedMeanScorer` does not implement it
- [ ] `score()` raises `ValueError` for empty groups, empty attributes, or any empty group
- [ ] `MeanMaxDifferenceScorer` overrides `_combine()` to return `max(differences)`
- [ ] `MeanMaxDifferenceScorer` is a `Scorer` instance
- [ ] Tests in `tests/test_scorer.py` cover: balanced groups, full-range unbalanced (score 1.0), multiple entities per group, multiple attributes, zero-variance attribute, three or more groups, floating-point values, and all error cases

## Blocked by

- Issue #020 (`Scorer` abstract interface and `MaxDifferenceScorer`)
