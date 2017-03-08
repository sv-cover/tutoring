from django import forms

from .models import Conversation, Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            'message'
        ]


class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = [
            # 'sender',
            # 'receiver',
            'subject'
        ]

    # sender_pk = forms.IntegerField(widget=forms.HiddenInput())
    # sender = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    #
    # receiver_pk = forms.IntegerField(widget=forms.HiddenInput())
    # receiver = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
