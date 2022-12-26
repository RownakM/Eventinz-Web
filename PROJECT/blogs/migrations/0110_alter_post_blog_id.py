# Generated by Django 3.2.12 on 2022-07-21 07:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0109_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('72757246-14e8-48e8-97ba-d8ddae9665db'), editable=False, max_length=400, unique=True),
        ),
    ]
