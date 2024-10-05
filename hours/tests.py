from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from hours.models import Hours, Task
from hours.scripts import add_tasks


class HoursTestCase(TestCase):
    def setUp(self):
        add_tasks.create_tasks()
        self.donations = Task.objects.get(name='donations procurement')
        self.joe = User.objects.create(username='joe124', password='verrysekrit')
        self.today = date(2024, 9, 25)

    def test_creating_hours(self):
        Hours.objects.create(user=self.joe, date=self.today,
                             task=self.donations, hours=12)
        self.assertEqual(Hours.objects.count(), 1)
        more = Hours(user=self.joe, date=self.today, task=self.donations, hours=13)
        self.assertRaises(ValidationError, more.clean)

    def test_bad_date(self):
        # date must be in the current year
        hours = Hours(user=self.joe, date=date(2023, 9, 25),
                      task=self.donations, hours=8)
        self.assertRaises(ValidationError, hours.clean_fields)
