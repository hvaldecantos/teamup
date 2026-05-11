"""Partitioning algorithm interfaces and implementations."""

from abc import ABC, abstractmethod
from itertools import combinations
from typing import Iterator

from teamup.entity import Entity
from teamup.partition import Partition
from teamup.scorer import Scorer


class PartitioningAlgorithm(ABC):
    """
    Abstract interface for entity partitioning algorithms.

    A partitioning algorithm takes a set of entities and divides them into
    disjoint groups while minimizing a score computed by a scorer. Different
    algorithms (brute force, genetic, simulated annealing) can be swapped
    in without touching the orchestrator.
    """

    @abstractmethod
    def partition(
        self,
        entities: list[Entity],
        num_groups: int,
        scorer: Scorer,
        attributes: list[str],
    ) -> Partition:
        """
        Partition entities into num_groups to minimize score.

        Args:
            entities: The list of entities to partition.
            num_groups: The number of groups to partition into.
            scorer: The scorer to evaluate partition quality.
            attributes: The list of attribute names to consider in scoring.

        Returns:
            A Partition object with the optimal (or near-optimal) grouping and score.
        """


class BruteForceAlgorithm(PartitioningAlgorithm):
    """
    Brute-force partitioning that exhaustively searches all permutations.

    Suitable for small datasets (≤20 entities). Finds the provably optimal
    partition by evaluating all possible groupings and selecting the one
    with the lowest score.
    """

    def partition(
        self,
        entities: list[Entity],
        num_groups: int,
        scorer: Scorer,
        attributes: list[str],
    ) -> Partition:
        """
        Find the optimal partition by exhaustive search.

        Uses a recursive approach to generate all possible ways to partition
        entities into exactly num_groups, evaluates each with the scorer,
        and returns the partition with the lowest score.

        Args:
            entities: The list of entities to partition.
            num_groups: The number of groups to partition into.
            scorer: The scorer to evaluate partition quality.
            attributes: The list of attribute names to consider in scoring.

        Returns:
            A Partition with the lowest score among all partitions.

        Raises:
            ValueError: If num_groups is invalid or attributes is empty.
        """
        if num_groups < 1:
            raise ValueError("num_groups must be at least 1")
        if num_groups > len(entities):
            raise ValueError("num_groups cannot exceed the number of entities")
        if not attributes:
            raise ValueError("attributes cannot be empty")

        best_partition: Partition | None = None
        best_score = float("inf")

        # Generate all partitions and find the best one
        for partition_groups in self._generate_partitions(
            entities, num_groups
        ):
            current_score = scorer.score(partition_groups, attributes)
            if current_score < best_score:
                best_score = current_score
                best_partition = Partition(
                    groups=partition_groups, score=current_score
                )

        if best_partition is None:
            raise RuntimeError("Failed to generate any valid partitions")

        return best_partition

    def _generate_partitions(
        self, entities: list[Entity], num_groups: int
    ) -> Iterator[list[list[Entity]]]:
        """
        Generate all possible partitions of entities into exactly num_groups.

        Uses a recursive approach: assigns entities one by one to groups,
        trying all possible assignments. Yields only complete partitions
        where exactly num_groups groups are non-empty.

        Args:
            entities: The entities to partition.
            num_groups: The desired number of groups.

        Yields:
            All possible partitions as lists of lists of Entity objects.
        """
        if not entities:
            return

        # Recursive helper to build partitions
        def _build_partitions(
            remaining_entities: list[Entity],
            current_groups: list[list[Entity]],
            num_remaining_groups: int,
        ) -> Iterator[list[list[Entity]]]:
            # Base case: no more entities to assign
            if not remaining_entities:
                # Yield only if we have exactly the right number of groups
                if num_remaining_groups == 0:
                    yield current_groups
                return

            # If we have no more groups to fill but still have entities,
            # we can't complete this partition
            if num_remaining_groups < 0:
                return

            # Take the first entity
            first_entity = remaining_entities[0]
            rest_entities = remaining_entities[1:]

            # Try adding this entity to each existing (non-empty) group
            for i in range(len(current_groups)):
                new_groups = [g[:] for g in current_groups]
                new_groups[i].append(first_entity)
                yield from _build_partitions(
                    rest_entities, new_groups, num_remaining_groups
                )

            # Try creating a new group with this entity
            # (only if we still have groups left to allocate)
            if num_remaining_groups > 0:
                new_groups = current_groups + [[first_entity]]
                yield from _build_partitions(
                    rest_entities, new_groups, num_remaining_groups - 1
                )

        # Start with the first entity in the first group
        first_entity = entities[0]
        rest_entities = entities[1:]
        initial_groups = [[first_entity]]

        yield from _build_partitions(
            rest_entities, initial_groups, num_groups - 1
        )
