# Generated by Django 3.2.12 on 2022-06-08 14:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0007_auto_20220608_1442'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='post',
        #     name='category',
        # ),
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('3e3a59b9-4b3e-45f9-aca1-7ae5c506cec1'), max_length=400),
        ),
        # migrations.DeleteModel(
        #     name='blog_category',
        # ),
    ]