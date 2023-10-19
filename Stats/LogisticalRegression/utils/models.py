from typing import Dict, List
from pydantic import BaseModel


class Entity(BaseModel):
    """
    Represents the Entity to be used in the Model

    Entity(type="users", path="path/to/csv", field="user", merge_key="username")
    """

    index: str
    path: str
    field: str
    merge_key: str


class Mapping(BaseModel):
    """
    Represents the Entity to be used in the Model

    Mapping(index="interactions", path="path/to/csv", field="interaction_type", default="null")
    """

    index: str
    path: str
    field: str
    default: str


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
