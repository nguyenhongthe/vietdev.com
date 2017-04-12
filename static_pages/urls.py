from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', views.PageDetailView.as_view(), name='detail'),
]
