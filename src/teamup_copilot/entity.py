"""Entity data model for TeamUp Copilot."""

from pydantic import BaseModel, ConfigDict, Field


class Entity(BaseModel):
    """
    Wraps a named identifier and arbitrary attributes.

    Provides type-safe access to attributes so that attribute errors are
    caught early.

    Attributes:
        id: The entity identifier (must be a non-empty string).
        attributes: A dictionary of named attributes with numeric values.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(..., min_length=1, description="Entity identifier")
    attributes: dict[str, float | int] = Field(
        default_factory=dict, description="Named numeric attributes"
    )

    def get_attribute(self, name: str) -> float | int:
        """
        Retrieve an attribute value by name.

        Args:
            name: The attribute name.

        Returns:
            The numeric value of the attribute.

        Raises:
            AttributeError: If the attribute does not exist.
        """
        if name not in self.attributes:
            raise AttributeError(
                f"Entity '{self.id}' has no attribute '{name}'. "
                f"Available attributes: {list(self.attributes.keys())}"
            )
        return self.attributes[name]

    def __getitem__(self, name: str) -> float | int:
        """Support bracket access to attributes."""
        return self.get_attribute(name)
