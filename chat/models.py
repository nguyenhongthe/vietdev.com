from django.contrib.auth.models import User
from django.db import models

from .mongo import ChatLog


class Conversation(models.Model):
    users = models.ManyToManyField(User, related_name='+')
    last_updated = models.DateTimeField()

    class Meta:
        ordering = ('-last_updated',)

    def get_user_display(self):
        x = [u.username for u in self.users.all()]
        return 'Conversation {}'.format(' - '.join(x))

    def get_last_message(self):
        m = ChatLog.objects(conversation_id=self.id).order_by('-created_at').first()
        if m:
            return m.message
        return '-'

