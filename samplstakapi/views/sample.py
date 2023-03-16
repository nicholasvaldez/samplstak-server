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

        sample = Sample.objects.create(
            file_url=request.data["file_url"],
            file_name=request.data["file_name"],
            instrument=instrument,
            producer=producer
        )
        sample.genre.set(genres)
        serializer = SampleSerializer(sample)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a sample

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            sample = Sample.objects.get(pk=pk)
        except Sample.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        sample.file_url = request.data["file_url"]
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


class SampleSerializer(serializers.ModelSerializer):
    """JSON serializer for samples
    """
    instrument = InstrumentSerializer(many=False)
    genre = GenreSerializer(many=True)

    class Meta:
        model = Sample
        fields = ('id', 'file_url', 'file_name',
                  'instrument', 'genre', 'producer')
