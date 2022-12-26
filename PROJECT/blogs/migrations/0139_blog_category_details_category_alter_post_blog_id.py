# Generated by Django 4.1 on 2022-08-13 05:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0138_blog_category_details_alter_post_blog_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog_category_details',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blogs.blog_category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('29dd20d2-33c2-42ff-823a-7a0797ae139f'), editable=False, max_length=400, unique=True),
        ),
    ]
