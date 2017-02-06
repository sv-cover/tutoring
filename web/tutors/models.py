from django.db import models

from CoverAccounts.models import CoverMember

class Language(models.Model):
    ''' A spoken language, such as English, Dutch, etc. '''

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Subject(models.Model):
    ''' Course subject, such as LinearAlgebra, Calculus, etc. '''

    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Offer(models.Model):
    ''' A tutoring offer, created by a student who wants to tutor. '''

    owner = models.OneToOneField(CoverMember, on_delete=models.CASCADE)

    # # TODO
    is_anonymous = models.BooleanField(default=True)

    # # TODO
    is_listed = models.BooleanField(default=False)

    # # TODO
    offered_languages = models.ManyToManyField(Language)

    # # TODO
    offered_subjects = models.ManyToManyField(Subject)

    # # TODO
    description = models.TextField()

    def get_absolute_url(self):
        '''  ''' #TODO

        # return reverse('request_detail', kwargs={"pk": self.pk})
        #TODO get_absolute_url
        return "/"

    def __str__(self):
        return self.owner.__str__()

class Request(models.Model):
    '''
        A tutoring request, created by a student who needs tutoring and can't
        find a tutor.
    '''

    # TODO
    owner = models.ForeignKey(CoverMember, on_delete=models.CASCADE)

    # TODO
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    # TODO
    is_anonymous = models.BooleanField(default=True)


    # TODO
    updated_at = models.DateTimeField(auto_now=True)

    # TODO
    description = models.TextField()

    # TODO
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        '''  ''' #TODO

        # return reverse('request_detail', kwargs={"pk": self.pk})
        #TODO get_absolute_url
        return "/"

    def __str__(self):
        return "%s: %s" % (self.owner, self.subject)
