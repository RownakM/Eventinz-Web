# Generated by Django 3.2.12 on 2022-06-25 07:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0081_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('e2067b82-0e23-4c73-af40-1cd571f76ccf'), editable=False, max_length=400, unique=True),
        ),
    ]
