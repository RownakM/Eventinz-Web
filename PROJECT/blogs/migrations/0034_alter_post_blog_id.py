# Generated by Django 3.2.12 on 2022-06-10 08:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0033_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('db5280da-1cc3-437b-b21b-4ab519b5f5a7'), editable=False, max_length=400, unique=True),
        ),
    ]
