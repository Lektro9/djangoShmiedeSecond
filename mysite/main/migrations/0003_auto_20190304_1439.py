# Generated by Django 2.1.7 on 2019-03-04 14:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190304_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thema',
            name='datum',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 4, 14, 39, 9, 882324, tzinfo=utc), verbose_name='Erstelldatum'),
        ),
    ]
