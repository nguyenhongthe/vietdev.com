from django import forms

from . import models


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = models.Page
        fields = '__all__'


