from django.db import models
from pydantic import BaseModel, StringConstraints, Field, HttpUrl, conint, constr

from typing_extensions import Annotated
from typing import Literal, Union

import abc

# Create your models here.

# Annotated -> Allows us to add Metadata to the Type Hint - which Pydantic uses for Validation


# Define your data model with required fields
class MyDataModel(BaseModel):
    field1: str
    field2: int


"""
from abc import ABC
ABC is an Abstract Base Class 

Our Entities will inherit from the base class and will have a common field called type

"""


class Entity(BaseModel, abc.ABC):
    @abc.abstractproperty
    def type(self):
        # pass
        return "Entity Parent Class"


class User(Entity):
    @property
    def type(self):
        return "user"

    username: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    email: Annotated[
        str,
        StringConstraints(min_length=3, strip_whitespace=True, pattern=r".+@.+\..+"),
    ]


class Post(Entity):
    @property
    def type(self):
        return "post"

    title: Annotated[str, StringConstraints(min_length=1)]
    body: Annotated[str, StringConstraints(min_length=1)]
    author: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]


class Page(Entity):
    @property
    def type(self):
        return "page"

    # type = Literal["page"]
    title: Annotated[str, StringConstraints(min_length=1)]
    content: Annotated[str, StringConstraints(min_length=1)]
    url: HttpUrl


class Session(Entity):
    @property
    def type(self):
        return "session"

    # type = Literal["session"]
    username: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    session_key: str


class Metadata(Entity):
    @property
    def type(self):
        return "metadata"

    # type = Literal["metadata"]
    id: int
    last_accessed: str
    ip_address: str
    user_agent: str
    array_of_dates: list
    array_of_strings: list
