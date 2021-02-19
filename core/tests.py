from datetime import datetime,timedelta
from rest_framework.test import APIClient, APITestCase

from .models import Event


# Create your tests here.
class EventTest(APITestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        self.sample_bodies = [{
              "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
              "category": "page interaction",
              "name": "pageview",
              "data": {
                "host": "www.consumeraffairs.com",
                "path": "/",
              },
              "timestamp": "2021-01-01 09:15:27.243860"
            },
        {
            "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
            "category": "page interaction",
            "name": "cta click",
            "data": {
                "host": "www.consumeraffairs.com",
                "path": "/",
                "element": "chat bubble"
            },
            "timestamp": "2021-01-01 09:15:27.243860"
        },
        {
            "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
            "category": "form interaction",
            "name": "submit",
            "data": {
                "host": "www.consumeraffairs.com",
                "path": "/",
                "form": {
                    "first_name": "John",
                    "last_name": "Doe"
                }
            },
            "timestamp": "2021-01-01 09:15:27.243860"
        }]

    def test_post_sample_data(self):
        for sample in self.sample_bodies:
            response = self.client.post('/theeye/events/', sample, format='json')
            self.assertEqual(response.status_code, 201)

    def test_list_endpoint(self):
        response = self.client.get('/theeye/events/')
        self.assertEqual(response.status_code, 200)


class EventListTest(APITestCase):

    @classmethod
    def setUpTestData(cls):

        sample_bodies = [{
              "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
              "category": "page interaction",
              "name": "pageview",
              "data": {
                "host": "www.consumeraffairs.com",
                "path": "/",
              },
              "timestamp": "2021-01-01 09:15:27.243860"
            },
        {
            "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
            "category": "page interaction",
            "name": "cta click",
            "data": {
                "host": "www.consumeraffairs.com",
                "path": "/",
                "element": "chat bubble"
            },
            "timestamp": "2021-01-01 09:15:27.243860"
        },
        {
            "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
            "category": "form interaction",
            "name": "submit",
            "data": {
                "host": "www.consumeraffairs.com",
                "path": "/",
                "form": {
                    "first_name": "John",
                    "last_name": "Doe"
                }
            },
            "timestamp": "2021-01-01 09:15:27.243860"
        }]

        for content in sample_bodies:
            Event.objects.create(**content)

    def test_inserted_data(self):
        response = self.client.get('/theeye/events/')
        self.assertEqual(len(response.data), 3)

