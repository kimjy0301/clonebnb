from django.shortcuts import render, redirect
from . import models as room_models, forms
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from django.urls import reverse
from django.http import Http404

from django_countries import countries
from django.views.generic import ListView, View
import math


# Create your views here.


class HomeView(ListView):
    model = room_models.Room
    template_name = "rooms/home.html"
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        totalPage = context["page_obj"].paginator.num_pages

        page = self.request.GET.get("page", 1)
        context["page"] = page

        countPage = 5

        startPage = int(
            math.floor(((int(page) - 1) / int(countPage))) * int(countPage) + 1
        )
        endPage = startPage + countPage

        if endPage > int(totalPage):
            context["pageRange"] = range(startPage, totalPage + 1)
            context["page_obj"].has_next = False
        else:
            context["pageRange"] = range(startPage, endPage)

        if startPage == 1:
            context["page_obj"].has_previous = False

        return context


class SearchView(ListView):
    def get(self, request):
        country = request.GET.get("country")

        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}
                if city != "Anywhere":
                    filter_args["city__startswith"] = city
                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests
                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms
                if beds is not None:
                    filter_args["beds__gte"] = beds
                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True
                if superhost is True:
                    filter_args["host__superhost"] = True

                qs = room_models.Room.objects.filter(**filter_args).order_by("created")

                for amenity in amenities:
                    qs = qs & room_models.Room.objects.filter(amenities=amenity)

                for facility in facilities:
                    qs = qs & room_models.Room.objects.filter(facilities=facility)

                paginator = Paginator(qs, 10, orphans=10)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "page": rooms}
                )

        else:
            form = forms.SearchForm()
        return render(request, "rooms/search.html", {"form": form})


def room_detail(request, pk):
    try:
        room = room_models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room})
    except room_models.Room.DoesNotExist:
        raise Http404()
        return redirect(reverse("core:home"))


def search_manual(request):
    city = str.capitalize(request.GET.get("city", "Anywhere"))
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", "0") or 0)
    price = int(request.GET.get("price", 0) or 0)
    guests = int(request.GET.get("guests", 0) or 0)
    bedrooms = int(request.GET.get("bedrooms", 0) or 0)
    beds = int(request.GET.get("beds", 0) or 0)
    bathrooms = int(request.GET.get("bathrooms", 0) or 0)
    selected_amenity = request.GET.getlist("amenities")
    selected_facility = request.GET.getlist("facilities")

    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))

    # 뷰단에서 데이터를 가져오는것들
    form = {
        "city": city,
        "selected_country": country,
        "selected_room_type": room_type,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "bathrooms": bathrooms,
        "selected_amenity": selected_amenity,
        "selected_facility": selected_facility,
        "instant": instant,
        "superhost": superhost,
    }

    # DB에서 값을 가져오는 것들.
    room_types = room_models.RoomType.objects.all()
    amenities = room_models.Amenity.objects.all()
    facilities = room_models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city
    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests
    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms
    if beds != 0:
        filter_args["beds__gte"] = beds
    if bathrooms != 0:
        filter_args["baths__gte"] = bathrooms

    if instant is True:
        filter_args["instant_book"] = True
    if superhost is True:
        filter_args["host__superhost"] = True

    rooms = room_models.Room.objects.filter(**filter_args)

    if len(selected_amenity) > 0:
        for a_id in selected_amenity:
            rooms = rooms & room_models.Room.objects.filter(amenities__pk=int(a_id))

    if len(selected_facility) > 0:
        for f_id in selected_facility:
            rooms = rooms & room_models.Room.objects.filter(facilities__pk=int(f_id))

    print(filter_args)
    print(str(rooms.query))

    return render(
        request, "rooms/search.html", context={**form, **choices, "rooms": rooms}
    )


def all_rooms(request):

    page = request.GET.get("page", 1)
    room_list = room_models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)
    try:
        rooms = paginator.page(page)
        return render(request, "rooms/home.html", {"page": rooms})
    except EmptyPage:
        return redirect("/")

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
