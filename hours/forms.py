from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field, Layout, Fieldset

from .models import Task, Hours

# Note: to get initial data into a form, use extra_context in the view
# it will end up in kwargs


class HoursForm(ModelForm):
    def __init__(self, *args, **kwargs):
        lang = kwargs.pop('language')
        super().__init__(*args, **kwargs)
        # if lang is not None:
        tasks = Task.tasks_for_language(lang)
        self.fields['task'].queryset = tasks
        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": ''}
        self.helper.form_id = 'hoursform'
        self.helper.layout = Layout(
            Fieldset('Volunteer Hours',
                     'date', 'task', 'hours',
                     Field('user', type='hidden'),
                     )
        )

    def task_choices(self):
        return Task.tasks_for_language(self.lang)

    class Meta:
        model = Hours
        fields = '''date task hours user'''.split()
        widgets = {
            'hours': forms.NumberInput(
                attrs={'step': 0.25, 'min': 0.25, 'max': 24}),
            'date': forms.DateInput(attrs={"type": "date"}),
        }


class HoursCreateForm(HoursForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', _('Create')))


class HoursUpdateForm(HoursForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', _('Update')))


# TODO: try this, so we can raise a ValidationError if the year doesn't match
class HoursDeleteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', _('Delete')))
