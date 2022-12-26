# Generated by Django 4.1 on 2022-10-28 14:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message_quote_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]