from teamup.entity import AttributeValue, Entity


def main() -> None:

    entity = Entity(
        id="entity_3",
        attributes={
            "count": AttributeValue(value=5),
            "ratio": AttributeValue(value=3.14),
            "value": AttributeValue(value=100)
        },
    )
    print(entity)


if __name__ == "__main__":
    main()
