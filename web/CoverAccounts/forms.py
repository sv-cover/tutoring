from django import forms
from .models import CoverMember

class FirstUseForm(forms.Form):
    """
    Form used to confirm agreement with the terms before adding a user to the database.
    """
    user_read_disclaimer = forms.BooleanField(
        required=True,
        label='I have read and agree to the <a href="/terms_conditions">terms and conditions</a> for this website.'
    )

    class Meta:
        fields = ['user_read_disclaimer']


class SettingsForm(forms.ModelForm):
    class Meta:
        model = CoverMember
        fields = [

            # Don't let the user change those. This should be done on svcover.nl
            # 'email',
            # 'first_name',
            # 'last_name',

            'appears_anonymous',
            'receives_weekly_mails',
            'receives_daily_mails'
        ]
