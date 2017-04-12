import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView, UpdateView
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from haystack.query import SearchQuerySet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from pure_pagination.mixins import PaginationMixin
from . import models
from . import forms
from . import serializers


class MainNavMixin(ContextMixin):
    nav = ''

    def get_context_data(self, **kwargs):
        context = super(MainNavMixin, self).get_context_data(**kwargs)
        context['nav'] = self.nav
        return context


class HomeIndexView(MainNavMixin, FormMixin, ListView):
    template_name = 'index.html'
    nav = 'home'
    form_class = forms.AdvancedSearchForm

    def get_context_data(self, **kwargs):
        context = super(HomeIndexView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get_queryset(self):
        language = self.request.GET.get('language')
        location = self.request.GET.get('location')
        rate = self.request.GET.get('rate', 0)
        is_available = True if self.request.GET.get('is_available') == 'on' else False
        techs = self.request.GET.getlist('technology')

        qs = SearchQuerySet().models(models.Profile)

        if language:
            qs = qs.filter(languages__in=[language])
        if techs:
            qs = qs.filter(technologies__in=techs)
        if location:
            qs = qs.filter(location_slug=location)
        if is_available:
            qs = qs.filter(is_available=True)

        qs = qs.filter(rate__range=[1, float(rate)])
        return qs

    def get_initial(self):
        language = self.request.GET.get('language')
        location = self.request.GET.get('location')
        rate = self.request.GET.get('rate')
        is_available = True if self.request.GET.get('is_available') == 'on' else False
        techs = self.request.GET.getlist('technology')
        return {
            'language': language,
            'location': location,
            'rate': rate,
            'is_available': is_available,
            'technology': techs
        }


class BrowseView(MainNavMixin, PaginationMixin, ListView):
    template_name = 'browse.html'
    nav = 'browse'
    paginate_by = 10

    def get_queryset(self):
        o = self.request.GET.get('o')
        is_available = self.request.GET.get('is_available')
        qs = models.Profile.objects.filter(banned=False, is_ready=True)

        if is_available == 'on':
            qs = qs.filter(is_available=True)

        if o == 'rate_low_to_high':
            qs = qs.order_by('rate')
        elif o == 'rate_high_to_low':
            qs = qs.order_by('-rate')
        elif o == 'age_young_to_old':
            qs = qs.exclude(birth_year=None).order_by('-birth_year')
        elif o == 'age_old_to_young':
            qs = qs.exclude(birth_year=None).order_by('birth_year')
        elif o == 'best_skills':
            qs = qs.order_by('-total_points')

        return qs

    def get_context_data(self, **kwargs):
        context = super(BrowseView, self).get_context_data(**kwargs)
        context['o'] = self.request.GET.get('o', '')
        context['is_available'] = self.request.GET.get('is_available', '')
        return context


class ProfileView(MainNavMixin, DetailView):
    template_name = 'profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'user__username'
    model = models.Profile

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        if self.request.user == self.get_object().user:
            context['nav'] = 'profile'
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'profile_edit.html'
    form_class = forms.EditProfileForm
    slug_url_kwarg = 'username'
    slug_field = 'user__username'

    def get_queryset(self):
        return models.Profile.objects.filter(banned=False, user=self.request.user)


class EditSkillsView(LoginRequiredMixin, DetailView):
    template_name = 'profile_skills.html'
    slug_url_kwarg = 'username'
    slug_field = 'user__username'

    def get_queryset(self):
        return models.Profile.objects.filter(banned=False, user=self.request.user)


class TechListAPIView(ListAPIView):
    serializer_class = serializers.TechSerializer
    queryset = models.Technology.objects.order_by('name')


class UserSkillsAPIView(ListAPIView):
    serializer_class = serializers.TechnologyMasteringLevelSerializer

    def get_queryset(self):
        return models.TechnologyMasteringLevel.objects.filter(user=self.request.user, removed=False)


class SaveSkillsView(APIView):
    def post(self, request, **kwargs):
        skills = list(filter(lambda x: x.get('technology'), request.data))
        user = request.user

        if len(skills) > 0:
            models.TechnologyMasteringLevel.objects.filter(user=user).update(removed=True)

        for s in skills:
            tech = models.Technology.objects.get(pk=s['technology']['id'])
            try:
                t = models.TechnologyMasteringLevel.objects.get(user=user, technology=tech)
                t.self_rate = s.get('rate', 0)
                t.year_exp = s.get('exp', 1)
                t.activity = s.get('activity')[0] if s.get('activity') else ''
                t.involved_real_projects = True if s.get('real_projects') else False
                t.removed = False
                t.save()
            except models.TechnologyMasteringLevel.DoesNotExist:
                t = models.TechnologyMasteringLevel(
                    user=user,
                    technology=tech,
                    self_rate=s.get('rate', 0),
                    year_exp=s.get('exp', 1),
                    activity=s.get('activity')[0] if s.get('activity') else '',
                    involved_real_projects=True if s.get('real_projects') else False
                )
                t.save()
            if t:
                models.Profile.objects.filter(user=user).update(is_ready=True)
        return Response({'ok': True})


class LanguageView(SingleObjectMixin, PaginationMixin, ListView):
    template_name = 'language.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=models.ProgrammingLanguage.objects.all())
        return super(LanguageView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return models.Profile.objects.filter(banned=False, is_ready=True,
                                             languages__in=[self.object]).order_by('-total_points')


class TechView(SingleObjectMixin, PaginationMixin, ListView):
    template_name = 'tech.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=models.Technology.objects.all())
        return super(TechView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        users = models.TechnologyMasteringLevel.objects.filter(technology=self.object).values_list('user_id', flat=True)
        return models.Profile.objects.filter(banned=False, is_ready=True, pk__in=users).order_by('-total_points')


class RequestEmailView(FormView):
    template_name = 'request_email.html'
    form_class = forms.RequestEmailForm

    def get(self, request, *args, **kwargs):
        u = self.request.GET.get('u')
        if u:
            try:
                p = models.Profile.objects.get(user__username=u, banned=False)
                if p.user.email:
                    return super(RequestEmailView, self).get(request, *args, **kwargs)
            except models.Profile.DoesNotExist:
                pass
        raise Http404()

    def get_context_data(self, **kwargs):
        context = super(RequestEmailView, self).get_context_data(**kwargs)
        context['req_user'] = self.request.GET.get('u')
        return context

    def get_initial(self):
        user = self.request.user
        if user.is_authenticated:
            return {'email': user.email}
        return {}

    def form_valid(self, form):
        email = form.cleaned_data['email']
        req_user = form.data['req_user']

        if email and req_user:
            try:
                p = models.Profile.objects.get(user__username=req_user, banned=False)
                if p.user.email:

                    profile_url = self.request.build_absolute_uri(p.get_absolute_url())

                    # send email
                    email_data = {
                        'from': 'Vietdev <{}>'.format(settings.DEFAULT_FROM_EMAIL),
                        'to': [email],
                        'subject': 'Request Dev Email on Vietdev.com',
                        'text': settings.REQUEST_EMAIL_BODY.format(dev_name=p.get_name(),
                                                                   profile_url=profile_url,
                                                                   dev_email=p.user.email)
                    }
                    r = requests.post(
                        'https://api.mailgun.net/v3/{}/messages'.format(settings.MAILGUN_DOMAIN),
                        data=email_data,
                        auth=('api', settings.MAILGUN_API_KEY)
                    )
                    if r.ok:
                        pass

            except models.Profile.DoesNotExist:
                pass

        return redirect('profiles:request_email_sent')


class SearchUserAutoCompleteView(ListAPIView):
    serializer_class = serializers.SearchUserAutoSerializer

    def get_queryset(self):
        q = self.request.GET.get('query')
        if q:
            return SearchQuerySet().models(models.Profile).autocomplete(username_auto=q)
        return []


class SearchResultsView(PaginationMixin, ListView):
    template_name = 'search.html'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            return SearchQuerySet().models(models.Profile).filter(content=q)[:200]
        return

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context
