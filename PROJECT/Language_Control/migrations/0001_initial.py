# Generated by Django 4.1 on 2022-10-05 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language_Control',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('english_text', models.TextField()),
                ('french_text', models.TextField()),
                ('status', models.CharField(choices=[('Disable', 'Disable'), ('Enable', 'Enable')], default='Disable', max_length=40)),
            ],
        ),
    ]
