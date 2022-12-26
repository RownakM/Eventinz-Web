# Generated by Django 3.2.12 on 2022-06-26 17:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0084_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('5bfe5c35-ce14-4b75-ab7b-78f8291b36d1'), editable=False, max_length=400, unique=True),
        ),
    ]