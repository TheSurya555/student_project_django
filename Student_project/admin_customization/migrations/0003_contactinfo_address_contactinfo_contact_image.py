# Generated by Django 5.0.6 on 2024-10-14 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_customization', '0002_contactinfo_herosection_workstep'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactinfo',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='contactinfo',
            name='contact_image',
            field=models.ImageField(blank=True, null=True, upload_to='contact_images/'),
        ),
    ]