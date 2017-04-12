from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    url(r'^$', views.HomeIndexView.as_view(), name='home'),

    url(r'^browse/$', views.BrowseView.as_view(), name='browse'),

    url(r'^profile/(?P<username>[\w._@+-]+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^profile/(?P<username>[\w._@+-]+)/edit/$', views.EditProfileView.as_view(), name='profile_edit'),
    url(r'^profile/(?P<username>[\w._@+-]+)/skills/$', views.EditSkillsView.as_view(), name='profile_skills'),

    url(r'^profile/skills/save/api/$', views.SaveSkillsView.as_view(), name='profile_skills_save_api'),
    url(r'^profile/skills/list/api/$', views.UserSkillsAPIView.as_view(), name='profile_skills_list_api'),
    url(r'^tech/list/api/$', views.TechListAPIView.as_view(), name='tech_list_api'),

    url(r'^request_email/$', views.RequestEmailView.as_view(), name='request_email'),
    url(r'^request_email/sent/$',
        TemplateView.as_view(template_name='request_email_sent.html'), name='request_email_sent'),

    url(r'^language/(?P<slug>[\w-]+)/$', views.LanguageView.as_view(), name='language'),
    url(r'^tech/(?P<slug>[\w-]+)/$', views.TechView.as_view(), name='tech'),

    url(r'^search/$', views.SearchResultsView.as_view(), name='search_results'),
    url(r'^search/user/auto/api/$', views.SearchUserAutoCompleteView.as_view(), name='search_auto'),

]
