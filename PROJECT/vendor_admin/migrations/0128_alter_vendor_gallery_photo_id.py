# Generated by Django 3.2.12 on 2022-08-05 11:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0127_alter_vendor_gallery_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('56b14930-d3b1-4a17-947f-7692b954f9cb'), max_length=300),
        ),
    ]