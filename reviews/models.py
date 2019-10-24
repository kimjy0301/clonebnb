from django.db import models
from core import models as core_models
from users import models as user_models
from rooms import models as room_models

# Create your models here.


class Review(core_models.AbstractTimeStampModel):
    """Review Model Definition"""

    review = models.TextField()
    accuracy = models.IntegerField()
    location = models.IntegerField()
    communication = models.IntegerField()
    check_in = models.IntegerField()
    cleanliness = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    room = models.ForeignKey(room_models.Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.review} - {self.room}"
