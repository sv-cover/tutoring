from django import forms

from tutors.models import Offer, Request

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            'offered_subjects',
            'offered_languages',
            'description',
            'is_listed',
        ]

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = [
            'subject',
            'description'
        ]
