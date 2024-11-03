from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    CARGO_CHOICES = (
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
    )
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, default='aluno')

    def is_aluno(self):
        return self.cargo == 'aluno'

    def is_professor(self):
        return self.cargo == 'professor'

    def is_administrador(self):
        return self.cargo == 'administrador'
