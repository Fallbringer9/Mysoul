from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"


class Profile(models.Model):
    objects = models.Manager()
    ROLE_CHOICES = [
        ('user', 'Utilisateur'),
        ('admin', 'Administrateur'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    is_premium = models.BooleanField(default=False)  #  Statut Premium
    premium_expiration_date = models.DateTimeField(null=True, blank=True)  #  Expiration

    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)  #  ID Client Stripe
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)  #  ID Abonnement Stripe

    def check_premium_status(self):
        """ Vérifie si l’abonnement Premium est toujours actif """
        if self.is_premium and self.premium_expiration_date:
            if self.premium_expiration_date < timezone.now():
                self.is_premium = False
                self.premium_expiration_date = None
                self.save()

    def activate_premium(self, duration_days=30):
        """ Active l'abonnement Premium pour une durée donnée """
        self.is_premium = True
        self.premium_expiration_date = timezone.now() + timezone.timedelta(days=duration_days)
        self.save()

    def check_subscription_status(self):
        """Vérifie si l'abonnement est expiré et le désactive"""
        if self.premium_expiration_date and self.premium_expiration_date < now():
            self.is_premium = False
            self.save()

    def __str__(self):
        return f"{self.user.username} - {'Premium' if self.is_premium else 'Gratuit'}"



# Crée automatiquement un profil lorsqu’un utilisateur est créé
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

