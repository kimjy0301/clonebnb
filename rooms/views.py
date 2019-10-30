from django.shortcuts import render
from datetime import datetime
from . import models as room_models
import math
from django.core.paginator import Paginator


# Create your views here.


def all_rooms(request):

    page = request.GET.get("page", 1)
    room_list = room_models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)
    rooms = paginator.get_page(page)
    print(dir(rooms))
    return render(request, "rooms/home.html", {"page": rooms})

    # page = request.GET.get("page", 1)
    # page = int(page or 1)
    # page_size = 10
    # limit = page_size * page
    # offset = limit - page_size

    # all_rooms = room_models.Room.objects.all()[offset:limit]
    # page_count = math.ceil(room_models.Room.objects.count() / page_size)

    # # print(str(all_rooms.query))
    # return render(
    #     request,
    #     "rooms/home.html",
    #     context={
    #         "all_rooms": all_rooms,
    #         "page": page,
    #         "page_count": page_count,
    #         "page_range": range(1, page_count + 1),
    #     },
    # )
