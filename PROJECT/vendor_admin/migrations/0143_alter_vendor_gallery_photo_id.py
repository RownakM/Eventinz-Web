# Generated by Django 4.1 on 2022-08-13 05:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0142_alter_vendor_gallery_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('850a24ee-fae7-4017-a85d-59683b9a95c2'), max_length=300),
        ),
    ]