from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


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

class RestrictNonMemberMiddleware(object):
    """
    Restricts access to anoymous users to the login page.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        login_path = reverse('CoverAccounts:login')

        if request.user.is_anonymous() and request.path != login_path:
            return HttpResponseRedirect(login_path)

        return self.get_response(request)
