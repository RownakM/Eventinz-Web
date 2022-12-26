# Generated by Django 3.2.12 on 2022-08-05 11:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0128_alter_vendor_gallery_photo_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_users',
            name='vendor_sub_cat_data',
            field=models.TextField(default='all'),
        ),
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('4f5e9873-b340-4646-b8b1-73f9b9d7c9a9'), max_length=300),
        ),
    ]