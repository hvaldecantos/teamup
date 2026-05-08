"""TeamUp Copilot - Collaborative entity partitioning and scoring."""

from .entity import Entity
from .partition import Partition
from .scorer import MaxDifferenceScorer, Scorer

__all__ = ["Entity", "Partition", "Scorer", "MaxDifferenceScorer"]
