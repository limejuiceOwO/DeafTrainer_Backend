# Generated by Django 3.0.4 on 2020-03-12 15:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('expiring_authtoken', '0002_auto_20200312_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='created_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
