from django.core.management.base import BaseCommand
from django.utils.timezone import now
from accounts.models import Profile

class Command(BaseCommand):
    help = "Désactive les comptes premium expirés"

    def handle(self, *args, **kwargs):
        expired_profiles = Profile.objects.filter(is_premium=True, premium_expiration_date__lt=now())

        if expired_profiles.exists():
            updated_count = expired_profiles.update(is_premium=False)
            self.stdout.write(self.style.SUCCESS(f"{updated_count} abonnements expirés désactivés."))
        else:
            self.stdout.write(self.style.SUCCESS("Aucun abonnement expiré aujourd'hui."))

