from django.core.management.base import BaseCommand
from accounts.models import Profile

class Command(BaseCommand):
    help = "Vérifie l'expiration des abonnements Premium et met à jour les statuts"

    def handle(self, *args, **kwargs):
        premium_users = Profile.objects.filter(is_premium=True)
        for profile in premium_users:
            profile.check_premium_status()

        self.stdout.write(self.style.SUCCESS(" Vérification des abonnements terminée."))
