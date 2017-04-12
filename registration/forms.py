import requests
from captcha.fields import ReCaptchaField
import re

from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.forms import PasswordChangeForm


class RegisterForm(UserCreationForm):
    class Meta:
        fields = ("username", 'email', 'password', 'captcha')
        model = User

    username = forms.CharField(required=True, label='Username', min_length=4, max_length=20,
                               widget=forms.TextInput(attrs={'autofocus': '',
                                                             'autocapitalize': 'none',
                                                             'placeholder': '4-20 characters'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput())
    password = forms.CharField(max_length=30, min_length=6, required=True, label='Password',
                               widget=forms.PasswordInput())
    captcha = ReCaptchaField(attrs={'theme': 'clean'}, label='')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields.pop('password1')
        self.fields.pop('password2')
        self.helper = FormHelper()
        self.helper.form_tag = False

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError('Email address is not valid.')
        return self.cleaned_data['email']


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, label='Username', min_length=3, max_length=20,
                               widget=forms.TextInput(attrs={'class': 'weui_input', 'autocapitalize': 'none',
                                                             'autofocus': ''}))
    password = forms.CharField(max_length=30, required=True, label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'weui_input'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'autofocus': ''}))
    captcha = ReCaptchaField(attrs={'theme': 'clean'}, label='')

    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = get_user_model()._default_manager.filter(
            email__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name=None,
             email_template_name=None,
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            link = 'https://{}{}'.format(settings.SITE_DOMAIN, reverse_lazy('registration:forgot_password_confirm', args=[uidb64, token]))
            email_data = {
                'from': 'Vietdev <{}>'.format(settings.DEFAULT_FROM_EMAIL),
                'to': [user.email],
                'subject': 'Vietdev: Reset Password',
                'text': settings.FORGOT_PASSWORD_EMAIL_BODY.format(link=link, username=user.username)
            }
            r = requests.post(
                'https://api.mailgun.net/v3/{}/messages'.format(settings.MAILGUN_DOMAIN),
                data=email_data,
                auth=('api', settings.MAILGUN_API_KEY)
            )
            if r.ok:
                pass


class NewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', required=True, widget=forms.PasswordInput(attrs={'autofocus': ''}))
    new_password2 = forms.CharField(label='Enter It Again', required=True, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(NewPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="Current", required=True,
                                   widget=forms.PasswordInput(attrs={'autofocus': ''}))
    new_password1 = forms.CharField(label="New Password", required=True, widget=forms.PasswordInput())
    new_password2 = forms.CharField(label="Enter It Again", required=True, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
