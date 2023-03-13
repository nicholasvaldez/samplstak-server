"""View module for handling requests about samples"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from samplstakapi.models import Sample


class SampleView(ViewSet):
    """SamplStak samples view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single sample

        Returns:
            Response -- JSON serialized sample
        """

    def list(self, request):
        """Handle GET requests to get all samples

        Returns:
            Response -- JSON serialized list of samples
        """


class SampleSerializer(serializers.ModelSerializer):
    """JSON serializer for samples
    """
    class Meta:
        model = Sample
        fields = ('id', 'file_url', 'file_name',
                  'instrument', 'genre', 'producer')
