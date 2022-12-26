# Generated by Django 3.2.12 on 2022-06-25 07:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0080_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('fb88e89e-45a4-48f5-a231-3cfb54ad9228'), editable=False, max_length=400, unique=True),
        ),
    ]