# Generated by Django 4.1 on 2022-08-13 07:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0145_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('4a192dfb-78ee-4732-bca7-0ae8ba1185aa'), editable=False, max_length=400, unique=True),
        ),
    ]
