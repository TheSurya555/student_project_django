# Generated by Django 5.0.6 on 2024-06-25 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signUp', '0010_customuser_professional_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
    ]