# Generated by Django 5.0.6 on 2024-07-31 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress_tracker', '0010_project_client_alter_project_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='progress',
            name='client_confirmation',
            field=models.BooleanField(default=False),
        ),
    ]