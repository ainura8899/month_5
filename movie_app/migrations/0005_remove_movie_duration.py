# Generated by Django 5.1.1 on 2024-10-12 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0004_movie_is_active_movie_view_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='duration',
        ),
    ]
