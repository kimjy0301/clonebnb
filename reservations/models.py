from django.db import models

from django.utils import timezone
import datetime

from . import managers
from core import models as core_models
from users import models as user_models
from rooms import models as room_models

# Create your models here.


class Reservation(core_models.AbstractTimeStampModel):
    """ 예약 모델 정의 """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceld"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        user_models.User, related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        room_models.Room, related_name="reservations", on_delete=models.CASCADE
    )
    objects = managers.CustomReservationManager()

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    # in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        is_finished = now > self.check_out
        if is_finished:
            BookedDay.objects.filter(reservation=self).delete()
        return is_finished

    # is_finished.boolean = True

    def save(self, *args, **kwargs):
        # PK가 없다는건 새로 저장되는 예약임.
        if self.pk is None:
            start = self.check_in
            end = self.check_out
            difference = end - start
            existing_booked_day = BookedDay.objects.filter(
                day__range=(start, end), reservation__room=self.room
            ).exists()
            if not existing_booked_day:
                super().save(*args, **kwargs)
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
                return
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.room.name


class BookedDay(core_models.AbstractTimeStampModel):

    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"
