from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from TP_DECOM_SD.EnvioDoc.models import Documento
from django.db.models import Q
from django.views import View
from TP_DECOM_SD.accounts.models import User

# View index
class DocumentoListView(LoginRequiredMixin, ListView):
    model = Documento
    template_name = 'apps/home/listar_documentos.html'
    context_object_name = 'documentos'
    paginate_by = 10
    ordering = 'titulo'
    login_url = 'login'

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

# View para visualizar documento
class DocumentoDetailView(LoginRequiredMixin, DetailView):
    model = Documento
    template_name = 'apps/home/visualizar_documento.html'
    context_object_name = 'documento'
    pk_url_kwarg = 'documento_id'
    login_url = 'login'

# View para deletar documento
class DocumentoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Documento
    template_name = 'apps/home/deletar_documento.html'
    success_url = reverse_lazy('listar_documentos')
    pk_url_kwarg = 'documento_id'
    login_url = 'login'

    def test_func(self):
        documento = self.get_object()
        return (
            self.request.user == documento.autor or 
            self.request.user.is_superuser or
            self.request.user.groups.filter(name='professor').exists()
        )


    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Documento excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

class UserListView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'apps/home/lista_usuarios.html'

    def test_func(self):
        return self.request.user.is_administrador()  # Permissão para acessar apenas administradores

    def get(self, request, *args, **kwargs):
        usuarios = User.objects.all()  # Obtém todos os usuários
        return render(request, self.template_name, {'usuarios': usuarios})

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        novo_cargo = request.POST.get('cargo')
        user = get_object_or_404(User, id=user_id)

        if novo_cargo in dict(User.CARGO_CHOICES).keys():
            user.cargo = novo_cargo
            user.save()
            messages.success(request, f"Cargo de {user.username} atualizado para {novo_cargo}.")
        else:
            messages.error(request, "Cargo inválido.")

        return redirect('listar_usuarios')  # Redireciona para a página da lista de usuários