from teamup.entity import AttributeValue, Entity
from teamup.partition import Partition
from teamup.scorer import MaxDifferenceScorer


def main() -> None:

    entity1 = Entity(
        id="entity_3",
        attributes={
            "count": AttributeValue(value=4),
            "ratio": AttributeValue(value=3.14),
            "value": AttributeValue(value=100)
        },
    )
    entity2 = Entity(
        id="entity_3",
        attributes={
            "count": AttributeValue(value=10),
            "ratio": AttributeValue(value=8.24),
            "value": AttributeValue(value=97)
        },
    )
    print(entity1)

    group1 = [entity1]
    group2 = [entity2]

    groups = [group1, group2]

    scorer = MaxDifferenceScorer()
    score = scorer.score(groups, ["count", "ratio", "value"])

    partition = Partition(groups=groups, score=score)
    print(partition)

    print(f"Score: {score}")


if __name__ == "__main__":
    main()
