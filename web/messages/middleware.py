from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class ConversationListMiddleware(object):
    """
    Creates a list of converations to render in sidebar.
    """

    pass

    # def __init__(self, get_response):
    #     self.get_response = get_response
    #     # One-time configuration and initialization.
    #
    # def __call__(self, request):
    #
    #     if request.path == reverse('admin:index'):
    #         if not (request.user.is_active and request.user.is_staff):
    #             return HttpResponseRedirect('/')
    #
    #     return self.get_response(request)
