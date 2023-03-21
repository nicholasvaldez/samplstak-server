from django.db import models
from .instrument import Instrument
from .genre import Genre
from .producer import Producer


class Drumkit(models.Model):

    name = models.CharField(max_length=100)
    producer = models.ForeignKey(
        Producer, on_delete=models.CASCADE, related_name="drumkit_producer")
    image = models.ImageField(upload_to='img')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              related_name="genre_of_drumkit")
