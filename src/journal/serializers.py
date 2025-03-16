from rest_framework import serializers
from .models import JournalEntry


class JournalEntrySerializers(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id', 'date', 'mood', 'formatted_date']

    def validate_sleep_hour(self, value):
        if value is not None and ( value < 0 or value > 24):
            raise serializers.ValidationError("Le nombre d'heure doit être compris en 0 et 24.")
        return True

    def get_formatted_date(self, obj):
        return obj.date.strftime("%d %B %Y")