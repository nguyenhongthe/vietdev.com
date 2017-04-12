from django.contrib import admin

from . import models, forms


@admin.register(models.Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'public', 'updated_at')
    list_filter = ('public',)
    list_editable = ('public',)
    search_fields = ('title',)
    form = forms.PageAdminForm
    save_on_top = True


