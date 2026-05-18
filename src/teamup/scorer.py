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


class NormalizedScorer(Scorer, ABC):
    """
    Abstract base class for scorers that normalize attribute values before scoring.

    Implements a two-phase algorithm:
    1. Normalize all attribute values to [0, 1] using global min/max across all entities.
    2. Compute per-attribute group sums, then per-attribute max_sum - min_sum differences.
    3. Delegate combining those differences to the abstract ``_combine()`` method.

    Zero-variance attributes (all entities share the same value) produce ``0.0``
    for all their normalized values.
    """

    def _normalize(
        self, groups: list[list[Entity]], attributes: list[str]
    ) -> list[list[dict[str, float]]]:
        """
        Compute normalized attribute values in [0, 1] using global min/max.

        Args:
            groups: A list of groups of entities.
            attributes: Attribute names to normalize.

        Returns:
            Parallel structure to groups, with each entity replaced by a dict
            of normalized float values.
        """
        all_entities = [entity for group in groups for entity in group]

        attr_min: dict[str, float] = {}
        attr_max: dict[str, float] = {}
        for attr_name in attributes:
            values = [float(entity[attr_name]) for entity in all_entities]
            attr_min[attr_name] = min(values)
            attr_max[attr_name] = max(values)

        normalized_groups: list[list[dict[str, float]]] = []
        for group in groups:
            normalized_group: list[dict[str, float]] = []
            for entity in group:
                normalized_attrs: dict[str, float] = {}
                for attr_name in attributes:
                    val = float(entity[attr_name])
                    min_val = attr_min[attr_name]
                    max_val = attr_max[attr_name]
                    if max_val == min_val:
                        normalized_attrs[attr_name] = 0.0
                    else:
                        normalized_attrs[attr_name] = (val - min_val) / (max_val - min_val)
                normalized_group.append(normalized_attrs)
            normalized_groups.append(normalized_group)

        return normalized_groups

    @abstractmethod
    def _combine(self, differences: list[float]) -> float:
        """
        Combine per-attribute max_group_sum - min_group_sum values into a score.

        Args:
            differences: One value per attribute.

        Returns:
            A single numeric score (lower is better).
        """

    def score(
        self, groups: list[list[Entity]], attributes: list[str]
    ) -> float:
        """
        Compute a normalized score for the partition.

        Args:
            groups: A list of groups, where each group is a list of Entity objects.
            attributes: A list of attribute names to evaluate.

        Returns:
            A numeric score produced by ``_combine()``.

        Raises:
            ValueError: If groups is empty, attributes is empty, or any group is empty.
        """
        if not groups:
            raise ValueError("groups cannot be empty")
        if not attributes:
            raise ValueError("attributes cannot be empty")
        if any(not group for group in groups):
            raise ValueError("all groups must be non-empty")

        normalized_groups = self._normalize(groups, attributes)

        differences: list[float] = []
        for attr_name in attributes:
            group_sums = [
                sum(entity[attr_name] for entity in normalized_group)
                for normalized_group in normalized_groups
            ]
            differences.append(max(group_sums) - min(group_sums))

        return self._combine(differences)


class MeanMaxDifferenceScorer(NormalizedScorer):
    """
    Concrete scorer that returns the maximum per-attribute normalized sum difference.

    Overrides ``_combine()`` to return ``max(differences)``, making it the most
    conservative (pessimistic) normalized scorer.
    """

    def _combine(self, differences: list[float]) -> float:
        return max(differences)

