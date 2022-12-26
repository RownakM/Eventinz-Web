# Generated by Django 3.2.12 on 2022-07-02 11:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0094_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('e907dab1-3daa-4754-aa9d-a82ef84da1f4'), editable=False, max_length=400, unique=True),
        ),
    ]
