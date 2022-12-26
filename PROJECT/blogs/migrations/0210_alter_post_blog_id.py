# Generated by Django 4.1 on 2022-10-11 07:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0209_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('c9d07ebf-f423-4100-a8a9-0b937b230816'), editable=False, max_length=400, unique=True),
        ),
    ]
