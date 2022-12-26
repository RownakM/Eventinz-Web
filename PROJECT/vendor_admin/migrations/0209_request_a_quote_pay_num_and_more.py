# Generated by Django 4.1 on 2022-10-08 14:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0208_alter_vendor_gallery_photo_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='request_a_quote',
            name='pay_num',
            field=models.CharField(default='1', max_length=200),
        ),
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('89c44ad5-8da9-4f1e-b649-65439b67ab9c'), max_length=300),
        ),
        migrations.AlterField(
            model_name='vendor_leads_package',
            name='valid_type',
            field=models.CharField(choices=[('Quarter', 'Quarter'), ('Year', 'Year'), ('Half-Yearly', 'Half-Yearly'), ('Month', 'Month')], max_length=4000),
        ),
    ]