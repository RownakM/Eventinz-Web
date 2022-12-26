# Generated by Django 4.1 on 2022-10-11 07:06

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0212_vendor_faq_alter_vendor_gallery_photo_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_faq',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('ee7dfe0e-7805-4a3b-9fae-3140825fc77b'), max_length=300),
        ),
        migrations.AlterField(
            model_name='vendor_leads_package',
            name='valid_type',
            field=models.CharField(choices=[('Year', 'Year'), ('Half-Yearly', 'Half-Yearly'), ('Quarter', 'Quarter'), ('Month', 'Month')], max_length=4000),
        ),
    ]
