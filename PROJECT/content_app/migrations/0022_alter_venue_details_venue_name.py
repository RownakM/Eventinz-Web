# Generated by Django 3.2.12 on 2022-06-16 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content_app', '0021_alter_venue_details_venue_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue_details',
            name='venue_name',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='content_app.event_categories'),
        ),
    ]
