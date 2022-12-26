# Generated by Django 3.2.12 on 2022-07-24 06:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0114_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('19a1a086-696d-47b5-bea8-b07e41500e1d'), editable=False, max_length=400, unique=True),
        ),
    ]