# Generated by Django 2.2.5 on 2019-09-30 11:50

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carbon_calculator', '0006_auto_20190928_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='stations',
        ),
        migrations.AddField(
            model_name='event',
            name='stationslist',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]