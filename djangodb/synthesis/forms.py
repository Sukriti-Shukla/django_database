from django import forms
from .models import SynthesisChemical

class SynthesisForm(forms.ModelForm):
    class Meta:
        model = SynthesisChemical
        fields = ['name', 'id', 'precursor_chemicals', 'synthesized_by', 'synthesized_on', 'added_by', 'added_on', 'proceduretype', 'proceduresubtype', 'description', 'custom_parameters', 'additional_fields', 'files']
