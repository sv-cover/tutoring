from django.db.models import Q
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView

from tutors.models import Offer
from tutors.forms import OfferForm


class OfferListView(ListView):
    ''' ''' #TODO

    context_object_name = 'offer_list'
    model = Offer
    template_name = 'tutors/offer_list.html'

    def get_context_data(self, **kwargs):
        context = super(OfferListView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q:
            context['q'] = q
        return context

    def get_queryset(self):
        q = self.request.GET.get('q')

        if q:
            return Offer.objects.filter(offered_subjects__name__icontains=q)

        else:
            own_offers = list(Offer.objects.filter(owner=self.request.user))
            other_offers = list(Offer.objects.exclude(owner=self.request.user))

            return own_offers + other_offers

class OfferCreateView(CreateView):
    model = Offer
    form_class = OfferForm
    template_name = 'forms.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OfferCreateView, self).form_valid(form)

class OfferUpdateView(UpdateView):
    model = Offer
    form_class = OfferForm
    template_name = 'tutors/offer_update.html'

    def get_object(self):
            return Offer.objects.get(owner = self.request.user)

class OfferDeleteView(DeleteView):
    model = Offer

    template_name = 'tutors/offer_confirm_delete.html'
    success_url = '/'

    def get_object(self):
            return Offer.objects.get(owner = self.request.user)
