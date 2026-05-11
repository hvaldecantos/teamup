from teamup.algorithm import BruteForceAlgorithm
from teamup.entity import AttributeValue, Entity
from teamup.partition import Partition
from teamup.partitioner import Partitioner
from teamup.scorer import MaxDifferenceScorer


def main() -> None:

    entity1 = Entity(
        id="entity_1",
        attributes={
            "count": AttributeValue(value=24),
            "ratio": AttributeValue(value=3.14),
            "value": AttributeValue(value=100),
        },
    )
    entity2 = Entity(
        id="entity_2",
        attributes={
            "count": AttributeValue(value=20),
            "ratio": AttributeValue(value=8.24),
            "value": AttributeValue(value=97),
        },
    )

    entity3 = Entity(
        id="entity_3",
        attributes={
            "count": AttributeValue(value=5),
            "ratio": AttributeValue(value=5.26),
            "value": AttributeValue(value=111)
        },
    )
    entity4 = Entity(
        id="entity_4",
        attributes={
            "count": AttributeValue(value=11),
            "ratio": AttributeValue(value=9.1),
            "value": AttributeValue(value=99)
        },
    )

    entities = [entity1, entity2, entity3, entity4]

    partitioner = Partitioner(
        BruteForceAlgorithm(),
        MaxDifferenceScorer())

    partition = partitioner.partition(
        entities, 2, ["count"]
    )

    for g in partition.groups:
        print("Group ------------")
        print(g)

    print(f"Partition score: {partition.score}")


if __name__ == "__main__":
    main()
