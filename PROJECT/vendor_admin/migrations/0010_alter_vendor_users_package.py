# Generated by Django 3.2.12 on 2022-04-29 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0009_alter_vendor_users_company_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_users',
            name='package',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]