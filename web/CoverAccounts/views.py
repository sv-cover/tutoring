from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from CoverAccounts.models import *
from CoverAccounts.forms import *


class LoginView(TemplateView):
    template_name = 'CoverAccounts/login.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous and not request.user.is_unknown:
            return redirect('tutors:offer_list')
        elif not request.user.is_anonymous:
            return redirect('CoverAccounts:first_use')
        return super(LoginView, self).get(request, *args, **kwargs)


class FirstUseView(FormView):
    """
    First use view
    """

    template_name = 'CoverAccounts/first_use.html'
    form_class = FirstUseForm

    def form_valid(self, form):
        cover_member = self.request.user.as_cover_member()
        cover_member.save()
        login(self.request, cover_member)
        return redirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous and not request.user.is_unknown:
            return redirect('tutors:offer_list')
        return super(FirstUseView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return '/'



class SettingsView(UpdateView):
    template_name = 'CoverAccounts/settings.html'
    form_class = SettingsForm
    model = CoverMember

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return '/accounts/settings'
