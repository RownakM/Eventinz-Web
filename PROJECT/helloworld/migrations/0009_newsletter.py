# Generated by Django 4.1 on 2022-08-13 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helloworld', '0008_entries_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsLetter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('subscribe_status', models.CharField(blank=True, choices=[(0, 'Subscribed'), (1, 'Un-Subscribed')], default=1, max_length=30)),
            ],
        ),
    ]
