# Generated by Django 2.2.3 on 2019-07-20 10:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20190720_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
    ]
