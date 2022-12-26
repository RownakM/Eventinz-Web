# Generated by Django 4.1 on 2022-10-08 14:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0207_alter_vendor_gallery_photo_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('1976bffe-ed49-4227-b6c1-7f1f7f08361a'), max_length=300),
        ),
        migrations.AlterField(
            model_name='vendor_leads_package',
            name='valid_type',
            field=models.CharField(choices=[('Half-Yearly', 'Half-Yearly'), ('Month', 'Month'), ('Quarter', 'Quarter'), ('Year', 'Year')], max_length=4000),
        ),
    ]
