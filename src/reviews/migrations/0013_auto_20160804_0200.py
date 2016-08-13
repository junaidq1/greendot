# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-04 02:00
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0012_auto_20160731_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='ques1',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='How nice is this person in their professional interactions (1-5)? (5 = most)?'),
        ),
    ]