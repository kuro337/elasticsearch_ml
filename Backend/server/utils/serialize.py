from model.models import Interaction, User, Post, Product, ESDocument


from exceptions.server_exceptions import UnknownESEntityError

import json


# Mapping of entity names to classes
ENTITY_CLASSES = {
    "Interaction": Interaction,
    "User": User,
    "Post": Post,
    "Product": Product,
}


def serialize_ws_data_esdoc(data: str) -> ESDocument:
    """
    Create an instance of the specified entity class with the provided data.

    :param entity_type: The name of the entity class to instantiate.
    :param data: The data to pass to the entity class's constructor.
    :return: An instance of the specified entity class, or None if the class name is invalid.
    """
    http_req = json.loads(data)

    entity_type = http_req.get("entity")
    entity_data = http_req.get("data")

    print(f"Entity received:\n {entity_type}")

    print(f"Data received:\n {entity_data}")

    entity_class = ENTITY_CLASSES.get(entity_type)
    if entity_class is None:
        raise UnknownESEntityError(entity_type)

    # Create an instance of the class
    instance = entity_class(**entity_data)
    return instance


def serialize_json_esdoc(entity_type: str, data: dict) -> ESDocument:
    """
    Create an instance of the specified entity class with the provided data.

    :param entity_type: The name of the entity class to instantiate.
    :param data: The data to pass to the entity class's constructor.
    :return: An instance of the specified entity class, or None if the class name is invalid.
    """
    entity_class = ENTITY_CLASSES.get(entity_type)
    if entity_class is None:
        raise UnknownESEntityError(entity_type)

    # Create an instance of the class
    instance = entity_class(**data)
    return instance
