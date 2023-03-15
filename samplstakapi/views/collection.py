"""View module for handling requests about users sample collection"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from samplstakapi.models import Collection, Sample, Producer, Genre
from django.contrib.auth.models import User


class CollectionView(ViewSet):
    """SamplStak collection view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single sample

        Returns:
            Response -- JSON serialized sample
        """

        sample = Collection.objects.get(pk=pk)
        serializer = CollectionSerializer(sample)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all samples in collection

        Returns:
            Response -- JSON serialized list of samples in collection
        """

        producer = Producer.objects.get(user=request.user)
        samples = Collection.objects.filter(producer=producer)
        serializer = CollectionSerializer(samples, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests

        Returns
            Response -- JSON serialized collection sample instance
        """
        producer = Producer.objects.get(user=request.user)
        sample = Sample.objects.get(pk=request.data["sample"])

        collection = Collection.objects.create(
            producer=producer,
            sample=sample
        )
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)


class GenreSerializer(serializers.ModelSerializer):
    """ JSON serializer for genres
    """
    class Meta:
        model = Genre
        fields = ('id', 'label')


class SampleSerializer(serializers.ModelSerializer):
    """ JSON serializer for genres
    """
    genre = GenreSerializer(many=True)

    class Meta:
        model = Sample
        fields = ('id', 'file_url', 'file_name', 'instrument', 'genre',)


class CollectionSerializer(serializers.ModelSerializer):
    """JSON serializer for sample collection
    """

    sample = SampleSerializer()

    class Meta:
        model = Collection
        fields = ('id', 'producer', 'sample')
