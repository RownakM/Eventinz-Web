# Generated by Django 3.2.12 on 2022-06-14 20:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0061_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('6651944c-4de9-4a94-abaf-fbc393e38480'), editable=False, max_length=400, unique=True),
        ),
    ]