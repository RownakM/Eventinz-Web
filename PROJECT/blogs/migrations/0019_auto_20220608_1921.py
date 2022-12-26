# Generated by Django 3.2.12 on 2022-06-08 19:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0018_auto_20220608_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('53177bf7-f0f2-4095-8f28-b2e6480309d1'), editable=False, max_length=400, unique=True),
        ),
        migrations.AlterField(
            model_name='postimage',
            name='images',
            field=models.ImageField(upload_to='main_site/blog/content_images'),
        ),
    ]