# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-29 17:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wishlist',
            unique_together=set([('feature', 'user')]),
        ),
    ]