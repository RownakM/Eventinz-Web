# Generated by Django 3.2.12 on 2022-05-20 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0039_auto_20220515_0834'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_users',
            name='Company_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
