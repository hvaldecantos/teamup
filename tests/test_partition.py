"""Tests for the Partition result object."""

from teamup.entity import Entity
from teamup.partition import Partition


def test_partition_creation_basic() -> None:
    """Test basic Partition creation."""
    group1 = [Entity(id="e1", attributes={"value": 10})]
    group2 = [Entity(id="e2", attributes={"value": 20})]
    groups = [group1, group2]
    score = 10.0

    partition = Partition(groups=groups, score=score)

    assert partition.groups == groups
    assert partition.score == score


def test_partition_creation_with_integer_score() -> None:
    """Test Partition creation with integer score."""
    group1 = [Entity(id="e1", attributes={"value": 10})]
    groups = [group1]
    score = 5

    partition = Partition(groups=groups, score=score)

    assert partition.score == 5
    assert isinstance(partition.score, int)


def test_partition_creation_with_float_score() -> None:
    """Test Partition creation with float score."""
    group1 = [Entity(id="e1", attributes={"value": 10})]
    groups = [group1]
    score = 5.5

    partition = Partition(groups=groups, score=score)

    assert partition.score == 5.5
    assert isinstance(partition.score, float)


def test_partition_multiple_groups() -> None:
    """Test Partition with multiple groups."""
    group1 = [
        Entity(id="e1", attributes={"value": 10}),
        Entity(id="e2", attributes={"value": 15}),
    ]
    group2 = [
        Entity(id="e3", attributes={"value": 20}),
    ]
    group3 = [
        Entity(id="e4", attributes={"value": 25}),
        Entity(id="e5", attributes={"value": 30}),
    ]
    groups = [group1, group2, group3]
    score = 15.0

    partition = Partition(groups=groups, score=score)

    assert len(partition.groups) == 3
    assert len(partition.groups[0]) == 2
    assert len(partition.groups[1]) == 1
    assert len(partition.groups[2]) == 2


def test_partition_empty_score() -> None:
    """Test Partition with zero score."""
    group1 = [Entity(id="e1", attributes={"value": 10})]
    groups = [group1]

    partition = Partition(groups=groups, score=0)

    assert partition.score == 0


def test_partition_negative_score() -> None:
    """Test Partition with negative score (unusual but valid)."""
    group1 = [Entity(id="e1", attributes={"value": 10})]
    groups = [group1]

    partition = Partition(groups=groups, score=-5.0)

    assert partition.score == -5.0


def test_partition_large_score() -> None:
    """Test Partition with large score value."""
    group1 = [Entity(id="e1", attributes={"value": 10})]
    groups = [group1]
    large_score = 999999.99

    partition = Partition(groups=groups, score=large_score)

    assert partition.score == large_score
