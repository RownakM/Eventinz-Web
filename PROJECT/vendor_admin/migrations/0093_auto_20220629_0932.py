# Generated by Django 3.2.12 on 2022-06-29 09:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0092_auto_20220627_0721'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_quote_invoice',
            name='milestone',
            field=models.CharField(default='0', max_length=300),
        ),
        migrations.AddField(
            model_name='vendor_quote_invoice',
            name='milestone_type',
            field=models.CharField(default='amt', max_length=300),
        ),
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('6a4ca472-b8b9-463d-afc5-01e707578497'), max_length=300),
        ),
    ]