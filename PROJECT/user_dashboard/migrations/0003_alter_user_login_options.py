# Generated by Django 3.2.12 on 2022-05-31 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard', '0002_auto_20220523_0523'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_login',
            options={'verbose_name_plural': 'User Profile'},
        ),
    ]