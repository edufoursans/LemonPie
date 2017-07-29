# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 04:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resumebuilder', '0006_groupentrylinkedlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cventrygroupentrypairing',
            name='cv_entry',
        ),
        migrations.RemoveField(
            model_name='cventrygroupentrypairing',
            name='group_entry',
        ),
        migrations.AlterField(
            model_name='groupentrylinkedlist',
            name='predecessor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='predecessor01', to='resumebuilder.GroupEntryLinkedList'),
        ),
        migrations.AlterField(
            model_name='groupentrylinkedlist',
            name='successor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='successor01', to='resumebuilder.GroupEntryLinkedList'),
        ),
        migrations.DeleteModel(
            name='CVEntryGroupEntryPairing',
        ),
    ]
