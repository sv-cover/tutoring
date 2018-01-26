from django.conf.urls import url

from . import views

app_name = 'telegram_bot'
urlpatterns = [
    url(r'^secreturl$', views.webhook, name='webhook'),
]
