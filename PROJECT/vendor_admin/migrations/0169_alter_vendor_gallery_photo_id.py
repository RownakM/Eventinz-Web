# Generated by Django 4.1 on 2022-08-19 16:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0168_alter_vendor_gallery_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('ccab3d73-90c9-4c23-8166-ec178f8800dd'), max_length=300),
        ),
    ]
