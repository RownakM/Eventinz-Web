# Generated by Django 4.1 on 2022-12-16 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexCMS', '0008_alter_vendor_categories_text_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Packages_CMS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Heading', models.CharField(max_length=1000)),
                ('image', models.ImageField(upload_to='main_site/package_cms/img')),
            ],
        ),
    ]