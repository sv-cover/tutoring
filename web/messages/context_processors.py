from itertools import chain

from .models import *

def conversationsOfUser(request):
    unsorted_conversations = []
    unread_message_count = 0

    if request.user.is_authenticated():
        unsorted_conversations = Conversation.objects.conversationsOf(request.user).all()

        for conv in list(unsorted_conversations):
            # unread_message_count += 1


            if conv.latest_message() is None:
                continue

            if conv.latest_message().sender == request.user:
                # unread_message_count += -1
                continue

            if conv.latest_message().read_by.count() > 0:
                msg_read_by = list(conv.latest_message().read_by.all())
                if not request.user in msg_read_by:
                    unread_message_count += 1
            else:
                unread_message_count += 1

    conversations_without_messages = filter(lambda conv: conv.latest_message() is None, unsorted_conversations)
    conversations_with_messages = filter(lambda conv: not conv.latest_message() is None, unsorted_conversations)

    sorted_conversations = sorted(conversations_with_messages, key=lambda conv: conv.latest_message().sent_at, reverse=True)

    return {
        'conversations': list(chain(conversations_without_messages, sorted_conversations))[:5],
        'unread_message_count': unread_message_count,
        'archived_conversations_count' : unsorted_conversations.count() - 5,
    }
