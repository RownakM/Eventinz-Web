# Generated by Django 4.1 on 2022-08-12 16:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0135_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('e5f52745-bcc1-4c30-a023-1c5e85517268'), editable=False, max_length=400, unique=True),
        ),
    ]
