from django.conf.urls import url

from .views import *

app_name = 'CoverAccounts'
urlpatterns = [
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^first_use$', FirstUseView.as_view(), name='first_use'),
    url(r'^settings$', SettingsView.as_view(), name='settings'),
]
