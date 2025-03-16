from django.core.management.base import BaseCommand
from django.utils import timezone
from challenges.models import Challenge
from datetime import timedelta

class Command(BaseCommand):
    help = "Envoie des rappels pour les défis avec une deadline proche"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        reminder_threshold = now + timedelta(days=2)  # Délais de rappel (2 jours avant)

        challenges = Challenge.objects.filter(
            status="pending",
            deadline__lte=reminder_threshold,
            reminder_sent=False
        )

        for challenge in challenges:
            # Simuler une notification (ajouter ici un envoi d'email ou de push notif)
            self.stdout.write(self.style.WARNING(f"🔔 Rappel : Le défi '{challenge.title}' arrive bientôt à échéance !"))

            # Marquer le rappel comme envoyé
            challenge.reminder_sent = True
            challenge.save()

        self.stdout.write(self.style.SUCCESS("✅ Vérification des rappels terminée."))
