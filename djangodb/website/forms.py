from django import forms
from .models import Chemical

class ChemicalForm(forms.ModelForm):
    class Meta:
        model = Chemical
        fields = ['labitemtype','labitemsubtype','labitemid','labitemname']
