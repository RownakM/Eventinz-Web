# Generated by Django 4.1 on 2022-08-13 07:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0149_alter_vendor_gallery_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('c42a881f-bdfd-44e4-878a-2b43d40dea0c'), max_length=300),
        ),
    ]