# Generated by Django 2.2.3 on 2019-07-21 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_problem_curator'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='progress',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='problem',
            name='curator',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='curatored', to=settings.AUTH_USER_MODEL),
        ),
    ]
