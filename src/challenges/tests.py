from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from challenges.models import Challenge
from datetime import timedelta, datetime
from django.utils import timezone

class TestChallengeAccess(APITestCase):

    def setUp(self):
        """Créer des utilisateurs et des défis pour tester les accès"""
        self.free_user = User.objects.create_user(username="free_user", password="freepass")
        self.premium_user = User.objects.create_user(username="premium_user", password="premiumpass")
        self.expired_premium_user = User.objects.create_user(username="expired_user", password="expiredpass")

        # Définir un compte premium valide et un expiré
        self.premium_user.profile.is_premium = True
        self.premium_user.profile.premium_expiration_date = timezone.now() + timedelta(days=7)
        self.premium_user.profile.save()

        self.expired_premium_user.profile.is_premium = True
        self.expired_premium_user.profile.premium_expiration_date = timezone.now() - timedelta(days=1)  # Expiré
        self.expired_premium_user.profile.save()

        # Création de défis
        self.free_challenge = Challenge.objects.create(
            title="Défi Gratuit", description="Accessible à tous", is_premium=False, user=self.free_user
        )
        self.premium_challenge = Challenge.objects.create(
            title="Défi Premium", description="Réservé aux Premium", is_premium=True, user=self.premium_user
        )

    def test_free_user_sees_only_free_challenges(self):
        """Teste qu'un utilisateur Free ne voit que les défis gratuits"""
        self.client.login(username="free_user", password="freepass")
        response = self.client.get("/api/free-challenges/")
        self.assertEqual(len(response.data), 1)  # Il ne doit voir que le défi gratuit

    def test_premium_user_sees_premium_challenges(self):
        """Teste qu'un utilisateur Premium voit les défis Premium"""
        self.client.login(username="premium_user", password="premiumpass")
        response = self.client.get("/api/premium-challenges/")
        self.assertEqual(len(response.data), 1)  # Il doit voir les défis Premium

    def test_expired_premium_user_no_premium_access(self):
        """Teste qu'un Premium expiré ne peut plus voir les défis Premium"""

        # Obtenir un token JWT pour l'utilisateur expiré
        response = self.client.post("/api/token/", {"username": "expired_user", "password": "expiredpass"},
                                    format="json")

        self.assertEqual(response.status_code, 200, "Échec de l'obtention du token pour l'utilisateur expiré")

        token = response.data["access"]

        # Ajouter le token dans l'en-tête Authorization
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Tester l'accès aux défis Premium
        response = self.client.get("/api/premium-challenges/")

        self.assertEqual(response.status_code, 403,
                         "Un utilisateur Premium expiré ne doit pas avoir accès aux défis Premium")


