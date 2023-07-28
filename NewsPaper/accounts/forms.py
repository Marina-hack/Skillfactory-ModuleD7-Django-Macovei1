from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from allauth.account.forms import SignupForm
from django.core.mail import mail_managers
from django.core.mail import mail_admins


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        mail_managers(
            subject='New subscriber',
            message=f'A subscriber {user.username} has registered at the website.'
        )
        mail_admins(
            subject='New subscriber',
            message=f'A subscriber {user.username} has registered at the website.'
        )
        return user

# class CustomSignupForm(SignupForm):
#     def save(self, request):
#         user = super().save(request)
#
#         subject = 'Wellcome to News Portal!'
#         text = f'{user.username}, you have signed up!'
#         html = (
#             f'<b>{user.username}</b>, your registration at '
#             f'<a href="http://127.0.0.1:8000/news">News Portal</a> is successful!'
#         )
#         msg = EmailMultiAlternatives(
#             subject=subject, body=text, from_email=None, to=[user.email]
#         )
#         msg.attach_alternative(html, "text/html")
#         msg.send()
#
#         mail_managers(
#             subject='Новый пользователь!',
#             message=f'Пользователь {user.username} зарегистрировался на сайте.'
#         )
#
#         return user


# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(label="Email")
#     first_name = forms.CharField(label="First name")
#     last_name = forms.CharField(label="Last name")
#
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#             "password1",
#             "password2",
#         )
