# forms.py
from django import forms
from .models import OffreEmploi

class OffreEmploiForm(forms.ModelForm):
    class Meta:
        model = OffreEmploi
        fields = ['titre', 'entreprise', 'localisation', 'type_contrat', 'categorie', 'description', 'salaire_min', 'salaire_max']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'salaire_min': forms.NumberInput(attrs={'step': '100'}),
            'salaire_max': forms.NumberInput(attrs={'step': '100'}),
        }
