from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Type
from model.interface import ESDocument
from pydantic import BaseModel, validator
from regex import E
import pandas as pd


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


class Feature(BaseModel):
    """
    @Feature
    Base Class for Features to be used in the Model
    """

    @abstractmethod
    def feature_type(self):
        """
        Returns the Feature Type
        """

    @abstractmethod
    def apply(self, *args, **kwargs) -> pd.DataFrame:
        """
        Apply the Feature to the DataFrame


        """


class DateDifferenceFeatureConfig(Feature):
    """
    @FeatureEngineering
    @DateDifferenceFeature

    @Params
    ```py
    start_entity : Entity to be used as the Start Date
    start_time_col : Column to be used as the Start Date
    end_entity : Entity to be used as the End Date
    end_time_col : Column to be used as the End Date
    new_col : Column to be used to store the Date Difference
    ```
    @Usage
    ```python
    # Add a Field "post_age" to the DataFrame
    # It is the difference (In Days) between end_entity and start_entity
    # If posts.timestamp is 4 days ago and interactions.timestamp is 2 days ago
    # Then post_age = 2

    date_feature_config = DateDifferenceFeatureConfig(
        start_entity=Post,
        end_entity=Interaction,
        start_time_col="timestamp",
        end_time_col="timestamp",
        new_col="post_age",
    )
    ```
    """

    start_entity: Type[ESDocument] | str
    start_time_col: str
    end_entity: Type[ESDocument] | str
    end_time_col: str
    new_col: str

    def feature_type(self):
        return "date_difference"

    def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply the Feature to the DataFrame and return the Modified DataFrame

        """
        from features.feature_engineering import apply_date_difference_feature

        return apply_date_difference_feature(data, self)


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


class EntityData(BaseModel):
    """
    Config for specifying Columns to be used
    """

    entity: Type[ESDocument]
    data: List[ESDocument]


class RetainColumnsConfig(BaseModel):
    """
    Config for specifying Columns to be Retained for Analysis Post-Scoring
    """

    entity_a_retain: EntityColumns
    entity_b_retain: EntityColumns


class EntityConfig(BaseModel):
    """
    Config for specifying Columns to be used
    @Params
    entity             : Entity to be used in the Model
    primary_key        : Primary Key for the Entity
    categorical_fields : Categorical Fields to be used in the Model
    training_fields    : Training Fields to be used in the Model
    data               : Data to be used in the Model
    display_fields     : Fields to be displayed in the Model once Scored or Trained

    """

    entity: Type[ESDocument]
    primary_key: str
    categorical_fields: List[str]
    training_fields: List[str]
    data: List[ESDocument]
    display_fields: Optional[List[str]] = None


class EntityScoringConfig(BaseModel):
    """
    Config for specifying Columns to be used
    """

    entity: Type[ESDocument]
    primary_key: str
    display_fields: Optional[List[str]] = None


class MappingConfig(BaseModel):
    """
    Config for specifying Columns to be used
    """

    entity: Type[ESDocument]
    primary_key: str = None
    default_value: str
    variance_key: str
    categorical_fields: List[str] = None
    training_fields: List[str] = None

    data: List[ESDocument]


class MapScoringToOriginalData(BaseModel):
    """
    Config for Mapping Generated Scores back to Original DataSet
    """

    entity_a: EntityScoringConfig
    entity_b: EntityScoringConfig

    score_field: str


class ScoringConfig(BaseModel):
    """
    Config to Map the Scoring Data to the Training Data

    We might have User and Post with categorical variables such as post_language, user_gender , username , post_id - etc.

    When we One-Encode our data we drop all other columns and retain only the numeric columns.

    Once we have the Model - we use this to maintain the mapping between our Transformations and Original Data
    """

    entity_a: EntityConfig
    entity_b: EntityConfig
    mapping: MappingConfig

    features: Optional[List[Feature]] = None

    target_variable: str

    target_config: InteractionTypeConfig

    feature_fields: List[str]

    score_field: Optional[str] = "score"


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

    entity_a: Optional[EntityColumns] = None
    entity_b: Optional[EntityColumns] = None
    interaction: Optional[EntityColumns] = None
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


class EntityMergeConfig(BaseModel):
    """
    Config to Merge Entities for Data Preparation , Training , and Scoring
    """

    entity_a: DocumentGLMConfig
    entity_b: DocumentGLMConfig
    mapping: DocumentGLMConfig


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

    start_entity: Type[ESDocument] | str
    start_time_col: str
    end_entity: Type[ESDocument] | str
    end_time_col: str
    new_col: str


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
