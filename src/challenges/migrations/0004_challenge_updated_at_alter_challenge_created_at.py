# Generated by Django 5.1.6 on 2025-02-19 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0003_challenge_deadline_challenge_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
