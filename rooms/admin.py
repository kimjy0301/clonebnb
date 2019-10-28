from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """항목 Admin"""

    # 방 세부화면에서 보여질 필드셋 정의
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

    # 방 목록에서 보여지는 컬럼 정의
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
        "count_amenities",
        "count_photos",
    )

    # 방 목록에서 오른쪽에 필터 리스트 정의
    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "city",
        "country",
    )

    # 방 목록에서 검색바 추가. = 일치하는것 ^시작하는것
    search_fields = ("=city", "^host__username")

    # Choices가 들어간 항목 리스트 모양 변경
    filter_horizontal = ("amenities", "facilities")
    filter_vertical = ("room_rules",)
    # 방목록에서 정렬하는 순서
    ordering = ("name", "price")

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):  # obj는 model
        return obj.photos.count()


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """사진 Admin"""

    pass
