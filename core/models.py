from django.db import models
from . import managers

# Create your models here.


class AbstractTimeStampModel(models.Model):

    """TimeStamp Model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomManager()

    class Meta:
        abstract = True

