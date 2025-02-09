from datetime import datetime
import csv
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from django.contrib.auth.models import User
from django.conf import settings
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

    def get_context_data(self, **kwargs):
        user_id = self.request.user.pk
        dl, dv, wl, wv = Hours.get_graph_data(user_id)
        context = super().get_context_data(**kwargs)
        context['dl'] = json.dumps(dl)
        context['dv'] = json.dumps(dv)
        context['wl'] = json.dumps(wl)
        context['wv'] = json.dumps(wv)
        return context

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


class AllHoursCSVDownloadView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition':
                     'attachment; filename="AllHours.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow(['Task', 'User', 'U.S. Citizen/Green Card?', 'Date', 'Hours',
                         'Comment'])
        for hrs in Hours.objects.order_by('task', 'user', 'date'):
            writer.writerow(
                [hrs.task, f"{hrs.user.first_name} {hrs.user.last_name}",
                 hrs.user.profile.us_citizen, hrs.date, hrs.hours, hrs.comment]
            )
        return response

class AllHoursCSVView(View):
    def get(self, request, *args, **kwargs):
        key = getattr(settings, 'HOURS_TABLE_KEY')
        if 'k' in request.GET and request.GET.get('k') == key:
            response = HttpResponse(
                content_type='text/csv',
                headers={'Content-Disposition': 'inline'},
            )
            writer = csv.writer(response)
            writer.writerow(['Task', 'UserID', 'Date', 'Hours'])
            for hrs in Hours.objects.order_by('task', 'user', 'date'):
                writer.writerow(
                    [hrs.task, hrs.user.id, hrs.date, hrs.hours]
                )
        else:
            response = redirect(reverse('login'))
        return response

def send_user_instructions(request, user_id):
    success = False
    try:
        user = User.objects.get(pk=user_id)
        from hours.scripts.email_preset_users import send_single_email
        send_single_email(user) 
        profile = user.profile
        profile.help_emailed = 'Y'
        profile.save()
        success = True
    except Exception:
        pass

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            return JsonResponse({'result': success})
        else:
            return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        response_text = (f"{user.first_name} was sent the instructions!" if success
                     else "Something went wrong.  The user was not notified!")
        return HttpResponse(response_text)

