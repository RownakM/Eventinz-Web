# Generated by Django 3.2.12 on 2022-06-08 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0013_alter_blog_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog_cms',
            name='Title_Image',
            field=models.ImageField(default=1, upload_to='main_site/blog/cms/img'),
            preserve_default=False,
        ),
    ]
