from django.conf import settings
from django.contrib.auth.hashers import check_password
# from django.contrib.auth.models import User

from coverapi import CoverAPI, APIError

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

    def __init__(self):
        self.api = CoverAPI(settings.COVER_API_URL, settings.COVER_API_APP, settings.COVER_API_SECRET)

    def authenticate(self, email=None, password=None, session_id=None):
        try:
            if session_id is not None:
                session = self.api.get_session(session_id)
            elif email is not None and password is not None:
                session = self.api.login(email, password)
            else:
                raise Exception("No session_id nor username and password were provided to authenticate()")

            # print("::: %s" % session.user)

            try:
                coverMember = CoverMember.objects.get(cover_id=session.user['id'])
                coverMember.email = session.user['email']
                coverMember.first_name = session.user['voornaam']

                if session.user['tussenvoegsel'] == "":
                    coverMember.last_name = session.user['achternaam']
                else:
                    coverMember.last_name = "{tussenvoegsel} {achternaam}".format(**session.user)

                coverMember.save()

            except CoverMember.DoesNotExist:
                coverMember = CoverMember(cover_id=session.user['id'])
                coverMember.email = session.user['email']
                coverMember.first_name = session.user['voornaam']

                if session.user['tussenvoegsel'] == "":
                    coverMember.last_name = session.user['achternaam']
                else:
                    coverMember.last_name = "{tussenvoegsel} {achternaam}".format(**session.user)

                if session.user['email'] in settings.STAFF_MEMBERS:
                    coverMember.is_staff = True
                    coverMember.is_admin = True

                coverMember.update_telegram_bot_token()

                coverMember.save()
                #
                # user = User(username=session.user['id'])
                # user.save()
            return coverMember
        except APIError:
            return None

    def get_user(self, user_id):
        try:
            return CoverMember.objects.get(pk=user_id)
        except CoverMember.DoesNotExist:
            return None
