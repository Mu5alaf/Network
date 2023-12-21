# Generated by Django 4.2.5 on 2023-10-31 17:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_remove_new_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='new_post',
            name='likest',
            field=models.ManyToManyField(default=None, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]