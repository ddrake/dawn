from datetime import datetime
import csv

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from django.contrib.auth.models import User
from .models import Hours, Language
from .forms import HoursCreateForm, HoursUpdateForm, ProfileUpdateForm


class SetLangView(View):
    def post(self, request, *args, **kwargs):
        lang = request.POST.get('lang', 'en-us')
        response = redirect(reverse('hours_list'))
        response.set_cookie('django_language', lang)
        return response


class HoursIndexView(LoginRequiredMixin, ListView):
    template_name = 'hours/list.html'

    def get_queryset(self):
        language_id = Language.objects.get(
            name=self.request.COOKIES.get('django_language', 'en-us')).pk
        return Hours.hours_with_translated_task_name(
            self.request.user.pk, language_id, datetime.now().year)


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
                       self.request.COOKIES.get('django_language', 'en-us')})
        return kwargs

    def get_initial(self):
        print(f"In get_initial: {self.request.session.get('last_task', '')=}")
        return {
            'user': self.request.user,
            'hours': 1,
            'task': self.request.session.get('last_task', ''),
        }

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            request.session['last_task'] = form.instance.task_id
        return super().post(request, *args, **kwargs)


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
                       self.request.COOKIES.get('django_language', 'en-us')})
        return kwargs


class HoursDeleteView(UserPassesTestMixin, DeleteView):
    model = Hours
    success_url = reverse_lazy('hours_list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user


class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'hours/profile_form.html'
    success_url = reverse_lazy('hours_list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user


class AllHoursCSVView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition':
                     'attachment; filename="AllHours.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow(['Task', 'User', 'U.S. Citizen?', 'Date', 'Hours'])
        for hrs in Hours.objects.order_by('task', 'user', 'date'):
            if not hrs.user.is_superuser:
                writer.writerow(
                    [hrs.task, f"{hrs.user.first_name} {hrs.user.last_name}",
                     hrs.user.profile.us_citizen, hrs.date, hrs.hours]
                )
        return response
