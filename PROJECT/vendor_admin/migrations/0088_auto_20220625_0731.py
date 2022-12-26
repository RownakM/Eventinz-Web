# Generated by Django 3.2.12 on 2022-06-25 07:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard', '0003_alter_user_login_options'),
        ('vendor_admin', '0087_auto_20220625_0721'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_quote_invoice',
            name='quote_user',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to='user_dashboard.user_login'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('dea1532d-5d48-4360-b6a8-99bdf19013f9'), max_length=300),
        ),
    ]