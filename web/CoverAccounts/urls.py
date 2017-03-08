from django.conf.urls import url

from .views import *

app_name = 'CoverAccounts'
urlpatterns = [
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', logoutView, name='logout'),
]
