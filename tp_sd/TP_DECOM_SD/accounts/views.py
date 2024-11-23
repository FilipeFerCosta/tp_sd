from django.shortcuts import render, redirect
from .models import RegistroAuditoria
from .forms import CustomUserCreationForm  # Importa o formulário personalizado
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'apps/accounts/register.html', {'form': form})


@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('listar_documentos')  

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('listar_documentos')  
    else:
        form = AuthenticationForm()
    return render(request, 'apps/accounts/login.html', {'form': form})



class ListaRegistrosAuditoria(LoginRequiredMixin, ListView):
    model = RegistroAuditoria
    template_name = 'apps/accounts/lista_registros_auditoria.html'  
    context_object_name = 'registros_auditoria'
    paginate_by = 10

    def get_queryset(self):
        return RegistroAuditoria.objects.order_by('-timestamp')
