# Generated by Django 4.1 on 2022-08-24 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventmanager', '0010_vendor_event_proposal_vendor_event_proposal_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='event_entries',
            name='vendor_type_json',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]
