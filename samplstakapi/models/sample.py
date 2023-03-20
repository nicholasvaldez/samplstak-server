from django.db import models
from .instrument import Instrument
from .genre import Genre
from .producer import Producer


class Sample(models.Model):

    file_url = models.FileField(
        upload_to='wav', default='wav/none/no-wav.wav')
    file_name = models.CharField(max_length=100)
    instrument = models.ForeignKey(Instrument, on_delete=models.DO_NOTHING)
    genre = models.ManyToManyField(Genre, related_name="genre_samples")
    producer = models.ForeignKey(
        Producer, on_delete=models.CASCADE, related_name="producer_samples")
