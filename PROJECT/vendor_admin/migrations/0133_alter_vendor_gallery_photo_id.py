# Generated by Django 3.2.12 on 2022-08-07 13:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0132_auto_20220807_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('430839d9-2cf3-4c7b-90f8-a00b1b5f3393'), max_length=300),
        ),
    ]
