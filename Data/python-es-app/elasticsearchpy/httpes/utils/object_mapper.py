from ..models import Entity, User, Post, Page, Session, Metadata
from ..types.error.entity_error import InvalidEntityTypeError

entities = {
    "user": User,
    "post": Post,
    "page": Page,
    "session": Session,
    "metadata": Metadata,
}

"""
def func(some : type) -> return_type:
  raise some_error
  return some_type

raise is used so the caller can try catch this

"""


def get_entity(entity_type: str) -> Entity:
    entity = entities.get(entity_type)
    if not entity:
        raise InvalidEntityTypeError(f"Invalid Type: {entity_type}")
    return entity
