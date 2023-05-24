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
    all_chemicals = Chemical.objects.all()
    if request.method == 'POST':
        form = ChemicalForm(request.POST, request.FILES)
        if form.is_valid():
            additional_fields = {}
            custom_names = []
            for key, value in request.POST.items():
                if key.startswith('custom_field_key_'):
                    field_index = key.split('_')[-1]
                    field_name =request.POST.get(f'custom_field_key_{field_index}')
                    if field_name!="":
                        custom_names.append(field_name)
                    
                    field_value = request.POST.get(f'additional_field_value_{key.split("_")[-1]}')
                    if field_name!="":
                        additional_fields[field_name] = field_value
                elif key.startswith('additional_field_name_'):
                    field_index = key.split('_')[-1]
                    field_name = value
                    field_value = request.POST.get(f'additional_field_value_{key.split("_")[-1]}')
                    if field_name!="custom":
                        additional_fields[field_name] = field_value
            
            chemical = form.save(commit=False)
            chemical.custom_fields = custom_names
            chemical.additional_fields = additional_fields
            chemical.json_data = json.dumps(additional_fields)
            chemical.save()
            messages.success(request, 'Item has been added to the database!')
            return redirect('home')
        else:
            messages.error(request, 'There was an error in your form. Please try again.')
    else:
        form = ChemicalForm()
    return render(request, 'input.html', {'form': form,'all': all_chemicals})

def input_template(request):
    selected_type = None
    additional_fields = []
    all_chemicals = Chemical.objects.all()
    
    if request.method == 'POST':
        selected_type = request.POST.get('labitemtype')
        selected_chemical = all_chemicals.filter(labitemtype=selected_type).first()
        
        if selected_chemical:
            additional_fields = selected_chemical.get_additional_fields()
            
            # Process the input values for additional_fields
            for field in additional_fields:
                field_key = field['key']
                field_value = request.POST.get(field_key)
                # Perform further processing or validation on the field value
                
                # Example: Print the key-value pair
                print(field_key, field_value)
    
    types = all_chemicals.order_by().values_list('labitemtype', flat=True).distinct()
    context = {'additional_fields': additional_fields, 'types': types, 'selected_type': selected_type, 'all': all_chemicals}
    
    return render(request, 'input_template.html', context)



def update_event(request, event_id):
    all_chemicals = Chemical.objects.all()
    event = Chemical.objects.get(id=event_id)
    # if request.method == 'POST':
    #     form = ChemicalForm(request.POST, request.FILES, instance=event)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Event has been updated!')
    #         return redirect('home')
    #     else:
    #         messages.error(request, 'There was an error in your form. Please try again.')
    # else:
    #     form = ChemicalForm(instance=event)
    # return render(request, 'update_event.html', {'form': form, 'event': event, 'all': all_chemicals})
    if request.method == 'POST':
        form = ChemicalForm(request.POST, request.FILES, instance=event)
        
        if form.is_valid():
            additional_fields = {}
            custom_names = []
            
            for key, value in request.POST.items():
                if key.startswith('custom_field_key_'):
                    field_index = key.split('_')[-1]
                    field_name = request.POST.get(f'custom_field_key_{field_index}')
                    if field_name != "":
                        custom_names.append(field_name)
                    
                    field_value = request.POST.get(f'additional_field_value_{field_index}')
                    if field_name != "":
                        additional_fields[field_name] = field_value
                elif key.startswith('additional_field_name_'):
                    field_index = key.split('_')[-1]
                    field_name = value
                    field_value = request.POST.get(f'additional_field_value_{field_index}')
                    if field_name != "custom":
                        additional_fields[field_name] = field_value
            
            event.custom_fields = custom_names
            event.json_data = json.dumps(additional_fields)
            form.save()
            
            messages.success(request, 'Event has been updated!')
            return redirect('home')
        else:
            messages.error(request, 'There was an error in your form. Please try again.')
    else:
        form = ChemicalForm(instance=event)
    
    context = {
        'form': form,
        'event': event,
        'all': all_chemicals,
    }
    return render(request, 'update_event.html', context)

# delete event
def delete_event(request, event_id):
    event = Chemical.objects.get(id=event_id)
    event.delete()
    messages.success(request, 'Event has been deleted!')
    return redirect('home')

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