# Generated by Django 4.1 on 2022-08-13 07:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0147_alter_vendor_gallery_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('7d1b906a-c869-4244-a7eb-3d931892dc69'), max_length=300),
        ),
    ]