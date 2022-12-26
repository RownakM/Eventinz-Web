# Generated by Django 4.1 on 2022-08-08 12:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0134_alter_listings_data_dnr_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_subscription',
            name='service_currency',
            field=models.CharField(default='NAa', max_length=300),
        ),
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('0252d766-5cec-435b-a2f8-65fedf06968b'), max_length=300),
        ),
    ]
