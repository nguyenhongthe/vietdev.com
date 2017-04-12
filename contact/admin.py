from django.contrib import admin

from . import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'checked')
    list_editable = ('checked',)
    list_filter = ('checked',)
    search_fields = ('name', 'email')

    def changelist_view(self, request, extra_context=None):
        if 'checked__exact' not in request.GET:
            q = request.GET.copy()
            q['checked__exact'] = 0
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(MessageAdmin, self).changelist_view(request, extra_context=extra_context)
