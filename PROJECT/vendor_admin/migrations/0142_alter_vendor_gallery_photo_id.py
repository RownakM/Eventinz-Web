# Generated by Django 4.1 on 2022-08-13 04:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0141_alter_vendor_gallery_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('3d0ef11c-7639-4d7e-8e06-f197e30aef6f'), max_length=300),
        ),
    ]
