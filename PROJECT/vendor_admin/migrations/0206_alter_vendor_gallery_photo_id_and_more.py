# Generated by Django 4.1 on 2022-10-08 12:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0205_alter_vendor_gallery_photo_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('928f81a0-c3f0-4f3f-9aa0-c627741fa4b4'), max_length=300),
        ),
        migrations.AlterField(
            model_name='vendor_leads_package',
            name='valid_type',
            field=models.CharField(choices=[('Quarter', 'Quarter'), ('Year', 'Year'), ('Half-Yearly', 'Half-Yearly'), ('Month', 'Month')], max_length=4000),
        ),
    ]