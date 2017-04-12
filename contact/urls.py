from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.ContactView.as_view(), name='form'),
    url(r'^ok/$', views.SuccessView.as_view(), name='success'),
]
