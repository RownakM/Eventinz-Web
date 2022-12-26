# Generated by Django 3.2.12 on 2022-06-14 20:29

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_admin', '0066_auto_20220614_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_questions',
            name='Question_Category',
            field=models.ForeignKey(default=26, on_delete=django.db.models.deletion.CASCADE, to='vendor_admin.vendor_categories'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vendor_gallery',
            name='photo_id',
            field=models.CharField(default=uuid.UUID('3ce04ed7-758b-4eb8-aaad-86bcbb0c6275'), max_length=300),
        ),
    ]