# Generated by Django 4.1 on 2022-10-05 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Language_Control', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language_control',
            name='status',
            field=models.CharField(choices=[('Enable', 'Enable'), ('Disable', 'Disable')], default='Disable', max_length=40),
        ),
    ]
