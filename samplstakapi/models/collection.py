from django.db import models
from django.contrib.auth.models import User
from .sample import Sample
from .producer import Producer


class Collection(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    sample = models.ForeignKey(
        Sample, on_delete=models.PROTECT, related_name="saved_samples")
