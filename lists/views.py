from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic import TemplateView

from . import models as list_models
from rooms import models as rooms_models


# Create your views here.


def save_room(request, pk):
    room = rooms_models.Room.objects.get_or_none(pk=pk)
    if room is not None:
        the_list, created = list_models.List.objects.get_or_create(
            user=request.user, name=f"{request.user.username}'s Favorite Houses"
        )
        the_list.rooms.add(room)
    return redirect(reverse("rooms:detail", kwargs={"pk": pk}))


def remove_room(request, pk):

    room = rooms_models.Room.objects.get_or_none(pk=pk)
    if room is not None:
        list = list_models.List.objects.get_or_none(user=request.user)
        list.rooms.remove(room)

    return redirect(reverse("rooms:detail", kwargs={"pk": pk}))


class SeeFavoriteView(TemplateView):
    template_name = "lists/detail.html"
