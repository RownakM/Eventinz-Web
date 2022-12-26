# Generated by Django 4.1 on 2022-10-17 06:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0213_alter_blog_category_details_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('d539194f-aea5-4847-8adb-798c8a130585'), editable=False, max_length=400, unique=True),
        ),
    ]
