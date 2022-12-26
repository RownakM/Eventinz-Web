# Generated by Django 4.1 on 2022-10-19 10:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0218_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('6b7451e8-9cb6-4f8b-96cf-b85714fbc211'), editable=False, max_length=400, unique=True),
        ),
    ]