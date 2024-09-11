from django.shortcuts import render, redirect
from .forms import DocumentoForm
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import Documento

def index(request):
    if request.method == 'POST':
        formulario = DocumentoForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('index') 
    else:
        formulario = DocumentoForm()
    
    return render(request, 'apps/EnvioDoc/index.html', {'formulario': formulario})

class Atualizar_forms(UpdateView):
    model = Documento 
    form_class = DocumentoForm 
    template_name = 'apps/EnvioDoc/editar_documento.html'
    success_url = reverse_lazy('busca_documentos') 


    def historico_alteracao(self, **kwargs):
        context = super().historico_alteracao(**kwargs)
        context['historico'] = self.object.history.all()  # Adiciona o histórico ao contexto
        return context
