# Generated by Django 3.2.12 on 2022-06-15 11:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0069_alter_vendor_gallery_photo_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_users',
            name='phone_code',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('57842a5f-6d8a-43a0-90ff-ac59a72af04d'), max_length=300),
        ),
    ]