from django.shortcuts import render, redirect
from .models import Chemical
from .forms import ChemicalForm
from django.contrib import messages
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline

import json

# Create your views here.
def home(request):
    all_chemicals = Chemical.objects.all()
    return render(request, 'home.html', {'all': all_chemicals})

# def input(request):
#     if request.method == 'POST':
#         form = ChemicalForm(request.POST, request.FILES)
#         if form.is_valid():
#             additional_fields = {}
#             for key, value in request.POST.items():
#                 if key.startswith('additional_field'):
#                     additional_fields[key] = value
#             chemical = form.save(commit=False)
#             chemical.json_data = json.dumps(additional_fields)
#             chemical.save()
#             messages.success(request, 'Item has been added to the database!')
#             return redirect('home')
#         else:
#             messages.error(request, 'There was an error in your form. Please try again.')
#     else:
#         form = ChemicalForm()
#     return render(request, 'input.html', {'form': form})
def input(request):
    if request.method == 'POST':
        form = ChemicalForm(request.POST, request.FILES)
        if form.is_valid():
            additional_fields = {}
            for key, value in request.POST.items():
                if key.startswith('additional_field_name_'):
                    field_name = value
                    field_value = request.POST.get(f'additional_field_value_{key.split("_")[-1]}')
                    additional_fields[field_name] = field_value
            chemical = form.save(commit=False)
            chemical.json_data = json.dumps(additional_fields)
            chemical.save()
            messages.success(request, 'Item has been added to the database!')
            return redirect('home')
        else:
            messages.error(request, 'There was an error in your form. Please try again.')
    else:
        form = ChemicalForm()
    return render(request, 'input.html', {'form': form})

def index(request):
    q = request.GET.get('q')

    if q:
        vector = SearchVector('labitemtype', 'labitemsubtype')
        query = SearchQuery(q)
        search_headline = SearchHeadline('labitemname', query)

        #videos = Video.objects.filter(title__search=q)
        #videos = Video.objects.annotate(search=vector).filter(search=query)
        #videos = Video.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.001).order_by('-rank')
        chemicals = Chemical.objects.annotate(rank=SearchRank(vector, query)).annotate(headline=search_headline).filter(rank__gte=0.001).order_by('-rank')
    else:
        chemicals = None

    
    context = {'chemicals' : chemicals}
    return render(request, 'index.html', context)