from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from challenges.models import Challenge
from challenges.serializers import ChallengeSerializer
from .permissions import IsAdmin, IsPremiumUser
from .serializers import PasswordResetSerializer, UserRegisterSerializer, UserSerializer


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.send_reset_email()
            return Response({"message": "Email de réinitialisation envoyé."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(generics.GenericAPIView):
    def post(self, request, uid, token):
        try:
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.set_password(request.data.get("new_password"))
                user.save()
                return Response({"message": "Mot de passe réinitialisé."}, status=status.HTTP_200_OK)
            return Response({"error": "Lien invalide."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé."}, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

class AdminChallengeViewSet(viewsets.ModelViewSet):
    """
    Vue réservée aux administrateurs pour gérer tous les défis.
    """
    queryset = Challenge.objects.all().order_by("id")
    serializer_class = ChallengeSerializer
    permission_classes = [IsAdmin]

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # ✅ Gérer les fichiers uploadés

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """ Permet à l'utilisateur de modifier son profil ou de désactiver son compte """
        if "deactivate" in request.data:
            request.user.is_active = False
            request.user.save()
            return Response({"message": "Votre compte a été désactivé."}, status=200)

        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def post(self, request):
        """ Réactiver un compte désactivé """
        user = request.user
        if user.is_active:
            return Response({"message": "Votre compte est déjà actif."}, status=400)

        user.is_active = True
        user.save()
        return Response({"message": "Votre compte a été réactivé avec succès."}, status=200)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reactivate(self, request):
        """ Réactiver un compte désactivé """
        user = request.user
        if user.is_active:
            return Response({"message": "Votre compte est déjà actif."}, status=400)

        user.is_active = True
        user.save()
        return Response({"message": "Votre compte a été réactivé avec succès."}, status=200)

class PremiumChallengeViewSet(viewsets.ModelViewSet):
    """
    Vue réservée aux utilisateurs Premium pour des défis avancés.
    """
    queryset = Challenge.objects.filter(is_premium=True).order_by("id")
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticated, IsPremiumUser]

class FreeChallengeViewSet(viewsets.ModelViewSet):
    """
    Vue réservée aux utilisateurs Free pour des défis avancés.
    """
    queryset = Challenge.objects.filter(is_premium=False).order_by("id")
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticated]

