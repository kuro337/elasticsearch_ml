"""
Sample Document Models to Test GLM Model Training
@User
"""
from typing import List
from model.models import User, ESDocument


user_document1 = User(
    username="Lizabeth Martin",
    first_name="Lizabeth",
    last_name="Martin",
    email="lizabeth.minam@aol.com",
    gender="Female",
    country="Canada",
    age=25,
    timestamp="2023-10-09T12:34:56",
)


user_document2 = User(
    username="Polina Milvus",
    first_name="Polina",
    last_name="Milvus",
    email="polina.minam@gmail.com",
    gender="Male",
    country="Canada",
    age=25,
    timestamp="2023-11-09T12:34:56",
)

user_document3 = User(
    username="Joaquin Vertex",
    first_name="Joaquin",
    last_name="Vertex",
    email="petriol.minam@gmail.com",
    gender="Male",
    country="USA",
    age=22,
    timestamp="2023-10-09T12:34:56",
)

user_document4 = User(
    username="James Martin",
    first_name="James",
    last_name="Memes",
    email="petriol.minam@aol.com",
    gender="Male",
    country="Canada",
    age=22,
    timestamp="2023-10-22T12:34:56",
)

user_document5 = User(
    username="Perone Marone",
    first_name="Perone",
    last_name="Marone",
    email="perone.marone@aol.com",
    gender="Female",
    country="USA",
    age=19,
    timestamp="2023-10-28T12:34:56",
)

user_document6 = User(
    username="Xavier Hajiah",
    first_name="Xavier",
    last_name="Hajiah",
    email="Xavier999.marone@aol.com",
    gender="Male",
    country="Canada",
    age=24,
    timestamp="2023-10-28T12:34:56",
)

user_document7 = User(
    username="Ajay Mirush",
    first_name="Ajay",
    last_name="Mirush",
    email="ajay.marone@gmail.com",
    gender="Female",
    country="USA",
    age=21,
    timestamp="2023-10-28T12:34:56",
)

user_document8 = User(
    username="Miyushi Farahson",
    first_name="Perone",
    last_name="Marone",
    email="perone.marone@ainlp.com",
    gender="Female",
    country="USA",
    age=22,
    timestamp="2023-10-28T12:34:56",
)

users: List[ESDocument] = [
    user_document1,
    user_document2,
    user_document3,
    user_document4,
    user_document5,
]
