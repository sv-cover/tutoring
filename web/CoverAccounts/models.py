from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class CoverMember(AbstractBaseUser):
    ''' Model of a cover member. Substitutes Django's default user model. '''

    cover_id = models.IntegerField(unique=True)

    # TODO
    email = models.EmailField('email address', unique=True, db_index=True)

    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)

    first_login = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    USERNAME_FIELD = 'cover_id'

    #TODO
    def has_module_perms(self, package_name):
        return self.is_active

    #TODO
    def has_perm(self, perm, obj=None):
        return self.is_active

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def full_name(self):
        ''' Convenience method, returns the full name '''

        if self.is_anonymous:
            return "Anonymous"
        else:
            return "%s %s" % (self.first_name, self.last_name)

    def foto_url(self):
        ''' Returns the  user's profile foto from cover website '''

        # return 'https://www.cheapdigitizing.com/wp-content/uploads/2014/11/user-placeholder.png'
        return 'http://svcover.nl/foto.php?lid_id=%d&format=square&width=120' % self.cover_id


    #
    # @property
    #
    #
    # @property
    # def last_active(self):
    #     '''
    #         The time that passed since the user last performed an action on this
    #         site
    #     '''
    #
    #     return "0 days"
    #
    # @property
    # def foto_url(self):
    #     ''' Returns the  user's profile foto from cover website '''
    #
    #     # return 'https://www.cheapdigitizing.com/wp-content/uploads/2014/11/user-placeholder.png'
    #     return 'https://www.svcover.nl/foto.php?lid_id=1254&amp;format=square&amp;width=80'
    #
    #
    # def get_absolute_url(self):
    #
    #     #TODO get_absolute_url
    #     return "/"
    #
    # def __str__(self):
    #     return "%s" % (self.user)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#
#     '''  ''' #TODO
#     if created:
#         Profile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     '''  ''' #TODO
#     pass
    # instance.profile.save()
