import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import FormView
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.views import logout

from . import forms
from profiles.models import Profile


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = forms.RegisterForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # create user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = True
            user.save()

            # send welcome email
            email_data = {
                'from': 'Vietdev <{}>'.format(settings.DEFAULT_FROM_EMAIL),
                'to': [email],
                'subject': 'Welcome to Vietdev.com',
                'text': settings.WELCOME_EMAIL_BODY.format(username=username, email=email)
            }
            r = requests.post(
                'https://api.mailgun.net/v3/{}/messages'.format(settings.MAILGUN_DOMAIN),
                data=email_data,
                auth=('api', settings.MAILGUN_API_KEY)
            )
            if r.ok:
                pass

            # make profile
            profile, _ = Profile.objects.get_or_create(user=user)

            # login
            auth_user = authenticate(username=username, password=password)
            auth_login(request, auth_user)

            return redirect('profiles:profile')

        return render(request, "registration/register.html", {'form': form})


def logout_then_login(request, login_url=None, extra_context=None):
    """
    Logs out the user if they are logged in. Then redirects to the log-in page.
    """
    if not login_url:
        login_url = settings.LOGIN_URL
    login_url = resolve_url(login_url)
    return logout(request, login_url, extra_context=extra_context)


