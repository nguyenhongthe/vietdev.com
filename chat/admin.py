from django.contrib import admin

from .models import Conversation


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('get_user_display', 'last_updated')
    search_fields = ('users__username',)
    raw_id_fields = ('users',)

