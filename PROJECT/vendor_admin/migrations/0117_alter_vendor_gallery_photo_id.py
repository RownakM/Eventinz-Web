# Generated by Django 3.2.12 on 2022-07-23 15:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0116_alter_vendor_gallery_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('8e15f11f-2198-48a7-9e6b-1cae1a66e28f'), max_length=300),
        ),
    ]