from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    CARGO_CHOICES = (
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('administrador', 'Administrador'),
    )
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, default='aluno')

    def is_aluno(self):
        return self.cargo == 'aluno'

    def is_professor(self):
        return self.cargo == 'professor'

    def is_administrador(self):
        return self.cargo == 'administrador'


class RegistroAuditoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    acao = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario.username} - {self.acao} - {self.timestamp}"
