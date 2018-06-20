from django.conf import settings
from django.contrib.auth.hashers import check_password

from .models import CoverMember


class EmailAuthBackend(object):
    """
    A custom authentication backend. Allows users to log in using their email address.
    """

    def authenticate(self, email=None, password=None, session_id=None):
        """
        Authentication method
        """
        try:
            user = CoverMember.objects.get(email=email)
            if user.check_password(password):
                return user
        except CoverMember.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = CoverMember.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except CoverMember.DoesNotExist:
            return None


class CoversiteAuthBackend:
    """
    An authentication backend for authentication Cover members that are already known to the system.
    """
    def authenticate(self, request, session=None):
        """
        Authenticates a known Cover Member based on the a CoverSession object.
        Updates the locally stored data of the member and returns an authenticated CoverMember object
        or None if no member could be authenticated.
        """
        if not session:
            return None

        try:
            cover_member = CoverMember.objects.get(cover_id=session.user['id'])
        except CoverMember.DoesNotExist:
            return None

        cover_member.email = session.user['email']
        cover_member.first_name = session.user['voornaam']

        if session.user['tussenvoegsel'] == "":
            cover_member.last_name = session.user['achternaam']
        else:
            cover_member.last_name = "{tussenvoegsel} {achternaam}".format(**session.user)

        cover_member.save()
        
        return cover_member


    def get_user(self, user_id):
        """
        Returns the CoverMember object corresponding to a user_id
        """
        try:
            return CoverMember.objects.get(pk=user_id)
        except CoverMember.DoesNotExist:
            return None
