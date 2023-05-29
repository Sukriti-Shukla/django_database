from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')  # Assuming you will have a 'home' view
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# Create your views here.
