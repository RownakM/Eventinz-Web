# Generated by Django 4.1 on 2022-09-15 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventmanager', '0018_vendor_event_proposal_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_event_proposal',
            name='grand_total',
            field=models.CharField(default=0, max_length=4000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendor_event_proposal',
            name='state_tax',
            field=models.CharField(default=0, max_length=4000),
            preserve_default=False,
        ),
    ]
