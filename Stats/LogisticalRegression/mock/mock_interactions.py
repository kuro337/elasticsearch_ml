"""
Sample Document Models to Test GLM Model Training
"""
from typing import List
from model.models import Interaction, ESDocument


interaction_document1 = Interaction(
    interaction_type="view",
    post_id="Abstract Classes",
    timestamp="2023-11-11T12:34:56",
    username="Joaquin Vertex",
)

interaction_document2 = Interaction(
    interaction_type="view",
    post_id="Abstract Classes",
    timestamp="2023-11-11T12:34:56",
    username="Lizabeth Martin",
)

interaction_document3 = Interaction(
    interaction_type="view",
    post_id="Pydantic Type System",
    timestamp="2023-11-11T12:34:56",
    username="Lizabeth Martin",
)

interaction_document4 = Interaction(
    interaction_type="view",
    post_id="Pydantic Type System",
    timestamp="2023-11-11T12:34:56",
    username="Perone Marone",
)

interaction_document5 = Interaction(
    interaction_type="view",
    post_id="Pydantic Type System",
    timestamp="2023-11-11T12:34:56",
    username="Perone Marone",
)
interaction_document6 = Interaction(
    interaction_type="like",
    post_id="JVM Heap Allocation",
    timestamp="2023-11-11T12:34:22",
    username="James Martin",
)

interaction_document7 = Interaction(
    interaction_type="view",
    post_id="JVM Heap Allocation",
    timestamp="2023-11-11T12:34:56",
    username="Perone Marone",
)

interaction_document8 = Interaction(
    interaction_type="view",
    post_id="JVM Heap Allocation",
    timestamp="2023-11-11T12:34:18",
    username="Perone Marone",
)

interaction_document9 = Interaction(
    interaction_type="view",
    post_id="The Event Loop and v8 Browser Runtime",
    timestamp="2023-11-20T12:34:56",
    username="Ajay Mirush",
)

interaction_document10 = Interaction(
    interaction_type="view",
    post_id="The Event Loop and v8 Browser Runtime",
    timestamp="2023-11-11T12:34:56",
    username="Ajay Mirush",
)

interaction_document11 = Interaction(
    interaction_type="view",
    post_id="The Event Loop and v8 Browser Runtime",
    timestamp="2023-11-11T12:34:56",
    username="Perone Marone",
)

interaction_document12 = Interaction(
    interaction_type="view",
    post_id="Natural Language Processing",
    timestamp="2023-11-11T12:34:56",
    username="Miyushi Farahson",
)

interaction_document13 = Interaction(
    interaction_type="view",
    post_id="Natural Language Processing",
    timestamp="2023-11-11T12:34:56",
    username="Polina Milvus",
)

interaction_document14 = Interaction(
    interaction_type="like",
    post_id="Natural Language Processing",
    timestamp="2023-11-11T12:34:56",
    username="Polina Milvus",
)

interaction_document15 = Interaction(
    interaction_type="like",
    post_id="Natural Language Processing",
    timestamp="2023-11-11T12:34:56",
    username="Polina Milvus",
)

interaction_document16 = Interaction(
    interaction_type="like",
    post_id="Natural Language Processing",
    timestamp="2023-11-11T12:34:56",
    username="Lizabeth Martin",
)

interactions: List[ESDocument] = [
    interaction_document1,
    interaction_document2,
    interaction_document3,
    interaction_document4,
    interaction_document5,
    interaction_document6,
    interaction_document7,
    interaction_document8,
    interaction_document9,
    interaction_document10,
    interaction_document11,
    interaction_document12,
]
