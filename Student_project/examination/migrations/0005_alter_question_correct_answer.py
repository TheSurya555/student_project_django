# Generated by Django 5.0.6 on 2024-09-12 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0004_alter_question_correct_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='correct_answer',
            field=models.TextField(),
        ),
    ]
