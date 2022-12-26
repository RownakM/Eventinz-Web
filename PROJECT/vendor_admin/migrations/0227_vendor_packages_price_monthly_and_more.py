# Generated by Django 4.1 on 2022-12-08 04:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0226_alter_vendor_gallery_photo_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_packages',
            name='price_monthly',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('28b731bd-baca-483c-840c-cb163dfb17b8'), max_length=300),
        ),
    ]
