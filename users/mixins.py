from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy


class LoggedOutOnlyView(UserPassesTestMixin):

    permission_denied_message = "Page not pound"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "로그인된 상태에선 이동 할 수 없는 URL 입니다.")
        return redirect(reverse("core:home"))


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, "로그인 후 이동할 수 있는 URL입니다.")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class EmailLoggedInOnlyView(UserPassesTestMixin):
    permission_denied_message = "Page not pound"

    def test_func(self):
        print(self.request.user.login_method)
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "Email 가입계정만 이동할 수 있는 URL입니다.")
        return redirect(reverse("core:home"))
