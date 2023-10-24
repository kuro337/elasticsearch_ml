"""
Pass Data to Prepare for GLM Model Training and Scoring
"""
import sys
import pandas as pd

from typing import List, Tuple, Optional

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
    EntityMergeConfig,
)

from features.feature_engineering import (
    apply_date_difference_feature,
    map_interaction_type_config,
    one_hot_encode_config,
)

from utils.prepare import (
    prepare_dataframe_from_documents,
    drop_irrelevant_columns_config,
    extract_columns_for_retention,
    add_columns_to_dataframe,
)


def prepare_dataset_glm(
    state: ScoringConfig, copy: bool = True
) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
    """
    @ModelPreparation
    - Prepare GLM Dataset from Configuration

    @Return
    transformed_df , original_df (optional)

    @Usage

    ```py
    # Prepare Dataset for GLM Model - with Copy of Data after Transforms
    transformed_df, original_df = prepare_dataset_glm(state_config, copy=True)

    # Copy defaults to False
    transformed_df = prepare_dataset_glm(state_config)

    ```
    """
    # Construct Merge Config from State Settings
    merge_config = EntityMergeConfig(
        entity_a=DocumentGLMConfig(
            doc_list=state.entity_a.data, merge_key=state.entity_a.primary_key
        ),
        entity_b=DocumentGLMConfig(
            doc_list=state.entity_b.data, merge_key=state.entity_b.primary_key
        ),
        mapping=DocumentGLMConfig(
            doc_list=state.mapping.data,
            variance_key=state.mapping.variance_key,
            default_value=state.mapping.default_value,
        ),
    )

    # Perform Merge
    merged_df_entities = prepare_dataframe_from_documents(
        entity_a=merge_config.entity_a,
        entity_b=merge_config.entity_b,
        entity_mapping=merge_config.mapping,
    )

    # print(merged_df_entities.columns)

    # Loop through Features and apply Feature Engineering
    for feature in state.features:
        merged_df_entities = feature.apply(merged_df_entities)

    if copy:
        original_data = merged_df_entities.copy()

    # print(f"Number of rows in merged_df_from_docs: {len(merged_df_entities)}")
    # print(merged_df_entities.columns)

    # Apply Feature Engineering for Target Variable
    merged_df_interaction_binomial = map_interaction_type_config(
        merged_df_entities, state.target_config
    )

    # Create Configuration for One Hot Encoding from State Settings
    one_encoding_config = CategoricalVariableConfig(
        entity_a=EntityColumns(
            entity=state.entity_a.entity,
            columns=state.entity_a.categorical_fields,
            primary_key=state.entity_a.primary_key,
        ),
        entity_b=EntityColumns(
            entity=state.entity_b.entity,
            columns=state.entity_b.categorical_fields,
            primary_key=state.entity_b.primary_key,
        ),
        interaction=EntityColumns(
            entity=state.mapping.entity, columns=state.mapping.categorical_fields
        ),
    )

    # Apply One Hot Encoding
    """
    This Config Adds One Hot Encoding to the DataFrame for Categorical Variables 

    Used to create the Data - Model Trains On (numeric)

    The Primary Key attribute if passed - will be retained (since required for Scoring)
    If PK passed - ensure removal of the PK columns from Training Data (user_username , post_post_id)
    """
    merged_df_categorical_fields_encoded = one_hot_encode_config(
        merged_df_interaction_binomial, one_encoding_config
    )

    print(merged_df_categorical_fields_encoded.columns)
    print("Printing VIEWED STATUS Dropping\n\n")
    print("viewed" in merged_df_categorical_fields_encoded.columns)
    print(
        f"Number of rows in merged_df_from_docs: {len(merged_df_categorical_fields_encoded)}"
    )

    # Return the DataFrame with the Target Variable
    if copy:
        return merged_df_categorical_fields_encoded, original_data
    return merged_df_categorical_fields_encoded, None
