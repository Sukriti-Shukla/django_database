from django.shortcuts import render
from labitems.models import Chemical
from synthesis.models import SynthesisChemical
from django.db.models import Q
import json
from django.http import JsonResponse
def homepage(request):
    
    return render(request, 'homepage.html',{})

def view_data(request):
    synthesischemicals = SynthesisChemical.objects.all()
    chemicals = Chemical.objects.all()
    # iterate over synthesischemicals and deserialize 'precursors' field
    for chem in synthesischemicals:
        if isinstance(chem.precursor_chemicals, str):  # check if it is a JSON string
            chem.precursor_chemicals = json.loads(chem.precursor_chemicals)

    return render(request, 'view_data.html', {'synthesischemicals': synthesischemicals, 'chemicals': chemicals})

def chemical_data(request):
    chemicals = Chemical.objects.all()
    return render(request, 'chemical_data.html', {'chemicals': chemicals})
 # Get Chemical data
def chemical_search(request):
    query = request.GET.get('q', '')

    chemicals = Chemical.objects.filter(
        Q(labitemname__icontains=query)  
    )

    return render(request, 'chemical_data.html', {
        'chemicals': chemicals,
    })

def synthesis_search(request):
    query = request.GET.get('q', '')

    synthesischemicals = SynthesisChemical.objects.filter(
        Q(name__icontains=query)
    )

    return render(request, 'view_data.html', {
        'synthesischemicals': synthesischemicals,
    })

