from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import RegistroAuditoria  
from TP_DECOM_SD.EnvioDoc.models import Documento

# Sinal para criação de um documento
@receiver(post_save, sender=Documento)
def registrar_auditoria_documento(sender, instance, **kwargs):
    RegistroAuditoria.objects.create(
        usuario=instance.autor,  # Use 'autor' para acessar o usuário associado
        acao=f"Documento {instance.id} criado."
    )

# Sinal para deleção de um documento
@receiver(post_delete, sender=Documento)
def registrar_auditoria_documento_deletado(sender, instance, **kwargs):
    acao = f'Documento "{instance.titulo}" deletado.'
    RegistroAuditoria.objects.create(usuario=instance.autor, acao=acao)
