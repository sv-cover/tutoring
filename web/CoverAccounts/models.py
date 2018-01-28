from django.contrib.auth.models import AbstractBaseUser
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings
from django.db import models

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
    receives_mail_notification = models.BooleanField(default=True, verbose_name="Enable mail digests", help_text="If checked, you will be receiving weekly email updates on what you missed.")

    first_login = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_alpha_user = models.BooleanField(default=False)

    is_banned = models.BooleanField(default=False)

    telegram_bot_token = models.CharField(unique=True, default=None, max_length=160, verbose_name="Telegram Bot Token", help_text="You can setup the \"CACTuS Messenger\" bot in Telegram. The bot will ask you for this code.")
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
        ''' Convenience method, returns the full name '''

        if self.appears_anonymous:
            return "Anonymous"
        else:
            return "%s %s" % (self.first_name, self.last_name)

    def foto_url(self):
        ''' Returns the  user's profile foto from cover website '''
        if self.appears_anonymous:
            return static('default_profile_400.png')
        else:
            return 'http://svcover.nl/foto.php?lid_id=%d&format=square&width=120' % self.cover_id

    def update_telegram_bot_token(self):
        self.telegram_id_counter += 1

        hasher = sha1()
        hasher.update(str(self.pk).encode('utf-8'))
        hasher.update(str(self.telegram_id_counter).encode('utf-8'))
        hasher.update(settings.TELEGRAM_HASH_SALT.encode('utf-8'))

        self.telegram_bot_token =  hasher.hexdigest()

        print(self.telegram_bot_token)
