from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
# Create your views here.

def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        # Redirect to a success page.
       
        else:
        # Return an 'invalid login' error message.
             messages.error(request, 'Invalid login credentials. Please try again.')
             return redirect('login')
      

    else:
        return render(request, 'registration/login.html',{})

def logout_user(request):
    logout(request)
    return redirect('/')

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
             form.save()
             username = form.cleaned_data['username']
             password = form.cleaned_data['password1']
             user = authenticate(username=username, password=password)
             login(request, user)
             messages.success(request, ('Your profile was successfully registered!'))
             return redirect('/')
    else:
        form = RegisterUserForm()
    return render(request, 'registration/register_user.html',{'form': form,})

    
def main_page(request):
    
    return render(request, 'main_page.html',{})


