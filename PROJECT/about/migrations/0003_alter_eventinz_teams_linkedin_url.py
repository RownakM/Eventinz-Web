# Generated by Django 4.1 on 2022-08-12 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0002_alter_eventinz_teams_linkedin_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventinz_teams',
            name='linkedin_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
