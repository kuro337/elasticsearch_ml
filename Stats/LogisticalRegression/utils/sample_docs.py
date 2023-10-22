"""
Sample Document Models to Test GLM Model Training
"""
from typing import List
from model.models import Interaction, User, Post, ESDocument


user_document1 = User(
    username="Fiero Martin",
    first_name="Maroni",
    last_name="Memes",
    email="petriol.minam@aol.com",
    gender="Male",
    country="Japan",
    age=20,
    timestamp="2023-10-09T12:34:56",
)


user_document2 = User(
    username="Polina Milvus",
    first_name="Polina",
    last_name="Milvus",
    email="polina.minam@gmail.com",
    gender="Male",
    country="Japan",
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
    gender="Female",
    country="USA",
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
    age=16,
    timestamp="2023-10-28T12:34:56",
)

post_document1 = Post(
    lang="java",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Joaquin Vertex",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-09T12:34:56",
    post_id="goat",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)

post_document2 = Post(
    lang="java",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Fiero Martin",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-09T12:34:56",
    post_id="goat",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)

post_document3 = Post(
    lang="java",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Filaman Petriol",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-09T12:34:56",
    post_id="jvmoop",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)

post_document4 = Post(
    lang="java",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Filaman Petriol",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-09T12:34:56",
    post_id="jvmoop",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)

post_document5 = Post(
    lang="java",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Fiero Martin",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-10T12:34:56",
    post_id="goat",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)

post_document6 = Post(
    lang="javascript",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Fiero Martin",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-09T12:34:56",
    post_id="jspost",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)


interaction_document1 = Interaction(
    interaction_type="view",
    post_id="goat",
    timestamp="2023-11-11T12:34:56",
    username="Joaquin Vertex",
)

interaction_document2 = Interaction(
    interaction_type="view",
    post_id="goat",
    timestamp="2023-11-11T12:34:56",
    username="Fiero Martin",
)

interaction_document3 = Interaction(
    interaction_type="like",
    post_id="goat",
    timestamp="2023-11-11T12:34:56",
    username="Fiero Martin",
)

interaction_document4 = Interaction(
    interaction_type="like",
    post_id="jspost",
    timestamp="2023-11-11T12:34:56",
    username="Perone Marone",
)

users: List[ESDocument] = [
    user_document1,
    user_document2,
    user_document3,
    user_document4,
    user_document5,
]

posts: List[ESDocument] = [
    post_document1,
    post_document2,
    post_document3,
    post_document4,
    post_document5,
    post_document6,
]

interactions: List[ESDocument] = [
    interaction_document1,
    interaction_document2,
    interaction_document3,
    interaction_document4,
]
