from datetime import datetime

from django.shortcuts import redirect
from django.views import View
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from .models import Hours
from .forms import HoursCreateForm, HoursUpdateForm


class SetLangView(View):
    def post(self, request, *args, **kwargs):
        lang = request.POST.get('lang', 'en-us')
        request.session['django_language'] = lang
        return redirect(reverse('hours_list'))


class HoursIndexView(LoginRequiredMixin, ListView):
    template_name = 'hours/list.html'

    def get_queryset(self):
        # TODO: try to handle this in a cleaner way using nested Prefetch
        language = self.request.session.get('django_language', 'en-us')
        hours = Hours.objects.filter(
            user_id=self.request.user.pk, date__year=datetime.now().year)
        for h in hours:
            h.task.name = h.task.translations.filter(
                language=language)[0].name
        return hours


# Note: I don't think we need a detail view in this case.  Just link from the listview.
# Note: we can use extracontext to get args into the form
class HoursCreateView(LoginRequiredMixin, CreateView):
    model = Hours
    form_class = HoursCreateForm
    template_name = 'hours/form.html'
    success_url = reverse_lazy('hours_list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'language':
                       self.request.session.get('django_language', 'en-us')})
        return kwargs

    def get_initial(self):
        return {
            'user': self.request.user,
            'hours': 1
        }


class HoursUpdateView(UserPassesTestMixin, UpdateView):
    model = Hours
    form_class = HoursUpdateForm
    template_name = 'hours/form.html'
    success_url = reverse_lazy('hours_list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'language':
                       self.request.session.get('django_language', 'en-us')})
        return kwargs


class HoursDeleteView(UserPassesTestMixin, DeleteView):
    model = Hours
    success_url = reverse_lazy('hours_list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user
