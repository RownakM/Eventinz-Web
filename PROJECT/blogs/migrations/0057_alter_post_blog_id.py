# Generated by Django 3.2.12 on 2022-06-13 17:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0056_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('d3df5665-469e-41eb-906d-48a6da985844'), editable=False, max_length=400, unique=True),
        ),
    ]
