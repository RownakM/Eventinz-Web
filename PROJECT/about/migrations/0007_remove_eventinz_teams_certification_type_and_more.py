# Generated by Django 4.1 on 2022-08-16 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0006_eventinz_teams_certification_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventinz_teams',
            name='certification_type',
        ),
        migrations.AddField(
            model_name='eventinz_teams',
            name='certification_link_1',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventinz_teams',
            name='certification_link_2',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventinz_teams',
            name='certification_link_3',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventinz_teams',
            name='certification_link_4',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventinz_teams',
            name='certification_link_5',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventinz_teams',
            name='certification_logo_1',
            field=models.ImageField(blank=True, null=True, upload_to='ev_teams/profile/user_certification/'),
        ),
        migrations.AddField(
            model_name='eventinz_teams',
            name='certification_logo_2',
            field=models.ImageField(blank=True, null=True, upload_to='ev_teams/profile/user_certification/'),
        ),
        migrations.AddField(
            model_name='eventinz_teams',
            name='certification_logo_3',
            field=models.ImageField(blank=True, null=True, upload_to='ev_teams/profile/user_certification/'),
        ),
        migrations.AddField(
            model_name='eventinz_teams',
            name='certification_logo_4',
            field=models.ImageField(blank=True, null=True, upload_to='ev_teams/profile/user_certification/'),
        ),
        migrations.AddField(
            model_name='eventinz_teams',
            name='certification_logo_5',
            field=models.ImageField(blank=True, null=True, upload_to='ev_teams/profile/user_certification/'),
        ),
    ]