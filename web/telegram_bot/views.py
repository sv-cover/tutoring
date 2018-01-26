import json
import requests

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

    num_updates = len(payload["result"])
    last_update = num_updates - 1
    chat_text = payload["result"][last_update]["message"]["text"]
    chat_id = payload["result"][last_update]["message"]["chat"]["id"]

    url = 'https://api.telegram.org/bot{}sendMessage' \
        .format(settings.TELEGRAM_BOT_API_TOKEN)
    response = requests.get(url, params={'text':chat_text, 'chat_id':chat_id})

    return HttpResponse(status=200)
