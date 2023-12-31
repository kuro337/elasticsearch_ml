"""
Test Suite for ElasticSearch API Service

python -m unittest test_elasticsearch.py

"""

import unittest
from model.models import User, Post, Interaction


class TestESDocument(unittest.TestCase):
    """
    @test -> ElasticSearch API Test Suite
    """

    def test_user_document(self):
        """
        @ ESDocument.User Tests
        """
        user_document = User(
            username="Filaman Petriol",
            first_name="Filaman",
            last_name="Petriol",
            email="petriol.minam@aol.com",
            gender="Male",
            country="Japan",
            age=20,
            timestamp="2023-10-09T12:34:56",
        )

        self.assertEqual(user_document.get_index_name(), "users")
        self.assertIsInstance(user_document.hash(), str)
        self.assertIsInstance(user_document.stringify(), str)

        print(f"Mapping for Interaction document: {user_document.get_mapping()}")
        print(user_document.model_dump_json(exclude_unset=True, indent=4))

        print(f"\nUser Doc Dump -> Embedding Unset\n: {user_document.model_dump()}")
        print(f"\nUser Doc Dump -> Embedding Unset\n: {user_document.dump_document()}")
        print(
            f"\nUser json Dump -> Embedding Unset\n: {user_document.model_dump_json()}"
        )
        print(
            f"\nUser json Dump -> Embedding Unset\n: {user_document.model_dump_json(exclude_unset=True)}"
        )
        print(f"\nUser json Dump -> Embedding Unset\n: {user_document.json_schema()}")

        print(
            f"\nUser Doc Dump -> Embedding Unset\n: {user_document.model_dump(exclude_unset=True)}"
        )

        user_document.embedding = [1, 2, 3, 4, 5]

        print(f"User Doc Dump -> Embedding Set\n: {user_document.model_dump()}")

        print(
            f"User Doc Dump -> Embedding Set\n: {user_document.model_dump(exclude_unset=True)}"
        )

    def test_post_document(self):
        """
        @ ESDocument.Post Tests
        """
        post_document = Post(
            lang="java",
            title="Great Post",
            short_title="This is some random post.",
            description="Read this post to read words that are written by me.",
            author="Filaman Petriol",
            tags="java, oop, elasticsearch",
            timestamp="2023-10-09T12:34:56",
            post_id="jvmheap",
            component="post",
            dynamic_path="/path/to/post",
            render_func="render_post",
        )

        self.assertEqual(post_document.get_index_name(), "posts")
        self.assertIsInstance(post_document.hash(), str)
        self.assertIsInstance(post_document.stringify(), str)

        print(f"Hashed Interation:\n{post_document.hash()}")
        print(f"Mapping for Interaction document: {post_document.get_mapping()}")
        print(post_document.model_dump_json(exclude_unset=True, indent=4))
        post_document.embedding = [1, 2, 3, 4, 5]
        print(post_document.model_dump())
        print(post_document.model_dump_json())

    def test_interaction_document(self):
        """
        @ ESDocument.Interaction Tests
        """

        interaction_document = Interaction(
            interaction_type="like",
            post_id="jvmheap",
            timestamp="2023-10-11T12:34:56",
            username="Filaman Petriol",
        )

        expected_mapping = {
            "properties": {
                "interaction_type": {"type": "text"},
                "post_id": {"type": "text"},
                "timestamp": {"type": "date"},
                "username": {"type": "text"},
            }
        }

        self.assertEqual(interaction_document.get_mapping(), expected_mapping)
        self.assertEqual(interaction_document.get_index_name(), "interactions")
        self.assertIsInstance(interaction_document.hash(), str)
        self.assertIsInstance(interaction_document.stringify(), str)

        print(f"Hashed Interation:\n{interaction_document.hash()}")
        interaction_document.embedding = [1, 2, 3, 4, 5]
        print(f"Mapping for Interaction document: {interaction_document.get_mapping()}")
        print(interaction_document.model_dump())
        print(interaction_document.model_dump_json(exclude_unset=True, indent=4))


if __name__ == "__main__":
    unittest.main()
