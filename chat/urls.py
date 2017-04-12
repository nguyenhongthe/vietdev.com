from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^inbox/$', views.inbox_view, name='inbox'),
    url(r'^inbox/(?P<username>[\w._@+-]+)/$', views.conversation_view, name='conversation'),
    url(r'^messages/load_more/api/', views.load_more_messages_view, name='load_more_messages'),
    url(r'^messages/read/api/', views.make_read_messages_view, name='make_read_messages')
]
