"""Tests for the Partitioner orchestrator."""

import pytest

from teamup.algorithm import BruteForceAlgorithm, PartitioningAlgorithm
from teamup.entity import Entity
from teamup.partitioner import Partitioner
from teamup.scorer import MaxDifferenceScorer, Scorer


class MockAlgorithm(PartitioningAlgorithm):
    """Mock algorithm for testing Partitioner."""

    def partition(
        self, entities, num_groups, scorer, attributes
    ):
        """Return a simple partition (all entities in one group)."""
        from teamup.partition import Partition

        return Partition(groups=[entities], score=0.0)


class MockScorer(Scorer):
    """Mock scorer for testing Partitioner."""

    def score(self, groups, attributes):
        """Always return 0."""
        return 0.0


def test_partitioner_creation() -> None:
    """Test basic Partitioner creation."""
    algorithm = BruteForceAlgorithm()
    scorer = MaxDifferenceScorer()
    partitioner = Partitioner(algorithm, scorer)

    assert partitioner is not None


def test_partitioner_with_mock_algorithm_and_scorer() -> None:
    """Test Partitioner works with mock implementations."""
    algorithm = MockAlgorithm()
    scorer = MockScorer()
    partitioner = Partitioner(algorithm, scorer)

    entities = [Entity(id="e1", attributes={"value": 10})]
    partition = partitioner.partition(entities, 1, ["value"])

    assert len(partition.groups) == 1
    assert partition.score == 0.0


def test_partitioner_with_brute_force_and_max_difference() -> None:
    """Test Partitioner end-to-end with BruteForceAlgorithm + MaxDifferenceScorer."""
    algorithm = BruteForceAlgorithm()
    scorer = MaxDifferenceScorer()
    partitioner = Partitioner(algorithm, scorer)

    entities = [
        Entity(id="e1", attributes={"skill": 10}),
        Entity(id="e2", attributes={"skill": 10}),
        Entity(id="e3", attributes={"skill": 5}),
        Entity(id="e4", attributes={"skill": 5}),
    ]

    partition = partitioner.partition(entities, 2, ["skill"])

    assert len(partition.groups) == 2
    # With [10,5] and [10,5], each sums to 15, difference is 0
    assert partition.score == 0.0


def test_partitioner_empty_entities_raises() -> None:
    """Test that empty entities list raises error."""
    algorithm = BruteForceAlgorithm()
    scorer = MaxDifferenceScorer()
    partitioner = Partitioner(algorithm, scorer)

    with pytest.raises(ValueError, match="entities cannot be empty"):
        partitioner.partition([], 1, ["value"])


def test_partitioner_invalid_num_groups_raises() -> None:
    """Test that invalid num_groups raises error."""
    algorithm = BruteForceAlgorithm()
    scorer = MaxDifferenceScorer()
    partitioner = Partitioner(algorithm, scorer)

    entities = [Entity(id="e1", attributes={"value": 10})]

    with pytest.raises(ValueError, match="num_groups must be at least 1"):
        partitioner.partition(entities, 0, ["value"])


def test_partitioner_empty_attributes_raises() -> None:
    """Test that empty attributes list raises error."""
    algorithm = BruteForceAlgorithm()
    scorer = MaxDifferenceScorer()
    partitioner = Partitioner(algorithm, scorer)

    entities = [Entity(id="e1", attributes={"value": 10})]

    with pytest.raises(ValueError, match="attributes cannot be empty"):
        partitioner.partition(entities, 1, [])


def test_partitioner_algorithm_swapping() -> None:
    """Test that Partitioner allows swapping algorithm without code changes."""
    scorer = MaxDifferenceScorer()
    partitioner1 = Partitioner(BruteForceAlgorithm(), scorer)
    partitioner2 = Partitioner(MockAlgorithm(), scorer)

    entities = [
        Entity(id="e1", attributes={"value": 10}),
        Entity(id="e2", attributes={"value": 20}),
    ]

    # Both partitioners should work without modification to Partitioner class
    partition1 = partitioner1.partition(entities, 2, ["value"])
    partition2 = partitioner2.partition(entities, 2, ["value"])

    assert partition1 is not None
    assert partition2 is not None


def test_partitioner_scorer_swapping() -> None:
    """Test that Partitioner allows swapping scorer without code changes."""
    algorithm = BruteForceAlgorithm()
    partitioner1 = Partitioner(algorithm, MaxDifferenceScorer())
    partitioner2 = Partitioner(algorithm, MockScorer())

    entities = [
        Entity(id="e1", attributes={"value": 10}),
        Entity(id="e2", attributes={"value": 20}),
    ]

    # Both partitioners should work without modification to Partitioner class
    partition1 = partitioner1.partition(entities, 2, ["value"])
    partition2 = partitioner2.partition(entities, 2, ["value"])

    assert partition1 is not None
    assert partition2 is not None


def test_partitioner_multi_attribute_integration() -> None:
    """Integration test: Partitioner with multiple attributes."""
    algorithm = BruteForceAlgorithm()
    scorer = MaxDifferenceScorer()
    partitioner = Partitioner(algorithm, scorer)

    entities = [
        Entity(id="alice", attributes={"strength": 10, "intelligence": 5}),
        Entity(id="bob", attributes={"strength": 8, "intelligence": 8}),
        Entity(id="charlie", attributes={"strength": 12, "intelligence": 4}),
        Entity(id="diana", attributes={"strength": 6, "intelligence": 9}),
    ]

    partition = partitioner.partition(
        entities, 2, ["strength", "intelligence"]
    )

    assert len(partition.groups) == 2
    assert all(len(group) > 0 for group in partition.groups)
    assert partition.score >= 0
