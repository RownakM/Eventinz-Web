# Generated by Django 4.1 on 2022-10-01 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0197_vendor_leads_package_alter_vendor_gallery_photo_id'),
        ('eventmanager', '0022_alter_event_reviews_vendor_to_user_review_from'),
    ]

    operations = [
        migrations.CreateModel(
            name='event_planner_CMS_french',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('image', models.ImageField(upload_to='event_planner_cms/images/')),
                ('heading', models.CharField(max_length=400)),
                ('sub_heading', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='create_event_packages_french',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('premium_amount', models.IntegerField()),
                ('freemium_features', models.TextField()),
                ('premium_features', models.TextField()),
                ('currency_country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor_admin.countries')),
            ],
        ),
    ]