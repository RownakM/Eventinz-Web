# Generated by Django 3.2.12 on 2022-05-15 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0038_rename_valid_to_vendor_subscription_valid_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_users',
            name='facebook_url',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='vendor_users',
            name='instagram_url',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='vendor_users',
            name='linkedin_url',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='vendor_users',
            name='twitter_url',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
