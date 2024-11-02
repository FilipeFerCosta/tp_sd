from .forms import DocumentoForm
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import Documento
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def index(request):
    if request.method == 'POST':
        formulario = DocumentoForm(request.POST, request.FILES)
        if formulario.is_valid():
            documento = formulario.save(commit=False)
            documento.autor = request.user
            documento.save()
            formulario.save_m2m()  # Para salvar a equipe selecionada
            messages.success(request, "Documento criado com sucesso!")
            return redirect('listar_documentos')
    else:
        formulario = DocumentoForm()
    
    return render(request, 'apps/EnvioDoc/index.html', {'formulario': formulario})

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

class Atualizar_forms(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Documento 
    form_class = DocumentoForm 
    template_name = 'apps/EnvioDoc/editar_documento.html'
    success_url = reverse_lazy('listar_documentos') 

    def test_func(self):
        documento = self.get_object()
        # Verifica se o usuário é o autor ou um professor ou administrador
        return self.request.user == documento.autor or self.request.user.is_professor() or self.request.user.is_administrador()

    def handle_no_permission(self):
        messages.error(self.request, "Você não tem permissão para editar este documento.")
        return redirect('listar_documentos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()  
        context['historico_alteracao'] = instance.history.all()  
        return context
