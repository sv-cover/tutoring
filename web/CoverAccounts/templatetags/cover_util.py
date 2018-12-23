from django.contrib.staticfiles.templatetags.staticfiles import static
from django import template

register = template.Library()

def _get_name(context, user=None, personalise=False, current_user=None):
    """ Gets the name of the user and anomynises it when needed. """
    if current_user is None:
        current_user = context.get('request').user
    if user is None:
        user = context.get('request').user
    if user.appears_anonymous and (user != current_user):
        return 'Anonymous'

    if personalise and (user == current_user):
        return 'You'
    
    return user.full_name

def _get_foto_url(context, user=None):
    """ Gets the url of the users foto and anomynises it when needed. """
    if not user:
        user = context.get('request').user
    if user.appears_anonymous and (user != context.get('request').user):
        return static('default_profile_400.png')
    
    return user.foto_url

@register.simple_tag(takes_context=True)
def cover_user_name(context, **kwargs):
    """ Shortcut for a users name """
    return _get_name(context, **kwargs)

@register.simple_tag(takes_context=True)
def cover_foto_url(context, **kwargs):
    """ Shortcut for a users foto """
    return _get_foto_url(context, **kwargs)