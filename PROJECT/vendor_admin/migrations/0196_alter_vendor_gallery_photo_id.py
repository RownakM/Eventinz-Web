# Generated by Django 4.1 on 2022-09-20 16:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0195_alter_vendor_gallery_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('07f652f2-28b1-4d24-9ca8-4c877d5c2137'), max_length=300),
        ),
    ]
