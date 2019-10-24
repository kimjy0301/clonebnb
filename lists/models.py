from django.db import models
from core import models as core_models
from users import models as user_models
from rooms import models as room_models

# Create your models here.


class List(core_models.AbstractTimeStampModel):
    """ 리스트 모델 정의 """

    name = models.CharField(max_length=80)
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    rooms = models.ManyToManyField(room_models.Room, blank=True)

    def __str__(self):
        return self.name
