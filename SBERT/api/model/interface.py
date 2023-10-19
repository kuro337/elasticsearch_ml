"""
Base model for Elasticsearch

This Model is used to create the Elasticsearch Indexes and Mappings

"""
import hashlib
import json
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
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
        return self.__class__.__name__.lower()

    @abstractmethod
    def get_mapping(self) -> Dict:
        """
        @Abstract Method
        Returning the Index Mapping for the Document Type

        """

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

    def schema(self) -> Dict:
        """
        Returns the Schema of the Document
        """
        return self.schema()
