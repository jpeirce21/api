# Generated by Django 2.2.3 on 2019-07-22 21:01

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_auto_20190719_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='more_info',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
