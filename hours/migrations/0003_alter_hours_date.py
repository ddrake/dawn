# Generated by Django 5.1 on 2024-10-05 17:13

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hours', '0002_alter_tasktranslation_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hours',
            name='date',
            field=models.DateField(default=datetime.datetime.today, help_text='The date the task was performed.', validators=[django.core.validators.MinValueValidator(datetime.date(2024, 1, 1)), django.core.validators.MaxValueValidator(datetime.date(2024, 10, 5))], verbose_name='Date'),
        ),
    ]