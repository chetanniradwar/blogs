# Generated by Django 4.2 on 2023-04-16 03:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='blog_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
