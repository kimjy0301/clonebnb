from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from rooms import models as room_models
from django.utils.html import mark_safe

# Register your models here.


class UserInline(admin.StackedInline):
    model = room_models.Room

    filter_horizontal = ("amenities", "facilities", "room_rules")

    def get_extra(self, request, obj=None, **kwargs):
        return 1


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """ Custom User Admin """

    inlines = [UserInline]

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                    "email_verified",
                    "email_secret",
                    "login_method",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost", "login_method")

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "get_thumbnail",
        "email_verified",
        "login_method",
    )

    def get_thumbnail(self, obj):
        url = ""
        if obj.avatar and hasattr(obj.avatar, "url"):
            url = obj.avatar.url
        return mark_safe(f'<img width="50px" src="{url}" />')

    get_thumbnail.short_description = "Thumbnail"
