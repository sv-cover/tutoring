from django import template

from tutors.models import Offer

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_user_is_tutor(context):

    print(context.get('user'))

    user = context.get('user')

    try:
        offer = Offer.objects.get(owner=user)
        return True
    except:
        return False
