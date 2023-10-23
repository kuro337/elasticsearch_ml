"""
ES serialization exceptions
"""


class UnknownESEntityError(Exception):
    """Exception raised for unknown Entity types in ES serialization."""

    def __init__(self, entity_type, message="Unknown entity type for ES serialization"):
        self.entity_type = entity_type
        self.message = f"{message}: {entity_type}"
        super().__init__(self.message)
