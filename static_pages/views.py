from django.views.generic import DetailView

from static_pages.models import Page


class PageDetailView(DetailView):
    template_name = 'static_pages/detail.html'
    queryset = Page.objects.filter(public=True)
