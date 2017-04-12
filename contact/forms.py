from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from django import forms

from . import models


class MessageForm(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ('name', 'email', 'content', 'captcha')

    name = forms.CharField(required=True, label='Your Name',
                           widget=forms.TextInput(attrs={'autofocus': ''}))
    email = forms.EmailField(required=True, label='Your Email',
                             widget=forms.EmailInput())
    content = forms.CharField(required=True, label='Your Message', widget=forms.Textarea(
                                  attrs={'maxlength': 2000,
                                         'placeholder': 'Please enter plain text, do not use HTML...'}))
    captcha = ReCaptchaField(attrs={'theme': 'clean'}, label='')

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
