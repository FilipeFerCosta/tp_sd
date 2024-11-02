from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.conf import settings
def validar_ano(value):
    if value < 1900 or value > 2024:
        raise ValidationError(_('O ano deve estar entre 1900 e 2024.'))

class Documento(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documentos_criados"
    )
    equipe = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="equipes"
    )
    resumo = models.TextField()
    palavras_chave = models.CharField(max_length=255)
    data_publicacao = models.PositiveIntegerField(validators=[validar_ano])
    revista = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to='documentos/')
    history = HistoricalRecords() 

    def __str__(self):
        return self.titulo
    
    def clean(self):
        super().clean()
        if not self.arquivo:
            raise ValidationError(_('O arquivo é obrigatório.'))
