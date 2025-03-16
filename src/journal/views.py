from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.permissions import IsPremiumUser
from .models import JournalEntry
from .serializers import JournalEntrySerializers
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner




class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializers
    permission_classes = [IsAuthenticated, IsOwner]

    # Filtrer pour que l'utilisateur ne voie que ses propres entrées
    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    # Associer automatiquement l'utilisateur lors de la création
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdvancedStatsView(APIView):
    """
    Vue qui retourne des statistiques avancées, accessible uniquement aux Premiums.
    """
    permission_classes = [IsAuthenticated, IsPremiumUser]

    def get(self, request):
        # Simulation de stats avancées
        data = {
            "total_completed_challenges": 42,
            "average_challenge_duration": "3 jours",
            "top_category": "Développement personnel"
        }
        return Response(data)
