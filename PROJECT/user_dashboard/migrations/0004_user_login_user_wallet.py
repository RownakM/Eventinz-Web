# Generated by Django 3.2.12 on 2022-06-30 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard', '0003_alter_user_login_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_login',
            name='user_wallet',
            field=models.IntegerField(default=0),
        ),
    ]
