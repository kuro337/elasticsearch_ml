"""
Prepare Data

By analyzing the coefficients of the logistic regression model, 
we can see which features have the most influence on whether a user views a post. 

Positive coefficients indicate a feature that increases the likelihood of viewing, 
Negative coefficients indicate a feature that decreases the likelihood. 

This can provide insights into user behavior and preferences.

Required Funcs

utils.prepare

prepare_model_dataframe - no deps
perform_feature_engineering - featureengineeringfoler
get_encoded_column_names - none

utils.models

DataModelMapping
Entity
Mapping

scoring.train_model

train_and_evaluate

"""
import sys

import pandas as pd
import numpy as np
from model.models import User, Post, Interaction, UserPostScore

from mock.mock_users import users
from mock.mock_posts import posts
from mock.mock_interactions import interactions


from utils.prepare import (
    prepare_dataframe_from_documents,
    drop_irrelevant_columns_config,
    extract_columns_for_retention,
    add_columns_to_dataframe,
)


from utils.dataframes import compare_dataframe_columns

from utils.models import (
    DocumentGLMConfig,
    DateDifferenceFeatureConfig,
    InteractionTypeConfig,
    EntityColumns,
    CategoricalVariableConfig,
    RelevancyConfig,
    ScoringConfig,
    RetainColumnsConfig,
    EntityConfig,
    MappingConfig,
    MapScoringToOriginalData,
    EntityScoringConfig,
)

from cache.save_model import save_model

from scoring.train_model import train_and_evaluate_config
from scoring.insights import map_scores_to_merged_df

from features.feature_engineering import (
    apply_date_difference_feature,
    map_interaction_type_config,
    one_hot_encode_config,
)

# 1. Feature Engineering

# 1.1 Loading and Merging the Data


# Using Objects Directly

print("Loading and Merging the Data\n")

# ________________
# @Config

# Entity ESDoc Class Configs for GLM
# Works using List[ESDoc] Directly such as User, Post , Interaction , Product
# ________________

# ---------
# @GLMConfigs
# ---------
entity_a_config = DocumentGLMConfig(doc_list=users, merge_key="username")
entity_b_config = DocumentGLMConfig(doc_list=posts, merge_key="post_id")

interactions_config = DocumentGLMConfig(
    doc_list=interactions,
    variance_key="interaction_type",
    default_value="error",
)

date_feature_config = DateDifferenceFeatureConfig(
    start_entity=Post,
    end_entity=Interaction,
    start_time_col="timestamp",
    end_time_col="timestamp",
    new_col="post_age",
)

"""
This Config Adds One Hot Encoding to the DataFrame for Categorical Variables 

Used to create the Data - Model Trains On (numeric)

The Primary Key attribute if passed - will be retained (since required for Scoring)
If PK passed - ensure removal of the PK columns from Training Data (user_username , post_post_id)
"""
one_encoding_config = CategoricalVariableConfig(
    entity_a=EntityColumns(
        entity=User, columns=["gender", "country"], primary_key="username"
    ),
    entity_b=EntityColumns(
        entity=Post, columns=["post_id", "author", "lang"], primary_key="post_id"
    ),
    interaction=EntityColumns(entity=Interaction, columns=["interaction_type"]),
)

binomial_config = InteractionTypeConfig(
    entity=Interaction,
    column="interaction_type",
    new_col="viewed",
    condition="view",
)

"""
Columns to Include in the Model Training
We map interaction_type=view as the Target Variable
So make sure to NOT include interaction_type
"""
include_columns = RelevancyConfig(
    entity_a=EntityColumns(entity=User, columns=["gender", "country"]),
    entity_b=EntityColumns(entity=Post, columns=["lang", "author"]),
    # interaction=EntityColumns(
    #     entity=Interaction, columns=["interaction_type", "viewed"]
    # ),
    features=["post_age"],
    target="viewed",
)

retain_columns = RetainColumnsConfig(
    entity_a_retain=EntityColumns(entity=User, columns=["username"]),
    entity_b_retain=EntityColumns(entity=Post, columns=["post_id"]),
)


# ---------

print("Merging from Doc Merge ESDoc\n")


merged_df_from_docs = prepare_dataframe_from_documents(
    entity_a=entity_a_config,
    entity_b=entity_b_config,
    entity_mapping=interactions_config,
)

# print(merged_df_from_docs.columns)

merged_df_from_docs = apply_date_difference_feature(
    merged_df_from_docs, date_feature_config
)


# print(merged_df_from_docs.columns)
# print(f"Number of rows in merged_df_from_docs: {len(merged_df_from_docs)}")


merged_df_interaction_binomial = map_interaction_type_config(
    merged_df_from_docs, binomial_config
)


merged_df_one_encode = one_hot_encode_config(
    merged_df_interaction_binomial, one_encoding_config
)

# print(merged_df_one_encode.columns)
# print(f"Number of rows in merged_df_from_docs: {len(merged_df_one_encode)}")
# sys.exit(1)

print("Printing from Doc Merge ESDoc\n")
print(merged_df_from_docs)
print(merged_df_from_docs.columns)

print(
    "\nMake Sure the PRIMARY_KEY IS PRESENT HERE TOO Columns we Need for Scoring (such as username and postid) are PRESENT\n"
)

print(merged_df_interaction_binomial.columns)

print(
    "\nMake Sure the Columns we Need for Scoring (such as username and postid) are PRESENT\n"
)
print(merged_df_one_encode.columns)

print(merged_df_from_docs.post_age)

print("Printed from Doc Merge ESDoc\n")


# DROP Columns for ESDoc Training
print("Printing Columns Before Dropping\n\n")
print(merged_df_one_encode.columns)

# Copies of cols from Original Data for Insights from Scoring.
# Add additional columns if needed such as Lang, Gender, etc.
# Pandas Dataframe maintains the index - so we can simply add it back to the DataFrame and it maps to right rows

original_data = merged_df_from_docs.copy()


print("Printing VIEWED STATUS Dropping\n\n")
print("viewed" in merged_df_one_encode.columns)

retained_columns = extract_columns_for_retention(merged_df_one_encode, retain_columns)


training_df = drop_irrelevant_columns_config(
    merged_df_one_encode,
    include_columns,
)
print("Printed Relevant Columns\n\n")
print(training_df["viewed"].value_counts())


### PERFORM TRAINING
# TRAIN ESDoc Data
lr_c, metrics_c = train_and_evaluate_config(training_df, target_column="viewed")
print(metrics_c)

save_model(lr_c, "cache/logistic_regression_model.joblib")


for metric, value in metrics_c.items():
    print(f"{metric}: {value}")

print(lr_c)

# Create a DataFrame to hold the feature names and coefficients
coef_df = pd.DataFrame(
    {"Feature": training_df.columns.drop("viewed"), "Coefficient": lr_c.coef_[0]}
).sort_values(by="Coefficient", ascending=False)

# Getting Odds
coef_df = coef_df.assign(Odds_ratio=np.exp(coef_df.get("Coefficient")))


print("\nCoefficients and Odds Ratios (sorted by value):")
print(coef_df.to_string(index=False))

# Print the sorted coefficients and the intercept
print("\nCoefficients (sorted by value):")
print(coef_df.to_string(index=False))
print(f"\nIntercept: {lr_c.intercept_[0]}")


print(
    "EsDoc Training Done\n\n-----------------------------\n---------------------------\n"
)

# SCORING
# Provide Different Data for Scoring than Training Data
# Make sure the New Scoring Data goes through the same Feature Engineering Pipeline
# EsDoc - Using Trained Model to Score User-Post


# Ensure 'viewed' column is dropped since it's the target
features_for_scoring = training_df.drop(columns=["viewed"])


print("Scoring Model")
# Now, use the trained model to predict probabilities and pass it the SCORING DATA (new/unseen)
# Columns in the Scoring Data should match exactly dataset as it was trained on
predicted_probabilities = lr_c.predict_proba(features_for_scoring)

print("Scored Model")

### ADDING BACK RETAINED COLUMNS FOR MAPPING SCORES

features_for_scoring = add_columns_to_dataframe(
    features_for_scoring,
    retained_columns,
    {"user_username": "username", "post_post_id": "post_id"},
)


# Define the names of entity A primary key and entity B primary key
entity_a_pk = "username"
entity_b_pk = "post_id"

### RETAIN_END------------------------

# Extract the probabilities of class 1 (viewed)
scores = predicted_probabilities[:, 1]

# Add the scores back to the original dataframe copy
features_for_scoring["score"] = scores


# MAPPING SCORES TO ORIGINAL DATA

# print number of rows in original_data
print(f"Number of rows in original_data: {len(original_data)}")
print(f"Number of rows in mapped_data_with_scores: {len(features_for_scoring)}")


mapping_scores_config = MapScoringToOriginalData(
    entity_a=EntityScoringConfig(
        entity=User,
        primary_key="username",
        display_fields=["gender", "country", "username"],
    ),
    entity_b=EntityScoringConfig(
        entity=Post,
        primary_key="post_id",
        display_fields=["lang", "author", "post_id"],
    ),
    score_field="score",
)

mapped_data_with_scores = map_scores_to_merged_df(
    original_data,
    features_for_scoring,
    scores_map=mapping_scores_config,
)

print(f"Number of rows in mapped_data_with_scores: {len(mapped_data_with_scores)}")
# Number of rows in mapped_data_with_scores: 33

# Check this val -> James Martin JVM Heap Allocation  0.583702

# -------------------END MAPPING SCORES TO ORIGINAL DATA

print("\nDebug: Columns in features_for_scoring\n", features_for_scoring.columns)
print("\nDebug: Top 5 rows in features_for_scoring\n")
print(features_for_scoring.head())

# Getting User Scores for Each Post
user_post_scores = (
    features_for_scoring.groupby([entity_a_pk, entity_b_pk])["score"]
    .mean()
    .reset_index()
)

for index, row in user_post_scores.iterrows():
    user_post_score = UserPostScore(
        username=row[entity_a_pk],
        post_id=row[entity_b_pk],
        score=row["score"],
    )
    print(f"\nUser-Post Score:\n{user_post_score.dump_document()}")

print("\nUser-Post Scores\n")
print(user_post_scores)

# User-Post Matrix
user_post_score_matrix = user_post_scores.pivot(
    index=entity_b_pk, columns=entity_a_pk, values="score"
)

# Fill NaN values
user_post_score_matrix = user_post_score_matrix.fillna(0)

print("\nUser-Post Score Matrix\n")
print(user_post_score_matrix)

# Printing Scores for Specific User
single_user_scores = features_for_scoring[
    features_for_scoring[entity_a_pk] == "Fiero Martin"
][[entity_b_pk, "score"]]

print("\nFiero Martin's Scores\n")
print(single_user_scores)
print("\nFiero Martin's end\n")

# List Posts by Average Score
average_scores = features_for_scoring.groupby(entity_b_pk)["score"].mean().reset_index()
sorted_posts = average_scores.sort_values(by="score", ascending=False)

print("\nSorted Posts by Scores\n")
print(sorted_posts)

# For top 10 posts
top_10_posts = sorted_posts.head(10)

print("\nTop 10 Posts\n")
print(top_10_posts)


print(
    "EsDoc Scoring Done\n\n-----------------------------\n---------------------------\n"
)

# If we have a new User and want to return the relevant Posts that they are likely to view - we would

# Create a Dataframe with the User, all Posts , and 4 Fake Interaction Rows for the User-Post
# Pass this data as Scoring Data to the Trained Model - and get the Scores for the top 10 Posts.

# Searching in ES using elasticsearch_dsl - to save the User-Post Scores

# UserPostScore - Model created in Library
# from elasticsearch_dsl import Search

# def get_top_posts_for_user(username, top_n=10):
#     s = Search(index="user_post_scores").query("match", username=username).sort({"score": {"order": "desc"}})[0:top_n]
#     response = s.execute()
#     for hit in response:
#         print(hit.post_id, hit.score)  # or do something else with these
