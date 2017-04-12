import requests
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from . import forms


class ContactView(FormView):
    template_name = 'contact/contact_form.html'
    form_class = forms.MessageForm

    def get_initial(self):
        user = self.request.user
        if user.is_authenticated:
            return {
                'name': user.profile.name,
                'email': user.email
            }
        return None

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        name = form.cleaned_data.get('name')
        content = form.cleaned_data.get('content', '')

        if not settings.DEBUG:
            # email to admin
            email_data = {
                'from': 'Vietdev <{}>'.format(settings.DEFAULT_FROM_EMAIL),
                'to': settings.ADMIN_EMAIL,
                'subject': 'Vietdev: Contact from {}'.format(name),
                'text': 'Sender: {}.\n\n{}'.format(email, content)
            }
            r = requests.post(
                'https://api.mailgun.net/v3/{}/messages'.format(settings.MAILGUN_DOMAIN),
                data=email_data,
                auth=('api', settings.MAILGUN_API_KEY)
            )
            if r.ok:
                pass

            form.save()

            # email to submitter
            email_data = {
                'from': 'Vietdev <{}>'.format(settings.DEFAULT_FROM_EMAIL),
                'to': [email],
                'subject': 'Vietdev: Contact Us',
                'text': 'Hello {},\n\nYou\'ve sent a message to Vietdev Team. '
                        'We will response as soon as possible if needed.'
                        '\n\nBest regards,\nVietdev'.format(name)
            }
            r = requests.post(
                'https://api.mailgun.net/v3/{}/messages'.format(settings.MAILGUN_DOMAIN),
                data=email_data,
                auth=('api', settings.MAILGUN_API_KEY)
            )
            if r.ok:
                pass

        return redirect('contact:success', permanent=False)


class SuccessView(TemplateView):
    template_name = 'contact/contact_success.html'



