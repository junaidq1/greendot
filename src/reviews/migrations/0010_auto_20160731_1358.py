# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-31 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_employee_service_line'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.CharField(max_length=120, null=True),
        ),
    ]