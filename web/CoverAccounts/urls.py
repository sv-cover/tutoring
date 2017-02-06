from django.conf.urls import url

from .views import LoginView, logoutView, ContactView

app_name = 'CoverAccounts'
urlpatterns = [
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', logoutView, name='logout'),
    # url(r'^/contact$', ContactView.as_view(), name='contact'),
    url(r'^(?P<pk>[0-9]+)/contact$', ContactView.as_view(), name='contact'),
]
