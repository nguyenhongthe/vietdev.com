import json

import arrow
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, Http404, redirect
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .mongo import ChatLog
from profiles.models import Profile
from . import models


@login_required
def inbox_view(request):
    c_list = models.Conversation.objects.filter(users__in=[request.user])
    if c_list:
        c = c_list[0]
        r = c.users.exclude(pk=request.user.id)[0]
        return redirect('chat:conversation', username=r.username)
    return render(request, 'chat/no_messages.html', {
        'nav': 'inbox'
    }, content_type='text/html')


@login_required
def conversation_view(request, username):
    try:
        receiver = Profile.objects.get(user__username=username, banned=False)
    except Profile.DoesNotExist:
        raise Http404()

    c_list = models.Conversation.objects.filter(users__in=[request.user])

    # try to create new conversation if it not exists
    cc = models.Conversation.objects.filter(users__in=[receiver.user]).filter(users__in=[request.user])
    if not cc:
        c = models.Conversation.objects.create(last_updated=timezone.now())
        c.users.set([receiver.user, request.user])
    else:
        c = cc[0]

    rows = ChatLog.objects(conversation_id=c.id).order_by('-created_at').limit(200)
    msg_list = []
    for r in rows:
        try:
            sender = User.objects.get(pk=r.sender_id)
            created_at = arrow.get(r.created_at).to(settings.TIME_ZONE)
            msg_list.append({
                'id_': r.id,
                'conversation_id': r.conversation_id,
                'sender': sender,
                'message': r.message,
                'is_unread': True if request.user.id not in r.read_users else False,
                'created_at': created_at.datetime,
                'created_at_formatted': created_at.format('DD MMM HH:mm')
            })
        except User.DoesNotExist:
            pass
    msg_list = sorted(msg_list, key=lambda j: j['created_at'], reverse=True)

    return render(request, 'chat/conversation.html', {
        'conversations': c_list,
        'current_conversation': c,
        'receiver': receiver,
        'msg_list': msg_list,
        'nav': 'inbox'
    }, content_type='text/html')


@login_required
@api_view(['GET'])
def load_more_messages_view(request):
    conversation_id = request.GET.get('conversation_id')
    page = request.GET.get('page')
    x = 200
    if conversation_id and page:
        try:
            page = int(page)
            end = page * x
            start = end - x
        except ValueError:
            return Response([])

        rows = ChatLog.objects(conversation_id=conversation_id).order_by('-created_at')[start:end]
        msg_list = []
        for r in rows:
            try:
                sender = User.objects.get(pk=r.sender_id)
                created_at = arrow.get(r.created_at).to(settings.TIME_ZONE)
                msg_list.append({
                    'id_': str(r.id),
                    'conversation_id': r.conversation_id,
                    'sender': sender.username,
                    'sender_url': sender.profile.get_absolute_url(),
                    'sender_avatar': sender.profile.get_avatar_url(),
                    'message': r.message,
                    'is_unread': True if request.user.id not in r.read_users else False,
                    'created_at': created_at.datetime,
                    'created_at_formatted': created_at.format('DD MMM HH:mm')
                })
            except User.DoesNotExist:
                pass
        msg_list = sorted(msg_list, key=lambda j: j['created_at'], reverse=True)
        return Response(msg_list)
    return Response([])


@login_required
@api_view(['POST'])
def make_read_messages_view(request):
    ids = request.data['ids']
    ids = json.loads(ids)
    messages = ChatLog.objects(id__in=ids)
    messages.update(add_to_set__read_users=[request.user.id])
    return Response({'ok': True})
