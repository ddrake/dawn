from datetime import datetime, date

from django.db import models
from django.db.models import Sum, Prefetch
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import (
    MinValueValidator as MinVal, MaxValueValidator as MaxVal)


class Task(models.Model):
    """
    A named task from a pre-defined list or null (unspecified).
    """
    name = models.CharField(max_length=60,
                            verbose_name=_('Task Name'),
                            help_text=_('The English name of the task'),
                            unique=True)

    @staticmethod
    def tasks_for_language(language):
        tasks = Task.objects.prefetch_related(Prefetch(
            'translations',
            queryset=TaskTranslation.objects.filter(language=language)))
        return tasks

    def __str__(self):
        # Todo: think about this.  It's currently only used for choice labels,
        # in which case, the queryset contains only records for one language.
        # In cases where queryset contains multiple translations, we simply
        # sort by language for consistency.
        # The ListView template specifies {{ task.name }}, rather than {{task}}
        # because we need to avoid calling this method in that case.
        rslt = self.translations.all().order_by('language')[0].name
        return rslt

    class Meta:
        ordering = ['name']


class TaskTranslation(models.Model):
    """
    A named task from a pre-defined list or null (unspecified).
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             verbose_name=_('Task'),
                             related_name='translations',
                             help_text=_('The task for translation'))

    name = models.CharField(max_length=60,
                            verbose_name=_('Task Name'),
                            help_text=_('The name of the task'))

    language = models.CharField(max_length=5,
                                verbose_name=_('Language'),
                                help_text=_('Task name language'))

    class Meta:
        constraints = [
            models.UniqueConstraint('name', 'language',
                                    name='name_unique_for_language'), ]
        ordering = ['name']


class Hours(models.Model):
    """
    Hours worked, typically by a volunteer.
    Each logged-in user can view, edit and delete their own records:
    date, hours worked and task for the current calendar year.
    Hours worked in a previous calendar year cannot be modified.  They
    can only be viewed in a CSV report by an admin.
    A user's last-specified task is saved in the session as their default
    to reduce data input.

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name=_('User'),
                             related_name='hours_worked',
                             help_text=_('The user who performed the task'))

    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             verbose_name=_('Task'),
                             related_name='hours_worked',
                             help_text=_('The task performed'))

    date = models.DateField(default=datetime.today,
                            validators=[MinVal(date(date.today().year, 1, 1)),
                                        MaxVal(date.today())],
                            verbose_name=_('Date'),
                            help_text=_('The date the task was performed.'))

    hours = models.FloatField(default=0, validators=[MinVal(0.25), MaxVal(24)],
                              verbose_name=_('Hours'),
                              help_text=_('The hours worked on this task/day'))

    @classmethod
    def user_hours_for_date(cls, user, date):
        hrs = Hours.objects.filter(user_id=user.pk, date=date
                                   ).aggregate(Sum('hours'))
        return 0 if hrs['hours__sum'] is None else hrs['hours__sum']

    @staticmethod
    def get_current_year():
        return datetime.now().year

    def clean(self):
        if (Hours.user_hours_for_date(self.user, self.date) + self.hours) > 24:
            raise ValidationError({'hours': _(
                "A maximum of 24 hours can be logged for a given date")},
                                  code="max_hours")

    def delete(self, **kwargs):
        if self.date.year != Hours.get_current_year():
            raise ValidationError(
                _("Only hours in the current year can be deleted"), code="current_year")
        else:
            super().delete(**kwargs)

    class Meta:
        ordering = ['-date']
