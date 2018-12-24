from datetime import datetime, timedelta
from django.utils import timezone

from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail
from django.core.mail import get_connection, EmailMultiAlternatives

from messages.models import Conversation
from CoverAccounts.models import CoverMember
from django.template import Context
from django.template.loader import get_template

class Command(BaseCommand):
    help = 'Sends an email digest to all users with new messages.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        self.stdout.write('{} - Start executing Daily Email Digest command.\nSend emails to the following users:'.format(datetime.now(timezone.utc)))

        messages_to_send = []

        email_subject = 'CACTuS - Daily update'
        email_from = 'tutoring@svcover.nl'

        mail_template_plain = get_template('task/daily_digest.txt')
        mail_template_html = get_template('task/daily_digest.html')

        for user in CoverMember.objects.filter(receives_daily_mails=True, is_active=True):

            conversations = list(Conversation.objects.conversations_of(user))
            conversations = [c for c in conversations
                             if c.latest_message()
                             and not user in c.latest_message().read_by.all()
                             and datetime.now(timezone.utc) - c.latest_message().sent_at
                             <= timedelta(hours=24)]

            if len(conversations) == 0:
                continue

            context = {
                'user': user,
                'conversations': conversations,
                'n_conversations': len(conversations),
            }
            mail_content_plain = mail_template_plain.render(context)
            mail_content_html = mail_template_html.render(context)

            message = EmailMultiAlternatives(email_subject, mail_content_plain, email_from, [user.email])
            message.attach_alternative(mail_content_html, 'text/html')

            print(' - {}'.format(user))
            messages_to_send.append(message)

        self.stdout.write('Talking to mail server...')

        with get_connection() as connection:
            connection.send_messages(messages_to_send)

        self.stdout.write('Done! Mails successfully sent to {n} people!\n{t} - Done.\n---'.
                          format(n=len(messages_to_send), t=datetime.now()))
