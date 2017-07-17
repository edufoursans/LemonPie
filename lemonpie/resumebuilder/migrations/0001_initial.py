# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 05:27
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CVEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CVEntryGroupEntryPairing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CVGeneral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('nb_columns', models.PositiveIntegerField(choices=[(1, 1), (2, 2)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CVGeneralGroupEntryPairing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cv_general', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumebuilder.CVGeneral')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityEntry',
            fields=[
                ('cventry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resumebuilder.CVEntry')),
                ('location_city', models.CharField(blank=True, max_length=50)),
                ('location_country', models.CharField(blank=True, max_length=50)),
                ('date_begin', models.DateField(blank=True)),
                ('date_end', models.DateField(blank=True, default=datetime.date.today)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('resumebuilder.cventry',),
        ),
        migrations.CreateModel(
            name='GroupEntry',
            fields=[
                ('cventry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resumebuilder.CVEntry')),
            ],
            options={
                'abstract': False,
            },
            bases=('resumebuilder.cventry',),
        ),
        migrations.CreateModel(
            name='PersonalEntry',
            fields=[
                ('cventry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resumebuilder.CVEntry')),
                ('family_name', models.CharField(max_length=50)),
                ('given_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
                ('email_address', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
            bases=('resumebuilder.cventry',),
        ),
        migrations.CreateModel(
            name='SkillEntry',
            fields=[
                ('cventry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resumebuilder.CVEntry')),
                ('skill_name', models.CharField(max_length=50)),
                ('skill_level', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
            ],
            options={
                'abstract': False,
            },
            bases=('resumebuilder.cventry',),
        ),
        migrations.AddField(
            model_name='cventrygroupentrypairing',
            name='cv_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CVEntry', to='resumebuilder.CVEntry'),
        ),
        migrations.AddField(
            model_name='cventry',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_resumebuilder.cventry_set+', to='contenttypes.ContentType'),
        ),
        migrations.CreateModel(
            name='EducationEntry',
            fields=[
                ('activityentry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resumebuilder.ActivityEntry')),
                ('diploma_title', models.CharField(max_length=50)),
                ('school_name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('resumebuilder.activityentry',),
        ),
        migrations.CreateModel(
            name='HobbyEntry',
            fields=[
                ('activityentry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resumebuilder.ActivityEntry')),
                ('hobby_name', models.CharField(max_length=50)),
                ('hobby_institution', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('resumebuilder.activityentry',),
        ),
        migrations.CreateModel(
            name='WorkEntry',
            fields=[
                ('activityentry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resumebuilder.ActivityEntry')),
                ('job_title', models.CharField(max_length=50)),
                ('company_name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('resumebuilder.activityentry',),
        ),
        migrations.AddField(
            model_name='cvgeneralgroupentrypairing',
            name='group_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumebuilder.GroupEntry'),
        ),
        migrations.AddField(
            model_name='cventrygroupentrypairing',
            name='group_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='GroupEntry', to='resumebuilder.GroupEntry'),
        ),
    ]
