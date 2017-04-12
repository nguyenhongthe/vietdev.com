from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timesince import timesince

from chat.mongo import ChatLog

register = template.Library()


@register.simple_tag()
def get_ws_host():
    return {
        'host': settings.WS_HOST,
        'port': settings.WS_PORT,
        'port_secure': settings.WS_PORT_SECURE
    }


@register.simple_tag()
def get_recipient(qs, user):
    try:
        return qs.exclude(pk=user.id)[0]
    except KeyError:
        pass
    return User.objects.none()


@register.filter("timesince_chat", is_safe=False)
def timesince_filter(value, arg=None):
    """Formats a date as the time since that date (i.e. "4 days, 6 hours")."""
    if not value:
        return ''
    try:
        if arg:
            ts = timesince(value, arg)
        else:
            ts = timesince(value)
        if ts == '0 minutes':
            return 'Just now'
        return ts
    except (ValueError, TypeError):
        return ''


@register.simple_tag()
def num_unread(conversation_id, user_id):
    return ChatLog.objects(conversation_id=conversation_id, read_users__nin=[user_id]).count()


@register.simple_tag()
def num_unread_by_user(user_id):
    return ChatLog.objects(read_users__nin=[user_id]).count()

