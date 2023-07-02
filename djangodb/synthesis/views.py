from django.shortcuts import render, redirect
from labitems.models import Chemical
from .forms import SynthesisForm
from django.db.models import Q
from django.http import JsonResponse
from .models import SynthesisChemical
import json
from django.http import HttpResponse
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline
from django.shortcuts import get_object_or_404

def search_chemicals(request):
    if 'term' in request.GET:
        chemicals = Chemical.objects.filter(labitemname__icontains=request.GET.get('term'))
        labitems = [{'id': chem.labitemid, 'name': chem.labitemname} for chem in chemicals]
        return JsonResponse(labitems, safe=False)
    return JsonResponse([], safe=False)

def index(request):
    q = request.GET.get('q')

    if q:
        vector = SearchVector('labitemname', 'labitemtype')
        query = SearchQuery(q)
        search_headline = SearchHeadline('labitemname', query)

        
        chemicals = Chemical.objects.annotate(rank=SearchRank(vector, query)).annotate(headline=search_headline).filter(rank__gte=0.001).order_by('-rank')
    else:
        chemicals = None

    
    context = {'chemicals' : chemicals}
    return JsonResponse(list(chemicals), safe=False)

def search_precursors(request):
    print(request.GET) 
    query = request.GET.get('q', '')
    if query:
        precursors = list(Chemical.objects.filter(Q(labitemname__icontains=query)).values('labitemid', 'labitemname'))
        synthesis_chemicals = list(SynthesisChemical.objects.filter(Q(name__icontains=query)).values('id', 'name'))
        precursors.extend(synthesis_chemicals)
    else:
        precursors = list(Chemical.objects.values('labitemid', 'labitemname'))
        synthesis_chemicals = list(SynthesisChemical.objects.values('id', 'name'))
        precursors.extend(synthesis_chemicals)

    return JsonResponse(precursors, safe=False)



def synthesis_input(request):
    chemicals = Chemical.objects.all()

    if request.method == 'POST':
        
        try:
            precursor_chemicals_json = request.POST.get('precursor_chemicals', '{}')
            precursor_chemicals = json.loads(precursor_chemicals_json)
        except json.JSONDecodeError:
            return HttpResponse("Error parsing JSON data for precursor chemicals", status=400)
        
       
        post_data = request.POST.copy()
        post_data['precursor_chemicals'] = precursor_chemicals

        form = SynthesisForm(post_data, request.FILES)
        if form.is_valid():
            additional_fields = {}
            custom_names = []
            for key, value in request.POST.items():
                if key.startswith('custom_field_key_'):
                    field_index = key.split('_')[-1]
                    field_name = request.POST.get(f'custom_field_key_{field_index}')
                    
                    if field_name != "":
                        custom_names.append(field_name)
                        if field_name not in additional_fields:
                            additional_fields[field_name] = {}
                        
                        timestamps = request.POST.getlist(f'additional_field_timestamp_{field_index}')
                        values = request.POST.getlist(f'additional_field_value_{field_index}')
                        
                        for i in range(len(timestamps)):
                            if timestamps[i] != "" and values[i] != "":
                                additional_fields[field_name][timestamps[i]] = values[i]
                                
                elif key.startswith('additional_field_name_'):
                    field_index = key.split('_')[-1]
                    field_name = value
                    
                    if field_name != "" and field_name != "custom":
                        if field_name not in additional_fields:
                            additional_fields[field_name] = {}
                        
                        timestamps = request.POST.getlist(f'additional_field_timestamp_{field_index}')
                        values = request.POST.getlist(f'additional_field_value_{field_index}')
                        
                        for i in range(len(timestamps)):
                            if timestamps[i] != "" and values[i] != "":
                                additional_fields[field_name][timestamps[i]] = values[i]

            synthesis_chemical = form.save()
            synthesis_chemical.custom_parameters= custom_names
            synthesis_chemical.additional_fields = additional_fields
            synthesis_chemical.save()
            return redirect('synthesis_input')  
        else:
            
            pass
    else:
        form = SynthesisForm()

    return render(request, 'synthesis_input.html', {'chemicals': chemicals, 'form': form})

def synthesischemical_list(request):
    synthesischemicals = SynthesisChemical.objects.all()
    chemicals = Chemical.objects.all()
    
    for chem in synthesischemicals:
        if isinstance(chem.precursor_chemicals, str):
            chem.precursor_chemicals = json.loads(chem.precursor_chemicals)

    return render(request, 'synthesischemical_list.html', {'synthesischemicals': synthesischemicals, 'chemicals': chemicals})

def synthesischemical_search(request):
    query = request.GET.get('q', '')

    synthesischemicals = SynthesisChemical.objects.filter(
        Q(name__icontains=query)
    )

    return render(request, 'synthesischemical_list.html', {
        'synthesischemicals': synthesischemicals,
    })

def precursor_list_search(request):
    query = request.GET.get('q', '')
    chemicals = Chemical.objects.filter(Q(labitemname__iexact=query))
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'chemical.html', {'precursor_chemicals': chemicals})
    else:
        return render(request, 'synthesischemical_list.html', {'precursor_chemicals': chemicals})
def synthesischemical_detail(request, synthesischemical_id):
    synthesischemical = get_object_or_404(SynthesisChemical, pk=synthesischemical_id)

    if isinstance(synthesischemical.precursor_chemicals, str):
        synthesischemical.precursor_chemicals = json.loads(synthesischemical.precursor_chemicals)

    return render(request, 'synthesischemical_detail.html', {'synthesischemical': synthesischemical})