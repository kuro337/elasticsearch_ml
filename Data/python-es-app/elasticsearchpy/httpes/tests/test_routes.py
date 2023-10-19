from unittest.mock import patch, Mock
from django.urls import reverse
from django.test import TestCase, Client
from elasticsearch.exceptions import ConnectionError
from pydantic import ValidationError
import json
from httpes.types.error.entity_error import InvalidEntityTypeError
from httpes.models import User


def raise_validation_error(*args, **kwargs):
    raise ValidationError([])  # No need to provide model instance here


class InsertCustomDataViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("httpes:insert-data")  # Use the actual name of your URL here

    def test_insert_invalid_entity(self):
        invalid_data = {
            "type": "notexists",
            "data": {"username": "testuser", "email": "testuser@example.com"},
        }

        with patch("httpes.views.get_entity") as mock_get_entity:
            mock_get_entity.return_value = (
                User  # This represents the User Pydantic model
            )

            # When the User model is instantiated with invalid data, it should raise a ValidationError.
            # We don't need to mock this behavior because it's inherent to the Pydantic model.
            response = self.client.post(
                self.url, json.dumps(invalid_data), content_type="application/json"
            )

            self.assertEqual(response.status_code, 503)
            # Check if the error response contains the expected validation error message
            self.assertTrue("error" in response.json())

    def test_insert_invalid_data(self):
        invalid_data = {
            "type": "user",
            "data": {
                "username": "a",  # Invalid due to short username
                "email": "testuser@example.com",
            },
        }

        with patch("httpes.views.get_entity") as mock_get_entity, patch(
            "httpes.models.User.parse_obj", side_effect=raise_validation_error
        ):
            mock_get_entity.return_value = User

            response = self.client.post(
                self.url, json.dumps(invalid_data), content_type="application/json"
            )

            self.assertEqual(response.status_code, 400)
            self.assertTrue("error" in response.json())

    def test_elasticsearch_connection_error(self):
        valid_data = {
            "type": "user",
            "data": {"username": "testuser", "email": "testuser@example.com"},
        }

        with patch(
            "httpes.services.elasticsearch_service.ElasticsearchService.insert_data"
        ) as mock_insert_data:
            # Simulate raising a ConnectionError
            mock_insert_data.side_effect = ConnectionError("Mock Connection Error")

            response = self.client.post(
                self.url, json.dumps(valid_data), content_type="application/json"
            )

            self.assertEqual(response.status_code, 503)
            self.assertEqual(
                response.json(),
                {
                    "error": "Unable to connect to Elasticsearch. Please try again later."
                },
            )


# You should add more tests for valid cases and other edge cases.
