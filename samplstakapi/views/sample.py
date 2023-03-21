"""View module for handling requests about samples"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
import os
from rest_framework import serializers, status
from samplstakapi.models import Sample, Instrument, Genre, Producer
import uuid
import base64
from django.core.files.base import ContentFile
import random


class SampleView(ViewSet):
    """SamplStak samples view"""

    def destroy(self, request, pk):
        sample = Sample.objects.get(pk=pk)
        sample.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk):
        """Handle GET requests for single sample

        Returns:
            Response -- JSON serialized sample
        """
        try:
            sample = Sample.objects.get(pk=pk)
        except Sample.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SampleSerializer(sample)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all samples

        Returns:
            Response -- JSON serialized list of samples
        """
        samples = Sample.objects.all()

        # Filter by genre if "genre" query parameter is present
        if 'genre' in request.query_params:
            genre_id = int(request.query_params['genre'])
            samples = samples.filter(genre=genre_id)

        # Filter by producer if "producer" query parameter is present
        elif 'producer' in request.query_params:
            producer = Producer.objects.get(user=request.auth.user)
            samples = samples.filter(producer=producer)

        # Sort randomly if "random" query parameter is present
        if 'random' in request.query_params:
            samples = samples.order_by('?')

        # Serialize samples and return response
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        producer = Producer.objects.get(user=request.auth.user)
        instrument = Instrument.objects.get(pk=request.data["instrument"])
        genre_ids = request.data.get("genre", [])
        if isinstance(genre_ids, int):  # convert int to list
            genre_ids = [genre_ids]
        genres = Genre.objects.filter(id__in=genre_ids)

        # Create the file path based on the upload_to parameter of the file_url field
        format, audiostr = request.data["file_url"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(
            audiostr), name=f'sample-{uuid.uuid4()}.{ext}')

        # Create the Sample object with the correct file path
        sample = Sample.objects.create(
            file_url=data,
            file_name=request.data["file_name"],
            instrument=instrument,
            producer=producer
        )
        sample.genre.set(genres)

        # Return serialized Sample instance in response
        serializer = SampleSerializer(sample)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a sample

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            sample = Sample.objects.get(pk=pk)
        except Sample.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # sample.file_url = request.data["file_url"]
        sample.file_name = request.data["file_name"]

        instrument_pk = request.data.get("instrument")
        if instrument_pk is not None:
            try:
                instrument = Instrument.objects.get(pk=instrument_pk)
            except Instrument.DoesNotExist:
                return Response({"instrument": ["Invalid pk"]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                sample.instrument = instrument

        genres_pks = request.data.get("genre")
        if genres_pks is not None:
            try:
                genres = Genre.objects.filter(pk__in=genres_pks)
            except Genre.DoesNotExist:
                return Response({"genre": ["Invalid pk"]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                sample.genre.set(genres)

        producer = Producer.objects.get(user=request.auth.user)
        sample.producer = producer
        sample.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


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


class ProducerSerializer(serializers.ModelSerializer):
    """ JSON serializer for producers
    """
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Producer
        fields = ('id', 'bio', 'image')


class SampleSerializer(serializers.ModelSerializer):
    """JSON serializer for samples
    """
    instrument = InstrumentSerializer(many=False)
    genre = GenreSerializer(many=True)
    file_url = serializers.FileField(
        max_length=None, use_url=True)
    producer = ProducerSerializer(many=False)

    class Meta:
        model = Sample
        fields = ('id', 'file_url', 'file_name',
                  'instrument', 'genre', 'producer')
