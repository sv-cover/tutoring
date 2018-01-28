from django.conf.urls import url
from django.conf import settings

from . import views


app_name = 'telegram_bot'
urlpatterns = [
    url(r'^bot%s' % settings.TELEGRAM_BOT_API_TOKEN, views.webhook, name='webhook'),
]
