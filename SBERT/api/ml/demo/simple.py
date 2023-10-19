"""
Demo using SBERT to find the similarity between a query and a passage

Models :

- all-mpnet-base-v2
- paraphrase-multilingual-mpnet-base-v2
- all-MiniLM-L12-v2
- multi-qa-MiniLM-L6-cos-v1
- paraphrase-MiniLM-L6-v2

"""

from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

query_embedding = model.encode("Name:Zerin,Age:28,Visits:0", convert_to_tensor=True)


passage_embedding = model.encode(
    [
        "Name:Polinzsk Email:pola@gmail.com Age:25 Visits:250",
        "Name:Zeron Email:zerppp@windows.com Age:21 Visits:2",
        "Name:Aakash Email:akaizn@shopify.com Age:28 Visits:33",
        "Name:Peronaz Email:perona@peron.com Age:30 Visits:11144",
        "Name:Milvani Email:melou@gmail.com Age:18 Visits:999",
        "abc@zzz.com",
    ],
    convert_to_tensor=True,
)

print(
    f"Dimensionality of the current model: {model.get_sentence_embedding_dimension()}"
)

# Semantic Similarity - use cosine-similarity
print("Similarity:", util.cos_sim(query_embedding, passage_embedding))

# Use dot-product to calculate similarity for Frequency of Words
print("Similarity:", util.dot_score(query_embedding, passage_embedding))


# Dot Product can be useful when Magnitude of Vectors is Important

# For ex :
# Document A: Vector A = [3, 4, 2] (representing counts of three distinct words)
# Document B: Vector B = [1, 2, 1] (representing counts of the same three distinct words)

# Here - Dot Product can be useful in doing Document Matching to see frequency of Words in Documents
