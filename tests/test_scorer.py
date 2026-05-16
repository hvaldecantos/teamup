"""Tests for the Scorer interface and implementations."""

import pytest

from teamup.entity import Entity
from teamup.scorer import MaxDifferenceScorer, MeanMaxDifferenceScorer, NormalizedMeanScorer, Scorer


def test_scorer_is_abstract() -> None:
    """Test that Scorer is an abstract interface."""
    # Should not be able to instantiate Scorer directly
    with pytest.raises(TypeError):
        Scorer()  # type: ignore


def test_max_difference_scorer_instantiation() -> None:
    """Test that MaxDifferenceScorer can be instantiated."""
    scorer = MaxDifferenceScorer()
    assert isinstance(scorer, Scorer)

def test_max_difference_scorer_single_group() -> None:
    """Test MaxDifferenceScorer with a single group."""
    # Single group with a single entity
    group1 = [Entity(id="e1", attributes={"value": 10})]
    groups = [group1]

    scorer = MaxDifferenceScorer()
    score = scorer.score(groups, ["value"])

    assert score == 0.0

def test_max_difference_scorer_single_attribute_balanced() -> None:
    """Test MaxDifferenceScorer with a single attribute, balanced groups."""
    # Two groups with equal sums
    group1 = [Entity(id="e1", attributes={"value": 10})]
    group2 = [Entity(id="e2", attributes={"value": 10})]
    groups = [group1, group2]

    scorer = MaxDifferenceScorer()
    score = scorer.score(groups, ["value"])

    assert score == 0.0


def test_max_difference_scorer_single_attribute_unbalanced() -> None:
    """Test MaxDifferenceScorer with a single attribute, unbalanced groups."""
    # Two groups with different sums
    group1 = [Entity(id="e1", attributes={"value": 20})]
    group2 = [Entity(id="e2", attributes={"value": 10})]
    groups = [group1, group2]

    scorer = MaxDifferenceScorer()
    score = scorer.score(groups, ["value"])

    # max_sum=20, min_sum=10, difference=10
    assert score == 10.0


def test_max_difference_scorer_multi_attribute() -> None:
    """Test MaxDifferenceScorer with multiple attributes."""
    group1 = [Entity(id="e1", attributes={"a": 10, "b": 5})]
    group2 = [Entity(id="e2", attributes={"a": 10, "b": 15})]
    groups = [group1, group2]

    scorer = MaxDifferenceScorer()
    score = scorer.score(groups, ["a", "b"])

    # Attribute 'a': group1_sum=10, group2_sum=10, difference=0
    # Attribute 'b': group1_sum=5, group2_sum=15, difference=10
    # Overall score is max(0, 10) = 10
    assert score == 10.0


def test_max_difference_scorer_multi_attribute_multiple_groups() -> None:
    """Test MaxDifferenceScorer with multiple attributes and multiple groups."""
    group1 = [Entity(id="e1", attributes={"a": 5, "b": 10})]
    group2 = [Entity(id="e2", attributes={"a": 10, "b": 5})]
    group3 = [Entity(id="e3", attributes={"a": 5, "b": 10})]
    groups = [group1, group2, group3]

    scorer = MaxDifferenceScorer()
    score = scorer.score(groups, ["a", "b"])

    # Attribute 'a': sums are [5, 10, 5], max=10, min=5, difference=5
    # Attribute 'b': sums are [10, 5, 10], max=10, min=5, difference=5
    # Overall score is max(5, 5) = 5
    assert score == 5.0


def test_max_difference_scorer_multi_entity_groups() -> None:
    """Test MaxDifferenceScorer with groups containing multiple entities."""
    # Group 1 has two entities with values 3 and 7 (sum=10)
    # Group 2 has two entities with values 5 and 5 (sum=10)
    group1 = [
        Entity(id="e1", attributes={"value": 3}),
        Entity(id="e2", attributes={"value": 7}),
    ]
    group2 = [
        Entity(id="e3", attributes={"value": 5}),
        Entity(id="e4", attributes={"value": 5}),
    ]
    groups = [group1, group2]

    scorer = MaxDifferenceScorer()
    score = scorer.score(groups, ["value"])

    # Both groups have sum=10, so difference=0
    assert score == 0.0


def test_max_difference_scorer_floating_point() -> None:
    """Test MaxDifferenceScorer with floating point attribute values."""
    group1 = [Entity(id="e1", attributes={"value": 10.5})]
    group2 = [Entity(id="e2", attributes={"value": 10.3})]
    groups = [group1, group2]

    scorer = MaxDifferenceScorer()
    score = scorer.score(groups, ["value"])

    assert abs(score - 0.2) < 1e-9


def test_max_difference_scorer_empty_groups_error() -> None:
    """Test that empty groups list raises ValueError."""
    scorer = MaxDifferenceScorer()

    with pytest.raises(ValueError, match="groups cannot be empty"):
        scorer.score([], ["value"])


def test_max_difference_scorer_empty_attributes_error() -> None:
    """Test that empty attributes list raises ValueError."""
    group1 = [Entity(id="e1", attributes={"value": 10})]
    groups = [group1]

    scorer = MaxDifferenceScorer()

    with pytest.raises(ValueError, match="attributes cannot be empty"):
        scorer.score(groups, [])


def test_max_difference_scorer_empty_group_error() -> None:
    """Test that empty group (no entities) raises ValueError."""
    group1 = [Entity(id="e1", attributes={"value": 10})]
    group2 = []  # Empty group
    groups = [group1, group2]

    scorer = MaxDifferenceScorer()

    with pytest.raises(ValueError, match="all groups must be non-empty"):
        scorer.score(groups, ["value"])


def test_max_difference_scorer_missing_attribute_error() -> None:
    """Test that missing attribute in entity raises AttributeError."""
    group1 = [Entity(id="e1", attributes={"value": 10})]
    group2 = [Entity(id="e2", attributes={"other": 5})]  # Missing 'value'
    groups = [group1, group2]

    scorer = MaxDifferenceScorer()

    with pytest.raises(AttributeError):
        scorer.score(groups, ["value"])


def test_max_difference_scorer_complex_case() -> None:
    """Test MaxDifferenceScorer with a complex realistic case."""
    # Create 3 groups with 3 attributes each
    group1 = [
        Entity(id="e1", attributes={"skill_a": 80,
               "skill_b": 70, "skill_c": 60}),
        Entity(id="e2", attributes={"skill_a": 60,
               "skill_b": 80, "skill_c": 70}),
    ]
    group2 = [
        Entity(id="e3", attributes={"skill_a": 70,
               "skill_b": 60, "skill_c": 80}),
    ]
    group3 = [
        Entity(id="e4", attributes={"skill_a": 75,
               "skill_b": 75, "skill_c": 75}),
    ]
    groups = [group1, group2, group3]

    scorer = MaxDifferenceScorer()
    score = scorer.score(groups, ["skill_a", "skill_b", "skill_c"])

    # Group sums:
    # Group 1: skill_a=140, skill_b=150, skill_c=130
    # Group 2: skill_a=70, skill_b=60, skill_c=80
    # Group 3: skill_a=75, skill_b=75, skill_c=75
    # Differences:
    # skill_a: 140-70=70
    # skill_b: 150-60=90
    # skill_c: 130-75=55
    # Overall: max(70, 90, 55) = 90
    assert score == 90.0


# ---------------------------------------------------------------------------
# NormalizedMeanScorer / MeanMaxDifferenceScorer tests
# ---------------------------------------------------------------------------


def test_normalized_mean_scorer_is_abstract() -> None:
    """NormalizedMeanScorer cannot be instantiated directly."""
    with pytest.raises(TypeError):
        NormalizedMeanScorer()  # type: ignore


def test_mean_max_difference_scorer_instantiation() -> None:
    """MeanMaxDifferenceScorer is a Scorer instance."""
    scorer = MeanMaxDifferenceScorer()
    assert isinstance(scorer, Scorer)


def test_mean_max_difference_scorer_balanced_groups() -> None:
    """Balanced groups produce a score of 0.0."""
    group1 = [Entity(id="e1", attributes={"value": 5})]
    group2 = [Entity(id="e2", attributes={"value": 5})]

    scorer = MeanMaxDifferenceScorer()
    assert scorer.score([group1, group2], ["value"]) == 0.0


def test_mean_max_difference_scorer_full_range_unbalanced() -> None:
    """Groups at opposite ends of the value range produce a score of 1.0."""
    group1 = [Entity(id="e1", attributes={"value": 0})]
    group2 = [Entity(id="e2", attributes={"value": 100})]

    scorer = MeanMaxDifferenceScorer()
    assert scorer.score([group1, group2], ["value"]) == 1.0


def test_mean_max_difference_scorer_multiple_entities_per_group() -> None:
    """Score is based on group means, not raw sums."""
    # Group1 mean = (0+100)/2 = 50, normalized mean = 0.5
    # Group2 mean = (50+50)/2 = 50, normalized mean = 0.5
    # Difference = 0.0
    group1 = [
        Entity(id="e1", attributes={"value": 0}),
        Entity(id="e2", attributes={"value": 100}),
    ]
    group2 = [
        Entity(id="e3", attributes={"value": 50}),
        Entity(id="e4", attributes={"value": 50}),
    ]

    scorer = MeanMaxDifferenceScorer()
    assert scorer.score([group1, group2], ["value"]) == 0.0


def test_mean_max_difference_scorer_multiple_attributes() -> None:
    """_combine() returns max across per-attribute differences."""
    # Attribute 'a': group1 = [0], group2 = [100] → normalized means 0.0 vs 1.0 → diff 1.0
    # Attribute 'b': group1 = [50], group2 = [50] → normalized means 0.5 vs 0.5 → diff 0.0
    # _combine = max(1.0, 0.0) = 1.0
    group1 = [Entity(id="e1", attributes={"a": 0, "b": 50})]
    group2 = [Entity(id="e2", attributes={"a": 100, "b": 50})]

    scorer = MeanMaxDifferenceScorer()
    assert scorer.score([group1, group2], ["a", "b"]) == 1.0


def test_mean_max_difference_scorer_zero_variance_attribute() -> None:
    """Zero-variance attribute contributes 0.0 to differences."""
    # Attribute 'const': all entities have value 7 → normalized = 0.0 everywhere → diff 0.0
    # Attribute 'v':     group1=0, group2=10 → diff 1.0
    # _combine = max(0.0, 1.0) = 1.0
    group1 = [Entity(id="e1", attributes={"const": 7, "v": 0})]
    group2 = [Entity(id="e2", attributes={"const": 7, "v": 10})]

    scorer = MeanMaxDifferenceScorer()
    assert scorer.score([group1, group2], ["const", "v"]) == 1.0


def test_mean_max_difference_scorer_three_groups() -> None:
    """Score works correctly with three or more groups."""
    # Attribute 'v' values: group1=0, group2=50, group3=100
    # Normalized means: 0.0, 0.5, 1.0 → diff = 1.0 - 0.0 = 1.0
    group1 = [Entity(id="e1", attributes={"v": 0})]
    group2 = [Entity(id="e2", attributes={"v": 50})]
    group3 = [Entity(id="e3", attributes={"v": 100})]

    scorer = MeanMaxDifferenceScorer()
    assert scorer.score([group1, group2, group3], ["v"]) == 1.0


def test_mean_max_difference_scorer_floating_point_values() -> None:
    """Score is computed correctly for floating-point attribute values."""
    group1 = [Entity(id="e1", attributes={"v": 1.0})]
    group2 = [Entity(id="e2", attributes={"v": 3.0})]
    # global min=1.0, max=3.0
    # normalized: group1 = 0.0, group2 = 1.0 → diff = 1.0
    scorer = MeanMaxDifferenceScorer()
    assert scorer.score([group1, group2], ["v"]) == pytest.approx(1.0)


def test_mean_max_difference_scorer_empty_groups_error() -> None:
    """Raises ValueError when groups list is empty."""
    scorer = MeanMaxDifferenceScorer()
    with pytest.raises(ValueError, match="groups cannot be empty"):
        scorer.score([], ["value"])


def test_mean_max_difference_scorer_empty_attributes_error() -> None:
    """Raises ValueError when attributes list is empty."""
    group1 = [Entity(id="e1", attributes={"value": 1})]
    scorer = MeanMaxDifferenceScorer()
    with pytest.raises(ValueError, match="attributes cannot be empty"):
        scorer.score([group1], [])


def test_mean_max_difference_scorer_empty_group_error() -> None:
    """Raises ValueError when any group contains no entities."""
    group1 = [Entity(id="e1", attributes={"value": 1})]
    group2: list[Entity] = []
    scorer = MeanMaxDifferenceScorer()
    with pytest.raises(ValueError, match="all groups must be non-empty"):
        scorer.score([group1, group2], ["value"])
