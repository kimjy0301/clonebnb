from django import forms
from . import models as user_models


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     try:
    #         user_models.User.objects.get(usename=email)
    #         return email
    #     except user_models.User.DoesNotExist:
    #         raise forms.ValidationError("해당하는 유저가 존재하지 않습니다.")

    def clean(self):

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = user_models.User.objects.get(username=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 일치하지 않습니다."))
        except user_models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("해당하는 유저가 존재하지 않습니다."))
