"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # from . import settings 는 안됨
from django.conf.urls.static import static
from django.conf.urls import url
from core import urls as core_urls
from rooms import urls as room_urls
from users import urls as user_urls
from reservations import urls as reservations_urls
from reviews import url as reviews_urls
from lists import url as lists_urls
from conversations import url as conversation_urls


urlpatterns = [
    path("", include(core_urls, namespace="core")),
    path("admin/", admin.site.urls),
    path("rooms/", include(room_urls, namespace="rooms")),
    path("users/", include(user_urls, namespace="users")),
    path("reservations/", include(reservations_urls, namespace="reservations")),
    path("reviews/", include(reviews_urls, namespace="reviews")),
    path("lists/", include(lists_urls, namespace="lists")),
    path("conversations/", include(conversation_urls, namespace="conversations")),
]


# 개발/운영 모드 체크

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
