from haystack import indexes

from . import models


class ProfileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    username = indexes.CharField(model_attr='user__username')
    name = indexes.CharField(model_attr='name')
    job_title = indexes.CharField(model_attr='job_title')
    location = indexes.CharField(model_attr='location__name')
    location_slug = indexes.CharField(model_attr='location__slug')
    rate = indexes.FloatField(model_attr='rate')
    is_available = indexes.BooleanField(model_attr='is_available')

    languages = indexes.MultiValueField()
    technologies = indexes.MultiValueField()

    url = indexes.CharField(model_attr='get_absolute_url')
    avatar = indexes.CharField(model_attr='get_avatar_url')
    created_at = indexes.DateTimeField(model_attr='created_at')

    # for autocomplete
    username_auto = indexes.EdgeNgramField(model_attr='build_search_autocomplete')

    def get_model(self):
        return models.Profile

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_ready=True, banned=False)

    def prepare_languages(self, obj):
        return [l.slug for l in obj.languages.all()]

    def prepare_technologies(self, obj):
        return [t.technology.slug for t in obj.get_techs_list()]
