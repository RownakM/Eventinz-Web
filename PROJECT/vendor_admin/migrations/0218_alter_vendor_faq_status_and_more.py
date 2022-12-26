# Generated by Django 4.1 on 2022-10-17 13:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0217_vendor_quote_invoice_tax_percent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_faq',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('deactive', 'deactive')], default='deactive', max_length=1000),
        ),
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('71bbcf50-8cd0-4484-bb9d-ed1fbc8e120c'), max_length=300),
        ),
        migrations.AlterField(
            model_name='vendor_leads_package',
            name='valid_type',
            field=models.CharField(choices=[('Month', 'Month'), ('Half-Yearly', 'Half-Yearly'), ('Quarter', 'Quarter'), ('Year', 'Year')], max_length=4000),
        ),
    ]
