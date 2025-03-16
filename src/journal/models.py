from django.db import models
from django.contrib.auth.models import User

# Journal de l'utilisateur, afin qu'il puisse rapidement partager son mood du jour

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    sleep_hours = models.FloatField(blank=True, null=True)
    gratitude_note = models.TextField(blank=True, null=True)
    mood = models.CharField(max_length=70, choices=[("Heureux","Heureux"),
                                                    ("Bof", "Bof"),
                                                    ("Triste", "Triste"),
                                                    ("Fatigué(e)", "Fatigué(e)")])

    def __str__(self):
        return f"{self.user.username} - {self.date}"
