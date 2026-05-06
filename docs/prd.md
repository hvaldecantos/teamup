# PRD: Balanced Partitioning Library

## Problem Statement

Team formation and group balancing is often done randomly or through captain-selection, which creates inherent statistical imbalances that undermine fair competition. The real competition should be decided by performance and strategy during the event, not by unbalanced team composition.

Users need a flexible, algorithmic way to partition entities (people, players, resources) into balanced groups based on multiple measurable attributes, ensuring no single group has a cumulative advantage.

## Solution

Build a general-purpose Python library that partitions entities into balanced groups by minimizing differences across group attribute sums. The library uses a strategy pattern to allow easy swapping of:
- **Search algorithms** (how to find the best partition)
- **Scoring metrics** (how to evaluate partition quality)

This enables users to start with brute-force solutions for small datasets and upgrade to advanced algorithms (genetic, simulated annealing) as needs evolve.

## User Stories

1. As a developer, I want to partition a list of entities into N groups by their attributes, so that each group is balanced across all attributes.

2. As a developer, I want to define my own entities with arbitrary attributes, so that the library works for any domain (sports, corporate teams, study groups, gaming lobbies).

3. As a developer, I want to use a brute-force algorithm for small datasets (<20 entities), so that I can find the optimal partition.

4. As a developer, I want to easily swap to a different algorithm in the future, so that I don't have to rewrite my integration when I have larger datasets.

5. As a developer, I want to use "maximum difference" as the scoring metric by default, so that I can balance teams with minimal configuration.

6. As a developer, I want to define custom scoring metrics, so that I can optimize for domain-specific balance criteria.

7. As a developer, I want to partition into any number of groups with variable sizes, so that I have flexibility in team configuration.

8. As a developer, I want all attributes weighted equally by default, so that no single attribute dominates the balancing.

9. As a developer, I want a clean builder API, so that I can configure the partitioner in a readable, extensible way.

10. As a developer, I want a Partition result object that includes the groups and their score, so that I can understand the quality of the partitioning.

11. As a developer, I want type-safe entity handling, so that the library catches attribute errors early.

12. As a developer, I want comprehensive test coverage, so that I can trust the library's correctness.

## Implementation Decisions

### Architecture & Strategy Pattern

The library will use the strategy pattern for two layers:
- **PartitioningAlgorithm**: Encapsulates different search strategies (BruteForce, future: Genetic, SimulatedAnnealing)
- **Scorer**: Encapsulates different evaluation metrics (MaxDifference, future: Variance, EuclideanDistance)

These strategies are injected into a `Partitioner` orchestrator that coordinates the search and scoring.

### Core Modules

1. **Entity & Data Models**
   - `Entity`: Wraps an entity with its identifier and attributes dictionary
   - `Partition`: Result object containing the groups (list of list of entities) and their quality score

2. **Strategy Interfaces**
   - `PartitioningAlgorithm` (abstract): Defines interface for partition search implementations
   - `Scorer` (abstract): Defines interface for scoring partition quality

3. **Algorithm Implementations**
   - `BruteForceAlgorithm`: Exhaustively searches all permutations to find the optimal partition. Works well for <20 entities.

4. **Scorer Implementations**
   - `MaxDifferenceScorer`: For each attribute, computes (max_group_sum - min_group_sum). Returns the maximum across all attributes as the score. Lower is better.

5. **Builder & Orchestrator**
   - `PartitionerBuilder`: Fluent builder for configuring and creating Partitioner instances with sensible defaults
   - `Partitioner` (deep module): Main coordinator that orchestrates the algorithm and scorer. Resilient to strategy changes.

6. **Utilities**
   - Internal helpers: permutation generation, attribute summation per group, validation

### API Contract

The primary user-facing API:

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

# result.groups -> [[Entity, Entity], [Entity, Entity]]
# result.score -> 3 (the max difference score)
```

### Design Decisions

- **Brute Force as MVP**: Simple to implement, correct by exhaustion. Limit to <20 entities.
- **All attributes equally weighted by default**: Simplifies API. Users can extend Scorer to implement weighted versions.
- **Maximum difference as default scoring**: Easy to understand, domain-agnostic.
- **Partition result object**: Provides future extensibility (add timing info, attempt count, etc. without API change).
- **Pluggable strategies**: Scored high on extensibility; trivial to add new algorithms or scorers.

## Testing Decisions

### Test Philosophy
- Test external behavior, not implementation details
- Focus on `Partitioner` as the main contract
- Validate that partitions are correctly balanced, not internal algorithm steps
- Use realistic test data (player attributes, etc.)

### Modules to Test

**High Priority (comprehensive coverage):**
- `Partitioner`: Integration of algorithm + scorer; verify correct partition generation and scoring
- `MaxDifferenceScorer`: Verify scoring logic on various attribute distributions

**Medium Priority (happy path + edge cases):**
- `BruteForceAlgorithm`: Verify it finds optimal solutions; test on small datasets
- `PartitionerBuilder`: Verify configuration and default injection

**Low Priority (minimal, for confidence):**
- `Entity`, `Partition`: Simple data containers; basic construction tests only
- Utilities: Test in context of higher-level tests

### Test Style
- Use pytest fixtures for common test data (player lists, attributes)
- Parametrize tests for multiple group counts, entity sizes, attribute combinations
- Include regression tests once optimal partitions are verified for small datasets

## Out of Scope

- Weighted attributes (can be added as Scorer extension)
- Constraint-based partitioning (e.g., "these two must be on same team")
- Advanced algorithms (genetic, simulated annealing) in MVP
- Web UI or CLI interface
- Integration with sports league management systems
- Performance optimization for large datasets (>20 entities)
- Attribute normalization or preprocessing

## Further Notes

### Future Extensions (Not in MVP)

Once the MVP is solid, natural extensions include:
- `GeneticAlgorithmStrategy` and `SimulatedAnnealingStrategy` for larger datasets
- `VarianceScorer` and `EuclideanDistanceScorer` for alternative balance metrics
- Weighted attribute support in Scorer
- Constraint plugins for team rules
- Benchmarking suite for algorithm comparison

### Open Questions for Future Development

- Should Entity support lazy attribute access (e.g., computed/derived attributes)?
- Should Partitioner cache results for repeated calls with same data?
- How should the library handle missing or invalid attributes in entities?

