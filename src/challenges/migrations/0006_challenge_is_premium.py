# Generated by Django 5.1.6 on 2025-02-27 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0005_challenge_reminder_sent_alter_challenge_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='is_premium',
            field=models.BooleanField(default=False),
        ),
    ]
