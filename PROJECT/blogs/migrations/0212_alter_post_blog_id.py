# Generated by Django 4.1 on 2022-10-12 17:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0211_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('2273036a-9fb7-4c93-bd93-eb3f9613710e'), editable=False, max_length=400, unique=True),
        ),
    ]
