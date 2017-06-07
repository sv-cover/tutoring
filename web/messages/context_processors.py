from .models import *

def conversationsOfUser(request):
    unsorted_conversations = []
    unread_message_count = 0

    if request.user.is_authenticated():
        unsorted_conversations = Conversation.objects.conversationsOf(request.user).all()

        for conv in list(unsorted_conversations):
            # unread_message_count += 1

            if conv.latest_message().sender == request.user:
                # unread_message_count += -1
                continue

            if conv.latest_message().read_by.count() > 0:
                msg_read_by = list(conv.latest_message().read_by.all())
                if not request.user in msg_read_by:
                    unread_message_count += 1
            else:
                unread_message_count += 1

    return {
        'conversations': unsorted_conversations, #sorted(unsorted, key=lambda conv: conv.latest_message().sent_at, reverse=True)[:5]
        'unread_message_count': unread_message_count
    }
