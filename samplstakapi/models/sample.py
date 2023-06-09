from django.db import models
from .instrument import Instrument
from .genre import Genre
from .producer import Producer
from .drumkit import Drumkit


class Sample(models.Model):

    file_url = models.FileField(
        upload_to='wav', default='wav/none/no-wav.wav')
    file_name = models.CharField(max_length=100)
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
    genre = models.ManyToManyField(Genre, related_name="genre_samples")
    producer = models.ForeignKey(
        Producer, on_delete=models.CASCADE, related_name="producer_samples")
    drumkit = models.ForeignKey(Drumkit, on_delete=models.PROTECT, null=True)
