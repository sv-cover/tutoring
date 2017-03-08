from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from CoverAccounts.models import CoverMember
from .models import Message, Conversation
from .forms import MessageForm, ConversationForm

class ConversationCreateView(CreateView):
    model = Message
    form_class = ConversationForm
    template_name = 'messages/conversation_new.html'

    def get_recipient(self):
                recipient_id = self.request.GET.get("to")
                return get_object_or_404(CoverMember, cover_id=recipient_id)

    def get_context_data(self, **kwargs):
        recipient = self.get_recipient()

        context = super(ConversationCreateView, self).get_context_data(**kwargs)
        context['recipient'] = recipient

        return context


    def form_valid(self, form):

        recipient = self.get_recipient()

        response = super(ConversationCreateView, self).form_valid(form)

        form.instance.save() #TODO: Not sure if this line is needed

        form.instance.participants.add(self.request.user)
        form.instance.participants.add(recipient)

        return response

class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'forms.html'

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.conversation = Conversation.objects.get(pk=self.kwargs['pk'])

        response = super(MessageCreateView, self).form_valid(form)

        return response

    def get_success_url(self):
        return self.object.conversation.get_absolute_url()

class ConversationListView(ListView):

    context_object_name = 'conversations'
    model = Conversation
    template_name = 'messages/conversation_list.html'

    def get_queryset(self):
        return self.model.objects.conversationsOf(self.request.user)


class ConversationDetailView(DetailView):

    context_object_name = 'conversation'
    model = Conversation
    template_name = 'messages/conversation_detail.html'

    # TODO: Make sure users cannot see other people's messages!!!

    def get_context_data(self, **kwargs):
        context = super(ConversationDetailView, self).get_context_data(**kwargs)
        context['form'] = MessageForm
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(MessageListView, self).get_context_data(**kwargs)
#
# class ContactView(FormView):
#
#     template_name = 'forms.html'
#     form_class = ContactForm
#
#     def get_initial(self):
#
#         sender = self.request.user
#
#         pk_receiver = self.kwargs.get('pk')
#         receiver = get_object_or_404(CoverMember, pk=pk_receiver)
#         #TODO: Change this to hash
#         # receiver = get_object_or_404(CoverMember, pk_hash=pk_hash_receiver)
#
#
#         return {
#             'sender_pk':sender.pk,
#             'sender':sender.full_name(),
#             'receiver_pk':receiver.pk,
#             'receiver':receiver.full_name(),
#             'subject':self.request.GET.get('subject')
#         }
#
#     def get_success_url(self):
#         return '/'
# #
#     def form_valid(self, form):
#
#         send_mail(
#             'Subject here',
#             'Here is the message.',
#             'studcee',
#             ['rafael@bankosegger.at'],
#             fail_silently=False,
#         )
#
#         return super(ContactView, self).form_valid(form)
#
# class ConversationView(ListView):
#     pass
