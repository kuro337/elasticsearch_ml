"""
Sample Document Models to Test GLM Model Training
@Post
"""
from typing import List
from model.models import Post, ESDocument


post_document1 = Post(
    lang="java",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Joaquin Vertex",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-09T12:34:56",
    post_id="JVM Heap Allocation",
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
    post_id="Virtual Threads",
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
    post_id="Abstract Classes",
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
    post_id="Object Oriented Programming",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)

post_document5 = Post(
    lang="python",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Fiero Martin",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-10T12:34:56",
    post_id="Pydantic Type System",
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
    post_id="The Event Loop and v8 Browser Runtime",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)

post_document7 = Post(
    lang="javascript",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Fiero Martin",
    tags="java, oop, elasticsearch",
    timestamp="2023-10-09T12:34:56",
    post_id="The Event Loop and v8 Browser Runtime",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)

post_document8 = Post(
    lang="python",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Fiero Martin",
    tags="python, ml, nlp, regression",
    timestamp="2023-10-09T12:34:56",
    post_id="General Linear Model - Logistic Regression",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)
post_document9 = Post(
    lang="python",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Fiero Martin",
    tags="python, ml, nlp, ai",
    timestamp="2023-10-09T12:34:56",
    post_id="HuggingFace Open Source AI/ML",
    component="post100",
    dynamic_path="/path/to/post1--",
    render_func="zppp_post",
)

post_document10 = Post(
    lang="python",
    title="Very Great Post",
    short_title="This is some random post!",
    description="Read this post to read words that are written by me.",
    author="Fiero Martin",
    tags="python, ml, nlp",
    timestamp="2023-10-09T12:34:56",
    post_id="Natural Language Processing",
    component="post100",
    dynamic_path="/path/to/post1",
    render_func="zppp_post",
)

posts: List[ESDocument] = [
    post_document1,
    post_document2,
    post_document3,
    post_document4,
    post_document5,
    post_document6,
    post_document7,
    post_document8,
    post_document9,
    post_document10,
]
