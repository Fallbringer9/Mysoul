from datetime import timedelta, date, datetime
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.utils.timezone import make_aware
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mysoul.settings')  # Remplace 'mysoul' par le nom de ton projet
django.setup()


class PermissionsTestCase(APITestCase):

    def setUp(self):
        """
        Création de plusieurs utilisateurs pour tester les permissions.
        """
        self.client = APIClient()  # On utilise APIClient pour DRF

        self.admin = User.objects.create_user(username="admin", password="adminpass")
        self.admin.profile.role = "admin"
        self.admin.profile.save()

        self.free_user = User.objects.create_user(username="free_user", password=make_password("freepass"))
        self.free_user.profile.is_premium = False
        self.free_user.profile.save()

        self.premium_user = User.objects.create_user(username="premium_user", password=make_password("premiumpass"))
        self.premium_user.profile.is_premium = True
        self.premium_user.profile.premium_expiration_date = make_aware(datetime.now() + timedelta(days=7))
        self.premium_user.profile.save()

        self.expired_premium_user = User.objects.create_user(username="expired_user",
                                                             password=make_password("expiredpass"))
        self.expired_premium_user.profile.is_premium = True
        self.expired_premium_user.profile.premium_expiration_date = make_aware(datetime.now() - timedelta(days=1))
        self.expired_premium_user.profile.save()

    def test_admin_access(self):
        """ Teste si un admin peut accéder aux vues admin. """
        self.client.force_authenticate(user=self.admin)  # 🔥 Force l'authentification pour DRF
        response = self.client.get("/api/admin-challenges/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_free_user_no_access_to_premium(self):
        """ Teste qu'un utilisateur Free ne peut pas accéder aux défis Premium. """
        self.client.force_authenticate(user=self.free_user)
        response = self.client.get("/api/premium-challenges/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_premium_user_access(self):
        """ Teste qu'un utilisateur Premium peut accéder aux défis Premium. """
        self.client.force_authenticate(user=self.premium_user)
        response = self.client.get("/api/premium-challenges/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_expired_premium_user_no_access(self):
        """ Teste qu'un Premium expiré ne peut pas accéder aux défis Premium. """
        self.client.force_authenticate(user=self.expired_premium_user)
        response = self.client.get("/api/premium-challenges/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
