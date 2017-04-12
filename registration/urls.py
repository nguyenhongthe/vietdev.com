from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views, forms

urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html', 'authentication_form': forms.LoginForm}, name='login'),
    url(r'^logout/$', views.logout_then_login, {'login_url': 'registration:login'}, name='logout'),

    url(r'^password/forgot/$', auth_views.password_reset, {'post_reset_redirect': 'registration:forgot_password_sent',
                                                           'template_name': 'registration/forgot_password.html',
                                                           'password_reset_form': forms.ForgotPasswordForm}, name='forgot_password'),
    url(r'^password/forgot/sent/$', TemplateView.as_view(template_name='registration/forgot_password_sent.html'), name='forgot_password_sent'),
    url(r'^password/forgot/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'set_password_form': forms.NewPasswordForm, 'post_reset_redirect': 'registration:login',
                                            'template_name': 'registration/forgot_password_confirm.html'}, name='forgot_password_confirm'),

    url(r'^password/change/$', auth_views.password_change,
            {'post_change_redirect': 'registration:logout', 'template_name': 'registration/change_password.html',
             'password_change_form': forms.ChangePasswordForm}, name='change_password'),

]
