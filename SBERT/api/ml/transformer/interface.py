"""
Interface for Transformer for Embeddings
"""
from abc import ABC, abstractmethod
from typing import Any, Dict
import torch
from sentence_transformers import SentenceTransformer


class TransformerInterface(ABC):
    """
    TransformerInterface is an abstract class that enforces the implementation
    of essential methods for transformers.
    """

    model: SentenceTransformer

    @abstractmethod
    def get_embedding(self, doc: Dict[str, Any]) -> torch.Tensor:
        """
        Returns the embedding for the document
        """

    @abstractmethod
    def get_model_type(self) -> str:
        """
        Returns the type of the transformer
        """

    @classmethod
    def model_dimensionality(cls, subclass) -> int:
        """
        Returns the Dimensionality of the Model
        """
        return subclass.model.get_sentence_embedding_dimension()
