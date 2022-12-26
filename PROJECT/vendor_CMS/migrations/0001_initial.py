# Generated by Django 3.2.12 on 2022-06-15 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='our_clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='vendor_site/images/our_clients/brand_images/')),
                ('caption', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='our_clients_CMS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Heading', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='vendor_category_CMS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Heading', models.CharField(max_length=300)),
                ('Sub_Heading', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='vendor_get_started',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Heading', models.CharField(max_length=300)),
                ('Sub_Heading', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='vendor_header',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bg_image', models.ImageField(upload_to='vendor_site/images/hero/')),
                ('Title', models.CharField(max_length=300)),
                ('Sub_Title', models.CharField(max_length=200)),
                ('Short_Text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='vendor_leads_CMS_main',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Heading', models.CharField(max_length=300)),
                ('SubTitle', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='vendor_leads_Steps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_no', models.IntegerField()),
                ('image', models.ImageField(upload_to='vendor_site/images/vendor_leads/icon/')),
                ('Heading', models.CharField(max_length=300)),
                ('Sub_Text', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='vendor_testimonials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Heading', models.CharField(max_length=300)),
            ],
        ),
    ]