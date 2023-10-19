"""
Application entry point for Interacting with Elasticsearch

Even if Index Schema is defined with Embedding - 
we can still insert Documents without providing the Embedding

"""

from typing import List
from elastic_search.es_service import ElasticSearchService
from model.interface import ESDocument
from model.models import User, Post, Interaction

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

post_document = Post(
    lang="java",
    title="Great Post",
    short_title="This is some random post.",
    description="Read this post to read words that are written by me.",
    author="Filaman Petriol",
    tags="java, oop, elasticsearch",
    date="2023-10-08T12:34:56",
    post_id="1",
    component="post",
    dynamic_path="/path/to/post",
    render_func="render_post",
)

interaction_document = Interaction(
    interaction_type="like",
    post_id="1",
    timestamp="2023-10-11T12:34:56",
    username="Filaman Petriol",
)

documents: List[ESDocument] = [user_document, post_document, interaction_document]

for doc in documents:
    es_service.doc_count(index=doc.get_index_name())

    print("Creating index\n\n")

    es_service.create_index(doc, embedding=True)

    print("Listing index\n\n")
    es_service.list_indices_and_mappings(index=doc.get_index_name())

    print("Creating Hash\n\n")
    # Generate Hash of the User Document for the Document ID
    # user_hash = generate_hash(user_document.model_dump())
    doc_hash = doc.hash()
    print(doc_hash)

    print("Creating Embedding\n\n")
    # Generate Vector<Float> Embedding from User Document and add it to User Object
    combined_embedding: List[float] = transformer.convert_doc_to_vector(doc.stringify())
    doc.embedding = combined_embedding

    print("Inserting Embedding\n\n")

    # Insert the Document with Embedding into Elasticsearch
    es_service.insert_document(
        document=doc, id=doc.hash(), index_name=doc.get_index_name()
    )

    result = es_service.semantic_search(
        query_vector=combined_embedding, index_name=doc.get_index_name(), debug=True
    )

    # Fuzzy Search
    print("Fuzzy Searching Embedding\n\n")

    search_filter = {"country": "jpn"}

    result = es_service.semantic_search(
        query_vector=combined_embedding,
        index_name=doc.get_index_name(),
        search_filter=search_filter,
        size=5,
        aprroximate=True,
        debug=True,
    )

    # print("Deleting Embedding\\n")

    # es_service.delete_index(index_name="user")

    print("Listing Indices\n\n")

    es_service.list_indices_and_mappings(index=doc.get_index_name())

    # print(result)
    # print(user_document.model_json_schema())
    # print(user_document)
