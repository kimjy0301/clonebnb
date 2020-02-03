from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy


class OnlyHostEditView(UserPassesTestMixin):

    permission_denied_message = "Page not pound"

    def test_func(self):
        room_number = self.kwargs.get(self.pk_url_kwarg)
        try:
            self.request.user.rooms.get(pk=room_number)
            return True
        except Exception:
            return False

    def handle_no_permission(self):
        messages.error(self.request, "접근할 수 없는 URL입니다.")
        return redirect(reverse("core:home"))
