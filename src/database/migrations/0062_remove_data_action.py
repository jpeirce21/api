# Generated by Django 2.2.5 on 2019-11-13 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0061_data_action'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='action',
        ),
    ]
