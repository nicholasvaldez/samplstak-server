"""View module for handling requests about instruments"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from samplstakapi.models import Instrument


class InstrumentView(ViewSet):
    """SamplStak instrument view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single instrument

        Returns:
            Response -- JSON serialized instrument 
        """

        instrument = Instrument.objects.get(pk=pk)
        serializer = InstrumentSerializer(instrument)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all instruments

        Returns:
            Response -- JSON serialized list of instruments
        """
        instruments = Instrument.objects.all()
        serializer = InstrumentSerializer(instruments, many=True)
        return Response(serializer.data)


class InstrumentSerializer(serializers.ModelSerializer):
    """JSON serializer for genres
    """
    class Meta:
        model = Instrument
        fields = ('id', 'label')
