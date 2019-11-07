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

