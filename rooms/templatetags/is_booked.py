from django import template
from reservations import models as reservation_models
import datetime

register = template.Library()

# takes_context=True를 해주면 User정보와 Context를 모두 받아 올 수 있다.
@register.simple_tag(takes_context=True)
def is_booked(context, room, day):
    # user = context["request"].user
    if day.number == 0:
        return
    try:
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        reservation_models.BookedDay.objects.get(day=date, reservation__room=room)
        return True
    except reservation_models.BookedDay.DoesNotExist:
        return False

