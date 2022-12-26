# Generated by Django 4.1 on 2022-10-11 07:03

from django.db import migrations, models
import tinymce.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0211_vendor_users_profile_complete_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor_FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Question', models.TextField()),
                ('Answer', tinymce.models.HTMLField()),
                ('status', models.CharField(choices=[('deactive', 'deactive'), ('active', 'active')], default='deactive', max_length=1000)),
            ],
        ),
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('cf515393-6c90-4d24-adb0-20e2f368f775'), max_length=300),
        ),
        migrations.AlterField(
            model_name='vendor_leads_package',
            name='valid_type',
            field=models.CharField(choices=[('Month', 'Month'), ('Year', 'Year'), ('Half-Yearly', 'Half-Yearly'), ('Quarter', 'Quarter')], max_length=4000),
        ),
    ]
