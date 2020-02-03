from django import template

register = template.Library()


@register.filter(name="previous_page")
def previous_page(value):

    if "page=" not in value:
        value = f"{value}&page=1"

    split = value.split("&")
    for s in split:
        if "page=" in s:
            page_num = str(int(s.replace("page=", "")) - 5)
            value = value.replace(s, "page=" + page_num)
    return value


@register.filter(name="next_page")
def next_page(value):

    if "page=" not in value:
        value = f"{value}&page=1"

    split = value.split("&")
    for s in split:
        if "page=" in s:
            page_num = str(int(s.replace("page=", "")) + 5)
            value = value.replace(s, "page=" + page_num)
    return value


@register.filter(name="change_page")
def change_page(value, page):

    if "page=" not in value:
        value = f"{value}&page=1"

    split = value.split("&")

    for s in split:
        if "page=" in s:
            value = value.replace(s, "page=" + str(page))

    return value

