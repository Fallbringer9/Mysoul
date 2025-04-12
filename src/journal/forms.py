from django import forms
from .models import JournalEntry

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['mood', 'gratitude_note']
        widgets = {
            'mood': forms.Select(attrs={
                'class': 'w-full border border-green-300 rounded-md p-2 shadow-sm'
            }),
            'gratitude_note': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Exprime ta gratitude ou ton ressenti...',
                'class': 'w-full border border-green-300 rounded-md p-2 shadow-sm'
            }),
        }
        labels = {
            'mood': "Ton humeur du jour",
            'gratitude_note': "Gratitude ou réflexion personnelle",
        }

