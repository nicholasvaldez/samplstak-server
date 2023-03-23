"""View module for handling requests about genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from samplstakapi.models import Drumkit, Genre, Producer, Sample
import uuid
import base64
from django.core.files.base import ContentFile
import random


class DrumkitView(ViewSet):
    """SamplStak drumkits view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single genre

        Returns:
            Response -- JSON serialized genre
        """

        drumkit = Drumkit.objects.get(pk=pk)
        serializer = DrumkitSerializer(drumkit)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all drumkits

        Returns:
            Response -- JSON serialized list of drumkits
        """
        drumkits = Drumkit.objects.all()
        if 'random' in request.query_params:
            drumkits = drumkits.order_by('?')
        elif 'producer' in request.query_params:
            producer = Producer.objects.get(user=request.auth.user)
            drumkits = drumkits.filter(producer=producer)

        serializer = DrumkitSerializer(drumkits, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to drumkits"""

        producer = Producer.objects.get(user=request.auth.user)
        genre = Genre.objects.get(pk=request.data['genre'])

        format, imgstr = request.data["image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr),
                           name=f'producer-{uuid.uuid4()}.{ext}')
        drumkit = Drumkit.objects.create(
            name=request.data['name'],
            producer=producer,
            genre=genre,
            image=data
        )

        serializer = DrumkitSerializer(drumkit)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        fields = ('id', 'bio', 'image', 'full_name')


class DrumkitSerializer(serializers.ModelSerializer):
    """JSON serializer for drumkits
    """
    image = serializers.ImageField(max_length=None, use_url=True)
    genre = GenreSerializer(many=False)
    producer = ProducerSerializer(many=False)

    class Meta:
        model = Drumkit
        fields = ('id', 'name', 'producer', 'image', 'genre')
