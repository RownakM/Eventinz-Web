# Generated by Django 4.1 on 2022-10-22 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventmanager', '0027_event_entries_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='create_event_packages',
            name='premium_validity',
            field=models.IntegerField(default=1, help_text='In Days'),
        ),
    ]