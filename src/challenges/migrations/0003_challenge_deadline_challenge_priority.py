# Generated by Django 5.1.6 on 2025-02-19 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0002_challenge_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='challenge',
            name='priority',
            field=models.CharField(choices=[('low', 'Faible'), ('medium', 'Moyenne'), ('high', 'Haute')], default='medium', max_length=10),
        ),
    ]
