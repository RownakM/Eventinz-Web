# Generated by Django 3.2.12 on 2022-05-03 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0024_auto_20220503_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_subscription',
            name='Valid_to',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
