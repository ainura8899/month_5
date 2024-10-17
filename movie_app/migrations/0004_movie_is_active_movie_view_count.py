# Generated by Django 5.1.1 on 2024-10-12 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0003_review_stars_alter_review_movie'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
