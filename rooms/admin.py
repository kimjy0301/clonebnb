from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """항목 Admin"""

    actions = ["change_country"]

    def change_country(self, request, queryset):
        updated_count = queryset.update(country="KR")  # queryset.update
        self.message_user(
            request, "{}건의 나라를 대한민국으로 변경".format(updated_count)
        )  # django message framework 활용

    change_country.short_description = "지정 포스팅을 대한민국으로 변경"

    inlines = [PhotoInline]

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
        "total_rating",
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

    raw_id_fields = ("host",)

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

    count_photos.short_description = "number of photos"
    count_amenities.short_description = "number of amenities"


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """사진 Admin"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"
