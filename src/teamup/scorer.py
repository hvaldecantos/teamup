"""Scoring interface and implementations for partition evaluation."""

from abc import ABC, abstractmethod

from teamup.entity import Entity


class Scorer(ABC):
    """
    Abstract interface for partition scoring strategies.

    A scorer evaluates the quality of a partition by computing a numeric score
    based on how attribute values are distributed across groups. Lower scores
    indicate better partitions.
    """

    @abstractmethod
    def score(
        self, groups: list[list[Entity]], attributes: list[str]
    ) -> float:
        """
        Compute a score for the given partition across specified attributes.

        Args:
            groups: A list of groups, where each group is a list of Entity objects.
            attributes: A list of attribute names to evaluate.

        Returns:
            A numeric score (lower is better).
        """


class MaxDifferenceScorer(Scorer):
    """
    Scorer that maximizes group balance by minimizing the maximum difference.

    For each attribute, computes the difference between the maximum and minimum
    group sums. The overall score is the maximum of these per-attribute differences.
    This encourages balanced distribution of attribute totals across groups.
    """

    def score(
        self, groups: list[list[Entity]], attributes: list[str]
    ) -> float:
        """
        Compute the max-difference score for a partition.

        For each attribute:
        1. Sum the attribute values across all entities in each group.
        2. Find max_sum and min_sum of these group totals.
        3. Compute the difference: max_sum - min_sum.

        The overall score is the maximum of all these per-attribute differences.

        Args:
            groups: A list of groups, where each group is a list of Entity objects.
            attributes: A list of attribute names to evaluate.

        Returns:
            The maximum difference across all attributes.

        Raises:
            ValueError: If groups is empty, attributes is empty, or any group is empty.
        """
        if not groups:
            raise ValueError("groups cannot be empty")
        if not attributes:
            raise ValueError("attributes cannot be empty")
        if any(not group for group in groups):
            raise ValueError("all groups must be non-empty")

        max_overall_difference = 0.0

        for attr_name in attributes:
            # Compute sum of this attribute across each group
            group_sums = []
            for group in groups:
                group_sum = sum(entity[attr_name] for entity in group)
                group_sums.append(group_sum)

            # Find max and min sums
            max_sum = max(group_sums)
            min_sum = min(group_sums)
            difference = max_sum - min_sum

            # Track the maximum difference
            max_overall_difference = max(max_overall_difference, difference)

        return max_overall_difference
