# Generated by Django 4.1 on 2022-08-15 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_app', '0028_cron_activities'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange_Rates_API',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=400)),
                ('password', models.CharField(max_length=500)),
                ('apikey', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
