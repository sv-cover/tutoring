from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.views.generic import FormView

from CoverAccounts.forms import AuthenticationForm, ContactForm
from CoverAccounts.models import CoverMember

class LoginView(FormView):
    """
    Log in view
    """

    template_name = 'CoverAccounts/login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        user = authenticate(email=self.request.POST['email'], password=self.request.POST['password'])
        # print("::: %s" % user)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect(self.get_success_url())
            else:
                return render(request, 'CoverAccounts/account_disabled.html')
        else:
            # TODO
            return redirect(self.get_success_url())

        return redirect(self.get_success_url())

def logoutView(request):
    """
    Log out view
    """
    logout(request)
    return redirect('/accounts/login')

class ContactView(FormView):

    template_name = 'forms.html'
    form_class = ContactForm

    def get_initial(self):

        sender = self.request.user

        receiver_pk = self.kwargs.get('pk')
        receiver = get_object_or_404(CoverMember, pk=receiver_pk)

        return {
            'sender_pk':sender.pk,
            'sender':sender.full_name(),
            'receiver_pk':receiver.pk,
            'receiver':receiver.full_name(),
            'subject':self.request.GET.get('subject')
        }

    # def get_success_url(self):
    #     return '/'
#
#     def form_valid(self, form):
#         return super(BecomeTutorView, self).form_valid(form)
