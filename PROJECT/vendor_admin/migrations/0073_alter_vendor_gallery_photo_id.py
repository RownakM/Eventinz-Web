# Generated by Django 3.2.12 on 2022-06-16 15:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0072_alter_vendor_gallery_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('faf90f38-209f-44b0-9339-6250645ba1d1'), max_length=300),
        ),
    ]
