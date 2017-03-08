from django.conf.urls import url

from .views import *

app_name = 'messages'
urlpatterns = [
    # url(r'^(?P<pk>[a-zA-Z0-9]+)/contact$', ContactView.as_view(), name='contact'),
    # url(r'^conversation/(?P<pk>[0-9]+)$', ConversationDetailView.as_view(), name='conversation_detail'),
    url(r'^new$', ConversationCreateView.as_view(), name='conversation_create'),
    url(r'^$', ConversationListView.as_view(), name='conversation_list'),
    url(r'^(?P<pk>[0-9]+)$', ConversationDetailView.as_view(), name='conversation_detail'),
    url(r'^(?P<pk>[0-9]+)/new$', MessageCreateView.as_view(), name='message_create'),
]
