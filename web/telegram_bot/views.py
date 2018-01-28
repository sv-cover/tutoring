import json
import requests
import re

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


from CoverAccounts.models import CoverMember

@csrf_exempt
@require_POST
def webhook(request):

    payload = json.loads(request.body.decode('utf-8'))
    chat_text = payload["message"]["text"]
    chat_id = payload["message"]["chat"]["id"]
    chat_reply = payload['message'].get('reply_to_message', None)


    # answer = 'Sorry, I don\'t know what you want from me. If you want to reply to someone\'s message, please use telegram\'s "reply" feature to do so.'

    answer = ''

    start_command = re.search('/start (.*)', chat_text)
    if start_command:
        chat_token = start_command.group(1)

        user = CoverMember.objects.get(telegram_bot_token=chat_token)
        user.telegram_chat_id = chat_id
        user.save()

        answer = 'Hoot hoot, %s! I am CACTuS Messenger. My job is to keep you up to date with all messages you receive in the tutoring system.\nIt\'s all set up! Just leave me doing my job in the background and  I\'ll let you know when the next message drops in.' % (user.first_name)

    elif chat_reply:
        pass

    url = 'https://api.telegram.org/bot{}/sendMessage' \
        .format(settings.TELEGRAM_BOT_API_TOKEN)
    response = requests.get(url, params={'text':chat_text, 'chat_id':chat_id})

    return HttpResponse(status=200)
