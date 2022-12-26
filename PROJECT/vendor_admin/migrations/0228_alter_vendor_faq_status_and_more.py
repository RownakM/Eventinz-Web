# Generated by Django 4.1 on 2022-12-08 04:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0227_vendor_packages_price_monthly_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_faq',
            name='status',
            field=models.CharField(choices=[('deactive', 'deactive'), ('active', 'active')], default='deactive', max_length=1000),
        ),
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('6d1661a2-692b-4cb8-b735-3d1c34c5fca6'), max_length=300),
        ),
        migrations.AlterField(
            model_name='vendor_leads_package',
            name='valid_type',
            field=models.CharField(choices=[('Half-Yearly', 'Half-Yearly'), ('Quarter', 'Quarter'), ('Year', 'Year'), ('Month', 'Month')], max_length=4000),
        ),
    ]
