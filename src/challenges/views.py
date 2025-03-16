from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters

from accounts.permissions import IsPremiumUser
from .models import Challenge
from .serializers import ChallengeSerializer
from journal.permissions import IsOwner  # Utiliser la permission déjà créée

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority']  # Permet de filtrer par statut et priorité
    search_fields = ['title', 'description']  # Permet la recherche par mot-clé
    ordering_fields = ['created_at', 'deadline']  # Permet de trier par date de création et deadline

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Challenge.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Marquer un défi comme terminé"""
        challenge = self.get_object()  # Récupère le défi demandé

        if challenge.status == "completed":
            return Response({"message": "Ce challenge est déjà terminé."}, status=status.HTTP_400_BAD_REQUEST)

        challenge.status = "completed"
        challenge.save()
        return Response({"message": "Challenge marqué comme terminé."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def fail(self, request, pk=None):
        """Marquer un défi comme abandonné"""
        challenge = self.get_object()  # Récupère le défi demandé

        if challenge.status == "failed":
            return Response({"message": "Ce challenge est déjà abandonné."}, status=status.HTTP_400_BAD_REQUEST)

        challenge.status = "failed"
        challenge.save()
        return Response({"message": "Challenge marqué comme abandonné."}, status=status.HTTP_200_OK)



class PremiumChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    """Vue pour les défis Premium, accessibles uniquement aux utilisateurs Premium"""
    serializer_class = ChallengeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPremiumUser]

    def get_queryset(self):
        """Filtrer les défis Premium de l'utilisateur connecté"""
        if not self.request.user.is_authenticated:
            return Challenge.objects.none()

        return Challenge.objects.filter(user=self.request.user, is_premium=True).order_by('id')


class FreeChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    """Vue pour les défis gratuits, accessibles à tous"""
    serializer_class = ChallengeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filtrer les défis gratuits de l'utilisateur connecté"""
        if not self.request.user.is_authenticated:
            return Challenge.objects.none()

        return Challenge.objects.filter(user=self.request.user, is_premium=False).order_by('id')











