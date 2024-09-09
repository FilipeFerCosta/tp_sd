from django.shortcuts import render, redirect
from .forms import DocumentoForm

def index(request):
    if request.method == 'POST':
        formulario = DocumentoForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('url_sucesso') 
    else:
        formulario = DocumentoForm()
    
    return render(request, 'apps/EnvioDoc/index.html', {'formulario': formulario})
