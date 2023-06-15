from django import forms
from .models import Chemical
from django.forms import TextInput, NumberInput, FileInput, Textarea

class ChemicalForm(forms.ModelForm):
    class Meta:
        model = Chemical
        fields = ['labitemtype','labitemsubtype','labitemid','labitemname', 'documents', 'files', 'json_data','additional_fields','custom_fields']
        widgets = {
            'labitemtype': TextInput(attrs={'class': 'form-control'}),
            'labitemsubtype': TextInput(attrs={'class': 'form-control'}),
            'labitemid': NumberInput(attrs={'class': 'form-control'}),
            'labitemname': TextInput(attrs={'class': 'form-control'}),
            'documents': FileInput(attrs={'class': 'form-control-file'}),
            'files': FileInput(attrs={'class': 'form-control-file'}),
            'json_data': Textarea(attrs={'class': 'form-control'}),
            'additional_fields': Textarea(attrs={'class': 'form-control'}),
            'custom_fields': TextInput(attrs={'class': 'form-control'}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(label='Search')


class UploadFileForm(forms.Form):
    file = forms.FileField()