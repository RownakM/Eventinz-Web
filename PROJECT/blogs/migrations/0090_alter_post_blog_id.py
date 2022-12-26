# Generated by Django 3.2.12 on 2022-06-30 08:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0089_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('5517faac-d90d-428b-b2ac-30ab7df686c4'), editable=False, max_length=400, unique=True),
        ),
    ]
