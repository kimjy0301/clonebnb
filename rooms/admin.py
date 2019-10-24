from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """항목 Admin"""

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        ("Time Info", {"fields": ("check_in", "check_out", "instant_book")}),
        (
            "Spaces Info",
            {"classes": ("wide",), "fields": ("amenities", "facilities", "room_rules")},
        ),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        ("Details", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "city",
        "country",
    )
    search_fields = ("=city", "^host__username")

    filter_horizontal = ("amenities", "facilities")
    filter_vertical = ("room_rules",)


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """사진 Admin"""

    pass
