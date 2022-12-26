# Generated by Django 3.2.12 on 2022-06-12 04:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0039_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('dc6a99d2-a4c3-43ea-a3b9-e3b00dceea63'), editable=False, max_length=400, unique=True),
        ),
    ]
