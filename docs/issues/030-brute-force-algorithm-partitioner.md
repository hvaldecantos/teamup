# Issue 030: BruteForce algorithm & Partitioner orchestrator

**Type**: AFK
**Status**: done

## What to build

Introduce the algorithm layer and the `Partitioner` orchestrator. Define an abstract `PartitioningAlgorithm` interface so future algorithms (genetic, simulated annealing) can be swapped in without touching the orchestrator. Implement `BruteForceAlgorithm` that exhaustively searches all permutations of entities across groups to find the partition with the lowest score. Wire everything together in `Partitioner`, which accepts any `PartitioningAlgorithm` and any `Scorer` and exposes a single `partition()` method.

## Acceptance criteria

- [x] Abstract `PartitioningAlgorithm` interface is defined
- [x] `BruteForceAlgorithm` finds the provably optimal partition for small datasets (≤20 entities)
- [x] `Partitioner` orchestrates the algorithm and scorer and returns a `Partition` result
- [x] Swapping the algorithm or scorer in `Partitioner` requires no changes to `Partitioner` itself
- [x] Tests verify that `BruteForceAlgorithm` finds the known-optimal partition for regression datasets
- [x] Integration tests run `Partitioner` end-to-end with `BruteForceAlgorithm` + `MaxDifferenceScorer`

## Blocked by

- Issue #020 (Partition result model & MaxDifferenceScorer)
