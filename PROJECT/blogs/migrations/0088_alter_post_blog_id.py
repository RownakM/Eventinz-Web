# Generated by Django 3.2.12 on 2022-06-29 09:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0087_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('bc4d6ca0-f483-4480-89e2-3159f85c1bd1'), editable=False, max_length=400, unique=True),
        ),
    ]