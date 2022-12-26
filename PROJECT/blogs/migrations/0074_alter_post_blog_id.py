# Generated by Django 3.2.12 on 2022-06-16 16:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0073_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('7a9992c9-784f-4ed5-b2b0-0b215c3a8f46'), editable=False, max_length=400, unique=True),
        ),
    ]