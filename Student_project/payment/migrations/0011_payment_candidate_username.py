# Generated by Django 5.0.6 on 2024-08-28 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0010_remove_payment_candidate'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='candidate_username',
            field=models.CharField(default='default_username', max_length=255),
        ),
    ]