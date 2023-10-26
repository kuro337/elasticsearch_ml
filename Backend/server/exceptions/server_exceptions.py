"""
ES serialization exceptions
"""


class UnknownESEntityError(Exception):
    """Exception raised for unknown Entity types in ES serialization."""

    def __init__(self, entity_type, message="Unknown entity type for ES serialization"):
        self.entity_type = entity_type
        self.message = f"{message}: {entity_type}"
        super().__init__(self.message)


class DocumentInsertionError(Exception):
    """Raised when there's an error during document insertion to ElasticSearch."""

    def __init__(self, exception_str: Exception):
        error_type = type(exception_str).__name__
        self.message = f"{error_type}: {str(exception_str)}"
        super().__init__(self.message)


class RecommendationSystemInternalError(Exception):
    """Raised when there's an error during score retrieval ElasticSearch."""

    def __init__(self, exception_str: Exception):
        error_type = type(exception_str).__name__
        self.message = f"{error_type}: {str(exception_str)}"
        super().__init__(self.message)


class NotUserEntityError(Exception):
    """Entity Passed was not a User"""


class GLMModelTrainingFailure(Exception):
    """Logistical Regression Model Failed Training and Scoring"""
