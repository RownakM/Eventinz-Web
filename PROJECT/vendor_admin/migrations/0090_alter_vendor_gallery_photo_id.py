# Generated by Django 3.2.12 on 2022-06-26 17:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0089_auto_20220625_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('f4e530e3-7f30-4ae8-ae25-e5770a5e92ef'), max_length=300),
        ),
    ]