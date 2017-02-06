from django import forms
from .models import CoverMember

class AuthenticationForm(forms.Form):
    """
    Login form
    """
    email = forms.EmailField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ['email', 'password']

class ContactForm(forms.Form):
    '''
        Form for sending a mail to a tutor.
    '''

    # def __init__(self, *args, **kwargs):
    #     super(ContactForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.pk:
    #         self.fields('sender').widget.attrs['readonly'] = True

    sender_pk = forms.IntegerField(widget=forms.HiddenInput())
    sender = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    receiver_pk = forms.IntegerField(widget=forms.HiddenInput())
    receiver = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    subject = forms.CharField()

    message = forms.CharField(widget=forms.Textarea)
