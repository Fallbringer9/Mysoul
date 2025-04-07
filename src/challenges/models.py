from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils import  timezone

class Challenge(models.Model):
    STATUS_CHOICES = [
        ('pending','En cours'),
        ('completed', 'Terminé'),
        ('failed', 'Abandonné')
    ]
    PRIORITY_CHOICES = [
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
    ]
    objects = models.Manager()


    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Lier à l'utilisateur
    title = models.CharField(max_length=200, verbose_name="Titre du défi")
    description = models.TextField()
    completed = models.BooleanField(default=False)  # Si le défi est terminé ou non
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    duration = models.IntegerField(default=0)
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    is_premium = models.BooleanField(default=False)
    reminder_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """ Met à jour automatiquement le statut avant de sauvegarder """
        if self.status == "pending":
            now = timezone.now()
            if self.created_at is None:
                self.created_at = now

            if self.deadline is not None and self.deadline < now:
                self.status = "failed"
            elif self.deadline is None and self.created_at <= now - timedelta(days=14):
                self.status = "completed"
        super().save(*args, **kwargs)  # Appel normal à save()



