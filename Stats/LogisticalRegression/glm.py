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
    prepare_model_dataframe,
    perform_feature_engineering,
    get_encoded_column_names,
    prepare_dataframe_from_documents,
    drop_irrelevant_columns_config,
    prepare_data_for_training_and_scoring,
)

from utils.models import (
    DataModelMapping,
    DocumentGLMConfig,
    DateDifferenceFeatureConfig,
    InteractionTypeConfig,
    Entity,
    Mapping,
    EntityColumns,
    CategoricalVariableConfig,
    RelevancyConfig,
    ScoringConfig,
)

from utils.dataframes import compare_dataframe_columns

from utils.sample_docs import users, posts, interactions

from scoring.train_model import train_and_evaluate, train_and_evaluate_config

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

# Entity ESDoc Class Configs for GLM
# Works using List[ESDoc] Directly such as User, Post , Interaction , Product

# ________________

# ---------

# GLM Configs

# Define Configuration for GLM Model Here

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

# Maintains State of Original Data and State of Data After Feature Engineering
# We do One Hot Encoding (New Cols for Categorical Data)
# Feature Engineering (New Cols for Date Difference , Post Age , etc.)
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

og_users = merged_df_one_encode["user_username"]
og_posts = merged_df_one_encode["post_post_id"]

training_df = drop_irrelevant_columns_config(include_columns, merged_df_one_encode)
scoring_df = training_df.copy()


compare_dataframe_columns(scoring_df, training_df, "Scoring Data", "Training Data")


print("Printed Relevant Columns\n\n")
# TRAIN ESDoc Data
lr_c, metrics_c = train_and_evaluate_config(training_df, target_column="viewed")
print(metrics_c)

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

# CONFIRM COLUMNS MATCH FOR TRAINING AND FIT
print("\n------------------- Column Matching Verification -------------------\n")
print("Columns used for model training:")
training_columns = training_df.drop(columns=["viewed"]).columns
print(training_columns)

print("\nColumns in data used for scoring/predictions:")
scoring_columns = features_for_scoring.columns
print(scoring_columns)

# Check if both have the same set of columns
if set(training_columns) == set(scoring_columns):
    print("\nColumns match: Yes")
else:
    print("\nColumns match: No")
    # If there's a mismatch, you can display the differing columns for debugging
    missing_in_scoring = set(training_columns) - set(scoring_columns)
    missing_in_training = set(scoring_columns) - set(training_columns)
    print("\nColumns present in training but missing in scoring:", missing_in_scoring)
    print("\nColumns present in scoring but missing in training:", missing_in_training)

print("\n--------------------------------------------------------------------\n")

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

# Add debug prints to understand the structure of your DataFrame
print("\nDebug: Columns in features_for_scoring\n")
print(features_for_scoring.columns)  # This will list all columns in your DataFrame
print("\nDebug: Top 5 rows in features_for_scoring\n")
print(features_for_scoring.head())  # This will print the first 5 rows of your DataFrame

# If you want to examine user-post scores, you can group the data by username and post_id and then calculate average scores
user_post_scores = (
    features_for_scoring.groupby(["user_username", "post_post_id"])["score"]
    .mean()
    .reset_index()
)

print("\nUser-Post Scores\n")
print(user_post_scores)

# To create a user-post matrix, you can pivot the table
user_post_score_matrix = user_post_scores.pivot(
    index="post_post_id", columns="user_username", values="score"
)

# Fill NaN values with 0 or any other identifier for no interaction
user_post_score_matrix = user_post_score_matrix.fillna(0)

print("\nUser-Post Score Matrix\n")
print(user_post_score_matrix)

# If you want to print scores for a specific user, e.g., 'JohnDoe'
john_doe_scores = features_for_scoring[
    features_for_scoring["user_username"] == "JohnDoe"
][["post_post_id", "score"]]

print("\nJohnDoe's Scores\n")
print(john_doe_scores)

# You can also list posts sorted by their average score
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
