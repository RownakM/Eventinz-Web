# Generated by Django 3.2.12 on 2022-05-03 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0026_vendor_subscription_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_subscription',
            name='country_cuurency',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
    ]