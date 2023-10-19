"""
Demo using SBERT to find the similarity between a query and a passage

Models :

- all-mpnet-base-v2
- paraphrase-multilingual-mpnet-base-v2
- all-MiniLM-L12-v2
- multi-qa-MiniLM-L6-cos-v1
- paraphrase-MiniLM-L6-v2

Best Quality - paraphrase-multilingual-mpnet-base-v2
Best Speed for Embeddings - paraphrase-MiniLM-L6-v2

"""

from sentence_transformers import SentenceTransformer, util
import torch

import matplotlib.pyplot as plt

import seaborn as sns

import pandas as pd

# Initialize model
model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

# Define the queries and data
queries = [
    "Name:Zerin,Age:28,Visits:0",
    "Name:Akron,Visits:2",
    "Name:Milvani,Age:18,Visits:996",
    "Aakash aakash@shopify.com 28",
]

data = [
    "Name:Polinzsk Email:pola@gmail.com Age:25 Visits:250",
    "Name:Zeron Email:zerppp@windows.com Age:21 Visits:2",
    "Name:Aakash Email:akaizn@shopify.com Age:28 Visits:33",
    "Name:Peronaz Email:perona@peron.com Age:30 Visits:11144",
    "Name:Milvani Email:melou@gmail.com Age:18 Visits:999",
    "abc@zzz.com",
]


def calculate_and_display_similarities(model_query, model_data):
    """
    Function to calculate and display similarities
    """

    query_embedding = model.encode(model_query, convert_to_tensor=True)
    passage_embeddings = model.encode(model_data, convert_to_tensor=True)

    # Calculate similarities
    cos_similarities = util.cos_sim(query_embedding, passage_embeddings)[0]
    dot_similarities = util.dot_score(query_embedding, passage_embeddings)[0]

    # Sort the similarities and data together from highest to lowest similarity
    cos_sorted_indices = torch.argsort(cos_similarities, descending=True)
    dot_sorted_indices = torch.argsort(dot_similarities, descending=True)

    print(f"\nQuery: {model_query}")
    print("Cosine Similarities:")
    for index in cos_sorted_indices:
        print(f"{model_data[index]}: {cos_similarities[index].item()}")

    print("Dot Similarities:")
    for index in dot_sorted_indices:
        print(f"{model_data[index]}: {dot_similarities[index].item()}")

    model_cos_data = {
        model_data[idx]: cos_similarities[idx].item() for idx in cos_sorted_indices
    }
    model_dot_data = {
        model_data[idx]: dot_similarities[idx].item() for idx in dot_sorted_indices
    }

    return model_cos_data, model_dot_data


# Process each query
all_cos_data = []
all_dot_data = []
for query in queries:
    cos_data, dot_data = calculate_and_display_similarities(query, data)
    # Process each query
    all_cos_data.append(cos_data)
    all_dot_data.append(dot_data)


# Creating DataFrame
cos_df = pd.DataFrame(all_cos_data, index=queries)
dot_df = pd.DataFrame(all_dot_data, index=queries)

fig, ax = plt.subplots(len(queries) * 2, 1, figsize=(10, 5 * len(queries)))
for idx, query in enumerate(queries):
    sns.heatmap(data=cos_df.loc[[query]].T, annot=True, ax=ax[idx * 2], fmt=".2f")
    ax[idx * 2].set_title(f"Cosine Sim - {query}")
    sns.heatmap(data=dot_df.loc[[query]].T, annot=True, ax=ax[idx * 2 + 1], fmt=".2f")
    ax[idx * 2 + 1].set_title(f"Dot Product Sim - {query}")

plt.tight_layout()
plt.subplots_adjust(wspace=0.5, hspace=0.5)  # adjusted spacing

plt.savefig("results/similarity_heatmaps.svg")
