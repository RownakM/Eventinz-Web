# Generated by Django 4.1 on 2022-10-02 07:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0196_alter_post_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('c21c9590-685e-4725-83c9-c45da3579ab5'), editable=False, max_length=400, unique=True),
        ),
    ]
