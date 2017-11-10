from django.contrib.auth.models import AbstractBaseUser
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models

import hashlib

class CoverMember(AbstractBaseUser):
    ''' Model of a cover member. Substitutes Django's default user model. '''

    cover_id = models.IntegerField(unique=True)

    # TODO
    email = models.EmailField('email address', unique=True, db_index=True)

    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)

    appears_anonymous = models.BooleanField(default=False, verbose_name="Hide personal details", help_text="Checking this means that your name and profile picture will not appear anywhere on this page. However your tutoring offers and requests can still be seen, including what you wrote in their descriptions.")
    receives_mail_notification = models.BooleanField(default=True, verbose_name="Enable mail notification", help_text="If checked, you will be receiving email notifications whenever someone writes you a message.")

    first_login = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_banned = models.BooleanField(default=False)

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
