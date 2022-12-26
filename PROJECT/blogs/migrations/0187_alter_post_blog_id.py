# Generated by Django 4.1 on 2022-09-07 12:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0186_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('9271b52b-d495-4de7-a664-0fdf6529e183'), editable=False, max_length=400, unique=True),
        ),
    ]