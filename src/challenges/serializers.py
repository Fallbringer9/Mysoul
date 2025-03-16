from datetime import datetime, timezone

from rest_framework import serializers
from .models import Challenge

class ChallengeSerializer(serializers.ModelSerializer):
    time_remaining = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'status', 'priority', 'deadline', 'created_at', 'updated_at', 'time_remaining', 'is_overdue']
        read_only_fields = ['created_at', 'updated_at']

    def get_time_remaining(self, obj):
        """Calcule le temps restant avant la deadline"""
        if obj.deadline:
            delta = obj.deadline - datetime.now(timezone.utc)
            return str(delta) if delta.total_seconds() > 0 else "Dépassé"
        return "Aucune deadline"

    def get_is_overdue(self, obj):
        """Renvoie True si la deadline est dépassée"""
        return obj.deadline and obj.deadline < datetime.now(timezone.utc)

    def validate_deadline(self, value):
        """Empêche l'ajout d'une deadline déjà passée"""
        if value < datetime.now(timezone.utc):
            raise serializers.ValidationError("La deadline ne peut pas être dans le passé.")
        return value
