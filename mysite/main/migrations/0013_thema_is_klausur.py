# Generated by Django 2.2.5 on 2019-11-26 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20190503_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='thema',
            name='is_klausur',
            field=models.BooleanField(default=False),
        ),
    ]
