# Issue 020: Partition result model & MaxDifferenceScorer

**Type**: AFK
**Status**: to-do

## What to build

Introduce the `Partition` result object and the scoring layer. Define an abstract `Scorer` interface so that scoring strategies are interchangeable. Implement `MaxDifferenceScorer` as the default: for each attribute it computes `max_group_sum − min_group_sum` across groups, then returns the maximum of those per-attribute differences as the overall score (lower is better). Also implement the `Partition` result object that holds the final groups and their score.

## Acceptance criteria

- [x] Abstract `Scorer` interface is defined with a `score(groups, attributes)` method signature
- [x] `MaxDifferenceScorer` implements `Scorer` and returns the correct score for known attribute distributions
- [x] `Partition` result object stores groups (list of list of `Entity`) and a numeric score
- [x] Tests cover `MaxDifferenceScorer` on multiple attribute distributions, including ties, single-attribute, and multi-attribute cases
- [x] Tests cover basic `Partition` construction

## Blocked by

- Issue #010 (project scaffold & `Entity` model)
