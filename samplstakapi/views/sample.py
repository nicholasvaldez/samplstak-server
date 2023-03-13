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
        sample = Sample.objects.get(pk=pk)
        serializer = SampleSerializer(sample)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all samples

        Returns:
            Response -- JSON serialized list of samples
        """
        samples = []
        samples = Sample.objects.all()
        if 'genre' in request.query_params:
            if request.query_params['genre'] == "pop":
                samples = samples.filter(genre=1)
            elif request.query_params['genre'] == "hiphop":
                samples = samples.filter(genre=2)
            elif request.query_params['genre'] == "rnb":
                samples = samples.filter(genre=3)
            elif request.query_params['genre'] == "lofi":
                samples = samples.filter(genre=4)
            elif request.query_params['genre'] == "edm":
                samples = samples.filter(genre=5)
        else:
            samples = Sample.objects.all()

        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SampleSerializer(serializers.ModelSerializer):
    """JSON serializer for samples
    """
    class Meta:
        model = Sample
        fields = ('id', 'file_url', 'file_name',
                  'instrument', 'genre', 'producer')
