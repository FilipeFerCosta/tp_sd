# accounts/views.py
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # Importa o formulário personalizado

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'apps/accounts/register.html', {'form': form})

# accounts/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('listar_documentos')  # Redireciona para a home após login
    else:
        form = AuthenticationForm()
    return render(request, 'apps/accounts/login.html', {'form': form})



