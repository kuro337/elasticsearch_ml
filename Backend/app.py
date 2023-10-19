"""
Application entry point for Interacting with Elasticsearch

Checking Memory Consumption

vmstat -s -S M 5

Application entry point for Interacting with Elasticsearch

Checking Memory Consumption
vmstat -s -S M 5
"""


from typing import List
from elastic_search.es_service import ElasticSearchService
from model.models import User
from utils.encryption import generate_hash


from ml.transformer.sbert.sbert_transformer import SbertTransformer

transformer = SbertTransformer()

# Usage
es_service = ElasticSearchService(cert_location="ssl/ca.crt")


user_document = User(
    username="Filaman Petriol",
    email="petriol.minam@aol.com",
    gender="Male",
    country="Japan",
    age=20,
)

es_service.doc_count(index_name="user")

print("Creating index\n\n")

es_service.create_index(user_document.model_dump(), index_name="user", embedding=True)

print("Listing index\n\n")
es_service.list_indices_and_mappings(index="user")

print("Creating Hash\n\n")
# Generate Hash of the User Document for the Document ID
user_hash = generate_hash(user_document.model_dump())

print("Creating Embedding\n\n")
# Generate Vector<Float> Embedding from User Document and add it to User Object
combined_embedding: List[float] = transformer.convert_doc_to_vector(
    user_document.model_dump()
)
user_document.embedding = combined_embedding


print("Inserting Embedding\n\n")

# Insert the Document with Embedding into Elasticsearch
es_service.insert_document(
    document=user_document.model_dump(), id=user_hash, index_name="user"
)

result = es_service.semantic_search(
    query_vector=combined_embedding, index_name="user", debug=True
)


# Fuzzy Search
print("Fuzzy Searching Embedding\n\n")

search_filter = {"country": "jpn"}

result = es_service.semantic_search(
    query_vector=user_document.embedding,
    index_name="user",
    search_filter=search_filter,
    size=5,
    aprroximate=True,
    debug=True,
)

# print("Deleting Embedding\\n")

# es_service.delete_index(index_name="user")

print("Listing Indices\n\n")

es_service.list_indices_and_mappings(index="user")

# print(result)


# print(user_document.model_json_schema())
# print(user_document)
