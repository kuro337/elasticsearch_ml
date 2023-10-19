"""
Types for Documents
"""

from typing import List
from pydantic import BaseModel, StringConstraints, HttpUrl, Field
from typing_extensions import Annotated


class User(BaseModel):

    """
    User Document

    Example JSON:
    ------------
    {
        "username": "JohnDoe",
        "email": "john.doe@example.com",
        "gender": "Male",
        "country": "USA",
        "age": 28
    }
    ------------
    """

    username: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    email: Annotated[
        str,
        StringConstraints(min_length=3, strip_whitespace=True, pattern=r".+@.+\..+"),
    ]
    gender: Annotated[str, StringConstraints(min_length=1)]
    country: Annotated[str, StringConstraints(min_length=2)]
    age: int
    # embedding: List[float] = Field(
    #     ..., description="The concatenated embedding of the document"
    # )


class Post(BaseModel):
    """
    Post Document

    JSON Payload:
    ------------
    {
        "title": "My First Post",
        "body": "This is the content of my first post.",
        "author": "JohnDoe"
    }
    ------------
    """

    title: Annotated[str, StringConstraints(min_length=1)]
    body: Annotated[str, StringConstraints(min_length=1)]
    author: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]


class Product(BaseModel):
    """
    Product Document

    JSON Payload:
    ------------
    {
        "id": 1,
        "url": "https://example.com/product/1",
        "last_accessed": "2023-10-15T08:00:00Z",
        "ip_address": "203.0.113.42",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "array_of_dates": ["2023-10-15", "2023-10-16"],
        "array_of_strings": ["example1", "example2"]
    }
    ------------
    """

    id: int
    url: HttpUrl
    last_accessed: str
    ip_address: str
    user_agent: str
    array_of_dates: list
    array_of_strings: list
