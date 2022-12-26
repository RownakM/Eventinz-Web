# Generated by Django 4.1 on 2022-09-20 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0196_alter_vendor_gallery_photo_id'),
        ('eventmanager', '0021_event_reviews_vendor_to_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_reviews_vendor_to_user',
            name='review_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor_admin.vendor_users'),
        ),
    ]
