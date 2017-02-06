from django import forms

from tutors.models import Offer, Request

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            'offered_subjects',
            'offered_languages',
            'description',
            'is_anonymous',
        ]

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = [
            'subject',
            'is_anonymous',
            'description'
        ]
