from pydantic import BaseModel, ValidationError, validator
from typing import Optional, List, Dict, Union, Type


class DataRequest(BaseModel):
    type: str
    data: Dict[
        str, Union[str, int]
    ]  # Adjust this type hint based on what `data` can include

    # Validate that the type field is one of the expected values
    @validator("type")
    def check_type(cls, v):
        if v not in ["user", "metadata", "post"]:
            raise ValueError('type must be one of "user", "metadata", "post"')
        return v


class User(BaseModel):
    name: str
    age: int
    email: str


class Metadata(BaseModel):
    key: str
    value: str


class Post(BaseModel):
    title: str
    content: str
