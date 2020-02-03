from django.urls import path
from . import views


app_name = "lists"

urlpatterns = [
    path("add/<int:pk>", views.save_room, name="save-room"),
    path("remove/<int:pk>", views.remove_room, name="remove-room"),
    path("favorite/", views.SeeFavoriteView.as_view(), name="see-favorite"),
]
