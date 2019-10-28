# Generated by Django 2.2.5 on 2019-10-20 14:48

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0043_auto_20191020_0406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='key_contact',
        ),
        migrations.AddField(
            model_name='vendor',
            name='location',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='service_area_states',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='properties_serviced',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='service_area',
            field=models.CharField(max_length=15),
        ),
    ]