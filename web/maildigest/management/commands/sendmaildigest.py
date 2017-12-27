from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, send_mass_mail
from django.core.mail import get_connection, EmailMultiAlternatives

from messages.models import Conversation, Message
from CoverAccounts.models import CoverMember
from django.template import Context
from django.template.loader import get_template

class Command(BaseCommand):
    help = 'Sends an email digest to all users with new messages.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        self.stdout.write('{} - Start executing Email Digest command.\nSend emails to the following users:'.format(datetime.now()))

        messages_to_send = []

        email_subject = 'CACTuS - Here is what happened'
        email_from = 'testbot@bankosegger.at'

        mail_template_plain = get_template('maildigest/digest.txt')
        mail_template_html = get_template('maildigest/digest.html')

        for user in CoverMember.objects.filter(is_alpha_user=True, receives_mail_notification=True):

            conversations = list(Conversation.objects.conversationsOf(user))
            conversations = [c for c in conversations if not user in c.latest_message().read_by.all()]

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

        self.stdout.write('Done! Mails successfully sent to {n} people!\n{t} - Done.\n---'.format(n=len(messages_to_send), t=datetime.now()))
