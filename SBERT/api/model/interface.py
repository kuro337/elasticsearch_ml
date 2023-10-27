"""
Base model for Elasticsearch

This Model is used to create the Elasticsearch Indexes and Mappings

"""
import hashlib
import json
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Type
from pydantic import BaseModel, root_validator


class ESDocument(BaseModel, ABC):
    """
    Abstract Class to be satisfied by each Entity that exists as an ES Document and Index
    """

    @abstractmethod
    def get_index_name(self) -> str:
        """
        @Abstract Method
        @Override
        Returning the Index Name for the Document Type
        """

    @abstractmethod
    def get_mapping(self) -> Dict:
        """
        @Abstract Method
        Returning the Index Mapping for the Document Type

        """

    @staticmethod
    def multi_type(
        primary_type: str = "keyword",
        secondary_type: str = "text",
    ) -> dict:
        """
        @staticmethod
        @dynamicmapping

        - Creates a Multi-Field Property for the Document SubClass

        @Usage
        ```py
        class Users(ESDocument):
            @fields...
            def get_mapping(self) -> Dict:
                return {
                    "properties": {
                        "username": self.multi_type("text"),
                        "post_id": self.multi_type("text"),
                    }
                }
        ```
        """
        return {
            "type": primary_type,
            "fields": {secondary_type: {"type": secondary_type}},
        }

    def hash(self):
        """
        Encrypts a Document to be stored in Elasticsearch
        """
        return hashlib.md5(
            self.model_dump_json(exclude_unset=True).encode()
        ).hexdigest()

    def stringify(self) -> str:
        """
        Converts the document into a string format: "Key1 Value1, Key2 Value2, Key3 Value3, ..."
        """
        return ", ".join(
            f"{k} {v}" for k, v in self.model_dump(exclude_unset=True).items()
        )

    def json_schema(self) -> str:
        """
        Returns the Schema of the Document
        """
        if hasattr(self, "embedding"):
            if self.embedding is None:
                return self.model_dump_json(exclude_unset=True)

        return self.model_dump_json()

    def dump_document(self) -> Dict:
        """
        Returns the Document as a Dictionary
        """
        return self.model_dump(exclude_unset=True)


class EmbeddingsDocument(ESDocument):
    """Base class for all embedding documents."""

    embedding: List[float]


class ESDocumentWithEmbedding(ESDocument, ABC):
    """Interface for all embedding documents."""

    @abstractmethod
    def get_primary_key(self) -> str:
        """
        @Abstract Method
        @Override
        Returning the Primary Key for the Document Subclass
        """

    @abstractmethod
    def get_embedding_document(
        self, embedding: List[float]
    ) -> Type[EmbeddingsDocument]:
        """Convert the document to its embedding representation."""
