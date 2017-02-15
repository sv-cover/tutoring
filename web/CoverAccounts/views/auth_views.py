from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import FormView

from CoverAccounts.forms import AuthenticationForm

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
