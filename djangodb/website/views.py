from django.shortcuts import render, redirect
from .models import Chemical
from .forms import ChemicalForm, UploadFileForm
from django.contrib import messages
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline
import pandas as pd
import json
from django.contrib.auth.decorators import login_required
import yaml
from django.http import JsonResponse,Http404
from django.conf import settings
import os
from .field_type import field_type
from django.templatetags.static import static
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
# def get_suggested_fields(labitemsubtype):
#     # Construct the file name based on the labitemsubtype
#     yaml_file = f'{labitemsubtype.replace(" ", "_")}_fields.yaml'
    
#     # Construct the absolute path to the yaml file
#     yaml_file_path = os.path.join(settings.STATIC_ROOT, 'yaml', yaml_file)
    
#     with open(yaml_file_path, 'r') as file:
#         # The yaml.safe_load function can parse a YAML file and return the resulting Python data.
#         suggested_fields = yaml.safe_load(file)
        
#     return suggested_fields
# def fetch_subtype_fields(request, subtype):
#     fields = get_suggested_fields(subtype.replace("-", " "))
#     return JsonResponse(fields, safe=False)
def get_suggested_fields(labitemsubtype):
    # Construct the file name based on the labitemsubtype
    yaml_file = f'{labitemsubtype.replace(" ", "_")}_fields.yaml'
    
    # Construct the absolute path to the yaml file
    #yaml_file_path = static(f'website/yaml/{yaml_file}')
    yaml_file_path = os.path.join(settings.STATIC_ROOT, 'yaml', yaml_file)
    # Check if the file exists
    if not os.path.isfile(yaml_file_path):
        raise FileNotFoundError(f"No YAML file found for subtype '{labitemsubtype}'")
        
    with open(yaml_file_path, 'r') as file:
        try:
            # The yaml.safe_load function can parse a YAML file and return the resulting Python data.
            suggested_fields = yaml.safe_load(file)
        except yaml.YAMLError as error:
            raise yaml.YAMLError(f"Error parsing YAML file: {error}")
            
    return suggested_fields

def fetch_subtype_fields(request):
    subtype = request.GET.get('subtype', '')
    subtype = subtype.replace(' ', '_')  # replace spaces with underscore
    #fields = subtypes.get(subtype, {})
    fields = field_type.get(subtype, {})
    return JsonResponse(fields)

def input(request):
    
    all_chemicals = Chemical.objects.all()
    if request.method == 'POST':
        form = ChemicalForm(request.POST, request.FILES)
        if form.is_valid():
            additional_fields = {}
            custom_names = []
            for key, value in request.POST.items():
                if key in field_type[request.POST.get('labitemsubtype').replace(" ", "_")]:
                    additional_fields[key] = value
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
            
            chemical = form.save(commit=False)
            chemical.custom_fields = custom_names
            chemical.additional_fields = additional_fields
            chemical.json_data = json.dumps(additional_fields)
            chemical.last_modified_by = request.user if request.user.is_authenticated else None
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


@login_required
def update_event(request, event_id):
    all_chemicals = Chemical.objects.all()
    event = Chemical.objects.get(id=event_id)
    form = ChemicalForm(request.POST or None, instance=event)
        
    if form.is_valid():
        chemical = form.save(commit=False)
        chemical.user = request.user  # Assign the current user to the 'user' field of the chemical
        chemical.save()
        messages.success(request, 'Event has been updated!')
        return redirect('home')
    return render(request, 'update_event.html', {'form': form, 'event': event, 'all': all_chemicals})
    

# delete event
def delete_event(request, event_id):
    event = Chemical.objects.get(id=event_id)
    event.delete()
    messages.success(request, 'Event has been deleted!')
    return redirect('home')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            data = pd.read_csv(request.FILES['file'])
            for index, row in data.iterrows():
                labitemtype = row.get('labitemtype', '')
                labitemsubtype = row.get('labitemsubtype', '')
                labitemid = row.get('labitemid', '')
                labitemname = row.get('labitemname', '')
                
                # Get additional fields
                additional_fields = row.to_dict()
                for field in ['labitemtype', 'labitemsubtype', 'labitemid', 'labitemname']:
                    if field in additional_fields:
                        del additional_fields[field]

                # Create new Chemical object
                Chemical.objects.create(
                    labitemtype=labitemtype,
                    labitemsubtype=labitemsubtype,
                    labitemid=labitemid,
                    labitemname=labitemname,
                    json_data=json.dumps(additional_fields)  # Store additional fields as JSON
                )

            return redirect('home')  # Redirect to a new page when done
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
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