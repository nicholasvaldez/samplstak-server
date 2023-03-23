import json
from rest_framework import status
from rest_framework.test import APITestCase
from samplstakapi.models import Instrument, Producer
from rest_framework.authtoken.models import Token


class InstrumentTests(APITestCase):

    fixtures = ['users', 'tokens', 'producers', 'instruments']

    def setUp(self):
        self.producer = Producer.objects.first()
        token = Token.objects.get(user=self.producer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_single_instrument(self):
        """
        Ensure we can get a single instrument
        """
        instrument = Instrument()
        instrument.label = "Kick"
        instrument.save()

        response = self.client.get(f"/instruments/{instrument.id}")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["label"], "Kick")
