from django import forms
from . import models as room_models
from django_countries.fields import CountryField


class SearchForm(forms.Form):
    city = forms.CharField(required=False)
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        queryset=room_models.RoomType.objects.all(),
        required=False,
        empty_label="Any kind",
    )
    price = forms.IntegerField(required=False, max_value=999999999, min_value=0)
    guests = forms.IntegerField(required=False, min_value=0)
    bedrooms = forms.IntegerField(required=False, min_value=0)
    beds = forms.IntegerField(required=False, min_value=0)
    baths = forms.IntegerField(required=False, min_value=0)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)

    amenities = forms.ModelMultipleChoiceField(
        queryset=room_models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    facilities = forms.ModelMultipleChoiceField(
        queryset=room_models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = room_models.Photo
        fields = ("caption", "file")

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        room = room_models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()


class HostingRoomForm(forms.ModelForm):
    class Meta:
        model = room_models.Room
        fields = {
            "name",
            "description",
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
            "room_type",
            "amenities",
            "facilities",
            "room_rules",
        }

    field_order = [
        "name",
        "description",
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
        "room_type",
        "amenities",
        "facilities",
        "room_rules",
    ]

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        return room


class EditRoomForm(forms.ModelForm):
    class Meta:
        model = room_models.Room
        fields = {
            "name",
            "description",
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
            "room_type",
            "amenities",
            "facilities",
            "room_rules",
        }

    field_order = [
        "name",
        "description",
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
        "room_type",
        "amenities",
        "facilities",
        "room_rules",
    ]
