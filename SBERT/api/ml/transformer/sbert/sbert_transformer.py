"""
Sentence Transformer - SBERT
"""

from typing import Any, Dict, List
from sentence_transformers import SentenceTransformer
import torch


from ml.transformer.interface import TransformerInterface


class SbertTransformer(TransformerInterface):
    """
    Sentence Transformer - SBERT

    """

    model: SentenceTransformer

    def __init__(self) -> None:
        self.model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

    def get_embedding(self, doc: Dict[str, Any]) -> torch.Tensor:
        """
        Returns the embedding for the document
        """
        doc_string = " ".join([str(value) for value in doc.values()])
        embedding = self.model.encode(doc_string, convert_to_tensor=True)
        return embedding

    def convert_doc_to_vector(self, string_value: str) -> List[float]:
        """
        Returns the embeddings for the document
        """

        # combined_string = " ".join([str(value) for value in doc.values()])
        combined_embedding = self.model.encode(string_value).tolist()
        return combined_embedding

    def get_model_type(self) -> str:
        """
        Returns the type of the transformer
        """
        return "SBERT"
