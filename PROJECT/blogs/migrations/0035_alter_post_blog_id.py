# Generated by Django 3.2.12 on 2022-06-10 09:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0034_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('25dfe75a-2201-4152-a785-fa086024a067'), editable=False, max_length=400, unique=True),
        ),
    ]