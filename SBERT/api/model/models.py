"""
Types for Documents

Also Available https://elasticsearch-dsl.readthedocs.io/en/latest/
"""

from typing import List, Optional, Dict, Type
from pydantic import StringConstraints, HttpUrl
from typing_extensions import Annotated

from model.interface import ESDocument, EmbeddingsDocument, ESDocumentWithEmbedding


class User(ESDocumentWithEmbedding):

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

    username: Annotated[str, StringConstraints(min_length=3)]
    first_name: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    last_name: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    email: Annotated[
        str,
        StringConstraints(min_length=3, strip_whitespace=True, pattern=r".+@.+\..+"),
    ]
    gender: Annotated[str, StringConstraints(min_length=1)]
    country: Annotated[str, StringConstraints(min_length=2)]
    age: int
    timestamp: Annotated[
        str, StringConstraints(min_length=8, strip_whitespace=True)
    ] = None

    def get_index_name(self) -> str:
        return "users"

    def get_primary_key(self) -> str:
        return "username"

    def get_mapping(self) -> Dict:
        return {
            "properties": {
                "username": self.multi_type("keyword", "text"),
                "first_name": {"type": "text"},
                "last_name": {"type": "text"},
                "email": self.multi_type("keyword", "text"),
                "gender": self.multi_type("keyword", "text"),
                "country": self.multi_type("keyword", "text"),
                "age": {"type": "integer"},
                "timestamp": {"type": "date"},
            }
        }

    def get_embedding_document(
        self, embedding: List[float]
    ) -> Type[EmbeddingsDocument]:
        """Convert the Post to its embedding representation."""
        return UserEmbeddings(username=self.username, embedding=embedding)


class Post(ESDocumentWithEmbedding):
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

    post_id: Annotated[str, StringConstraints(min_length=3)]
    component: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    dynamic_path: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    render_func: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    timestamp: Annotated[
        str, StringConstraints(min_length=3, strip_whitespace=True)
    ] = None

    def get_primary_key(self) -> str:
        return "post_id"

    def get_index_name(self) -> str:
        return "posts"

    def get_mapping(self) -> Dict:
        return {
            "properties": {
                "lang": self.multi_type("keyword", "text"),
                "title": {"type": "text"},
                "short_title": {"type": "text"},
                "description": {"type": "text"},
                "author": {"type": "text"},
                "tags": {"type": "text"},
                "timestamp": {"type": "date"},
                "post_id": self.multi_type("keyword", "text"),
                "component": {"type": "text"},
                "dynamic_path": {"type": "text"},
                "render_func": {"type": "text"},
            }
        }

    def get_embedding_document(
        self, embedding: List[float]
    ) -> Type[EmbeddingsDocument]:
        """Convert the Post to its embedding representation."""

        return PostEmbeddings(post_id=self.post_id, embedding=embedding)


class Interaction(ESDocument):
    """
    User-Post Interaction
    """

    interaction_type: Annotated[str, StringConstraints(min_length=1)]
    post_id: Annotated[str, StringConstraints(min_length=3)]
    timestamp: Optional[Annotated[str, StringConstraints(min_length=1)]] = None
    username: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]

    def get_primary_key(self) -> str:
        return "post_id"

    def get_index_name(self) -> str:
        return "interactions"

    def get_mapping(self) -> Dict:
        return {
            "properties": {
                "interaction_type": self.multi_type("keyword", "text"),
                "post_id": self.multi_type("keyword", "text"),
                "timestamp": {"type": "date"},
                "username": self.multi_type("keyword", "text"),
            }
        }


class UserPostScore(ESDocument):
    """
    User-Post Interaction
    """

    username: Annotated[str, StringConstraints(min_length=1)]
    post_id: Annotated[str, StringConstraints(min_length=1)]
    score: float
    timestamp: Optional[Annotated[str, StringConstraints(min_length=1)]] = None

    def get_index_name(self) -> str:
        return "user_post_scores"

    def get_mapping(self) -> Dict:
        return {
            "properties": {
                "username": self.multi_type("keyword", "text"),
                "post_id": self.multi_type("keyword", "text"),
                "score": {"type": "float"},
                "timestamp": {"type": "date"},
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

    product_id: int
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


class UserEmbeddings(ESDocument):
    """
    User Embeddings Document

    JSON Payload:
    ------------
    {
        "username": "JohnDoe",
        "embedding": [0.1, 0.2, 0.3, 0.4, 0.5]
    }
    ------------
    """

    username: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    embedding: List[float]

    def get_primary_key(self) -> str:
        return "username"

    def get_index_name(self) -> str:
        return "user_embeddings"

    def get_mapping(self) -> Dict:
        return {
            "properties": {
                "username": {"type": "keyword"},
                "embedding": {
                    "type": "dense_vector",
                    "dims": 768,
                    "index": True,
                    "similarity": "cosine",
                },
            }
        }


class PostEmbeddings(ESDocument):
    """
    User Embeddings Document

    JSON Payload:
    ------------
    {
        "post_id": "jvmoop",
        "embedding": [0.1, 0.2, 0.3, 0.4, 0.5]
    }
    ------------
    """

    post_id: Annotated[str, StringConstraints(min_length=3, strip_whitespace=True)]
    embedding: List[float]

    def get_primary_key(self) -> str:
        return "post_id"

    def get_index_name(self) -> str:
        return "post_embeddings"

    def get_mapping(self) -> Dict:
        return {
            "properties": {
                "post_id": {"type": "keyword"},
                "embedding": {
                    "type": "dense_vector",
                    "dims": 768,
                    "index": True,
                    "similarity": "cosine",
                },
            }
        }
