"""View module for handling requests about samples"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from samplstakapi.models import Sample, Instrument, Genre, Producer


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
        producer_id = Producer.objects.get(user=request.auth.user)
        samples = Sample.objects.all()
        if 'genre' in request.query_params:
            if request.query_params['genre'] == "1":
                samples = samples.filter(genre=1)
            elif request.query_params['genre'] == "2":
                samples = samples.filter(genre=2)
            elif request.query_params['genre'] == "3":
                samples = samples.filter(genre=3)
            elif request.query_params['genre'] == "4":
                samples = samples.filter(genre=4)
            elif request.query_params['genre'] == "5":
                samples = samples.filter(genre=5)
        elif 'producer' in request.query_params:
            samples = samples.filter(producer=producer_id)
        else:
            samples = Sample.objects.all()

        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InstrumentSerializer(serializers.ModelSerializer):
    """ JSON serializer for instruments
    """
    class Meta:
        model = Instrument
        fields = ('id', 'label')


class GenreSerializer(serializers.ModelSerializer):
    """ JSON serializer for genres
    """
    class Meta:
        model = Genre
        fields = ('id', 'label')


class SampleSerializer(serializers.ModelSerializer):
    """JSON serializer for samples
    """
    instrument = InstrumentSerializer(many=False)
    genre = GenreSerializer(many=True)

    class Meta:
        model = Sample
        fields = ('id', 'file_url', 'file_name',
                  'instrument', 'genre', 'producer')
