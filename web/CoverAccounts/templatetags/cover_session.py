from urlparse import urlparse, urlunparse, parse_qs

from django import template
from django.conf import settings
from django.utils.datastructures import MultiValueDict
from django.utils.http import urlencode


register = template.Library()


def _cover_session_url(base, context=None, next_url=None, next_field='referrer'):
    """ Injects a Cover session url with the next field. """
    if next_url is None:
        if context:
            next_url = context.get('request').build_absolute_uri()
        else:
            return base

    parts = list(urlparse(base))
    query_parts = MultiValueDict(parse_qs(parts[4]))
    query_parts[next_field] = next_url
    parts[4] = urlencode(query_parts, True)
    return urlunparse(parts)


@register.simple_tag(takes_context=True)
def cover_login_url(context, **kwargs):
    """ Provides a shortcut for the Cover login url  """
    base = getattr(settings, 'COVER_LOGIN_URL', 'https://www.svcover.nl/sessions.php?view=login')
    return _cover_session_url(base, context=context, **kwargs)


@register.simple_tag(takes_context=True)
def cover_logout_url(context, **kwargs):
    """ Provides a shortcut for the Cover logout url  """
    base = getattr(settings, 'COVER_LOGOUT_URL', 'https://www.svcover.nl/sessions.php?view=logout')
    return _cover_session_url(base, context=context, **kwargs)
