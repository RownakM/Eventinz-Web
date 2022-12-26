# Generated by Django 3.2.12 on 2022-05-03 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0017_auto_20220502_1913'),
    ]

    operations = [
        migrations.CreateModel(
            name='States',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('country_id', models.CharField(max_length=200)),
                ('country_code', models.CharField(max_length=200)),
                ('country_name', models.CharField(max_length=300)),
                ('state_code', models.CharField(max_length=300)),
                ('latitude', models.CharField(max_length=300)),
                ('longitude', models.CharField(max_length=300)),
            ],
        ),
    ]
