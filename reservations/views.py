from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.http import Http404

from . import models as reservations_models
from rooms import models as room_models
from reviews import forms as reviews_form

import datetime

# Create your views here.


class CreateError(Exception):
    pass


def createReservation(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year=year, month=month, day=day)
        room = room_models.Room.objects.get(pk=room)
        reservations_models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "예약 할 수 없습니다.")
        return redirect(reverse("core:home"))
    except reservations_models.BookedDay.DoesNotExist:
        reservation = reservations_models.Reservation.objects.create(
            status=reservations_models.Reservation.STATUS_PENDING,
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetail(View):
    def get(self, request, pk):
        reservation = reservations_models.Reservation.objects.get_or_none(pk=pk)
        if (not reservation) or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()

        # 리뷰에 있는 폼을 가져다 쓸수있음
        form = reviews_form.CreateReviewForm()

        return render(
            self.request,
            "reservations/detail.html",
            {"reservation": reservation, "form": form},
        )


def EditReservation(request, pk, verb):

    reservation = reservations_models.Reservation.objects.get_or_none(pk=pk)
    if (not reservation) or (
        reservation.guest != request.user and reservation.room.host != request.user
    ):
        raise Http404()

    if verb == "confirmed":
        reservation.status = reservations_models.Reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = reservations_models.Reservation.STATUS_CANCELED
        reservations_models.BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "예약이 수정되었습니다.")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))

