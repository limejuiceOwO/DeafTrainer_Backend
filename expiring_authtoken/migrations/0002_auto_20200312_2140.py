# Generated by Django 3.0.4 on 2020-03-12 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expiring_authtoken', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='user',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
