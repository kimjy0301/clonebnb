import os
import requests
from django.views.generic import FormView, DetailView
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages

from . import forms
from users import models as user_models


# class LoginView(View):
#     def get(self, request):
#         form = forms.LoginForm()
#         return render(request, "users/login.html", {"form": form})

#     def post(self, request):
#         form = forms.LoginForm(request.POST)

#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(request, "users/login.html", {"form": form})


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        print(email)
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"환영합니다. {user.first_name}")
        return super().form_valid(form)


def log_out(request):
    logout(request)
    messages.success(request, "정상적으로 Logout 되었습니다.")
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):

        form.save()

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user_models.User.verify_email(user)

        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = user_models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.save()
        # 성공메시지 추가 해줘야함
    except user_models.User.DoesNotExist:
        # 나중에 에러메시지 추가해줘야됨
        pass
    return redirect(reverse("core:home"))


def gitgub_login(request):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):

    try:
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        code = request.GET.get("code", None)
        post_data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
        }
        if code is not None:
            token_request = requests.post(
                url="https://github.com/login/oauth/access_token",
                data=post_data,
                headers={"Accept": "application/json"},
            )
            result_json = token_request.json()
            error = result_json.get("error", None)
            if error is not None:
                raise GithubException("Github RestApi 호출 실패.")
            else:
                access_token = result_json.get("access_token")

                profile_request = requests.get(
                    url="https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:
                        user = user_models.User.objects.get(username=email)
                        if user.login_method == user_models.User.LOGIN_GITHUB:
                            login(request, user)
                        else:
                            raise GithubException(
                                f"{user.login_method.upper() } 방식을 사용하여 로그인해주세요."
                            )
                    except user_models.User.DoesNotExist:
                        new_user = user_models.User.objects.create(
                            username=email,
                            first_name=name,
                            bio=bio,
                            email=email,
                            email_verified=True,
                        )
                        new_user.set_unusable_password()
                        new_user.login_method = user_models.User.LOGIN_GITHUB
                        new_user.save()
                        login(request, new_user)
                        messages.success(request, f"환영합니다. {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("사용자 이름 불러오기 실패.")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    app_key = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoExcepction(Exception):
    pass


def kakao_callback(request):
    try:
        app_key = os.environ.get("KAKAO_ID")
        code = request.GET.get("code")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        post_data = {
            "grant_type": "authorization_code",
            "client_id": app_key,
            "redirect_uri": redirect_uri,
            "code": code,
        }

        token_request = requests.post(
            f"https://kauth.kakao.com/oauth/token", data=post_data
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoExcepction("카카오 인증코드 수신 실패.")
        access_token = token_json.get("access_token", None)

        profile_request = requests.get(
            f"https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()

        kakao_account = profile_json.get("kakao_account")
        if kakao_account is None:
            raise KakaoExcepction("카카오 계정 불러오기 실패.")
        email = kakao_account.get("email")
        if email is None:
            raise KakaoExcepction("카카오 계정에 이메일 접근 권한을 확인해주세요.")

        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            user = user_models.User.objects.get(email=email)

            if user.login_method != user_models.User.LOGIN_KAKAO:
                raise KakaoExcepction(f"{user.login_method.upper() } 방식을 사용하여 로그인해주세요.")
        except user_models.User.DoesNotExist:

            user = user_models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=user_models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatart", ContentFile(photo_request.content)
                )
        login(request, user)
        messages.success(request, f"환영합니다. {user.first_name}")

        return redirect(reverse("core:home"))
    except KakaoExcepction as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    model = user_models.User
    context_object_name = "user_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hello"] = "hello!"
        return context
