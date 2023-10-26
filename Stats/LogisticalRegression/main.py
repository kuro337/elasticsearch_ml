"""
@LogisticalRegression
- General Linear Model

@Prepare
@Train
@Score

@Elasticsearch
"""
from mock_data.mock_users import users
from mock_data.mock_posts import posts
from mock_data.mock_interactions import interactions
from mock_data.gen_feature_set import simulate_interactions
from model.models import User, Post, Interaction

from utils.models import (
    DateDifferenceFeatureConfig,
    InteractionTypeConfig,
    ScoringConfig,
    EntityConfig,
    MappingConfig,
)

from utils.prepare import (
    drop_irrelevant_columns_config,
    extract_columns_for_retention,
)

from prepare.prepare_data import prepare_dataset_glm
from scoring.train_model import train_and_evaluate_config
from scoring.score import score_data, map_scores_to_data, get_scores
from cache.save_model import save_model, print_model_coefficients


# 1. Dataset Preparation

# 1.1 Loading and Merging the Data

print("Loading and Merging the Data\n")

# @MockData
interactions = simulate_interactions(users, posts, random_attribute=True)

"""
@Config
@Compatibility -> List[ESDoc]
@GLMConfigs

Represents State of the Entire GLM Regression Model for our Dataset

@Actions
- We do One Hot Encoding (New Cols for Categorical Data)
- Feature Engineering (New Cols for Date Difference , Post Age , etc.)
"""
model_state_mapping = ScoringConfig(
    entity_a=EntityConfig(
        entity=User,
        primary_key="username",
        categorical_fields=["gender", "username", "country"],
        training_fields=["gender", "country"],
        data=users,
    ),
    entity_b=EntityConfig(
        entity=Post,
        primary_key="post_id",
        categorical_fields=["lang", "author", "post_id"],
        training_fields=["lang", "author"],
        data=posts,
    ),
    mapping=MappingConfig(
        entity=Interaction,
        default_value="error",
        variance_key="interaction_type",
        categorical_fields=["interaction_type"],
        data=interactions,
    ),
    features=[
        DateDifferenceFeatureConfig(
            start_entity=Post,
            end_entity=Interaction,
            start_time_col="timestamp",
            end_time_col="timestamp",
            new_col="post_age",
        )
    ],
    target_variable="viewed",
    target_config=InteractionTypeConfig(
        entity=Interaction,
        column="interaction_type",
        new_col="viewed",
        condition="view",
    ),
    feature_fields=["post_age"],
    score_field="score",
    debug=True,
)


print("Merging from Doc Merge ESDoc\n")

# @Merge
merged_df_one_encode, original_data = prepare_dataset_glm(
    model_state_mapping, copy=True
)


# @Retain
# Cloning Series for Retention for Scoring and Mapping

retained_columns = extract_columns_for_retention(
    merged_df_one_encode, state=model_state_mapping
)

training_df = drop_irrelevant_columns_config(
    merged_df_one_encode,
    state=model_state_mapping,
)

print("Printed Relevant Columns\n\n")
print(training_df["viewed"].value_counts())


# @Training

# @Cache
# lr_c = load_model("cache/logistic_regression_model.joblib") # Using Cached Model

# @Train
# Training a New Model

# @Model @Metrics - Trained Model & Training Metrics
lr_c, metrics_c = train_and_evaluate_config(
    training_df, target_column="viewed", debug=True
)

save_model(lr_c, "cache/logistic_regression_model.joblib")

print_model_coefficients(lr_c, training_df)


# @Scoring

# - With a Trained Model - we can pass New Data and make Predictions
# - Data passed requires passthrough of Feature Engineering Pipeline

predicted_probabilities = score_data(training_df, lr_c)
print("Scored Model")
scores = predicted_probabilities[:, 1]


final_data_scored = map_scores_to_data(
    original_data=original_data,
    transformed_data=training_df,
    retained_dfs=retained_columns,
    model_scores=scores,
    state=model_state_mapping,
    score_field="score",
)

get_scores(final_data_scored, model_state_mapping)

# <==============================================EOF
