# Generated by Django 4.1 on 2022-10-01 20:45

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventinz_Terms_And_Conditions', '0002_rename_privacy_policy_text_eventinz_privacy_policy_content_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Eventinz_Privacy_Policy_french',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_image', models.ImageField(upload_to='privacy/content/')),
                ('page_header', models.CharField(max_length=1000)),
                ('content', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='Eventinz_Terms_french',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_image', models.ImageField(upload_to='tnc/content/')),
                ('page_header', models.CharField(max_length=1000)),
                ('content', tinymce.models.HTMLField()),
            ],
        ),
    ]