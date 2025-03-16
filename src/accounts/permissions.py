from datetime import date

from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Permission personnalisée : seuls les admins peuvent accéder à certaines ressources.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == "admin"

class IsPremiumUser(permissions.BasePermission):
    """
    Permission qui restreint l'accès aux utilisateurs premium uniquement.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or not user.profile.is_premium:
            return False

        # ✅ Vérifier si `premium_expiration_date` est un datetime, et convertir en date si nécessaire
        expiration_date = user.profile.premium_expiration_date
        if hasattr(expiration_date, 'date'):  # Vérifie si c'est un datetime
            expiration_date = expiration_date.date()  # Convertit en date

        return expiration_date >= date.today()

