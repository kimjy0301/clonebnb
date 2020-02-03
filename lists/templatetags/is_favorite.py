from django import template
from lists import models as lists_models

register = template.Library()

# takes_context=True를 해주면 User정보와 Context를 모두 받아 올 수 있다.
@register.simple_tag(takes_context=True)
def is_favorite(context, room):
    user = context.request.user

    list = lists_models.List.objects.get_or_none(user=user)

    if list is not None:
        return room in list.rooms.all()
    else:
        return False
