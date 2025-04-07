from django import forms
from .models import Challenge  # Assure-toi que Challenge est bien dans models.py

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ["title", "duration"]  # Assure-toi que ces champs existent dans ton modèle
        widgets = {
            "title": forms.TextInput(attrs={"class": "w-full p-2 border rounded-lg"}),
            "duration": forms.NumberInput(attrs={"class": "w-full p-2 border rounded-lg"}),
        }
