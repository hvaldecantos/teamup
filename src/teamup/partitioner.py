"""Partitioner orchestrator for coordinating algorithms and scorers."""

from teamup.algorithm import PartitioningAlgorithm
from teamup.entity import Entity
from teamup.partition import Partition
from teamup.scorer import Scorer


class Partitioner:
    """
    Orchestrates partitioning by coordinating a PartitioningAlgorithm and Scorer.

    The Partitioner accepts any implementation of PartitioningAlgorithm and
    any implementation of Scorer, allowing flexible swapping of strategies
    without modifying the orchestrator itself.
    """

    def __init__(
        self, algorithm: PartitioningAlgorithm, scorer: Scorer
    ) -> None:
        """
        Initialize the Partitioner with an algorithm and scorer.

        Args:
            algorithm: A PartitioningAlgorithm implementation.
            scorer: A Scorer implementation.
        """
        self._algorithm = algorithm
        self._scorer = scorer

    def partition(
        self, entities: list[Entity], num_groups: int, attributes: list[str]
    ) -> Partition:
        """
        Partition entities into the specified number of groups.

        Delegates to the algorithm to find the optimal (or near-optimal)
        partition using the configured scorer to evaluate quality.

        Args:
            entities: The list of entities to partition.
            num_groups: The number of groups to create.
            attributes: The list of attribute names to optimize for.

        Returns:
            A Partition object with groups and their quality score.

        Raises:
            ValueError: If inputs are invalid.
            RuntimeError: If partitioning fails.
        """
        if not entities:
            raise ValueError("entities cannot be empty")
        if num_groups < 1:
            raise ValueError("num_groups must be at least 1")
        if not attributes:
            raise ValueError("attributes cannot be empty")

        return self._algorithm.partition(
            entities, num_groups, self._scorer, attributes
        )
