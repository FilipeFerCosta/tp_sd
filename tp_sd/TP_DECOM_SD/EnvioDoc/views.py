from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .forms import DocumentoForm
from .models import Documento
from dotenv import load_dotenv
import os
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
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
        # Processar a validação do formulário
        response = super().form_valid(form)

        # Obter o documento atualizado
        documento = self.object

        # Configurações do e-mail
        subject = f"Atualização no artigo: {documento.titulo}"
        message = (
            f"O artigo '{documento.titulo}' foi atualizado.\n\n"
            f"Resumo da alteração:\n"
            f"{documento.resumo}\n\n"
            f"Confira no sistema para mais detalhes."
        )
        from_email = os.getenv('EMAIL_HOST_USER')
        
        if not from_email:
            raise ValueError("EMAIL_HOST_USER não configurado no .env")
        
        # Enviar e-mail para o destinatário fixo
        recipient_list = ["rafarodrigues919@gmail.com"] #Troque de acordo a necessidade

        # Verificar se há destinatário
        if not recipient_list:
            return HttpResponse('Nenhum destinatário válido encontrado.') 

        # Enviar e-mail
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Header inválido encontrado ao tentar enviar o e-mail.')
        except Exception as e:
            # Logar o erro no console ou no sistema de logs
            print(f"Erro ao enviar e-mail: {e}")
            return HttpResponse('Ocorreu um problema ao enviar o e-mail.')

        return response
