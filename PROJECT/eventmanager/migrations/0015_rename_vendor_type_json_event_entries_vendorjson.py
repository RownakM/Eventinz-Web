# Generated by Django 4.1 on 2022-08-24 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventmanager', '0014_alter_event_entries_vendor_type_json'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event_entries',
            old_name='vendor_type_json',
            new_name='vendorjson',
        ),
    ]
