# Generated by Django 4.1 on 2022-10-16 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventmanager', '0025_event_reviews_user_to_vendor_vendor_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='create_event_packages',
            options={'verbose_name_plural': "'Create Event' - Packages"},
        ),
        migrations.AlterModelOptions(
            name='event_budget_settings',
            options={'verbose_name_plural': 'Event Budget Manager'},
        ),
        migrations.AlterModelOptions(
            name='event_entries',
            options={'verbose_name_plural': 'Event Entries'},
        ),
        migrations.AlterModelOptions(
            name='event_heads_manager',
            options={'verbose_name_plural': 'Event Guests Manager'},
        ),
        migrations.AlterModelOptions(
            name='event_planner_cms',
            options={'verbose_name_plural': "'Event Planner' - Manager"},
        ),
    ]
