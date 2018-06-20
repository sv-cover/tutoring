from django.conf import settings
from django.contrib.auth import get_user, authenticate, login
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.signals import user_logged_out
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.functional import SimpleLazyObject
from django.shortcuts import render

from coverapi import CoverAPI, APIError

from .models import UnknownCoverMember


def get_cover_user(request):
    """
    Determines the correct user object corresponding to the current coversession.
    Returns 
    - a CoverMember object if the user is a known user
    - an UnknownCoverMember object if the user is a logged in Covermember who is unkown to the system
    - an AnonymousUser object if there is no active Cover session
    """
    cookie_name = getattr(settings, 'COVER_COOKIE', 'cover_session_id')
    session_id = request.COOKIES.get(cookie_name, 0)

    cover_api = CoverAPI(settings.COVER_API_URL, settings.COVER_API_APP, settings.COVER_API_SECRET)

    try:
        session = cover_api.get_session(session_id)
    except APIError:
        # No active Cover session (or something else is wrong with the website)
        return AnonymousUser()

    # Get user object (CoverMember or AnonymousUser) for the current Django session
    user = get_user(request)

    if user.get_username() != session.user['id']:
        # Current Django session user and the current Cover session don't match, logout the Django session
        user_logged_out.send(sender=user.__class__, request=request, user=user)
        request.session.flush()
        user = AnonymousUser()

    if isinstance(user, AnonymousUser):
        # No active Django session, try to authenticate the Cover user
        user = authenticate(request, session=session)
        if not user:
            user = UnknownCoverMember(session)
        elif user.is_active:
            # Initiate Django session
            login(request, user)

    return user or AnonymousUser()


class CoverAuthenticationMiddleware(object):
    """
    Provides authentication for cover sessions.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not hasattr(request, 'session'):
            raise ImproperlyConfigured("The Cover auth middleware requires the session middleware to be installed.")
        request.user = SimpleLazyObject(lambda: get_cover_user(request))
        return self.get_response(request)


class RestrictAdminMiddleware(object):
    """
    Restricts access to the admin page to only logged-in users with a certain user-level.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if request.path == reverse('admin:index'):
            if not (request.user.is_active and request.user.is_staff):
                return HttpResponseRedirect('/')

        return self.get_response(request)


class RestrictUnknownUserMiddleware(object):
    """
    Restricts access for anonymous users and unknown Cover members. 
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        anonymous_allowed_paths = [
            reverse('CoverAccounts:login'),
            reverse('terms_conditions'),
            reverse('telegram_bot:webhook'),
        ]

        unkown_allowed_paths = anonymous_allowed_paths + [
            reverse('CoverAccounts:first_use'),
        ]

        if request.user.is_anonymous and request.path not in anonymous_allowed_paths:
            return HttpResponseRedirect(reverse('CoverAccounts:login'))

        if not request.user.is_anonymous and request.user.is_unknown and request.path not in unkown_allowed_paths:
            return HttpResponseRedirect(reverse('CoverAccounts:first_use'))

        if not request.user.is_anonymous and not request.user.is_unknown and not request.user.is_active:
            return render(request, 'CoverAccounts/account_disabled.html')

        return self.get_response(request)
