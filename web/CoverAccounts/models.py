from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings
from django.db import models
from datetime import datetime

from hashlib import sha1

import hashlib


class CoverMember(AbstractBaseUser):
    ''' Model of a cover member. Substitutes Django's default user model. '''

    cover_id = models.IntegerField(unique=True)

    # TODO
    email = models.EmailField('email address', unique=True, db_index=True)

    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)

    appears_anonymous = models.BooleanField(default=False, verbose_name="Hide personal details", help_text="Checking this means that your name and profile picture will not appear anywhere on this page. However your tutoring offers and requests can still be seen, including what you wrote in their descriptions.")
    receives_weekly_mails = models.BooleanField(default=False, verbose_name="Enable weekly mail digests", help_text="If checked, you will be receiving weekly email updates on new messages, but of course only if there are unread ones.")
    receives_daily_mails = models.BooleanField(default=True, verbose_name="Enable daily mail digests", help_text="If checked, you will be receiving daily email updates on new messages, but of course only if there are unread ones.")

    first_login = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_alpha_user = models.BooleanField(default=False)

    is_banned = models.BooleanField(default=False)

    telegram_bot_token = models.CharField(default=None, max_length=160, verbose_name="Telegram Bot Token", help_text="You can setup the \"CACTuS Messenger\" bot in Telegram. The bot will ask you for this code.")
    telegram_chat_id = models.IntegerField(null=True)

    telegram_id_counter = models.IntegerField(default=0)

    USERNAME_FIELD = 'cover_id'

    #TODO
    def pk_hash(self):
        m =  hashlib.md5()
        m.update(str(self.pk).encode('utf-8'))
        m.update('salt q23u90ruefwjods'.encode('utf-8'))
        return m.hexdigest()

    #TODO
    def has_module_perms(self, package_name):
        return self.is_active

    #TODO
    def has_perm(self, perm, obj=None):
        return self.is_active

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """ Convenience method, returns the full name """
        return u'{} {}'.format(self.first_name, self.last_name)

    @property
    def is_unknown(self):
        """ Provide distinction from Cover members who are unknown to the system. """
        return False

    @property
    def foto_url(self):
        ''' Returns the  user's profile foto from cover website '''
        return '//svcover.nl/foto.php?lid_id={}&format=square&width=120'.format(self.cover_id)

    def update_telegram_bot_token(self):
        self.telegram_id_counter += 1

        hasher = sha1()
        hasher.update(str(self.pk).encode('utf-8'))
        hasher.update(str(self.telegram_id_counter).encode('utf-8'))
        hasher.update(settings.TELEGRAM_HASH_SALT.encode('utf-8'))

        self.telegram_bot_token =  hasher.hexdigest()

        print(self.telegram_bot_token)

    def __eq__(self, other):
        return self.cover_id == other.cover_id

    def update_member(self, session_user):
        self.email = session_user['email']
        self.first_name = session_user['voornaam']

        if session_user['tussenvoegsel'] == "":
            self.last_name = session_user['achternaam']
        else:
            self.last_name = "{tussenvoegsel} {achternaam}".format(**session_user)

        if session_user['member_till'] is None and not self.is_active:
            self.is_active = True
        elif session_user['member_till'] is not None:
            member_till = datetime.strptime(session_user['member_till'], '%Y-%m-%d')
            if datetime.now() > member_till:
                self.is_active = False
       
        if session_user['email'] in settings.STAFF_MEMBERS:
            self.is_staff = True
            self.is_admin = True

        if any(c in session_user['committees'] for c in settings.ADMIN_COMMITTEES):
            self.is_staff = True
            self.is_admin = True

        self.save()


class UnknownCoverMember(AnonymousUser):
    def __init__(self, cover_session):
        self.cover_session = cover_session

    def __str__(self):
        return 'UnknownCoverMember'

    @property
    def first_name(self):
        return self.cover_session.user['voornaam']
        
    @property
    def last_name(self):
        if self.cover_session.user['tussenvoegsel'] == "":
            return self.cover_session.user['achternaam']
        return "{tussenvoegsel} {achternaam}".format(**self.cover_session.user)

    @property
    def full_name(self):
        """ Convenience method, returns the full name """
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def is_anonymous(self):
        """ Provide distinction from AnonymousUser. The user is unknown to the sytem, but not anonymous. """
        return False

    @property
    def is_unknown(self):
        """ Provide distinction from Cover members who are known to the system. """
        return True

    def get_username(self):
        return self.cover_session.user['id']

    def as_cover_member(self):
        """ Returns this user as a CoverMember object. """
        cover_member = CoverMember(cover_id=self.cover_session.user['id'])
        cover_member.email = self.cover_session.user['email']
        cover_member.first_name = self.first_name
        cover_member.last_name = self.last_name

        if cover_member.email in settings.STAFF_MEMBERS:
            cover_member.is_staff = True
            cover_member.is_admin = True

        print 'Committees: ' + str(self.cover_session.user['committees'])
        if any(c in self.cover_session.user['committees'] for c in settings.ADMIN_COMMITTEES):
            cover_member.is_staff = True
            cover_member.is_admin = True

        cover_member.update_telegram_bot_token()

        return cover_member
