from abc import ABC
from typing import Dict, List, Optional, Type
from model.interface import ESDocument
from pydantic import BaseModel


class Entity(BaseModel):
    """
    Represents the Entity to be used in the Model

    Entity(type="users", path="path/to/csv", field="user", merge_key="username")
    """

    index: str
    path: str
    # field: str
    merge_key: str


class Mapping(BaseModel):
    """
    Represents the Entity to be used in the Model

    Mapping(index="interactions", path="path/to/csv", field="interaction_type", default="null")
    """

    index: str
    path: str
    variance_field: str
    default: str


class DateDifferenceFeatureConfig(BaseModel):
    """
    Configuration for feature engineering steps.
    Includes information about columns used for specific calculations and transformations.
    """

    start_entity: Type[ESDocument] | str
    start_time_col: str
    end_entity: Type[ESDocument] | str
    end_time_col: str
    new_col: str


class InteractionTypeConfig(BaseModel):
    """
    Feature Engineering for Mapping Interaction Type as a Binomial Feature
    """

    entity: Type[ESDocument]
    column: str
    new_col: str
    condition: str


class EntityColumns(BaseModel):
    """
    Config for specifying Columns to be used
    """

    entity: Type[ESDocument]
    columns: List[str]
    primary_key: str = None


class ScoringConfig(BaseModel):
    """
    Config to Map the Scoring Data to the Training Data

    We might have User and Post with categorical variables such as post_language, user_gender , username , post_id - etc.

    When we One-Encode our data we drop all other columns and retain only the numeric columns.

    Once we have the Model - we use this to maintain the mapping between our Transformations and Original Data
    """

    target_variable: str

    entity_a: Type[ESDocument]
    entity_a_pk: str
    entity_a_categorical_cols: List[str]

    entity_b: Type[ESDocument]
    entity_b_pk: str
    entity_b_categorical_cols: List[str]

    model_entity: Type[ESDocument]
    model_variance_key: str
    model_default_value: str
    model_categorical_cols: List[str]

    feature_cols: List[str]


class CategoricalVariableConfig(BaseModel):
    """
    Configuration for feature engineering steps.
    Includes information about columns used for specific calculations and transformations.

    This Class defines the entities and Variables for the OneHotEncoding Feature

    @Usage

    ```python
    one_encoding_config = OneHotEncodingConfig(
        entity_a = {User , ["gender","username","age"]},
        entity_b_cols = {Post , ["post_id","title","content"]},
        interaction_cols = {Interaction , ["interaction_type","timestamp"]}

    ```
    """

    entity_a: EntityColumns
    entity_b: EntityColumns
    interaction: EntityColumns


class RelevancyConfig(BaseModel):
    """
    Configuration for feature engineering steps.
    Includes information about columns used for specific calculations and transformations.

    This Class defines the Entities and Variables to Exclude from the Model for Training

    Features - the extra columns to be used in the Model that are derived from Feature Engineering
    @Usage

    ```python
    one_encoding_config = OneHotEncodingConfig(
        entity_a = {User , ["gender","username","age"]},
        entity_b_cols = {Post , ["post_id","title","content"]},
        interaction_cols = {Interaction , ["interaction_type","timestamp"]}

    ```
    """

    entity_a: EntityColumns
    entity_b: EntityColumns
    interaction: EntityColumns
    features: List[str]
    target: str


class DocumentGLMConfig(BaseModel):
    """
    Config Object for the GLM Model

    Provide the List of Entities and the merge_key that Interaction Shares between entities

    Usage:

    ```py
    user_entity = Entity(doc_list=users, merge_key="username")
    post_entity = Entity(doc_list=posts, merge_key="post_id")
    interaction_entity = Entity(
        doc_list=interactions,
        merge_key="post_id",
        default_value="error",
        variance_key="interaction_type"
        )

    ```
    """

    doc_list: List[ESDocument]

    merge_key: Optional[str] = None

    variance_key: Optional[str] = None

    default_value: Optional[str] = "none"


class DataModelMapping(BaseModel):
    """
    Pass the appropriate params to this Object to prepare our Model for GLM Training

    @entities : List of the File Name and Path to be used in the Model for the Entities
    @mapping  : Dict that contains the file name of the Mapping Entity and the Path
    @merge_keys : Dict that contains the keys to be used for merging the Entities

    Usage:
    ```py
    data_model = DataModelMapping(
    entities=[
        Entity(type="users", path="path/to/csv", field="user", merge_key="username"),
        Entity(type="posts", path="path/to/csv", field="post", merge_key="post_id"),
    ],
    mapping=Mapping(index="interactions", path="path/csv", field="inter_field", default="null")
    )
    ```
    """

    entities: List[Entity]
    mapping: Mapping


class DateDifferenceFeature(BaseModel):
    """
    Date Difference Feature
    """

    date_col_1: str  # Name of the first date column
    date_col_2: str  # Name of the second date column
    difference_col: str  # Name of the column where the date difference will be stored


class PresenceFeature(BaseModel):
    """
    Date Difference Feature


    column="interaction_type",
    new_col="viewed",
    condition="view",

    """

    column: str
    new_col: str
    condition: str
