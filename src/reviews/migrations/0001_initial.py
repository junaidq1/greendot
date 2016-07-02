# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-26 05:01
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('email', models.CharField(max_length=120)),
                ('level', models.CharField(max_length=120)),
                ('service_area', models.CharField(max_length=120)),
                ('office', models.CharField(max_length=120)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length_working', models.PositiveIntegerField(verbose_name='how long have you worked with this person? (months)?')),
                ('ques1', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='How much did you enjoy working with this person? (5 = most)?')),
                ('ques2', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='How much did you learn from this individual while working with them? (5 = most)')),
                ('ques3', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='How competent is this person in their area? (5 = most)')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('work_again', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=1, verbose_name='would you work with this person again if you had the choice?')),
                ('content', models.TextField(blank=True, max_length=1200, verbose_name='Please provide some comments on what it was like to work with this person')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Employee')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_contributor', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upvotes', models.NullBooleanField()),
                ('downvotes', models.NullBooleanField()),
                ('v_timestamp', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employeevoted', to='reviews.Employee')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votereview', to='reviews.Review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('review', 'employee', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([('user', 'employee')]),
        ),
    ]
