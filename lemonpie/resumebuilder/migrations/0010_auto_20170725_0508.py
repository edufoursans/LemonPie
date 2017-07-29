# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 05:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resumebuilder', '0009_auto_20170725_0456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupentrylinkedlist',
            name='element',
        ),
        migrations.AddField(
            model_name='groupentrylinkedlist',
            name='cv_entry',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='cv_entry', to='resumebuilder.CVEntry'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='groupentrylinkedlist',
            name='group_entry',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='group_entry', to='resumebuilder.GroupEntry'),
            preserve_default=False,
        ),
    ]
