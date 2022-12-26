# Generated by Django 4.1 on 2022-10-05 08:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0200_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('9e6fee8a-c5f4-44e6-b451-f2ed9546de26'), editable=False, max_length=400, unique=True),
        ),
    ]