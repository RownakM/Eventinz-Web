# Generated by Django 4.1 on 2022-08-12 16:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0139_alter_vendor_gallery_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('cf6e6eef-5936-483a-82d7-940c2c64a946'), max_length=300),
        ),
    ]