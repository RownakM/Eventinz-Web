# Generated by Django 4.1 on 2022-10-10 13:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0210_alter_vendor_gallery_photo_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_users',
            name='profile_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('dd56f6ef-668a-47e0-9b34-96c243e65a85'), max_length=300),
        ),
        migrations.AlterField(
            model_name='vendor_leads_package',
            name='valid_type',
            field=models.CharField(choices=[('Half-Yearly', 'Half-Yearly'), ('Year', 'Year'), ('Quarter', 'Quarter'), ('Month', 'Month')], max_length=4000),
        ),
    ]