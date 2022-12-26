# Generated by Django 4.1 on 2022-12-16 09:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0226_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('fc8a450e-a869-4695-81bb-4cd3a4946f71'), editable=False, max_length=400, unique=True),
        ),
    ]
