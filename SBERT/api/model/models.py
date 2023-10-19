"""
Types for Documents
"""

from typing import List, Optional, Dict
from pydantic import StringConstraints, HttpUrl
from typing_extensions import Annotated

from model.interface import ESDocument


class User(ESDocument):

    """
    User Document

    Example JSON:
    ------------
    {
        "username": "JohnDoe",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "gender": "Male",
        "country": "USA",
        "age": 28
    }
    ------------
    """

    username: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    first_name: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    last_name: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    email: Annotated[
        str,
        StringConstraints(min_length=3, strip_whitespace=True, pattern=r".+@.+\..+"),
    ]
    gender: Annotated[str, StringConstraints(min_length=1)]
    country: Annotated[str, StringConstraints(min_length=2)]
    age: int
    embedding: Optional[List[float]] = None

    def get_index_name(self) -> str:
        return "users"

    def get_mapping(self) -> Dict:
        return {
            "properties": {
                "username": {"type": "text"},
                "first_name": {"type": "text"},
                "last_name": {"type": "text"},
                "email": {"type": "text"},
                "gender": {"type": "text"},
                "country": {"type": "text"},
                "age": {"type": "integer"},
            }
        }


class Post(ESDocument):
    """
    Post Document

    JSON Payload:
    ------------
    {
     "title" : "My First Post",
     "body"  : "This is the content of my first post.",
     "author": "JohnDoe"
    }


    export const post: Post = {
      rootPagePath: 'java',
      title       : 'Generics and Enums in Java Quicksort Implementation',
      shortTitle  : 'Java Generics & Enums',
      description : 'Exploring the power of Java Generics and Enums with a Quicksort example.',
      tags: 'java generics enums algorithms quicksort',
      date: 'September 22, 2023',
      postId: 'java-generics-enums-quicksort',
      component: '<java-generics-enums-quicksort></java-generics-enums-quicksort>',
      pathForDynamicLoad: 'src/posts/Infra/JavaGenericsEnumsQuicksort',
      renderFunc: () => html`<java-generics-enums-quicksort></java-generics-enums-quicksort>`
    }
            ------------
    """

    lang: Annotated[str, StringConstraints(min_length=1)]
    title: Annotated[str, StringConstraints(min_length=1)]
    short_title: Annotated[str, StringConstraints(min_length=1)]
    description: Annotated[str, StringConstraints(min_length=3)]
    author: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    tags: Annotated[str, StringConstraints(min_length=2)]
    date: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    post_id: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    component: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    author: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    dynamic_path: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    author: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    render_func: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    embedding: Optional[List[float]] = None

    def get_index_name(self) -> str:
        return "posts"

    def get_mapping(self) -> Dict:
        return {
            "properties": {
                "lang": {"type": "text"},
                "title": {"type": "text"},
                "short_title": {"type": "text"},
                "description": {"type": "text"},
                "author": {"type": "text"},
                "tags": {"type": "text"},
                "date": {"type": "text"},
                "post_id": {"type": "text"},
                "component": {"type": "text"},
                "dynamic_path": {"type": "text"},
                "render_func": {"type": "text"},
            }
        }


class Interaction(ESDocument):
    """
    User-Post Interaction
    """

    interaction_type: Annotated[str, StringConstraints(min_length=1)]
    post_id: Annotated[str, StringConstraints(min_length=1)]
    timestamp: Annotated[str, StringConstraints(min_length=1)]
    username: Annotated[str, StringConstraints(min_length=1)]
    embedding: Optional[List[float]] = None

    def get_index_name(self) -> str:
        return "interactions"

    def get_mapping(self) -> Dict:
        return {
            "properties": {
                "interaction_type": {"type": "text"},
                "post_id": {"type": "text"},
                "timestamp": {"type": "date"},
                "username": {"type": "text"},
            }
        }


class Product(ESDocument):
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

    def get_index_name(self) -> str:
        return "products"

    def get_mapping(self) -> Dict:
        return {
            "properties": {
                "id": {"type": "integer"},
                "url": {"type": "text"},
                "last_accessed": {"type": "date"},
                "ip_address": {"type": "text"},
                "user_agent": {"type": "text"},
                "array_of_dates": {"type": "date"},
                "array_of_strings": {"type": "text"},
            }
        }
