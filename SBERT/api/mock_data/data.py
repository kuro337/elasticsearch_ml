"""
Application entry point for Interacting with Elasticsearch

Even if Index Schema is defined with Embedding - 
we can still insert Documents without providing the Embedding

Insert 10 Posts
Insert 1 User 

Which Posts to show to user?

User-Post Scores Exist in Index 
"""
from typing import List

from model.interface import ESDocument
from model.models import User, Post, Interaction, UserPostScore


# @ESDoc Instances
user_1 = User(
    username="Fiero Martin",
    first_name="Maroni",
    last_name="Memes",
    email="petriol.minam@aol.com",
    gender="Fmeale",
    country="Italy",
    age=24,
    timestamp="2023-10-09T12:34:56",
)

user_2 = User(
    username="Pierre Osborne",
    first_name="Maroni",
    last_name="Memes",
    email="petriol.minam@aol.com",
    gender="Male",
    country="Japan",
    age=20,
    timestamp="2023-10-09T12:34:56",
)

user_3 = User(
    username="Menoscha Zaxiar",
    first_name="Menoscha",
    last_name="Zaxiar",
    email="Menoscha.Zaxiar@aol.com",
    gender="Female",
    country="USA",
    age=23,
    timestamp="2023-10-09T12:34:56",
)


post_1 = Post(
    lang="python",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Filaman Petriol",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-09T12:34:56",
    post_id="pyspark",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)

post_2 = Post(
    lang="python",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Filaman Petriol",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-09T12:34:56",
    post_id="pythonml",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)

post_3 = Post(
    lang="java",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Unknown User",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-09T12:34:56",
    post_id="jvmoop",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)

post_4 = Post(
    lang="python",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Unknown User",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-09T12:34:56",
    post_id="dask",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)

post_5 = Post(
    lang="python",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Unknown User",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-09T12:34:56",
    post_id="async_python",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)

post_6 = Post(
    lang="java",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Unknown User",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-09T12:34:56",
    post_id="virtual_threads",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)

interaction_1 = Interaction(
    interaction_type="view",
    post_id="pyspark",
    timestamp="2023-11-11T12:34:56",
    username="Petriol Petriol",
)

user_scores = [
    UserPostScore(
        username="Fiero Martin",
        post_id="async_python",
        score=0.6,
        timestamp="2023-11-11T12:34:56",
    ),
    UserPostScore(
        username="Fiero Martin",
        post_id="pythonml",
        score=0.6,
        timestamp="2023-11-11T12:34:56",
    ),
    UserPostScore(
        username="Fiero Martin",
        post_id="virtual_threads",
        score=0.7,
        timestamp="2023-11-11T12:34:56",
    ),
    UserPostScore(
        username="Fiero Martin",
        post_id="dask",
        score=0.44,
        timestamp="2023-11-11T12:34:56",
    ),
    UserPostScore(
        username="Fiero Martin",
        post_id="pyspark",
        score=0.4,
        timestamp="2023-11-11T12:34:56",
    ),
    UserPostScore(
        username="Pierre Osborne",
        post_id="pyspark",
        score=0.8,
        timestamp="2023-11-11T12:34:56",
    ),
    UserPostScore(
        username="Menoscha Zaxiar",
        post_id="pyspark",
        score=0.8,
        timestamp="2023-11-11T12:34:56",
    ),
    UserPostScore(
        username="Menoscha Zaxiar",
        post_id="pyspark",
        score=0.8,
        timestamp="2023-11-11T12:34:56",
    ),
]

similar_user = User(
    username="Menoscha Zaviar",
    first_name="Menoscha",
    last_name="Zaviar",
    email="Menoscha.Zaxiar@aol.com",
    gender="Female",
    country="USA",
    age=23,
    timestamp="2023-10-09T12:34:56",
)

similar_post = Post(
    lang="java",
    title="Very Great Posts",
    short_title="This is some random posts!",
    description="Read this post to read words that are written by me.",
    author="Null User",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-09T12:34:56",
    post_id="virtual_th",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="pppp_post",
)

users = [user_1, user_2, user_3]
posts = [post_1, post_2, post_3, post_4, post_5, post_6]

documents: List[ESDocument] = [*users, *posts, *user_scores]
