from django.core.management.base import BaseCommand
from datetime import datetime
from django.utils import timezone
from django.conf import settings


from coverapi import CoverAPI, APIError

from CoverAccounts.models import CoverMember

class Command(BaseCommand):
    help = 'Updates member information in the database from the Cover server.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write('{} - Start executing Update Members command.\nMake updates to the following users:'.format(datetime.now(timezone.utc)))
        cover_api = CoverAPI(settings.COVER_API_URL, settings.COVER_API_APP, settings.COVER_API_SECRET)
        for user in CoverMember.objects.all():
            request = cover_api.request_json({'method':'secretary_read_member'}, data={'member_id': user.cover_id})
            user.update_member(request['result'])
            self.stdout.write(' - {}'.format(user))

        self.stdout.write('Done updating members')

