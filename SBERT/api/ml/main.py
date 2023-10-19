"""
App to Generate Embeddings from Strings
"""

from transformer.sbert.sbert_transformer import SbertTransformer

transformer = SbertTransformer()

document = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "gender": "Male",
    "country": "USA",
    "age": "28",
}

embedding = transformer.get_embedding(document)

# embedding = transformer.get_embedding(document)

print(embedding)
