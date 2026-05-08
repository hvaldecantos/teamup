"""Partition result object for storing partitioning outcomes."""

from pydantic import BaseModel, Field

from teamup.entity import Entity


class Partition(BaseModel):
    """
    Represents a partition of entities and its quality score.

    A partition groups entities into disjoint subsets (groups) and stores
    an overall numeric score that measures the quality of this partition.

    Attributes:
        groups: A list of groups, where each group is a list of Entity objects.
        score: The numeric quality score of this partition (lower is better).
    """

    groups: list[list[Entity]] = Field(
        ...,
        description="A list of groups, each containing Entity objects",
    )
    score: float | int = Field(
        ..., description="Quality score of the partition (lower is better)"
    )
