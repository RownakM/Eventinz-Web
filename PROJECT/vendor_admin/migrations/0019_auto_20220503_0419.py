# Generated by Django 3.2.12 on 2022-05-03 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0018_states'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('state_id', models.CharField(max_length=300)),
                ('state_code', models.CharField(max_length=300)),
                ('state_name', models.CharField(max_length=300)),
                ('country_id', models.CharField(max_length=300)),
                ('country_code', models.CharField(max_length=300)),
                ('country_name', models.CharField(max_length=300)),
                ('latitude', models.CharField(default='NA', max_length=300)),
                ('longitude', models.CharField(default='NA', max_length=300)),
            ],
        ),
        migrations.AlterField(
            model_name='states',
            name='latitude',
            field=models.CharField(blank=True, default='NA', max_length=300),
        ),
        migrations.AlterField(
            model_name='states',
            name='longitude',
            field=models.CharField(blank=True, default='NA', max_length=300),
        ),
    ]
