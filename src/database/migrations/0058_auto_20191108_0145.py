# Generated by Django 2.2.5 on 2019-11-08 01:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0057_auto_20191104_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date_and_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date_and_time',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='onboarding_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
