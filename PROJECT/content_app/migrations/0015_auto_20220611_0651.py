# Generated by Django 3.2.12 on 2022-06-11 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_app', '0014_venue_main_home'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue_main_home',
            name='venue_by_event',
            field=models.CharField(default=0, max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue_main_home',
            name='venue_by_event_subheading',
            field=models.CharField(default=0, max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue_main_home',
            name='venue_by_venue',
            field=models.CharField(default=0, max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue_main_home',
            name='venue_by_venue_subheading',
            field=models.CharField(default=0, max_length=300),
            preserve_default=False,
        ),
    ]
