# Generated by Django 3.2.12 on 2022-05-02 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0014_vendor_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='currency_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_name', models.CharField(max_length=200)),
                ('currency_code', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
    ]
