# Balancing groups

A general-purpose Python library for partitioning entities into balanced groups by minimizing attribute differences across groups.

## When to use

When forming teams or any N-way split where some kind of fairness matters.

## How it will works

- **`MaxDifferenceScorer`** — for each attribute, computes `max_group_sum − min_group_sum` across all groups, then returns the maximum across all attributes. Lower is better.
- **`BruteForceAlgorithm`** — exhaustively tries all partitions to find the optimal split. Suitable for <20 entities.
- Both are pluggable via the strategy pattern; swap in custom algorithms or scorers without changing the rest of your code.

## Architecture

```
Entity / Partition  →  data models
Scorer              →  evaluates partition quality
PartitioningAlgorithm → searches for the best partition
Partitioner         →  orchestrates algorithm + scorer
PartitionerBuilder  →  fluent builder with sensible defaults
```

## Requirements

Python 3.10+. See `pyproject.toml` for dependencies.
