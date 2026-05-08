# Issue 040: PartitionerBuilder & full API contract

**Type**: AFK
**Status**: to-do

## What to build

Expose the library's complete public API through a fluent `PartitionerBuilder`. The builder defaults to `BruteForceAlgorithm` and `MaxDifferenceScorer` so users can get started with zero configuration. It supports partitioning into any number of groups and accepts an `attributes_to_balance` list. The finished API matches the contract published in the PRD exactly:

```python
partitioner = PartitionerBuilder() \
    .with_algorithm(BruteForceAlgorithm()) \
    .with_scorer(MaxDifferenceScorer()) \
    .build()

result = partitioner.partition(
    entities=[Entity("Alice", {"speed": 8, "skill": 9}), ...],
    num_groups=2,
    attributes_to_balance=["speed", "skill"]
)
# result.groups -> [[Entity, ...], [Entity, ...]]
# result.score  -> <float>
```

## Acceptance criteria

- [ ] `PartitionerBuilder` fluent API works with zero configuration (defaults applied automatically)
- [ ] `with_algorithm()` and `with_scorer()` allow explicit overrides
- [ ] `partition()` accepts `num_groups` and `attributes_to_balance`; both are validated at call time
- [ ] All public symbols are exported from the top-level package `__init__.py`
- [ ] Integration tests use the exact API contract snippet above and cover 2-group and 3-group scenarios
- [ ] `num_groups` and `attributes_to_balance` validation raises clear errors on bad input

## Blocked by

- Issue #030 (BruteForce algorithm & Partitioner orchestrator)
