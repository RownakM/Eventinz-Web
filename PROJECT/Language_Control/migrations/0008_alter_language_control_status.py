# Generated by Django 4.1 on 2022-10-18 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Language_Control', '0007_alter_language_control_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language_control',
            name='status',
            field=models.CharField(choices=[('Enable', 'Enable'), ('Disable', 'Disable')], default='Disable', max_length=40),
        ),
    ]