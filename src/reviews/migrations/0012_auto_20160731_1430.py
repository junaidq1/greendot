# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-31 14:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0011_auto_20160731_1358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='service_Line',
            new_name='service_line',
        ),
    ]
