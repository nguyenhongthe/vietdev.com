import arrow

from channels.generic.websockets import JsonWebsocketConsumer
from channels import Group
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

from . import content_processors
from . import models
from .exceptions import ClientError
from .utils import catch_client_error
from .mongo import ChatLog


class ChatConsumer(JsonWebsocketConsumer):

    http_user = True
    strict_ordering = False

    def get_handler(self, *args, **kwargs):
        handler = super(ChatConsumer, self).get_handler(*args, **kwargs)
        return catch_client_error(handler)

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        try:
            receiver = User.objects.get(pk=kwargs.get('receiver_id', 0))
            c = models.Conversation.objects.filter(users__in=[self.message.user]).filter(users__in=[receiver])
            if c:
                Group("conv-{}".format(c[0].id)).add(message.reply_channel)
            else:
                raise ClientError('ACCESS_DENIED')
        except User.DoesNotExist:
            # this is flexible for sending any flags to current connection,
            # we can easily handle them by using plain JS
            raise ClientError('ACCESS_DENIED')

        self.message.reply_channel.send({"accept": True})

    def receive(self, content, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        conv = content.get('conversation')
        if conv:
            try:
                c = models.Conversation.objects.get(pk=content['conversation'], users__in=[self.message.user])
                if content['command'] == 'join':
                    content['join'] = c.id
            except models.Conversation.DoesNotExist:
                raise ClientError('ACCESS_DENIED')

            if content['command'] == 'send':
                content['sender'] = self.message.user.username
                content['sender_url'] = self.message.user.profile.get_absolute_url()
                content['sender_avatar'] = self.message.user.profile.get_avatar_url()
                content['created_at'] = arrow.now(settings.TIME_ZONE).format('DD MMM HH:mm')
                content['message'] = content_processors.cleanup_chat_text(content['message'].replace('\n', '<br>'))

                # save info into mongoDB
                m = ChatLog(
                    conversation_id=conv,
                    sender_id=self.message.user.id,
                    message=content['message'],
                    read_users=[self.message.user.id],
                    created_at=timezone.now()
                )
                m.save()

                # also send the mongo ID, so we can easy handle it later
                content['id_'] = str(m.id)

                # update last post time without calling signals
                models.Conversation.objects.filter(pk=conv).update(last_updated=timezone.now())

            self.group_send('conv-{}'.format(conv), content)

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        try:
            receiver = User.objects.get(pk=kwargs.get('receiver_id', 0))
            c = models.Conversation.objects.filter(users__in=[self.message.user]).filter(users__in=[receiver])
            if c:
                # let's discard the channel out of group after disconnected
                Group("conv-{}".format(c[0].id)).discard(message.reply_channel)
        except User.DoesNotExist:
            pass
