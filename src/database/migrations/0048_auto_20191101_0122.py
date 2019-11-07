# Generated by Django 2.2.5 on 2019-11-01 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0047_auto_20191028_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='owner_email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='email',
            field=models.EmailField(blank=True, db_index=True, max_length=254, null=True),
        ),
    ]