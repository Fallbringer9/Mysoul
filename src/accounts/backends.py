from django.contrib.auth.backends import ModelBackend


class CustomAuthBackend(ModelBackend):
    """ Bloque la connexion des utilisateurs désactivés """
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)
        if user and not user.is_active:
            return None  # Empêche la connexion d'un compte désactivé
        return user
