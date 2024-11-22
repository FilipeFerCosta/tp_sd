from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .forms import DocumentoForm
from .models import Documento
from django.core.mail import send_mail
from django.contrib.auth.models import User
from dotenv import load_dotenv
import os

# Carregar o arquivo .env
load_dotenv()

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

    def form_valid(self, form):
        response = super().form_valid(form)

        # Obtenha o objeto atualizado
        documento = self.object
        
        # Detalhes do e-mail
        subject = f"Atualização no artigo: {documento.titulo}"
        message = (
            f"O artigo '{documento.titulo}' foi atualizado.\n\n"
            f"Resumo da alteração:\n"
            f"{documento.descricao}\n\n"  # Adapte o campo para mostrar o conteúdo relevante
            f"Confira no sistema para mais detalhes."
        )
        # Carregar o e-mail do remetente do .env
        from_email = os.getenv('EMAIL_HOST_USER')

        # Enviar e-mails para todos os usuários
        users = User.objects.all()
        recipient_list = [user.email for user in users if user.email]

        if recipient_list:  # Verifica se há destinatários com e-mails
            send_mail(
                subject, message, from_email, recipient_list, fail_silently=False
            )

        return response
