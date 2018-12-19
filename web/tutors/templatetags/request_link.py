from django import template
from django.core.urlresolvers import reverse

register = template.Library()

def _create_link(user, request):
    for conversation in request.conversations.all():
        if user in conversation.participants.all():
            return conversation.get_absolute_url()

    return reverse('messages:conversation_create') + '?to=' + str(request.owner.cover_id) + '&request=' + str(request.id)

@register.simple_tag(takes_context=True)
def create_request_link(context, **kwargs):
    user = context.get('request').user
    return _create_link(user, **kwargs)