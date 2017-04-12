from django.contrib.sitemaps import Sitemap

from .models import Profile, ProgrammingLanguage, Technology, Location


class ProfileSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Profile.objects.filter(banned=False, is_ready=True)

    def lastmod(self, obj):
        return obj.updated_at


class ProgrammingLanguageSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return ProgrammingLanguage.objects.all()


class TechnologySitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return Technology.objects.all()
