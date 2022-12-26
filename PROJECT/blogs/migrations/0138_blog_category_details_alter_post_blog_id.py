# Generated by Django 4.1 on 2022-08-13 05:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0137_post_cover_image_alter_post_blog_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog_Category_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_image', models.ImageField(upload_to='main_site/blog/category_images/coverimage/')),
                ('Heading', models.CharField(max_length=3000)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.CharField(default=uuid.UUID('94fa97b5-5980-4147-b9be-5ba12917344a'), editable=False, max_length=400, unique=True),
        ),
    ]
