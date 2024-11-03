# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Certifique-se de que está importando o seu modelo de usuário

class CustomUserAdmin(UserAdmin):
    model = User
    # Aqui você pode personalizar os campos que deseja exibir
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('cargo',)}),  # Adicione seu campo 'cargo' aqui
    )

admin.site.register(User, CustomUserAdmin)