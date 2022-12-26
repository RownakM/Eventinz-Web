# Generated by Django 3.2.12 on 2022-06-15 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_CMS', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='our_clients',
            options={'verbose_name_plural': 'Vendor Clients'},
        ),
        migrations.AlterModelOptions(
            name='our_clients_cms',
            options={'verbose_name_plural': 'Vendor Clients CMS'},
        ),
        migrations.AlterModelOptions(
            name='vendor_category_cms',
            options={'verbose_name_plural': 'Vendor Category CMS'},
        ),
        migrations.AlterModelOptions(
            name='vendor_get_started',
            options={'verbose_name_plural': 'Vendor Get Started'},
        ),
        migrations.AlterModelOptions(
            name='vendor_header',
            options={'verbose_name_plural': 'Vendor Header'},
        ),
        migrations.AlterModelOptions(
            name='vendor_leads_cms_main',
            options={'verbose_name_plural': 'Vendor Leads CMS'},
        ),
        migrations.AlterModelOptions(
            name='vendor_leads_steps',
            options={'verbose_name_plural': 'Vendor Leads Steps'},
        ),
        migrations.AlterModelOptions(
            name='vendor_testimonials',
            options={'verbose_name_plural': 'Vendor Testimonials'},
        ),
    ]