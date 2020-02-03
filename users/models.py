from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.shortcuts import reverse
from core import managers

# Create your models here.


class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"
    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"
    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "영어"), (LANGUAGE_KOREAN, "한국어"))

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"
    CURRENCY_CHOICES = ((CURRENCY_USD, "달러"), (CURRENCY_KRW, "원"))

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    avatar = models.ImageField(blank=True, upload_to="avatar_photos")
    gender = models.CharField(
        default=GENDER_MALE, choices=GENDER_CHOICES, max_length=10, blank=True
    )
    bio = models.TextField(blank=True)
    birthdate = models.DateField(null=True)  # DateTImeField 랑은 다르다.
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )

    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )
    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="", blank=True)
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    objects = managers.CustomManager()

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            self.save()
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )
            send_mail(
                "Verify CloneBnb Account",
                strip_tags(html_message),
                settings.EMAIL_HOST_USER,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
        return

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

