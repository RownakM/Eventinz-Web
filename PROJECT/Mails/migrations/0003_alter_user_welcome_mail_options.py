# Generated by Django 4.1 on 2022-10-16 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mails', '0002_user_welcome_mail_french'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_welcome_mail',
            options={'verbose_name_plural': 'Welcome Mail - User'},
        ),
    ]