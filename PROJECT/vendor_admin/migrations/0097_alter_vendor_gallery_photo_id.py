# Generated by Django 3.2.12 on 2022-06-30 09:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0096_auto_20220630_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('9b376106-81ef-4dc2-b3c5-d5a4f9532c1f'), max_length=300),
        ),
    ]
