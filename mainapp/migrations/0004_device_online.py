# Generated by Django 3.2.6 on 2021-09-06 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_device_hub'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='online',
            field=models.BooleanField(default=False),
        ),
    ]
