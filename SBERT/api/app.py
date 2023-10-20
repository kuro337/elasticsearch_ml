"""
Application entry point for Interacting with Elasticsearch

Even if Index Schema is defined with Embedding - 
we can still insert Documents without providing the Embedding

"""
import pandas as pd

from typing import List
from model.interface import ESDocument
from model.models import User, Post, Interaction

from elastic_search.es_service import ElasticSearchService


from ml.transformer.sbert.sbert_transformer import SbertTransformer

transformer = SbertTransformer()

# Usage
es_service = ElasticSearchService.create_service(cert_location="ssl/ca.crt")


user_document = User(
    username="Fiero Martin",
    first_name="Maroni",
    last_name="Memes",
    email="petriol.minam@aol.com",
    gender="Male",
    country="Japan",
    age=20,
    timestamp="2023-10-09T12:34:56",
)

post_document = Post(
    lang="java",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Filaman Petriol",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-09T12:34:56",
    post_id="jvmoop",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)

interaction_document = Interaction(
    interaction_type="view",
    post_id="goat",
    timestamp="2023-11-11T12:34:56",
    username="Petriol Petriol",
)

documents: List[ESDocument] = [user_document, post_document, interaction_document]

for doc in documents:
    # es_service.doc_count(index=doc.get_index_name())

    # print("Creating index\n\n")

    # es_service.create_index(doc, embedding=True)

    # print("Listing index\n\n")
    # es_service.list_indices_and_mappings(index=doc.get_index_name())

    # print("Creating Hash\n\n")
    # Generate Hash of the User Document for the Document ID
    # user_hash = generate_hash(user_document.model_dump())
    # doc_hash = doc.hash()
    # print(doc_hash)

    # print("Creating Embedding\n\n")
    # Generate Vector<Float> Embedding from User Document and add it to User Object
    combined_embedding: List[float] = transformer.convert_doc_to_vector(doc.stringify())
    # doc.embedding = combined_embedding

    print("Inserting Embedding\n\n")

    # Insert the Document with Embedding into Elasticsearch
    es_service.insert_document(
        document=doc, id=doc.hash(), index_name=doc.get_index_name()
    )

    result = es_service.semantic_search(
        query_vector=combined_embedding, index_name=doc.get_index_name(), debug=True
    )

    results_df = pd.DataFrame(result)

    # Display the DataFrame
    print(results_df)
    print(results_df.columns)
    print(results_df.head())
    print(results_df.describe())

    # Fuzzy Search
    print("Fuzzy Searching Embedding\n\n")

    search_filter = {"country": "jpn"}

    result = es_service.semantic_search(
        query_vector=combined_embedding,
        index_name=doc.get_index_name(),
        search_filter=search_filter,
        size=5,
        approximate=True,
        debug=True,
    )

    # Now, create a DataFrame using this list of documents
    results_df = pd.DataFrame(result)

    # Display the DataFrame
    print(results_df)
    print(results_df.columns)
    print(results_df.head())
    print(results_df.describe())


# docs = es_service.fetch_documents(index_name="posts")

# df = pd.DataFrame(docs)

# # Print the first few rows of the DataFrame
# print(df.head())

# print(df.describe())

# print(df.columns)

# print("\nRow values:")
# for index, row in df.iterrows():
#     print(f"Row {index + 1}:")
#     for column in df.columns:
#         print(f"{column}: {row[column]}")
#     print("\n")  # add a new line between rows
