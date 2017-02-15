from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.views.generic import FormView
from django.views.generic.list import ListView

from CoverAccounts.forms import ContactForm
from CoverAccounts.models import CoverMember

class ContactView(FormView):

    template_name = 'forms.html'
    form_class = ContactForm

    def get_initial(self):

        sender = self.request.user

        receiver_pk = self.kwargs.get('pk')
        receiver = get_object_or_404(CoverMember, pk=receiver_pk)


        return {
            'sender_pk':sender.pk,
            'sender':sender.full_name(),
            'receiver_pk':receiver.pk,
            'receiver':receiver.full_name(),
            'subject':self.request.GET.get('subject')
        }

    def get_success_url(self):
        return '/'
#
    def form_valid(self, form):

        send_mail(
            'Subject here',
            'Here is the message.',
            'testbot@bankosegger.at',
            ['rafael@bankosegger.at'],
            fail_silently=False,
        )

        return super(ContactView, self).form_valid(form)

class ConversationView(ListView):
    pass
