# Generated by Django 3.2.12 on 2022-05-09 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0034_vendor_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_subscription',
            name='vendor_categories',
            field=models.CharField(default=0, max_length=400),
            preserve_default=False,
        ),
    ]
