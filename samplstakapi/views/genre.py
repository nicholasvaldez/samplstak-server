"""View module for handling requests about genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from samplstakapi.models import Genre


class GenreView(ViewSet):
    """SamplStak genres view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single genre

        Returns:
            Response -- JSON serialized genre
        """

        genre = Genre.objects.get(pk=pk)
        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all genres

        Returns:
            Response -- JSON serialized list of genres
        """
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)


class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for genres
    """
    class Meta:
        model = Genre
        fields = ('id', 'label')
