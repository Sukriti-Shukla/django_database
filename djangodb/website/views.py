from django.shortcuts import render, redirect
from .models import Chemical
from .forms import ChemicalForm
from django.contrib import messages

# Create your views here.
def home(request):
    all_chemicals = Chemical.objects.all()
    return render(request, 'home.html', {'all': all_chemicals})

def input(request):
    if request.method == 'POST':
        form = ChemicalForm(request.POST or None)
        if form.is_valid():
            form.save()
        else:
            labitemtype = request.POST['labitemtype']
            labitemsubtype = request.POST['labitemsubtype']
            labitemid = request.POST['labitemid']
            labitemname = request.POST['labitemname']
            messages.success(request, ('There was an error in your form. Please try again.'))
            #return redirect('input')
            return render(request, 'input.html',{'labitemtype': labitemtype, 'labitemsubtype': labitemsubtype, 'labitemid': labitemid, 'labitemname': labitemname})
        messages.success(request, ('Item has been added to the database!'))
        return redirect('home')
    else:

        return render(request, 'input.html',{})
