# Generated by Django 3.2.12 on 2022-06-08 14:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_auto_20220608_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('4e3c7fed-86ae-414a-89cc-1089e231e734'), max_length=400),
        ),
    ]
