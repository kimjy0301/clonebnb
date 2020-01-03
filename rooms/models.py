from django.db import models
from django.urls import reverse

from django_countries.fields import CountryField

from core import models as core_models
from users import models as user_models

# Create your models here.


class AbstractItem(core_models.AbstractTimeStampModel):
    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    """방 타입"""

    class Meta:
        verbose_name = "Room Type"
        ordering = ["name"]


class Amenity(AbstractItem):
    """어메니티"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """시설"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """방 규칙"""

    class Meta:
        verbose_name = "House Rule"


class Room(core_models.AbstractTimeStampModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField(help_text="묵을 게스트 수")
    beds = models.IntegerField(help_text="침대 갯수")
    bedrooms = models.IntegerField(help_text="침실 갯수")
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        user_models.User, related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        RoomType, related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    room_rules = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()

        if all_reviews.count() > 0:
            return round(all_ratings / all_reviews.count(), 2)
        else:
            return 0

    def first_photo(self):

        # photo1,photo2,photo3, = self.photos.all()[:3] 이런식으로 해주면 array 언패킹해서 데이터 할당됨. 파이썬의 기능

        photos = self.photos.all()

        if photos.count() > 0:
            photo, = photos[:1]
            return photo.file.url
        else:
            photo = "/static/img/noimage.svg"
            return photo

    def get_next_four_photos(self):
        photos = self.photos.all()
        if photos.count() > 0:
            photos = photos[1:5]
            return photos


class Photo(core_models.AbstractTimeStampModel):
    """방 사진"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey(Room, related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption
