# Generated by Django 3.2.12 on 2022-06-01 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='index_headers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Header', models.CharField(max_length=300)),
                ('sub_header', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Index Headers',
            },
        ),
        migrations.CreateModel(
            name='index_slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='main_site/slider/img')),
            ],
            options={
                'verbose_name_plural': 'Index Slider',
            },
        ),
    ]
