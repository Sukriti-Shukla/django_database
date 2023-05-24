from django import forms
from .models import Chemical

class ChemicalForm(forms.ModelForm):
    class Meta:
        model = Chemical
        fields = ['labitemtype','labitemsubtype','labitemid','labitemname', 'documents', 'json_data']

class SearchForm(forms.Form):
    query = forms.CharField(label='Search')

