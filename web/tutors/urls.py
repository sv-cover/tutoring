from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic import RedirectView

from .views import OfferListView, OfferCreateView, OfferUpdateView, OfferDeleteView, RequestListView, RequestCreateView, RequestUpdateView, RequestDeleteView

app_name = 'tutors'
urlpatterns = [

    url(r'^requests$', RequestListView.as_view(), name='request_list'),
    url(r'^requests/new$', RequestCreateView.as_view(), name='request_create'),
    url(r'^requests/(?P<pk>[0-9]+)/edit$', RequestUpdateView.as_view(), name='request_update'),
    url(r'^requests/(?P<pk>[0-9]+)/delete$', RequestDeleteView.as_view(), name='request_delete'),

    url(r'^tutors$', OfferListView.as_view(), name='offer_list'),
    url(r'^tutors/new$', OfferCreateView.as_view(), name='offer_create'),
    url(r'^tutors/edit$', OfferUpdateView.as_view(), name='offer_update'),
    # url(r'^tutors/hide$', OfferUpdateView.as_view(), name='offer_hide'),
    url(r'^tutors/delete$', OfferDeleteView.as_view(), name='offer_delete'),


    url(r'^offers', RedirectView.as_view(url='tutors')),
    url(r'^$', RedirectView.as_view(url='tutors')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
