# Generated by Django 3.2.12 on 2022-04-30 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0012_alter_vendor_users_valid_till'),
    ]

    operations = [
        migrations.CreateModel(
            name='vendor_packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(max_length=200)),
                ('package_features', models.CharField(max_length=300)),
                ('price', models.IntegerField(default=0)),
            ],
        ),
    ]
