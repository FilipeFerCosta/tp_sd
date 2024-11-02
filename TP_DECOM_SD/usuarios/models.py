from django.contrib.auth.models import AbstractUser
from django.db import models

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
    class Meta:
        permissions = [
            ("can_create_post", "Pode criar postagens"),
            ("can_delete_post", "Pode deletar postagens"),
        ]