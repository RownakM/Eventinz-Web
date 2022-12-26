# Generated by Django 3.2.12 on 2022-06-19 06:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0081_alter_vendor_gallery_photo_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='request_a_quote',
            name='status',
            field=models.CharField(default='pending', max_length=200),
        ),
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('5f8b407d-37a5-4e1f-bc48-b94e680944a9'), max_length=300),
        ),
    ]
