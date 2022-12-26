# Generated by Django 4.1 on 2022-08-23 17:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0172_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('b30a9d8d-55c8-43de-97ee-6fd4a3c11373'), editable=False, max_length=400, unique=True),
        ),
    ]