"""Tests for the Entity data model."""

import pytest

from src.teamup.entity import AttributeValue, Entity


def test_entity_creation_basic() -> None:
    """Test basic Entity creation."""
    entity = Entity(id="entity_1", attributes={"score": 10.5})
    assert entity.id == "entity_1"
    assert entity.attributes == {"score": AttributeValue(value=10.5)}


def test_entity_creation_with_empty_attributes() -> None:
    """Test Entity creation with empty attributes dictionary."""
    entity = Entity(id="entity_2")
    assert entity.id == "entity_2"
    assert entity.attributes == {}


def test_entity_creation_with_numeric_attributes() -> None:
    """Test Entity creation with both int and float attributes."""
    entity = Entity(
        id="entity_3",
        attributes={"count": 5, "ratio": 3.14, "value": 100},
    )
    assert entity.attributes == {
        "count": AttributeValue(value=5),
        "ratio": AttributeValue(value=3.14),
        "value": AttributeValue(value=100),
    }


def test_entity_get_attribute_success() -> None:
    """Test retrieving an existing attribute."""
    entity = Entity(id="entity_4", attributes={"health": 75.5})
    assert entity.get_attribute("health") == 75.5


def test_entity_bracket_access() -> None:
    """Test bracket notation for attribute access."""
    entity = Entity(id="entity_5", attributes={"power": 42})
    assert entity["power"] == 42


def test_entity_get_attribute_missing() -> None:
    """Test that accessing a missing attribute raises descriptive error."""
    entity = Entity(id="entity_6", attributes={"existing": 100})

    with pytest.raises(
        AttributeError,
        match="Entity 'entity_6' has no attribute 'missing'.*Available attributes.*existing",
    ):
        entity.get_attribute("missing")


def test_entity_bracket_access_missing() -> None:
    """Test bracket notation raises error for missing attributes."""
    entity = Entity(id="entity_7", attributes={"attr": 10})

    with pytest.raises(AttributeError):
        entity["nonexistent"]


def test_entity_id_cannot_be_empty() -> None:
    """Test that empty ID is rejected."""
    with pytest.raises(ValueError):
        Entity(id="")


def test_entity_multiple_attributes() -> None:
    """Test Entity with multiple attributes."""
    attrs = {"a": 1, "b": 2.5, "c": 3, "d": 4.7}
    entity = Entity(id="multi", attributes=attrs)

    assert entity["a"] == 1
    assert entity["b"] == 2.5
    assert entity["c"] == 3
    assert entity["d"] == 4.7


def test_entity_attribute_list_in_error() -> None:
    """Test that error message includes available attributes."""
    entity = Entity(
        id="test_entity",
        attributes={"foo": 1, "bar": 2, "baz": 3},
    )

    with pytest.raises(AttributeError) as exc_info:
        entity.get_attribute("missing")

    error_msg = str(exc_info.value)
    assert "foo" in error_msg or "bar" in error_msg or "baz" in error_msg
