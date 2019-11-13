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


class SignUpForm(forms.ModelForm):
    class Meta:
        model = user_models.User
        fields = ("first_name", "last_name", "email", "birthdate")
        widgets = {
            "birthdate": forms.DateInput(
                format=("%m/%d/%Y"),
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a date",
                    "type": "date",
                },
            )
        }

    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user_models.User.objects.get(username=email)
            raise forms.ValidationError("해당 이메일로 생성된 계정이 존재합니다.")
        except user_models.User.DoesNotExist:
            return email

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password != password2:
            raise forms.ValidationError("동일한 비밀번호를 입력해주세요.")
        else:
            return password

    def save(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = super().save(commit=False)

        user.username = email
        user.set_password(password)
        user.save()


# class SignUpForm(forms.Form):

#     first_name = forms.CharField(max_length=80)
#     last_name = forms.CharField(max_length=80)
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         try:
#             user_models.User.objects.get(email=email)
#             raise forms.ValidationError("해당 이메일로 생성된 계정이 존재합니다.")
#         except user_models.User.DoesNotExist:
#             return email

#     def clean_password2(self):
#         password = self.cleaned_data.get("password")
#         password2 = self.cleaned_data.get("password2")

#         if password != password2:
#             raise forms.ValidationError("동일한 비밀번호를 입력해주세요.")
#         else:
#             return password

#     def save(self):
#         first_name = self.cleaned_data.get("first_name")
#         last_name = self.cleaned_data.get("last_name")
#         email = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password")

#         user = user_models.User.objects.create_user(
#             username=email, email=email, password=password
#         )
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()
