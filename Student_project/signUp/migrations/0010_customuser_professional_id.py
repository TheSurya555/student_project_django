# Generated by Django 5.0.6 on 2024-06-05 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signUp', '0009_alter_customuser_role_adminprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='professional_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
