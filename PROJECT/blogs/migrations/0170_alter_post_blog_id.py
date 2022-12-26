# Generated by Django 4.1 on 2022-08-22 06:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0169_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('bed019b4-9aa0-49dd-9013-7cdda966c279'), editable=False, max_length=400, unique=True),
        ),
    ]