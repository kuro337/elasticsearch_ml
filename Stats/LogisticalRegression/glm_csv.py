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
)

from utils.models import (
    DataModelMapping,
    Entity,
    Mapping,
)


from scoring.train_model import train_and_evaluate


# 1. Feature Engineering

# 1.1 Loading and Merging the Data

# CONFIG OBJECT - Define Entities and Mapping
data_model = DataModelMapping(
    entities=[
        Entity(
            index="users",
            path="../dataset/csv/users.csv",
            # field="userxx",
            merge_key="username",
        ),
        Entity(
            index="posts",
            path="../dataset/csv/posts.csv",
            # field="postxx",
            merge_key="post_id",
        ),
    ],
    mapping=Mapping(
        index="interactions",
        path="../dataset/csv/interactions.csv",
        variance_field="interaction_type",
        default="none",
    ),
)

# Using Objects Directly
# implement

print("Loading and Merging the Data\n")

# Converts 3 csv's to a Single DataFrame - and adds Default Values where no Join between User+Post on Interaction
merged_df = prepare_model_dataframe(data_model.model_dump())


merged_df_encoded = perform_feature_engineering(merged_df)

print("Printing merged dataframe Head after Feature Engineering\n")
print(merged_df_encoded.head())
print("Printing all column names\n")
print(merged_df_encoded.columns)


# Keep a copy of the original DataFrame for later reference
## USE THIS TO GET USER-POST SCORES - NOT FOR TRAINING
merged_df_copy = merged_df_encoded.copy()


# RELEVANCY_COLUMNS - CSV
columns_to_encode = [
    "gender",
    "country",
    "lang",
    "author",
    "interaction_type",
    "viewed",
]
# Getting the names of the encoded columns to keep for training
columns_to_keep = get_encoded_column_names(columns_to_encode, merged_df_encoded)
print("\nColumn Names to be Used for Training Set\n")
print(columns_to_keep)
# Dropping the identified irrelevant columns
merged_df_encoded = merged_df_encoded[
    merged_df_encoded.columns[merged_df_encoded.columns.isin(columns_to_keep)]
]

print("\nPrinting remaining column names for TRAIN SET\n")
print(merged_df_encoded.columns)


# Usage - CSV
lr, metrics = train_and_evaluate(merged_df_encoded, target_column="viewed")
print(metrics)

for metric, value in metrics.items():
    print(f"{metric}: {value}")


# Create a DataFrame to hold the feature names and coefficients
coef_df = pd.DataFrame(
    {"Feature": merged_df_encoded.columns.drop("viewed"), "Coefficient": lr.coef_[0]}
).sort_values(by="Coefficient", ascending=False)


# Print the sorted coefficients and the intercept
print("\nCoefficients (sorted by value):")
print(coef_df.to_string(index=False))
print(f"\nIntercept: {lr.intercept_[0]}")

# 2. Computing Scores


# Dropping the target column 'viewed' as it's not a feature
features_df = merged_df_copy[merged_df_encoded.columns].drop(columns=["viewed"])


# Compute predicted probabilities
predicted_probabilities = lr.predict_proba(features_df)

# Extract the probabilities of the positive class (class 1: viewed)
# The second column of the output gives the predicted probabilities of the positive class
scores = predicted_probabilities[:, 1]

# Create a new column in the original data to hold the scores
merged_df_copy["score"] = scores

# Printing all Users and their Scores associated with Posts

user_post_scores = (
    merged_df_copy.groupby(["username", "post_id"])["score"].mean().reset_index()
)

# Pivot the data to get a user-post score matrix
user_post_score_matrix = user_post_scores.pivot(
    index="post_id", columns="username", values="score"
)

# Fill any NaN values with a default score, if desired (e.g., 0)
user_post_score_matrix = user_post_score_matrix.fillna(0)

# Now, user_post_score_matrix will have posts as rows, users as columns,
# and the cells will contain the scores

# Print the results
print("\nUser-Post Score Matrix\n")
print(user_post_score_matrix)

# Score for a User
john_doe_scores = merged_df_copy[merged_df_copy["username"] == "JohnDoe"][
    ["post_id", "score"]
]

# Print or save the scores to a file
print("\nJohn Scores\n")

print(john_doe_scores)

print(merged_df_copy.head())
print(merged_df_copy.columns)
average_scores = merged_df_copy.groupby("post_id")["score"].mean().reset_index()

sorted_posts = average_scores.sort_values(by="score", ascending=False)
print("\nSorted Posts\n")

print(sorted_posts)

print("\nTop 10 Posts\n")
top_10_posts = sorted_posts.head(10)
print(top_10_posts)
