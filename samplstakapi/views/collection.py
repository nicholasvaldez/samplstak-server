"""View module for handling requests about users sample collection"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from samplstakapi.models import Collection, Sample, Producer, Genre, Drumkit, Instrument
from django.contrib.auth.models import User


class CollectionView(ViewSet):
    """SamplStak collection view"""

    def destroy(self, request, pk):
        sample = Collection.objects.get(pk=pk)
        sample.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

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
        samples = []
        samples = Collection.objects.all()
        if 'genre' in request.query_params:
            genre_id = int(request.query_params['genre'])
            samples = [
                s for s in samples if genre_id in s.sample.genre.values_list('id', flat=True)]
        elif 'instrument' in request.query_params:
            instrument_id = int(request.query_params['instrument'])
            samples = samples.filter(sample__instrument__id=instrument_id)
        elif 'producer' in request.query_params:
            producer = Producer.objects.get(user=request.auth.user)
            samples = samples.filter(producer=producer)

        else:
            # producer = Producer.objects.get(user=request.user)
            samples = Collection.objects.all()

        serializer = CollectionSerializer(samples, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests

        Returns
            Response -- JSON serialized collection sample instance
        """
        sample = Sample.objects.get(pk=request.data['sample'])
        producer = Producer.objects.get(user=request.auth.user)

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


class InstrumentSerializer(serializers.ModelSerializer):
    """ JSON serializer for instruments
    """
    class Meta:
        model = Instrument
        fields = ('id', 'label')


class ProducerSerializer(serializers.ModelSerializer):
    """ JSON serializer for producers
    """
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Producer
        fields = ('id', 'bio', 'image')


class DrumkitSerializer(serializers.ModelSerializer):
    """ JSON serializer for producers
    """
    image = serializers.ImageField(max_length=None, use_url=True)
    producer = ProducerSerializer(many=False)

    class Meta:
        model = Drumkit
        fields = ('id', 'name', 'producer', 'image', 'genre')


class SampleSerializer(serializers.ModelSerializer):
    """ JSON serializer for genres
    """
    genre = GenreSerializer(many=True)
    producer = ProducerSerializer(many=False)
    drumkit = DrumkitSerializer(many=False)
    instrument = InstrumentSerializer(many=False)

    class Meta:
        model = Sample
        fields = ('id', 'file_url', 'file_name',
                  'instrument', 'genre', 'producer', 'drumkit')


class CollectionSerializer(serializers.ModelSerializer):
    """JSON serializer for sample collection
    """

    sample = SampleSerializer()

    class Meta:
        model = Collection
        fields = ('id', 'producer', 'sample')
