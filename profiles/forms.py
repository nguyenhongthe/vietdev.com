import posixpath

from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, HTML
from django import forms
from django.conf import settings
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from . import models


class AdvancedSearchForm(forms.Form):
    language = forms.ModelChoiceField(label='Programming Language', required=False,
                                      queryset=models.ProgrammingLanguage.objects.all(),
                                      to_field_name='slug')
    technology = forms.ModelMultipleChoiceField(label='Technologies', required=False,
                                                queryset=models.Technology.objects.all(),
                                                to_field_name='slug')
    location = forms.ModelChoiceField(label='Location', required=False,
                                      queryset=models.Location.objects.all(),
                                      to_field_name='slug')
    rate = forms.CharField(label='Rate')
    is_available = forms.CharField(label='Only show who are available for hire', required=False,
                                   widget=forms.CheckboxInput())

    def __init__(self, *args, **kwargs):
        super(AdvancedSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            'language', 'technology', 'location',
            Field('rate', template='_field_rate.html'),
            'is_available'
        )


class RequestEmailForm(forms.Form):
    email = forms.EmailField(label='Your Email', required=True,
                             widget=forms.EmailInput(attrs={'autofocus': 'autofocus'}))
    captcha = ReCaptchaField(attrs={'theme': 'clean'}, label='')

    def __init__(self, *args, **kwargs):
        super(RequestEmailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


def thumbnail(image_path, width, height):
    absolute_url = posixpath.join(settings.MEDIA_URL, image_path)
    return '<img src="%s" alt="%s" class="widget-img" />' % (absolute_url, image_path)


class ImageWidget(forms.ClearableFileInput):
    template = '<div>%(image)s</div>' \
               '<div>%(clear_template)s</div>' \
               '<div>%(input)s</div>'

    def __init__(self, attrs=None, template=None, width=200, height=200):
        if template is not None:
            self.template = template
        self.width = width
        self.height = height
        super(ImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        if not self.is_required:
            checkbox_name = self.clear_checkbox_name(name)
            checkbox_id = self.clear_checkbox_id(checkbox_name)
            substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
            substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
            substitutions['clear'] = forms.CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})

        input_html = super(forms.ClearableFileInput, self).render(name, value, attrs)
        if value and hasattr(value, 'width') and hasattr(value, 'height'):
            image_html = thumbnail(value.name, self.width, self.height)
            output = self.template % {'input': input_html,
                                      'image': image_html,
                                      'clear_template': self.template_with_clear % substitutions}
        else:
            output = input_html
        return mark_safe(output)


class EditProfileForm(forms.ModelForm):
    rate = forms.CharField(label='Rate')

    class Meta:
        model = models.Profile
        fields = ('is_available', 'name', 'job_title', 'location', 'rate', 'birth_year', 'sex', 'avatar',
                  'english_level', 'languages', 'homepage', 'twitter', 'github', 'about', 'software', 'hardware')
        labels = {
            'twitter': 'Twitter Username',
            'github': 'Github Username',
            'is_available': 'I\'m available for hire'
        }
        widgets = {
            'avatar': ImageWidget
        }
        help_texts = {
            'job_title': 'Whatever title you want to stick on your name.',
            'languages': 'Select programming languages you master.',
            'about': 'Enter more info about you that can make your profile looks more impressive.',
            'software': 'Select software you are using for developing. This field is optional.',
            'hardware': 'Select hardware you have. This field is optional.',
        }

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("Personal Info",
                     'is_available', 'name', 'job_title', 'location',
                     'birth_year', 'sex',
                     'avatar', css_class='mt-0'),

            HTML('<button class="btn btn-primary btn-block" type="submit">'
                 '<i class="material-icons">&#xE5CA;</i> Save Profile</button>'),

            Fieldset("Dev Info",
                     Field('rate', template='_field_rate.html'),
                     'english_level', 'languages'),
            Fieldset("References",
                     'homepage', 'twitter', 'github'),

            HTML('<button class="btn btn-primary btn-block" type="submit">'
                 '<i class="material-icons">&#xE5CA;</i> Save Profile</button>'),

            Fieldset("More Info",
                     'about', 'software', 'hardware'),
        )
