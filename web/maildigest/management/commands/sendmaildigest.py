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
        messages_to_send = []

        email_subject = 'CACTuS - Weekly Digest'
        email_from = 'tutoring@svcover.nl'

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

            messages_to_send.append(message)

        self.stdout.write('Email Digest command executing...')

        with get_connection() as connection:
            connection.send_messages(messages_to_send)

        self.stdout.write('Mail sent to {} people!'.format(len(messages_to_send)))
