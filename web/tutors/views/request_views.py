from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from tutors.models import Subject, Request
from tutors.forms import RequestForm

class RequestListView(ListView):
    ''' ''' #TODO
    template_name = 'tutors/request_list.html'

    def get_queryset(self):
        subjects = list(Subject.objects.all())
        requests_per_subject = []
        for subject in subjects:
            requests = list(Request.objects.filter(subject=subject))
            if len(requests) > 0:
                requests_per_subject += [{'subject':subject, 'requests':requests}]

        # Order in such a way that the user's tutoring requests always are on top.
        requests_per_subject.sort(key = lambda x:
            not any([r.owner == self.request.user for r in x['requests']]))

        # own_requests = list(Request.objects.filter(owner=self.request.user))
        # other_requests = list(Request.objects.exclude(owner=self.request.user))

        return requests_per_subject

class RequestCreateView(CreateView):
    model = Request
    form_class = RequestForm
    template_name = 'tutors/request_create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(RequestCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('tutors:request_list')

class RequestUpdateView(UpdateView):
    ''' ''' #TODO

    model = Request
    form_class = RequestForm
    template_name = 'tutors/request_update.html'
    context_object_name = 'tutoring_request'

    def get_object(self, queryset=None):
        tutoring_request_pk = self.kwargs.get('pk')
        tutoring_request = get_object_or_404(Request, pk=tutoring_request_pk)

        # Prohibit user from editing requests from other people
        if(tutoring_request.owner != self.request.user):
            raise Http404

        return tutoring_request

    def get_success_url(self):
        return reverse('tutors:request_list')

class RequestDeleteView(DeleteView):
    model = Request

    template_name = 'tutors/request_confirm_delete.html'
    context_object_name = 'tutoring_request'

    def get_object(self, queryset=None):
        tutoring_request_pk = self.kwargs.get('pk')
        tutoring_request = get_object_or_404(Request, pk=tutoring_request_pk)

        # Prohibit user from editing requests from other people
        if(tutoring_request.owner != self.request.user):
            raise Http404

        return tutoring_request

    def get_success_url(self):
        return reverse('tutors:request_list')
