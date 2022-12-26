# Generated by Django 3.2.12 on 2022-07-09 05:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0103_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('876d8172-8e22-4bf6-aab8-f5ef029dd740'), editable=False, max_length=400, unique=True),
        ),
    ]