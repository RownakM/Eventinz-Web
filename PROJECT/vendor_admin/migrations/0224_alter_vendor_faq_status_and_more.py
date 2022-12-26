# Generated by Django 4.1 on 2022-10-19 19:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0223_vendor_categories_thumbnail_cover_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_faq',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('deactive', 'deactive')], default='deactive', max_length=1000),
        ),
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('68786afd-f0da-4c43-9e1c-3ec05ca42eef'), max_length=300),
        ),
    ]
