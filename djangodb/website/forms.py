from django import forms
from .models import Chemical

class ChemicalForm(forms.ModelForm):
    class Meta:
        model = Chemical
        fields = ['labitemtype','labitemsubtype','labitemid','labitemname', 'documents', 'files', 'json_data','additional_fields','custom_fields']

class SearchForm(forms.Form):
    query = forms.CharField(label='Search')

from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()


