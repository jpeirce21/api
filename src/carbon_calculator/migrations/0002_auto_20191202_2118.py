# Generated by Django 2.2.5 on 2019-12-02 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carbon_calculator', '001_cc_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calcuser',
            name='cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='calcuser',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='calcuser',
            name='savings',
            field=models.IntegerField(default=0),
        ),
    ]
