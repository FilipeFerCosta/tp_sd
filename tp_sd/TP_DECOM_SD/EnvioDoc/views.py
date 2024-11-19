from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .forms import DocumentoForm
from .models import Documento

class DocumentoCreateView(LoginRequiredMixin, CreateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'apps/EnvioDoc/index.html'
    success_url = reverse_lazy('listar_documentos')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Define o autor como o usuário logado
        return super().form_valid(form)

class DocumentoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'apps/EnvioDoc/editar_documento.html'
    success_url = reverse_lazy('listar_documentos')

    def test_func(self):
        documento = self.get_object()
        return self.request.user == documento.autor or self.request.user.is_superuser


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        context['historico_alteracao'] = instance.history.all()
        return context
