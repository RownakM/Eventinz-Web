# Generated by Django 4.1 on 2022-08-25 12:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0181_alter_vendor_gallery_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('abafec21-f374-45ad-94a9-59041a98d38c'), max_length=300),
        ),
    ]
