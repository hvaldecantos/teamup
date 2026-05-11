"""Tests for partitioning algorithms."""

import pytest

from teamup.algorithm import BruteForceAlgorithm, PartitioningAlgorithm
from teamup.entity import Entity
from teamup.scorer import MaxDifferenceScorer


def test_brute_force_algorithm_is_partitioning_algorithm() -> None:
    """Test that BruteForceAlgorithm implements PartitioningAlgorithm."""
    algorithm = BruteForceAlgorithm()
    assert isinstance(algorithm, PartitioningAlgorithm)


def test_partitioning_algorithm_is_abstract() -> None:
    """Test that PartitioningAlgorithm is abstract."""
    with pytest.raises(TypeError):
        PartitioningAlgorithm()  # type: ignore


def test_brute_force_single_group() -> None:
    """Test BruteForceAlgorithm with a single group."""
    entities = [
        Entity(id="e1", attributes={"value": 10}),
        Entity(id="e2", attributes={"value": 20}),
    ]
    algorithm = BruteForceAlgorithm()
    scorer = MaxDifferenceScorer()

    partition = algorithm.partition(entities, 1, scorer, ["value"])

    assert len(partition.groups) == 1
    assert len(partition.groups[0]) == 2
    assert partition.score == 0.0  # Single group has no difference


def test_brute_force_two_groups_balanced() -> None:
    """Test BruteForceAlgorithm finds optimal partition for two balanced groups."""
    # Two entities with equal values should partition evenly
    entities = [
        Entity(id="e1", attributes={"value": 10}),
        Entity(id="e2", attributes={"value": 10}),
    ]
    algorithm = BruteForceAlgorithm()
    scorer = MaxDifferenceScorer()

    partition = algorithm.partition(entities, 2, scorer, ["value"])

    assert len(partition.groups) == 2
    assert partition.score == 0.0  # Perfectly balanced


def test_brute_force_three_entities_two_groups() -> None:
    """Test BruteForceAlgorithm with three entities into two groups."""
    # Three entities: [5, 10, 10]
    # Best partition: [5, 10] and [10] -> sums 15 and 10 -> diff 5
    # Another: [5] and [10, 10] -> sums 5 and 20 -> diff 15
    entities = [
        Entity(id="e1", attributes={"value": 5}),
        Entity(id="e2", attributes={"value": 10}),
        Entity(id="e3", attributes={"value": 10}),
    ]
    algorithm = BruteForceAlgorithm()
    scorer = MaxDifferenceScorer()

    partition = algorithm.partition(entities, 2, scorer, ["value"])

    assert len(partition.groups) == 2
    # Optimal score is 5 (diff between 15 and 10)
    assert partition.score == 5.0


def test_brute_force_multiple_attributes() -> None:
    """Test BruteForceAlgorithm with multiple attributes."""
    entities = [
        Entity(id="e1", attributes={"skill": 10, "power": 5}),
        Entity(id="e2", attributes={"skill": 10, "power": 5}),
    ]
    algorithm = BruteForceAlgorithm()
    scorer = MaxDifferenceScorer()

    partition = algorithm.partition(
        entities, 2, scorer, ["skill", "power"]
    )

    assert len(partition.groups) == 2
    assert partition.score == 0.0  # Perfectly balanced on both attributes


def test_brute_force_num_groups_greater_than_entities_raises() -> None:
    """Test that partitioning with more groups than entities raises error."""
    entities = [Entity(id="e1", attributes={"value": 10})]
    algorithm = BruteForceAlgorithm()
    scorer = MaxDifferenceScorer()

    with pytest.raises(ValueError, match="num_groups cannot exceed"):
        algorithm.partition(entities, 2, scorer, ["value"])


def test_brute_force_invalid_num_groups_raises() -> None:
    """Test that invalid num_groups raises error."""
    entities = [Entity(id="e1", attributes={"value": 10})]
    algorithm = BruteForceAlgorithm()
    scorer = MaxDifferenceScorer()

    with pytest.raises(ValueError, match="num_groups must be at least 1"):
        algorithm.partition(entities, 0, scorer, ["value"])


def test_brute_force_empty_attributes_raises() -> None:
    """Test that empty attributes list raises error."""
    entities = [Entity(id="e1", attributes={"value": 10})]
    algorithm = BruteForceAlgorithm()
    scorer = MaxDifferenceScorer()

    with pytest.raises(ValueError, match="attributes cannot be empty"):
        algorithm.partition(entities, 1, scorer, [])


def test_brute_force_known_optimal_partition() -> None:
    """Test that BruteForceAlgorithm finds known-optimal partition."""
    # Known regression case: partition into 2 groups with minimal difference
    # Entities: [1, 2, 3, 4] -> total 10
    # Optimal: [1, 4] and [2, 3] -> both sum to 5 -> diff 0
    entities = [
        Entity(id="e1", attributes={"value": 1}),
        Entity(id="e2", attributes={"value": 2}),
        Entity(id="e3", attributes={"value": 3}),
        Entity(id="e4", attributes={"value": 4}),
    ]
    algorithm = BruteForceAlgorithm()
    scorer = MaxDifferenceScorer()

    partition = algorithm.partition(entities, 2, scorer, ["value"])

    assert len(partition.groups) == 2
    assert partition.score == 0.0  # Perfectly balanced

    # Verify that both groups sum to 5
    group1_sum = sum(e["value"] for e in partition.groups[0])
    group2_sum = sum(e["value"] for e in partition.groups[1])
    assert group1_sum == 5
    assert group2_sum == 5
