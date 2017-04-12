from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from profiles.sitemaps import ProfileSitemap, ProgrammingLanguageSitemap, TechnologySitemap


sitemaps = {
    'profiles': ProfileSitemap,
    'programing_languages': ProgrammingLanguageSitemap,
    'technologies': TechnologySitemap
}


urlpatterns = [
    url(r'^wtf_admin/', admin.site.urls),
    url(r'', include('profiles.urls', namespace='profiles')),
    url(r'', include('chat.urls', namespace='chat')),
    url(r'', include('registration.urls', namespace='registration')),
    url(r'^contact/', include('contact.urls', namespace='contact')),
    url(r'^page/', include('static_pages.urls', namespace='pages')),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

