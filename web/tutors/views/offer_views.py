from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic import CreateView, UpdateView, DeleteView

from CoverAccounts.forms import SettingsForm

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
            q = q.lower()
            fun = lambda x: any(q in s.name.lower() for s in x.offered_subjects.all())
            return filter(fun, list(Offer.objects.all()))

        else:
            own_offers = list(Offer.objects.filter(owner=self.request.user))
            other_offers = list(Offer.objects.exclude(owner=self.request.user))

            return own_offers + other_offers

class OfferCreateView(CreateView):
    model = Offer
    form_class = OfferForm
    template_name = 'tutors/offer_create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OfferCreateView, self).form_valid(form)

class OfferUpdateView(FormView):

    # This class thinks it's just an offer form view, and creates an offer view which is not used
    # TODO: There probabaly is a better way.
    form_class = OfferForm

    template_name = 'tutors/offer_update.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        offer_form = OfferForm(instance = Offer.objects.get(owner=request.user))
        offer_form.prefix = 'offer_form'

        settings_form = SettingsForm(instance = request.user)
        settings_form.prefix = 'settings_form'

        return self.render_to_response(self.get_context_data(offer_form=offer_form, form=settings_form))

    def post(self, request, *args, **kwargs):
        offer_form = OfferForm(request.POST, prefix='offer_form', instance=Offer.objects.get(owner=request.user))
        settings_form = SettingsForm(request.POST, prefix='settings_form', instance=request.user)

        if offer_form.is_valid() and settings_form.is_valid():
            offer = offer_form.save()
            cover_member = settings_form.save()

            return HttpResponseRedirect(self.success_url)
        else:
            offer_form.prefix = 'offer_form'
            settings_form.prefix = 'settings_form'
            return self.render_to_response(self.get_context_data(offer_form=offer_form, settings_form=settings_form))

class OfferDeleteView(DeleteView):
    model = Offer

    template_name = 'tutors/offer_confirm_delete.html'
    success_url = '/'

    def get_object(self):
            return Offer.objects.get(owner = self.request.user)
