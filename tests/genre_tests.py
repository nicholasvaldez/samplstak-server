import json
from rest_framework import status
from rest_framework.test import APITestCase
from samplstakapi.models import Genre, Producer
from rest_framework.authtoken.models import Token


class GenreTests(APITestCase):

    fixtures = ['users', 'tokens', 'producers', 'genres']

    def setUp(self):
        self.producer = Producer.objects.first()
        token = Token.objects.get(user=self.producer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_genres(self):
        """
        Ensure we can get a single genre
        """
        genre = Genre()
        genre.label = "Hip-Hop"
        genre.save()

        response = self.client.get(f"/genres/{genre.id}")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["label"], "Hip-Hop")
