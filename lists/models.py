from django.db import models
from core import models as core_models
from users import models as user_models
from rooms import models as room_models

# Create your models here.


class List(core_models.AbstractTimeStampModel):
    """ 리스트 모델 정의 """

    name = models.CharField(max_length=80)
    user = models.OneToOneField(
        user_models.User, related_name="list", on_delete=models.CASCADE
    )
    rooms = models.ManyToManyField(room_models.Room, related_name="lists", blank=True)

    def __str__(self):
        return self.name

    def count_rooms(self):
        return self.rooms.count()

    count_rooms.short_description = "number of rooms"
