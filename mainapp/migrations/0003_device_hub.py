# Generated by Django 3.2.6 on 2021-09-01 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20210901_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='hub',
            field=models.BooleanField(default=False),
        ),
    ]