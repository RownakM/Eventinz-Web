# Generated by Django 3.2.12 on 2022-06-13 12:59

from django.db import migrations,models
# import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0057_vendor_public_packages_vendor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_users',
            name='event_category_serve',
            field=models.JSONField(default=dict),
        ),
    ]
