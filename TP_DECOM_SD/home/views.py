from django.views.generic import ListView, DetailView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from TP_DECOM_SD.EnvioDoc.models import Documento
from django.db.models import Q

# View index
class DocumentoListView(ListView):
    model = Documento
    template_name = 'apps/home/listar_documentos.html'
    context_object_name = 'documentos'
    paginate_by = 10
    ordering = 'titulo'

    def get_queryset(self):
        termo_busca = self.request.GET.get('q', '')
        queryset = Documento.objects.all()
        if termo_busca:
            queryset = queryset.filter(
                Q(titulo__icontains=termo_busca) |
                Q(autores__icontains=termo_busca) |
                Q(revista__icontains=termo_busca) |
                Q(palavras_chave__icontains=termo_busca) |
                Q(resumo__icontains=termo_busca) |
                Q(data_publicacao__icontains=termo_busca)
            )
        ordenacao = self.request.GET.get('ordenacao', 'titulo')
        return queryset.order_by(ordenacao)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['ordenacao'] = self.request.GET.get('ordenacao', 'titulo')
        return context


class DocumentoDetailView(DetailView):
    model = Documento
    template_name = 'apps/home/visualizar_documento.html'
    context_object_name = 'documento'
    pk_url_kwarg = 'documento_id'

class DocumentoDeleteView(DeleteView):
    model = Documento
    template_name = 'apps/home/deletar_documento.html'
    success_url = reverse_lazy('listar_documentos')
    pk_url_kwarg = 'documento_id'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Documento excluído com sucesso!')
        return super().delete(request, *args, **kwargs)