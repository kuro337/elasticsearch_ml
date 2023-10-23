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

from model.models import User, Post, Interaction

import pandas as pd

from utils.prepare import (
    prepare_dataframe_from_documents,
    drop_irrelevant_columns_config,
)

from utils.dataframes import compare_dataframe_columns
from utils.sample_docs import users, posts, interactions

from utils.models import (
    DocumentGLMConfig,
    DateDifferenceFeatureConfig,
    InteractionTypeConfig,
    EntityColumns,
    CategoricalVariableConfig,
    RelevancyConfig,
    ScoringConfig,
)

from cache.save_model import save_model

from scoring.train_model import train_and_evaluate_config

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

feature_config = DateDifferenceFeatureConfig(
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
        entity=User, columns=["gender", "username", "country"], primary_key="username"
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

include_columns = RelevancyConfig(
    entity_a=EntityColumns(entity=User, columns=["gender", "username", "country"]),
    entity_b=EntityColumns(entity=Post, columns=["lang", "author", "post_id"]),
    interaction=EntityColumns(
        entity=Interaction, columns=["interaction_type", "viewed"]
    ),
    features=["post_age"],
    target="viewed",
)

"""
Represents State of the Entire GLM Regression Model for our Dataset

@Actions
- We do One Hot Encoding (New Cols for Categorical Data)
- Feature Engineering (New Cols for Date Difference , Post Age , etc.)
"""
model_state_mapping = ScoringConfig(
    target_variable="viewed",
    entity_a=User,
    entity_a_pk="username",
    entity_a_categorical_cols=["gender", "username", "country"],
    entity_b=Post,
    entity_b_pk="post_id",
    entity_b_categorical_cols=["lang", "author", "post_id"],
    model_entity=Interaction,
    model_variance_key="interaction_type",
    model_default_value="error",
    model_categorical_cols=["interaction_type"],
    feature_cols=["post_age"],
)

print("Merging from Doc Merge ESDoc\n")


merged_df_from_docs = prepare_dataframe_from_documents(
    entity_a=entity_a_config,
    entity_b=entity_b_config,
    entity_mapping=interactions_config,
)
merged_df_from_docs = apply_date_difference_feature(merged_df_from_docs, feature_config)

merged_df_interaction_binomial = map_interaction_type_config(
    merged_df_from_docs, binomial_config
)

merged_df_one_encode = one_hot_encode_config(
    merged_df_interaction_binomial, one_encoding_config
)


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


# Keep a copy of the original DataFrame for later reference
## COPY OF ESDOC - USE THIS TO GET USER-POST SCORES - NOT FOR TRAINING
##
merged_df_one_encode_copy = merged_df_one_encode.copy()

# DROP Columns for ESDoc Training
print("Printing Columns Before Dropping\n\n")
print(merged_df_one_encode.columns)

# Copies of cols from Original Data for Insights from Scoring.
# Add additional columns if needed such as Lang, Gender, etc.
og_users = merged_df_one_encode["user_username"]
og_posts = merged_df_one_encode["post_post_id"]

training_df = drop_irrelevant_columns_config(include_columns, merged_df_one_encode)
scoring_df = training_df.copy()


compare_dataframe_columns(scoring_df, training_df, "Scoring Data", "Training Data")


print("Printed Relevant Columns\n\n")

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
features_for_scoring = scoring_df.drop(columns=["viewed"])


print("Scoring Model")
# Now, use the trained model to predict probabilities and pass it the SCORING DATA (new/unseen)
# Columns in the Scoring Data should match exactly dataset as it was trained on
predicted_probabilities = lr_c.predict_proba(features_for_scoring)

print("Scored Model")

# These were copies we made of primary key fields in line 210-211
# We add them here because the exact same Model has to be used for Scoring
features_for_scoring["user_username"] = og_users
features_for_scoring["post_post_id"] = og_posts

# Extract the probabilities of class 1 (viewed)
scores = predicted_probabilities[:, 1]

# Add the scores back to the original dataframe copy
features_for_scoring["score"] = scores

print("\nDebug: Columns in features_for_scoring\n", features_for_scoring.columns)
print("\nDebug: Top 5 rows in features_for_scoring\n")
print(features_for_scoring.head())

# Getting User Scores for Each Post
user_post_scores = (
    features_for_scoring.groupby(["user_username", "post_post_id"])["score"]
    .mean()
    .reset_index()
)

print("\nUser-Post Scores\n")
print(user_post_scores)

# User-Post Matrix
user_post_score_matrix = user_post_scores.pivot(
    index="post_post_id", columns="user_username", values="score"
)

# Fill NaN values
user_post_score_matrix = user_post_score_matrix.fillna(0)

print("\nUser-Post Score Matrix\n")
print(user_post_score_matrix)

# Printing Scores for Specific User
single_user_scores = features_for_scoring[
    features_for_scoring["user_username"] == "Fiero Martin"
][["post_post_id", "score"]]

print("\nFiero Martin's Scores\n")
print(single_user_scores)
print("\nFiero Martin's end\n")

# List Posts by Average Score
average_scores = (
    features_for_scoring.groupby("post_post_id")["score"].mean().reset_index()
)
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
