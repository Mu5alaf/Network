# Generated by Django 4.2.5 on 2023-10-31 10:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_remove_likesmodel_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='new_post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked', to=settings.AUTH_USER_MODEL),
        ),
    ]