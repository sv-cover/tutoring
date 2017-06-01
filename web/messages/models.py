from django.db import models
from django.db.models import Q
from django.urls import reverse

from CoverAccounts.models import CoverMember

class ConversationManager(models.Manager):
    '''
        The manager for Conversation.
    '''

    def conversationsOf(self, user):
        return self.all().filter(participants__in=[user])

class Conversation(models.Model):
    '''
        A conversation, between one or more CoverMembers
    '''

    subject = models.CharField('Subject', max_length=140)

    participants = models.ManyToManyField(CoverMember, blank=True)

    objects = ConversationManager()

    def latest_message(self):
        latest = self.messages.latest('sent_at')
        return latest

    def __str__(self):
        return "%s" % self.subject

    def get_absolute_url(self):
        return reverse('messages:conversation_detail', args=[str(self.pk)])


class Message(models.Model):
    '''
        A message, sent from one CoverMember to another.
    '''

    # The converation in which this message was sent
    conversation = models.ForeignKey(Conversation, related_name='messages', null=True, blank=True, verbose_name='Conversation')

    # The CoverMember sending this message.
    sender = models.ForeignKey(CoverMember, default=None, related_name='sent_messages', on_delete=models.CASCADE)

    # The time at which the message was sent
    sent_at = models.DateTimeField('sent at', auto_now_add=True)

    # The message string itself.
    message = models.TextField()

    def __str__(self):
        return "%s: %s" % (self.sent_at, self.sender)
