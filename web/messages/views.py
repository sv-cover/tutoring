import requests

from django.conf import settings
from django.core.mail import send_mail
from django.http import Http404
from django.core.urlresolvers import reverse
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

        conversation = self.object.conversation
        participants = list(conversation.participants.all())
        for p in participants:
            sender = self.object.sender.full_name if p != self.request.user else 'You'
            msg = '*%s* @ %s:\n%s' % (sender, conversation.subject, self.object.message)

            if p.telegram_chat_id:
                url = 'https://api.telegram.org/bot{}/sendMessage' \
                    .format(settings.TELEGRAM_BOT_API_TOKEN)
                telegram_response = requests.get(url, params = {
                                    'text':msg,
                                    'chat_id':p.telegram_chat_id,
                                    'parse_mode':'Markdown'
                                })
                print(p, telegram_response)

        return response

    def get_success_url(self):
        return self.object.conversation.get_absolute_url()

class ConversationListView(ListView):

    context_object_name = 'conversations2'
    model = Conversation
    template_name = 'messages/conversation_list.html'

    def get_queryset(self):
        return self.model.objects.conversationsOf(self.request.user)

class ConversationDetailView(DetailView):

    context_object_name = 'conversation'
    model = Conversation
    template_name = 'messages/conversation_detail.html'

    def get(self, request, *args, **kwargs):

        response = super(ConversationDetailView, self).get(request, **kwargs)

        user_in_conversation = self.object.participants \
            .filter(cover_id=request.user.cover_id)\
            .count() > 0

        if user_in_conversation:

            # Mark all messages in conversation as read by this user
            for message in self.object.messages.all():
                message.read_by.add(request.user)

            return response

        else:

            # If a user tries to access another person's conversation, we act
            # as if the website doesn't exist.
            raise Http404('No conversation found matching the query')


    def get_context_data(self, **kwargs):
        context = super(ConversationDetailView, self).get_context_data(**kwargs)
        context['form'] = MessageForm
        return context

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
#             'testbot@bankosegger.at',
#             ['rafael@bankosegger.at'],
#             fail_silently=False,
#         )
#
#         return super(ContactView, self).form_valid(form)
#
# class ConversationView(ListView):
#     pass
