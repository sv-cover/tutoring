from django import forms
from .models import CoverMember

class AuthenticationForm(forms.Form):
    """
    Login form
    """
    email = forms.EmailField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)
    special = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ['email', 'password', 'special']

class SettingsForm(forms.ModelForm):
    class Meta:
        model = CoverMember
        fields = [
            # 'email',
            'first_name',
            'last_name',
            'appears_anonymous',
            'receives_mail_notification'
        ]
