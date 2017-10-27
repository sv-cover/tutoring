from django import forms
from .models import CoverMember

class AuthenticationForm(forms.Form):
    """
    Login form
    """
    email = forms.EmailField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)
    special = forms.CharField(widget=forms.widgets.PasswordInput)
    user_read_disclaimer = forms.BooleanField(required=True, \
        label='I have read and agree to the <a href="/terms_conditions">terms and conditions</a> for this website.')

    class Meta:
        fields = ['email', 'password', 'special', 'user_read_disclaimer']

class SettingsForm(forms.ModelForm):
    class Meta:
        model = CoverMember
        fields = [

            # Don't let the user change those. This should be done on svcover.nl
            # 'email',
            # 'first_name',
            # 'last_name',

            'appears_anonymous',
            # 'receives_mail_notification'
        ]
