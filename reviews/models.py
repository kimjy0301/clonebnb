from django.db import models
from core import models as core_models
from users import models as user_models
from rooms import models as room_models

from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Review(core_models.AbstractTimeStampModel):
    """Review Model Definition"""

    review = models.TextField()
    accuracy = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    location = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    communication = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    check_in = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    cleanliness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(
        user_models.User, related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        room_models.Room, related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} - {self.room}"

    def rating_average(self):
        avg = (
            self.accuracy
            + self.location
            + self.communication
            + self.check_in
            + self.cleanliness
            + self.value
        ) / 6
        return round(avg, 2)

    __str__.short_description = "리뷰"
    rating_average.short_description = "평점"

    class Meta:
        ordering = ("-created",)

