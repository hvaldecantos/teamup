# Issue 055: Rename to `NormalizedScorer` and switch normalized aggregation to sums

**Type**: AFK
**Status**: done

## What to build

Update the normalized scorer model so it reflects total normalized group contribution instead of per-entity average contribution.

Build a thin vertical slice that includes:

1. Rename the abstract base scorer from `NormalizedMeanScorer` to `NormalizedScorer`.
2. Keep global attribute normalization to `[0, 1]` unchanged.
3. Change group aggregation inside normalized scoring from mean to sum for each attribute.
4. Compute per-attribute difference as `max_group_sum - min_group_sum`.
5. Keep `MeanMaxDifferenceScorer` as the concrete max combiner strategy, inheriting from the renamed base.
6. Keep validation/error contracts unchanged for empty groups, empty attributes, and empty inner groups.
7. Preserve a transition alias from `NormalizedMeanScorer` to `NormalizedScorer` for compatibility during migration.
8. Update scorer tests and terminology so expected behavior is explicitly sum-based and naming is consistent.

This issue should be implemented without changing partitioner orchestration behavior or algorithm search behavior.

## Acceptance criteria

- [x] `NormalizedScorer` exists as the abstract normalized base scorer.
- [x] The normalized scoring pipeline aggregates group values by sum, not mean.
- [x] Per-attribute differences are computed from normalized group sums.
- [x] `MeanMaxDifferenceScorer` remains a valid `Scorer` and uses max-combination behavior.
- [x] Existing validation/error behavior for invalid input remains unchanged.
- [x] Backward-compatible aliasing allows `NormalizedMeanScorer` imports during migration.
- [x] Tests in scorer test suite reflect sum-based semantics and pass.
- [x] Documentation/comments in the scorer area no longer describe mean-based behavior for this scorer.

## Blocked by

- None - can start immediately
