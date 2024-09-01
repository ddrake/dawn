from datetime import datetime, date

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MinValueValidator as MinVal, MaxValueValidator as MaxVal)


class Task(models.Model):
    """
    A named task from a pre-defined list or null (unspecified).
    """
    task_name = models.CharField(max_length=60,
                                 verbose_name=_('Task Name'),
                                 help_text=_('The name of the task'))


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

    task = models.ForeignKey(Task, on_delete=models.SET_NULL,
                             null=True, blank=True,
                             verbose_name=_('Task'),
                             related_name='hours_worked',
                             help_text=_('The task performed')),

    date = models.DateField(default=datetime.today,
                            validators=[MinVal(date(datetime.today().year, 1, 1)),
                                        MaxVal(date(datetime.today().year, 12, 31))],
                            verbose_name=_('Date'),
                            help_text=_('The date the task was performed.'))

    hours = models.FloatField(default=0, validators=[MinVal(0), MaxVal(24)],
                              verbose_name=_('Hours'),
                              help_text=_('The hours worked on this task/day'))
