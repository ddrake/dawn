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
        print(f"{lang=}")
        request.session['django_language'] = lang
        return redirect(reverse('hours_list'))


class HoursIndexView(LoginRequiredMixin, ListView):
    template_name = 'hours/list.html'

    def get_queryset(self):
        language = self.request.session.get('django_language', 'en-us')
        print(f"{language=}")
        hours = Hours.objects.select_related().filter(
            user_id=self.request.user.pk, date__year=datetime.now().year)
        for h in hours:
            print(f"{h=}")
            print(f"{h.task_id=}")
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

    def get(self, request, *args, **kwargs):
        self.extra_context = {'language': request.session.get('language', 'en-us')}
        print(f"{self.extra_context=}")
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        if self.extra_context:
            return {
                'language': self.extra_context['language'],
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


class HoursDeleteView(UserPassesTestMixin, DeleteView):
    model = Hours
    # form_class = HoursDeleteForm
    success_url = reverse_lazy('hours_list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = context['view'].request.user
    #     hasfarmyears = has_farm_years(user)
    #     context['has_farm_years'] = hasfarmyears
    #     return context
