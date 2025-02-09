from datetime import datetime, date, timedelta

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models, connection
from django.db.models import Sum, Prefetch
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import (
    MinValueValidator as MinVal, MaxValueValidator as MaxVal)
from django.urls import reverse
from django.utils.html import format_html


class Language(models.Model):
    """
    A supported language
    """
    name = models.CharField(max_length=5,
                            verbose_name=_('Language'),
                            unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_('User'),
        related_name='profile')

    us_citizen = models.BooleanField(
        default=False,
        help_text=_('Check this box if you are a U.S Citizen or have a Green Card'))

    help_emailed = models.CharField(
        max_length=1, default='N',
        help_text=_('Was the instructional email sent to this user?'))

    def username(self):
        return self.user.username

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    def is_staff(self):
        return self.user.is_staff

    def user_instructions_email(self):
        url = reverse('send_user_instructions', args=[self.user.pk])
        return format_html('<a href="{}">Send Email</a>', url)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Task(models.Model):
    """
    A named task from a pre-defined list or null (unspecified).
    """
    name = models.CharField(
        max_length=60,
        verbose_name=_('Task Name'),
        help_text=_('The English name of the task'),
        unique=True)

    @staticmethod
    def tasks_for_language(language):
        lang = Language.objects.get(name=language)
        tasks = Task.objects.prefetch_related(Prefetch(
            'translations',
            queryset=TaskTranslation.objects.filter(language=lang)))
        return tasks

    def __str__(self):
        # Todo: think about this.  It's currently only used for choice labels,
        # in which case, the queryset contains only records for one language.
        # In cases where queryset contains multiple translations, we simply
        # sort by language for consistency.
        # The ListView template specifies {{ task.name }}, rather than {{task}}
        # because we need to avoid calling this method in that case.
        rslt = self.translations.all().order_by('language')
        return rslt[0].name if rslt.count() > 0 else self.name

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

    language = models.ForeignKey(Language, on_delete=models.CASCADE,
                                 verbose_name=_('Language'),
                                 help_text=_('Task name language'))

    def __str__(self):
        return f"{self.name} ({self.language})"

    class Meta:
        constraints = [
            models.UniqueConstraint('name', 'language',
                                    name='name_unique_for_language'), ]
        ordering = ['name']


# helper for validation
def first_of_year():
    return date(datetime.now().year, 1, 1)


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
                            validators=[MinVal(first_of_year),
                                        MaxVal(date.today)],
                            verbose_name=_('Date'),
                            help_text=_('The date the task was performed.'))

    hours = models.FloatField(default=0, validators=[MinVal(0.25), MaxVal(24)],
                              verbose_name=_('Hours'),
                              help_text=_('The hours worked on this task/day'))

    comment = models.TextField(verbose_name=_('Comment'), null=True, blank=True)

    @classmethod
    def user_hours_for_date(cls, user, date):
        hrs = Hours.objects.filter(user_id=user.pk, date=date
                                   ).aggregate(Sum('hours'))
        return 0 if hrs['hours__sum'] is None else hrs['hours__sum']

    @staticmethod
    def get_current_year():
        return datetime.now().year

    @staticmethod
    def hours_with_translated_task_name(user_id, language_id, year):
        return Hours.objects.raw(
            """select h.id, h.user_id, h.date,
            h.hours, tr.language_id, tr.name task_name
            from hours_hours h join hours_task t
            on h.task_id = t.id join hours_tasktranslation tr
            on t.id = tr.task_id
            where h.user_id = %s and tr.language_id = %s
            and Extract(YEAR FROM date)=%s
            order by h.date desc;
            """, [user_id, language_id, year])

    @staticmethod
    def get_graph_data(user_id):
        """
        Returns two dicts, one with data for the daily graph,
        the other for the weekly graph, keys are strings (labels)
        values are floats (total hours)
        """
        npts = 8 # graph points
        diw = 7 # days in week
        d = timedelta(days=1)
        td = datetime.now().date()
        # normal calendar weeks start on sunday. map it to 0
        tdwkday = td.weekday() + 1 if td.weekday() < 6 else 0
        prev_sun = td - d * tdwkday
        start_date = prev_sun - diw * d * (npts - 1)
    
        # first construct the unsorted dict paird
        pairs = Hours.daily_hours_for_user_start_to_today(user_id, start_date)
        paird = {p[0]: p[1] for p in pairs}
        day = start_date
        # populate the dict with all the days from start_date thru today
        while day <= td:
            if day not in paird:
                paird[day] = 0
            day += d

        # now generate the graph data
        dates = sorted(list(paird.keys()))
        daily = {k.strftime('%-m/%-d'): paird[k]
                 for k in dates[-npts:]}
        weekly = {}
        for i in range(npts):
            subdates = dates[diw*i:diw*(i+1)]
            key = subdates[0].strftime('%-m/%-d')
            weekly[key] = sum([paird[d] for d in subdates])
        return (list(daily.keys()), list(daily.values()),
                list(weekly.keys()), list(weekly.values()))


    @staticmethod
    def daily_hours_for_user_start_to_today(user_id, start_date):
        """
        Returns a list of (date, hours) pairs, one for each day in the range
        start_date thru today with hours recorded by the given user,
        such that hours is the total hours worked by the user that day.
        """
        sql = """SELECT date, sum(hours) FROM public.hours_hours
                 WHERE user_id = %s AND date >= %s
                 GROUP BY date ORDER BY date;"""
        with connection.cursor() as cursor:
            cursor.execute(sql, [user_id, start_date])
            return cursor.fetchall()

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
