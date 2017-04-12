from django.conf import settings
from mongoengine import *
from django.utils import timezone

connect(settings.MONGO_DB_NAME, host=settings.MONGO_SERVER_URL)


class ChatLog(Document):
    conversation_id = IntField()
    sender_id = IntField()
    message = StringField()
    read_users = ListField(IntField())
    created_at = DateTimeField(default=timezone.now())

    meta = {
        'indexes': [
            '-created_at',
        ]
    }




