# Generated by Django 4.1 on 2022-10-04 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventmanager', '0023_event_planner_cms_french_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event_entries',
            name='is_archieve',
            field=models.BooleanField(default=False),
        ),
    ]