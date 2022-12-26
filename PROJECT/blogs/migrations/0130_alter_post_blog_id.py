# Generated by Django 4.1 on 2022-08-08 12:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0129_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('995d6dd4-64c5-452a-a9ce-664b37fc6347'), editable=False, max_length=400, unique=True),
        ),
    ]
