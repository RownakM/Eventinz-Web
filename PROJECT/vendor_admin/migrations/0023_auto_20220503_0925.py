# Generated by Django 3.2.12 on 2022-05-03 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0022_auto_20220503_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_subscription',
            name='Valid_to',
            field=models.DateTimeField(blank=True, default='NAa'),
        ),
        migrations.AlterField(
            model_name='vendor_subscription',
            name='Vendor_company_name',
            field=models.CharField(blank=True, default='NAa', max_length=300),
        ),
        migrations.AlterField(
            model_name='vendor_subscription',
            name='Vendor_name',
            field=models.CharField(blank=True, default='NAa', max_length=200),
        ),
        migrations.AlterField(
            model_name='vendor_subscription',
            name='invoice_id',
            field=models.CharField(blank=True, default='NAa', max_length=400),
        ),
        migrations.AlterField(
            model_name='vendor_subscription',
            name='package_description',
            field=models.CharField(blank=True, default='NAa', max_length=200),
        ),
        migrations.AlterField(
            model_name='vendor_subscription',
            name='package_fee',
            field=models.IntegerField(blank=True, default='NAa'),
        ),
        migrations.AlterField(
            model_name='vendor_subscription',
            name='package_name',
            field=models.CharField(blank=True, default='NAa', max_length=300),
        ),
        migrations.AlterField(
            model_name='vendor_subscription',
            name='payment_by',
            field=models.CharField(blank=True, default='NAa', max_length=300),
        ),
        migrations.AlterField(
            model_name='vendor_subscription',
            name='purchase_type',
            field=models.CharField(blank=True, default='NAa', max_length=300),
        ),
        migrations.AlterField(
            model_name='vendor_subscription',
            name='service_fee',
            field=models.IntegerField(blank=True, default='NAa'),
        ),
        migrations.AlterField(
            model_name='vendor_subscription',
            name='time',
            field=models.CharField(blank=True, default='NAa', max_length=300),
        ),
        migrations.AlterField(
            model_name='vendor_subscription',
            name='vendor_email',
            field=models.EmailField(blank=True, default='NAa', max_length=254),
        ),
        migrations.AlterField(
            model_name='vendor_subscription',
            name='vendor_phone',
            field=models.IntegerField(blank=True, default='NAa'),
        ),
    ]