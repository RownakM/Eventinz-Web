# Generated by Django 3.2.12 on 2022-07-23 15:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0117_alter_vendor_gallery_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('589bb0eb-533b-493d-853e-7544c791001c'), max_length=300),
        ),
    ]
