# Generated by Django 5.0.6 on 2024-12-01 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0015_userprofile_university'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='career_objective',
            field=models.TextField(blank=True, null=True, verbose_name='Career Objective'),
        ),
    ]
