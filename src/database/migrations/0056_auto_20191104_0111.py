# Generated by Django 2.2.5 on 2019-11-04 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0055_auto_20191103_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingstatement',
            name='community',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.Community'),
        ),
        migrations.AlterField(
            model_name='event',
            name='community',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Community'),
        ),
    ]
