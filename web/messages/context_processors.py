from .models import *

def conversationsOfUser(request):
    unsorted = []

    if request.user.is_authenticated():
        unsorted = Conversation.objects.conversationsOf(request.user).all()

    return {
        'conversations': unsorted #sorted(unsorted, key=lambda conv: conv.latest_message().sent_at, reverse=True)[:5]
    }
