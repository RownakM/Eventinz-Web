# Generated by Django 3.2.12 on 2022-05-27 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0041_vendor_categories_french'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChoiceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='SampleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('your_choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor_admin.choicelist')),
            ],
        ),
    ]